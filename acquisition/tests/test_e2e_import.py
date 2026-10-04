"""Acquisition -> intake -> importer (services/data) end to end, using the real ING-01 files."""
import json, shutil, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "acquisition"))
import intake
from services.data.contracts import validate, DataError
from services.data.importer import Pipeline

EX = ROOT / "data ingestion" / "examples"
UP = EX / "upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv"
CM = EX / "cash_monkey_orders_2026-09-30_2026-09-30_synthetic.csv"
man = lambda p: json.loads(p.with_suffix(".manifest.json").read_text())


class E2E(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.pipe = Pipeline(self.tmp / "state")

    def acquire_and_submit(self, path, src, rt, run, start="2026-09-30", end="2026-09-30"):
        rec = intake.intake(path, man(path), run, start, end, src, rt, self.tmp / "arch")
        out, _ = intake.submit(rec, man(path), self.tmp / "out")
        req = json.loads(out.read_text())
        validate("import-request.schema.json", req)
        return rec, req

    def test_downloaded_checksum_matches_imported_raw_file(self):
        rec, req = self.acquire_and_submit(UP, "upright_replica", "paid_orders", "e1")
        self.assertEqual(rec["import_state"], "not_submitted")        # acquisition done, import not yet
        batch = self.pipe.import_bytes(req["csv_text"].encode(), req["manifest"])
        self.assertEqual(batch["status"], "imported")
        self.assertEqual(batch["file"]["checksum"], rec["checksum"])
        self.assertEqual(batch["counts"]["row_count"], rec["row_count"])
        self.assertEqual(batch["reconciliation"]["state"], "verified")

    def test_cash_monkey_also_imports(self):
        rec, req = self.acquire_and_submit(CM, "cash_monkey_replica", "orders", "e2")
        batch = self.pipe.import_bytes(req["csv_text"].encode(), req["manifest"])
        self.assertEqual((batch["status"], batch["file"]["checksum"]), ("imported", rec["checksum"]))

    def test_resubmitting_same_file_does_not_double_publish(self):
        _, req = self.acquire_and_submit(UP, "upright_replica", "paid_orders", "e3")
        first = self.pipe.import_bytes(req["csv_text"].encode(), req["manifest"])
        second = self.pipe.import_bytes(req["csv_text"].encode(), req["manifest"])
        self.assertEqual((first["status"], second["status"]), ("imported", "duplicate_noop"))

    def test_wrong_date_range_never_reaches_importer(self):
        with self.assertRaises(intake.IntakeRejected):
            intake.intake(UP, man(UP), "e4", "2026-10-01", "2026-10-02", "upright_replica", "paid_orders", self.tmp / "arch")
        self.assertEqual(self.pipe.batches() if self.pipe.db_path.exists() else [], [])

    def test_importer_rejects_tampered_bytes_even_if_intake_were_bypassed(self):
        _, req = self.acquire_and_submit(UP, "upright_replica", "paid_orders", "e5")
        bad = req["csv_text"].replace("47.64", "47.65", 1).encode()
        batch = self.pipe.import_bytes(bad, req["manifest"])
        self.assertEqual((batch["status"], batch["error"]["code"]), ("failed", "checksum_mismatch"))

if __name__ == "__main__": unittest.main()
