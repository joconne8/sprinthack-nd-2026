import json
import shutil
import tempfile
import unittest
from pathlib import Path

from services.data.contracts import DataError, digest
from services.data.importer import Pipeline
from services.data.inventory.store import inventory_response, load_pack

ROOT = Path(__file__).resolve().parents[1] / "goodwill/synthetic-data"


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pipeline = Pipeline(Path(self.temp.name)/"state")

    def test_event_dates_and_one_snapshot_fixed_controls(self):
        load_pack(self.pipeline, ROOT)
        result = inventory_response(self.pipeline, "2026-08-01", "2026-08-31", "2026-08-31T23:59:59-04:00")
        self.assertEqual(result["metrics"][0]["value"], "1443")
        self.assertEqual(result["metrics"][1]["value"], "765")
        self.assertEqual(result["coverage_state"], "complete")
        earlier = inventory_response(self.pipeline, "2026-08-01", "2026-08-31", "2026-08-01T23:59:59-04:00")
        self.assertEqual(earlier["metrics"][1]["value"], "832")
        midmonth = inventory_response(self.pipeline, "2026-08-01", "2026-08-31", "2026-08-15T23:59:59-04:00")
        self.assertEqual(midmonth["metrics"][1]["value"], "757")

    def test_repeat_pack_no_duplicates_and_row_lineage(self):
        first = load_pack(self.pipeline, ROOT)
        again = load_pack(self.pipeline, ROOT)
        self.assertEqual(first["input_ids"], again["input_ids"])
        with self.pipeline.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM listing_events").fetchone()[0], 3181)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM inventory_snapshots").fetchone()[0], 6019)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM inventory_inputs").fetchone()[0], 3)
            input_file = db.execute("SELECT i.file_id FROM inventory_inputs i JOIN listing_events l ON l.input_id=i.id LIMIT 1").fetchone()[0]
            self.assertEqual(len(input_file), 64)

    def test_missing_snapshot_and_uncovered_period_unavailable(self):
        before = inventory_response(self.pipeline, "2026-08-01", "2026-08-31")
        self.assertTrue(all(m["value"] is None for m in before["metrics"]))
        load_pack(self.pipeline, ROOT)
        after = inventory_response(self.pipeline, "2026-08-01", "2026-08-31", "2026-08-02T23:59:59-04:00")
        self.assertIsNone(after["metrics"][1]["value"])
        sept = inventory_response(self.pipeline, "2026-09-01", "2026-09-01")
        self.assertIsNone(sept["metrics"][0]["value"])
        with self.assertRaises(DataError):
            inventory_response(self.pipeline, "2026-09-01", "2026-09-01", "2026-08-31T23:59:59-04:00")

    def test_partial_snapshot_rejected_even_with_rehashed_manifest(self):
        pack = Path(self.temp.name)/"pack"
        shutil.copytree(ROOT, pack)
        file = pack/"12_inventory_snapshots_aug2026.csv"
        lines = file.read_bytes().splitlines(keepends=True)
        file.write_bytes(b"".join(lines[:-1]))
        manifest = json.loads((pack/"manifest.json").read_text())
        manifest["files"][file.name]["sha256"] = digest(file.read_bytes())
        manifest["files"][file.name]["rows"] -= 1
        (pack/"manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(DataError, "incomplete_snapshot"):
            load_pack(self.pipeline, pack)
        self.assertIsNone(inventory_response(self.pipeline, "2026-08-01", "2026-08-31")["metrics"][0]["value"])
