"""Jack mc's control ledger; expected amounts are handwritten in fixtures/expected-results/, not parser outputs."""
import tempfile
import unittest

from services.data.importer import Pipeline
from services.metrics.query import metric_response
from tests.acceptance.qa_support import SCENARIOS, artifact, scenario_file


def net(pipeline, start, end=None, **filters):
    return metric_response(pipeline, start, end or start, "upright_replica", filters.get("platform"), filters.get("store"))


def value(response, index=0):
    return response["metrics"][index]["value"]


# Each check raises AssertionError on mismatch, so seeded-defect tests can reuse them.

def check_core_ledger(tc, pipeline):
    s = SCENARIOS["core_ledger"]
    exp = s["expected"]
    initial = scenario_file("core_ledger", "initial")
    tc.assertEqual(pipeline.import_bytes(*initial)["status"], "imported")
    response = net(pipeline, s["date"])
    tc.assertEqual(value(response), exp["after_initial"]["net"])
    tc.assertEqual(response["evidence"]["gross_item_sales"], exp["after_initial"]["gross"])
    tc.assertEqual(response["evidence"]["refunds"], exp["after_initial"]["refunds"])
    tc.assertEqual(response["evidence"]["row_count"], exp["after_initial"]["rows"])
    tc.assertEqual(response["metrics"][0]["availability"], "available")

    tc.assertEqual(pipeline.import_bytes(*initial)["status"], exp["after_replay"]["status"])
    tc.assertEqual(value(net(pipeline, s["date"])), exp["after_replay"]["net"])

    overlap = pipeline.import_bytes(*scenario_file("core_ledger", "overlap"))
    tc.assertEqual(overlap["counts"]["accepted_rows"], exp["after_overlap"]["accepted_rows"])
    tc.assertEqual(overlap["counts"]["duplicate_rows"], exp["after_overlap"]["duplicate_rows"])
    response = net(pipeline, s["date"])
    tc.assertEqual(value(response), exp["after_overlap"]["net"])
    tc.assertEqual(response["evidence"]["row_count"], exp["after_overlap"]["rows"])

    correction = scenario_file("core_ledger", "correction")
    refused = pipeline.import_bytes(*correction)
    tc.assertEqual(refused["status"], exp["after_unapproved_correction"]["status"])
    tc.assertIn(exp["after_unapproved_correction"]["error"], {e["code"] for e in refused["exceptions"]})
    tc.assertEqual(value(net(pipeline, s["date"])), exp["after_unapproved_correction"]["net"])

    approved = pipeline.import_bytes(*correction, allow_corrections=True)
    tc.assertEqual(approved["counts"]["corrected_rows"], exp["after_approved_correction"]["corrected_rows"])
    response = net(pipeline, s["date"])
    tc.assertEqual(value(response), exp["after_approved_correction"]["net"])
    tc.assertEqual(response["evidence"]["gross_item_sales"], exp["after_approved_correction"]["gross"])
    tc.assertEqual(response["evidence"]["refunds"], exp["after_approved_correction"]["refunds"])


def check_coverage_gap(tc, pipeline):
    exp = SCENARIOS["coverage_gap"]["expected"]
    pipeline.import_bytes(*scenario_file("coverage_gap", "sep29"))
    pipeline.import_bytes(*scenario_file("coverage_gap", "oct01"))
    response = net(pipeline, "2026-09-29", "2026-10-01")
    tc.assertEqual(response["coverage"]["missing_or_partial_days"], exp["range_sep29_oct01_missing_days"])
    tc.assertNotEqual(response["metrics"][0]["availability"], "available")
    response = net(pipeline, "2026-09-30")
    tc.assertEqual(value(response), exp["sep30_value"])
    tc.assertEqual(response["metrics"][0]["availability"], exp["sep30_availability"])


def check_buyer_store_keys(tc, pipeline):
    s = SCENARIOS["buyer_store_keys"]
    exp = s["expected"]
    batch = pipeline.import_bytes(*scenario_file("buyer_store_keys", "keys"))
    tc.assertEqual(batch["status"], "imported")
    tc.assertEqual(sorted({e["code"] for e in batch["exceptions"]}), exp["exception_codes"])
    everything = net(pipeline, s["date"])
    tc.assertEqual(value(everything), exp["all_platforms_net"])
    tc.assertEqual(value(everything, 1), exp["all_platforms_customers"])
    tc.assertEqual(everything["metrics"][1]["availability"], "unavailable")
    ebay = net(pipeline, s["date"], platform="eBay")
    tc.assertEqual((value(ebay), value(ebay, 1)), (exp["ebay_net"], exp["ebay_customers"]))
    shop = net(pipeline, s["date"], platform="ShopGoodwill")
    tc.assertEqual((value(shop), value(shop, 1)), (exp["shopgoodwill_net"], exp["shopgoodwill_customers"]))
    tc.assertEqual(value(net(pipeline, s["date"], store="GW-001")), exp["store_gw001_net"])
    tc.assertEqual(value(net(pipeline, s["date"], store="unknown")), exp["store_unknown_net"])


class IndependentLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pipeline = Pipeline(self.tmp.name)

    def test_refunds_replay_overlap_and_correction(self):
        check_core_ledger(self, self.pipeline)

    def test_inclusive_edges_and_alternate_dates(self):
        exp = SCENARIOS["date_boundaries"]["expected"]
        self.assertEqual(self.pipeline.import_bytes(*scenario_file("date_boundaries", "sep30"))["status"], "imported")
        self.assertEqual(value(net(self.pipeline, "2026-09-30")), exp["sep30"])
        self.assertEqual(value(net(self.pipeline, "2026-09-29")), exp["sep29_before_any_sep29_file"])
        self.pipeline.import_bytes(*scenario_file("date_boundaries", "oct01"))
        self.assertEqual(value(net(self.pipeline, "2026-10-01")), exp["oct01"])
        both = net(self.pipeline, "2026-09-30", "2026-10-01")
        self.assertEqual((value(both), both["metrics"][0]["availability"]), (exp["sep30_to_oct01"], "available"))

    def test_row_outside_requested_period_blocks_file(self):
        exp = SCENARIOS["date_boundaries"]["expected"]
        batch = self.pipeline.import_bytes(*scenario_file("date_boundaries", "outside_period"))
        self.assertEqual(batch["status"], exp["outside_period_status"])
        self.assertIn(exp["outside_period_reason"], {e["code"] for e in batch["exceptions"]})
        self.assertIsNone(value(net(self.pipeline, "2026-09-30")))

    def test_missing_day_is_unknown_not_zero(self):
        check_coverage_gap(self, self.pipeline)

    def test_other_timezone_report_only_partially_covers_day(self):
        exp = SCENARIOS["coverage_gap"]["expected"]
        self.assertEqual(self.pipeline.import_bytes(*scenario_file("coverage_gap", "utc_sep30"))["status"], "imported")
        response = net(self.pipeline, "2026-09-30")
        self.assertEqual(response["metrics"][0]["availability"], exp["utc_file_sep30_availability"])
        self.assertEqual(response["coverage"]["missing_or_partial_days"], exp["utc_file_sep30_missing_days"])

    def test_missing_sources_are_unavailable(self):
        exp = SCENARIOS["missing_source"]["expected"]
        response = net(self.pipeline, "2026-09-30")
        self.assertEqual((value(response), response["metrics"][0]["availability"]),
                         (exp["never_imported_value"], exp["never_imported_availability"]))
        self.pipeline.import_bytes(*scenario_file("core_ledger", "initial"))
        other = metric_response(self.pipeline, "2026-09-30", "2026-09-30", "cash_monkey_replica")
        self.assertEqual(value(other), exp["other_source_value_after_upright_import"])

    def test_buyer_namespaces_and_store_keys(self):
        check_buyer_store_keys(self, self.pipeline)

    def test_missing_buyer_keeps_sales_but_hides_customers(self):
        exp = SCENARIOS["buyer_store_keys"]["expected"]
        spec = SCENARIOS["buyer_store_keys"]["files"]["missing_buyer_oct01"]
        self.pipeline.import_bytes(*artifact(spec, "2026-10-01"))
        response = net(self.pipeline, "2026-10-01", platform="eBay")
        self.assertEqual(value(response), exp["missing_buyer_oct01_net"])
        self.assertEqual(value(response, 1), exp["missing_buyer_oct01_customers"])

    def test_invalid_rows_fail_without_publishing(self):
        exp = SCENARIOS["invalid_rows"]["expected"]
        for name in ("refund_exceeds_gross", "negative_gross", "three_decimals", "conflicting_same_file"):
            with self.subTest(name):
                batch = self.pipeline.import_bytes(*scenario_file("invalid_rows", name))
                self.assertEqual(batch["status"], "failed")
                self.assertIn(exp[name], {e["code"] for e in batch["exceptions"]} | {batch["error"]["code"]})
                self.assertIsNone(value(net(self.pipeline, "2026-09-30")))

    def test_exact_duplicate_within_file_counts_once(self):
        exp = SCENARIOS["invalid_rows"]["expected"]
        batch = self.pipeline.import_bytes(*scenario_file("invalid_rows", "exact_duplicate_same_file"))
        self.assertEqual(batch["counts"]["duplicate_rows"], exp["exact_duplicate_same_file_duplicate_rows"])
        self.assertEqual(value(net(self.pipeline, "2026-09-30")), exp["exact_duplicate_same_file_net"])

    def test_invalid_money_keeps_last_good(self):
        self.pipeline.import_bytes(*artifact([{"key": "A", "gross": "12.34", "refund": "2.34"}]))
        bad = self.pipeline.import_bytes(*artifact([{"key": "B", "gross": "NaN", "refund": "0.00"}]))
        self.assertEqual(bad["status"], "failed")
        response = net(self.pipeline, "2026-09-30")
        self.assertEqual(value(response), "10.00")  # 12.34-2.34, unchanged by the failed file
        self.assertTrue(response["freshness"]["is_last_good"])
        self.assertNotEqual(response["metrics"][0]["availability"], "available")


if __name__ == "__main__":
    unittest.main()
