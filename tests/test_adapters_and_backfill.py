import importlib.util
import json
import tempfile
import time
import unittest
from pathlib import Path

from services.data.adapters import fixture_manifest, import_intake
from services.data.importer import Pipeline
from services.metrics.query import metric_response
from tests.helpers import payload, row

ROOT = Path(__file__).resolve().parents[1]


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pipeline = Pipeline(Path(self.temp.name)/"state")

    def test_full_acquisition_record_adapter_preserves_exact_bytes(self):
        spec = importlib.util.spec_from_file_location("intake_for_test", ROOT/"acquisition/intake.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        folder = ROOT/"data ingestion/examples"
        file = folder/"upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv"
        manifest = json.loads((folder/"upright_paid_orders_2026-09-30_2026-09-30_synthetic.manifest.json").read_text())
        archive = Path(self.temp.name)/"intake"
        record = module.intake(file, manifest, "test-acquired-run", "2026-09-30", "2026-09-30", "upright_replica", "paid_orders", archive)
        batch = import_intake(self.pipeline, archive/"runs/test-acquired-run.json")
        self.assertEqual(batch["status"], "imported")
        self.assertEqual(batch["file"]["checksum"], record["checksum"])
        result = metric_response(self.pipeline, "2026-09-30", "2026-09-30", "upright_replica")
        self.assertEqual(result["metrics"][0]["value"], "7127.78")
        self.assertEqual(result["metrics"][0]["availability"], "partial")

    def test_fixture_replay_invalid_and_incremental_day(self):
        pack = ROOT/"goodwill/synthetic-data"
        base = pack/"08_ebay_listing_sales_aug2026.csv"
        self.pipeline.import_file(base, fixture_manifest(base, "2026-08-01", "2026-08-31", "ebay_fixture", "sales"))
        original = metric_response(self.pipeline, "2026-08-01", "2026-08-31", "ebay_fixture")
        self.assertEqual(original["metrics"][0]["value"], "55515.26")
        replay = pack/"test-fixtures/ebay_duplicate_replay.csv"
        batch = self.pipeline.import_file(replay, fixture_manifest(replay, "2026-08-01", "2026-08-31", "ebay_fixture", "sales"))
        self.assertEqual(batch["counts"]["duplicate_rows"], 25)
        self.assertEqual(batch["status"], "duplicate_noop")
        invalid = pack/"test-fixtures/ebay_invalid_rows.csv"
        batch = self.pipeline.import_file(invalid, fixture_manifest(invalid, "2026-08-01", "2026-08-31", "ebay_fixture", "sales"))
        self.assertEqual(batch["counts"]["rejected_rows"], 5)
        self.assertEqual(batch["status"], "failed")
        incremental = pack/"incremental/ebay_sep01_2026.csv"
        batch = self.pipeline.import_file(incremental, fixture_manifest(incremental, "2026-09-01", "2026-09-01", "ebay_fixture", "sales"))
        self.assertEqual(batch["counts"]["accepted_rows"], 30)
        after = metric_response(self.pipeline, "2026-08-01", "2026-08-31", "ebay_fixture")
        self.assertEqual(after["metrics"][0]["value"], original["metrics"][0]["value"])

    def test_late_refund_backfill_and_reprocessing_are_reproducible(self):
        original = payload([row(day="2026-08-31"), row("B", "20.00", "2.00", day="2026-08-31")], start="2026-08-31", end="2026-08-31")
        self.pipeline.import_bytes(*original)
        before = metric_response(self.pipeline, "2026-08-31", "2026-08-31", "upright_replica")
        revised = payload([row(refund="5.00", day="2026-08-31"), row("B", "20.00", "2.00", day="2026-08-31")], start="2026-08-31", end="2026-08-31")
        batch = self.pipeline.import_bytes(*revised, allow_corrections=True)
        self.assertEqual(batch["counts"]["corrected_rows"], 1)
        self.assertEqual(batch["counts"]["duplicate_rows"], 1)
        after = metric_response(self.pipeline, "2026-08-31", "2026-08-31", "upright_replica")
        self.assertEqual(before["metrics"][0]["value"], "27.00")
        self.assertEqual(after["metrics"][0]["value"], "23.00")
        self.pipeline.import_bytes(*revised, allow_corrections=True)
        repeat = metric_response(self.pipeline, "2026-08-31", "2026-08-31", "upright_replica")
        self.assertEqual(repeat["metrics"], after["metrics"])
        self.assertEqual(repeat["metric_run_id"], after["metric_run_id"])
