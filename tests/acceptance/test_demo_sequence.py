"""End-to-end demo sequence: actual replica download -> HTTP import -> reconcile -> API -> evidence.

Expected totals come from QA's own reading of the downloaded bytes and from
hand-evaluated spot rows, not from the importer. Browser acceptance is required;
export remains explicitly deferred from P0.
"""
import tempfile
import unittest

from tests.acceptance.qa_support import ROOT, SCENARIOS, run_demo_sequence

SPOT = SCENARIOS["demo_spot_checks"]


class DemoSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.steps = {s["step"]: s for s in run_demo_sequence(cls.tmp.name)}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_downloaded_bytes_are_exactly_what_was_imported_and_archived(self):
        for step in self.steps.values():
            with self.subTest(step["step"]):
                self.assertEqual(step["download"]["sha256"], step["download"]["manifest_checksum"])
                self.assertEqual(step["import"]["file_id"], step["download"]["sha256"])
                self.assertTrue(step["raw_download_matches"])

    def test_first_day_import_matches_qa_raw_sum(self):
        step = self.steps["sep29"]
        self.assertEqual((step["import"]["http_status"], step["import"]["status"]), (201, "imported"))
        self.assertEqual(step["import"]["reconciliation_state"], "verified")
        self.assertEqual(step["download"]["row_count"], SPOT["rows_per_day"])
        day = step["metrics_by_day"]["2026-09-29"]
        self.assertEqual(day["value"], step["qa_raw_net_by_day"]["2026-09-29"])
        self.assertEqual((day["availability"], day["coverage"], day["rows"]), ("available", "complete", SPOT["rows_per_day"]))
        self.assertIsNone(step["metrics_by_day"]["2026-09-30"]["value"])  # not yet acquired: unknown, not zero
        self.assertEqual(step["evidence"]["spot"]['["UP-20260929-0001"]'], SPOT["rows"]["UP-20260929-0001"]["net"])

    def test_replay_changes_nothing(self):
        first, replay = self.steps["sep29"], self.steps["sep29_replay"]
        self.assertEqual(replay["download"]["sha256"], first["download"]["sha256"])
        self.assertEqual(replay["import"]["status"], "duplicate_noop")
        self.assertEqual(replay["metrics_by_day"]["2026-09-29"], first["metrics_by_day"]["2026-09-29"])

    def test_overlapping_two_day_file_adds_only_new_day(self):
        first, step = self.steps["sep29"], self.steps["sep29_sep30_overlap"]
        self.assertEqual(step["import"]["status"], "imported")
        self.assertEqual(step["import"]["counts"]["duplicate_rows"], SPOT["rows_per_day"])
        self.assertEqual(step["import"]["counts"]["accepted_rows"], SPOT["rows_per_day"])
        self.assertEqual(step["metrics_by_day"]["2026-09-29"]["value"], first["metrics_by_day"]["2026-09-29"]["value"])
        self.assertEqual(step["metrics_by_day"]["2026-09-30"]["value"], step["qa_raw_net_by_day"]["2026-09-30"])
        self.assertEqual(step["range_metric"]["availability"], "available")
        self.assertEqual(step["evidence"]["scope_total"], step["range_metric"]["value"])
        self.assertEqual(step["evidence"]["total_rows"], 2 * SPOT["rows_per_day"])
        for key in ("UP-20260930-0001", "UP-20260930-0002"):
            self.assertEqual(step["evidence"]["spot"]['["%s"]' % key], SPOT["rows"][key]["net"])

    def test_portal_manifest_total_agrees_with_qa_and_api(self):
        step = self.steps["sep29_sep30_overlap"]
        self.assertEqual(step["download"]["portal_demo_net_sales"], step["range_metric"]["value"])

    def test_dashboard_shows_api_values(self):
        from tests.acceptance.dashboard_browser import run_dashboard_acceptance
        observed = run_dashboard_acceptance()
        self.assertTrue(observed['passed'])
        self.assertGreaterEqual(len(observed['acquired']), 2)

    @unittest.skip("Export is deferred from P0 (planning/development.md); not silently waived")
    def test_export_matches_evidence(self):
        pass


if __name__ == "__main__":
    unittest.main()
