import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from services.data.adapters import fixture_manifest
from services.data.contracts import DataError, cents, manifest_metadata, validate
from services.data.importer import Pipeline
from services.metrics.query import evidence_response, metric_response
from tests.helpers import payload, row


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pipeline = Pipeline(self.temp.name)

    def metric(self, source="upright_replica", start="2026-09-30", end="2026-09-30", **kwargs):
        return metric_response(self.pipeline, start, end, source, **kwargs)

    def test_fixed_ledger_excludes_source_net_shipping_tax_fees(self):
        # Manually derived: (1000-100)+(2000-200)=2700 cents. No source-net use.
        batch = self.pipeline.import_bytes(*payload([row(), row("B", "20.00", "2.00")], item_sales="30.00", refunds="3.00", demo_net_sales="27.00"))
        self.assertEqual(batch["status"], "imported")
        self.assertEqual(batch["counts"]["accepted_rows"], 2)
        metric = self.metric()
        self.assertEqual(metric["metrics"][0]["value"], "27.00")
        self.assertEqual(metric["metrics"][0]["availability"], "available")
        self.assertEqual(metric["metrics"][1]["value"], "2")
        for strategic in metric["metrics"][2:]:
            self.assertIsNone(strategic["value"])
            self.assertEqual(strategic["availability"], "unavailable")

    def test_raw_bytes_and_source_row_lineage(self):
        data, manifest = payload([row()])
        batch = self.pipeline.import_bytes(data, manifest)
        with self.pipeline.db() as db:
            artifact = db.execute("SELECT * FROM source_files").fetchone()
        self.assertEqual(Path(artifact["artifact_ref"]).read_bytes(), data)
        self.assertEqual(os.stat(artifact["artifact_ref"]).st_mode & 0o222, 0)
        metrics = self.metric()
        evidence = evidence_response(self.pipeline, metrics["metric_run_id"], "2026-09-30", "2026-09-30", "upright_replica")
        self.assertEqual(evidence["scope_total"], "9.00")
        source_row = evidence["rows"][0]
        self.assertEqual(source_row["source_row_number"], 1)
        self.assertEqual(source_row["batch_id"], batch["batch_id"])
        self.assertEqual(source_row["file_id"], manifest["file_checksum"])
        self.assertEqual(source_row["original_row"]["net_sales"], "9999.00")

    def test_duplicate_and_overlap_noop(self):
        original = payload([row(), row("B", "20.00", "2.00")])
        self.pipeline.import_bytes(*original)
        run = self.metric()["metric_run_id"]
        replay = self.pipeline.import_bytes(*original)
        self.assertEqual(replay["status"], "duplicate_noop")
        self.assertEqual(replay["counts"]["duplicate_rows"], 2)
        overlap = self.pipeline.import_bytes(*payload([row("B", "20.00", "2.00")]))
        self.assertEqual(overlap["status"], "duplicate_noop")
        self.assertEqual(self.metric()["metric_run_id"], run)
        self.assertEqual(self.metric()["metrics"][0]["value"], "27.00")

    def test_overlap_with_new_rows(self):
        self.pipeline.import_bytes(*payload([row()]))
        second = self.pipeline.import_bytes(*payload([row(), row("B", "20.00", "2.00")]))
        self.assertEqual(second["counts"]["duplicate_rows"], 1)
        self.assertEqual(self.metric()["metrics"][0]["value"], "27.00")

    def test_duplicate_in_file_and_conflicting_in_file(self):
        batch = self.pipeline.import_bytes(*payload([row(), row()]))
        self.assertEqual(batch["counts"]["duplicate_rows"], 1)
        self.assertEqual(self.metric()["metrics"][0]["value"], "9.00")
        conflict = self.pipeline.import_bytes(*payload([row("C"), row("C", "11.00")]))
        self.assertEqual(conflict["status"], "failed")
        self.assertEqual(self.metric()["metrics"][0]["value"], "9.00")

    def test_explicit_correction_preserves_historical_evidence(self):
        first = self.pipeline.import_bytes(*payload([row()]))
        old_run = self.metric()["metric_run_id"]
        correction = payload([row(refund="2.00")])
        rejected = self.pipeline.import_bytes(*correction)
        self.assertEqual(rejected["status"], "failed")
        self.assertEqual(self.metric()["metrics"][0]["value"], "9.00")
        accepted = self.pipeline.import_bytes(*correction, allow_corrections=True)
        self.assertEqual(accepted["counts"]["corrected_rows"], 1)
        self.assertEqual(self.metric()["metrics"][0]["value"], "8.00")
        old = self.metric(run_id=old_run)
        self.assertEqual(old["metrics"][0]["value"], "9.00")
        with self.pipeline.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM sale_versions WHERE supersedes IS NOT NULL").fetchone()[0], 1)

    def test_malformed_rows_block_entire_publication(self):
        self.pipeline.import_bytes(*payload([row()]))
        previous = self.metric()["metric_run_id"]
        batch = self.pipeline.import_bytes(*payload([row("B", "20.00"), row("BAD", "NaN")]))
        self.assertEqual(batch["status"], "failed")
        self.assertEqual(batch["counts"]["accepted_rows"], 1)
        self.assertEqual(batch["counts"]["rejected_rows"], 1)
        self.assertIsNone(batch["reconciliation"]["source_gross"])
        response = self.metric()
        self.assertEqual(response["metric_run_id"], previous)
        self.assertTrue(response["freshness"]["is_last_good"])
        self.assertEqual(response["metrics"][0]["value"], "9.00")
        with self.pipeline.db() as db:
            bad = db.execute("SELECT * FROM staging_rows WHERE batch_id=? AND status='rejected'", (batch["batch_id"],)).fetchone()
        self.assertEqual(bad["row_number"], 2)
        self.assertIn('"BAD"', bad["original_json"])

    def test_all_seeded_money_id_date_negatives(self):
        cases = [row(gross="-1.00"), row(refund="11.00"), row(paid_order_id=""),
                 row(paid_at="not-a-date"), row(currency="EUR"), row(synthetic="false"),
                 row(gross="1.001"), row(quantity="0"), row(grain="unknown")]
        for invalid in cases:
            with self.subTest(invalid=invalid):
                batch = self.pipeline.import_bytes(*payload([invalid]))
                self.assertEqual(batch["status"], "failed")
                self.assertEqual(batch["counts"]["rejected_rows"], 1)
        self.assertIsNone(self.metric()["metrics"][0]["value"])

    def test_wrong_period_checksum_header_and_control_failure(self):
        for data, manifest in [payload([row()], start="2026-09-29", end="2026-09-29"),
                               payload([row()], file_checksum="0"*64),
                               payload([row()], item_sales="123.00")]:
            batch = self.pipeline.import_bytes(data, manifest)
            self.assertEqual(batch["status"], "failed")
        data, manifest = payload([row()])
        changed = data.replace(b"gross_sales", b"unknown_sales", 1)
        from services.data.contracts import digest
        manifest["file_checksum"] = digest(changed)
        self.assertEqual(self.pipeline.import_bytes(changed, manifest)["error"]["code"], "invalid_headers")

    def test_missing_store_and_buyer_remain_visible(self):
        batch = self.pipeline.import_bytes(*payload([row(store_id="", buyer_id=""), row("B")]))
        self.assertEqual(batch["status"], "imported")
        self.assertEqual(len(batch["exceptions"]), 2)
        self.assertEqual(self.metric()["metrics"][0]["value"], "18.00")
        self.assertIsNone(self.metric()["metrics"][1]["value"])
        self.assertEqual(self.metric(store="unknown")["metrics"][0]["value"], "9.00")
        exception = batch["exceptions"][0]
        self.pipeline.resolve_exception(exception["id"], "Reviewed; input remains missing until corrected export")
        self.assertEqual(self.pipeline.batch(batch["batch_id"])["exceptions"][0]["status"], "resolved")
        self.assertIsNone(self.metric()["metrics"][1]["value"])
        with self.assertRaises(DataError):
            self.pipeline.resolve_exception(exception["id"], "overwrite")

    def test_unmapped_store_not_assigned_to_known_store(self):
        batch = self.pipeline.import_bytes(*payload([row(store_id="UNRECOGNIZED")]))
        self.assertEqual(batch["exceptions"][0]["code"], "unmapped_store")
        self.assertEqual(self.metric(store="unknown")["metrics"][0]["value"], "9.00")
        self.assertEqual(self.metric(store="GW-001")["metrics"][0]["value"], "0.00")

    def test_incremental_day_does_not_change_original_period(self):
        self.pipeline.import_bytes(*payload([row()]))
        self.pipeline.import_bytes(*payload([row("B", "20.00", "2.00", day="2026-10-01")], start="2026-10-01", end="2026-10-01"))
        self.assertEqual(self.metric()["metrics"][0]["value"], "9.00")
        self.assertEqual(self.metric(start="2026-10-01", end="2026-10-01")["metrics"][0]["value"], "18.00")
        both = self.metric(end="2026-10-01")
        self.assertEqual(both["metrics"][0]["value"], "27.00")
        self.assertEqual(both["coverage"]["state"], "complete")

    def test_zero_verified_rows_distinct_from_missing_source(self):
        missing = self.metric()
        self.assertIsNone(missing["metrics"][0]["value"])
        self.pipeline.import_bytes(*payload([]))
        self.assertEqual(self.metric()["metrics"][0]["value"], "0.00")
        self.assertEqual(self.metric()["metrics"][0]["availability"], "available")
        self.assertIsNone(self.metric(source="not_connected")["metrics"][0]["value"])

    def test_mixed_platform_customers_not_summed(self):
        self.pipeline.import_bytes(*payload([row(), row("B", channel="Shopgoodwill")]))
        self.assertIsNone(self.metric()["metrics"][1]["value"])
        self.assertEqual(self.metric(platform="eBay")["metrics"][1]["value"], "1")

    def test_filtered_report_cannot_claim_complete_coverage(self):
        self.pipeline.import_bytes(*payload([row()], channels=["eBay"]))
        metric = self.metric()
        self.assertEqual(metric["metrics"][0]["availability"], "partial")
        self.assertEqual(metric["metrics"][0]["value"], "9.00")

    def test_reporting_midnight_converts_source_timestamp(self):
        record = row(paid_at="2026-10-01T06:30:00+00:00", reporting_date="2026-09-30", reporting_timezone="America/Los_Angeles")
        self.pipeline.import_bytes(*payload([record], reporting_timezone="America/Los_Angeles"))
        self.assertIsNone(self.metric()["metrics"][0]["value"])
        converted = self.metric(start="2026-10-01", end="2026-10-01")
        self.assertEqual(converted["metrics"][0]["value"], "9.00")
        self.assertEqual(converted["metrics"][0]["availability"], "partial")
        evidence = evidence_response(self.pipeline, converted["metric_run_id"], "2026-10-01", "2026-10-01", "upright_replica")
        self.assertEqual(evidence["rows"][0]["source_date"], "2026-09-30")

    def test_archive_tampering_detected(self):
        data, manifest = payload([row()])
        self.pipeline.import_bytes(data, manifest)
        path = next(self.pipeline.archive_root.rglob('*.csv'))
        path.chmod(0o644)
        path.write_bytes(b"tampered")
        with self.assertRaisesRegex(DataError, "archive_corrupt"):
            self.pipeline.import_bytes(data, manifest)

    def test_expense_or_settlement_report_does_not_become_revenue(self):
        data, manifest = payload([row()], source_name="fedex_expenses", report_type="charges")
        self.assertEqual(self.pipeline.import_bytes(data, manifest)["error"]["code"], "unsupported_report")
        self.assertIsNone(self.metric(source="fedex_expenses")["metrics"][0]["value"])

    def test_different_grains_cannot_double_count_one_source(self):
        self.pipeline.import_bytes(*payload([row()]))
        data, manifest = payload([row(grain="one row per paid order item")], report_type="paid_order_items")
        self.assertEqual(self.pipeline.import_bytes(data, manifest)["error"]["code"], "source_report_conflict")
        self.assertEqual(self.metric()["metrics"][0]["value"], "9.00")

    def test_contracts_reject_wrong_shapes_and_false_availability(self):
        self.pipeline.import_bytes(*payload([row()]))
        response = self.metric()
        for mutate in [lambda r: r.update(synthetic=False), lambda r: r["metrics"][0].update(value=9.0),
                       lambda r: r["metrics"][0].update(value="garbage"),
                       lambda r: r["metrics"][0].update(availability="unavailable", value="0.00")]:
            bad = copy.deepcopy(response)
            mutate(bad)
            with self.assertRaises(DataError):
                validate("metrics.schema.json", bad)
        metadata = manifest_metadata(payload([row()], channels=["eBay"])[1])
        self.assertEqual(manifest_metadata(metadata)["filters"]["channels"], ["eBay"])

    def test_real_august_fixture_expected_totals(self):
        root = Path(__file__).resolve().parents[1] / "goodwill/synthetic-data"
        file = root / "02_upright_paid_order_items_aug2026.csv"
        metadata = fixture_manifest(file, "2026-08-01", "2026-08-31", "upright_fixture", "paid_order_items")
        batch = self.pipeline.import_file(file, metadata)
        self.assertEqual(batch["counts"]["accepted_rows"], 650)
        metrics = self.metric(source="upright_fixture", start="2026-08-01", end="2026-08-31")
        self.assertEqual(metrics["metrics"][0]["value"], "36157.10")
        self.assertIsNone(metrics["metrics"][1]["value"])

    def test_ragged_row_quarantined_with_original_extra_columns(self):
        data, manifest = payload([row()])
        malformed = data[:-2]+b",unexpected\r\n"
        from services.data.contracts import digest
        manifest["file_checksum"] = digest(malformed)
        batch = self.pipeline.import_bytes(malformed, manifest)
        self.assertEqual(batch["status"], "failed")
        self.assertEqual(batch["exceptions"][0]["code"], "malformed_row")
        with self.pipeline.db() as db:
            raw = json.loads(db.execute("SELECT original_json FROM staging_rows").fetchone()[0])
        self.assertEqual(raw["_extra_columns"], ["unexpected"])

    def test_unexpected_failure_rolls_back_whole_database_transaction(self):
        self.pipeline.import_bytes(*payload([row()]))
        before = self.metric()
        with patch('services.data.importer.reconcile', side_effect=RuntimeError('injected failure')):
            with self.assertRaisesRegex(RuntimeError, 'injected failure'):
                self.pipeline.import_bytes(*payload([row('B')]))
        self.assertEqual(self.metric(), before)
        self.assertEqual(len(self.pipeline.batches()), 1)

    def test_disjoint_reconciliation_counts_and_money_for_overlap(self):
        self.pipeline.import_bytes(*payload([row()]))
        batch = self.pipeline.import_bytes(*payload([row(), row('B', '20.00', '2.00')]))
        counts = batch['counts']
        self.assertEqual(counts['accepted_rows']+counts['duplicate_rows']+counts['rejected_rows'], counts['row_count'])
        controls = batch['reconciliation']
        self.assertEqual(controls['source_gross'], '30.00')
        self.assertEqual(controls['accepted_gross'], '20.00')
        self.assertEqual(controls['duplicate_gross'], '10.00')
        self.assertEqual(controls['rejected_gross'], '0.00')


if __name__ == "__main__":
    unittest.main()
