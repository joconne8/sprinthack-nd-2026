import json, shutil, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import intake

EX = Path(__file__).resolve().parents[2] / "data ingestion" / "examples"
UP = EX / "upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv"
CM = EX / "cash_monkey_orders_2026-09-30_2026-09-30_synthetic.csv"
man = lambda p: json.loads(p.with_suffix(".manifest.json").read_text())


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.args = dict(requested_start="2026-09-30", requested_end="2026-09-30")

    def run_intake(self, path=UP, manifest=None, run="r1", src="upright_replica", rt="paid_orders", **kw):
        a = {**self.args, **kw}
        return intake.intake(path, manifest or man(path), run, a["requested_start"], a["requested_end"], src, rt, self.tmp / "arch")

    def test_happy_path_both_sources(self):
        r = self.run_intake()
        self.assertEqual((r["row_count"], r["acquisition_state"], r["import_state"]), (128, "acquired_verified", "not_submitted"))
        self.assertEqual(r["checksum"], man(UP)["file_checksum"])
        c = self.run_intake(CM, run="r2", src="cash_monkey_replica", rt="orders")
        self.assertEqual(c["row_count"], 32)

    def test_archive_is_byte_identical_and_read_only(self):
        r = self.run_intake()
        self.assertEqual(Path(r["artifact_ref"]).read_bytes(), UP.read_bytes())
        with self.assertRaises(PermissionError):
            if Path(r["artifact_ref"]).stat().st_mode & 0o200:
                raise AssertionError("writable")
            open(r["artifact_ref"], "ab")

    def test_same_bytes_not_archived_twice(self):
        a = self.run_intake(run="a"); b = self.run_intake(run="b")
        self.assertTrue(a["newly_archived"]); self.assertFalse(b["newly_archived"])
        self.assertEqual(a["artifact_ref"], b["artifact_ref"])

    def test_run_id_cannot_be_reused(self):
        self.run_intake()
        with self.assertRaises(intake.IntakeRejected) as e: self.run_intake()
        self.assertEqual(e.exception.code, "run_id_reused")

    def rejects(self, code, **kw):
        with self.assertRaises(intake.IntakeRejected) as e: self.run_intake(**kw)
        self.assertEqual(e.exception.code, code)
        self.assertFalse((self.tmp / "arch").exists(), "rejected file must not be archived")

    def test_wrong_date_range_rejected(self):
        self.rejects("wrong_period_in_manifest", requested_start="2026-10-01", requested_end="2026-10-01")

    def test_wrong_report_rejected(self):
        self.rejects("wrong_report", src="cash_monkey_replica", rt="orders")

    def test_missing_and_empty_file_rejected(self):
        self.rejects("file_missing", path=self.tmp / "nope.csv", manifest=man(UP))
        e = self.tmp / "empty.csv"; e.write_bytes(b"")
        self.rejects("file_empty", path=e, manifest=man(UP))

    def test_tampered_bytes_rejected(self):
        t = self.tmp / "t.csv"; t.write_bytes(UP.read_bytes().replace(b"47.64", b"47.65", 1))
        self.rejects("checksum_mismatch", path=t, manifest=man(UP))

    def mutated(self, fn):
        data = fn(UP.read_text()).encode(); t = self.tmp / "m.csv"; t.write_bytes(data)
        m = man(UP); m["file_checksum"] = intake._sha256(data); return t, m

    def test_unexpected_schema_rejected(self):
        t, m = self.mutated(lambda s: s.replace("paid_order_id", "order_ref", 1))
        self.rejects("unexpected_schema", path=t, manifest=m)

    def test_row_outside_period_rejected(self):
        t, m = self.mutated(lambda s: s.replace(",2026-09-30,America", ",2026-10-05,America", 1))
        self.rejects("row_outside_requested_period", path=t, manifest=m)

    def test_truncated_file_row_count_rejected(self):
        t, m = self.mutated(lambda s: "\n".join(s.splitlines()[:-5]) + "\n")
        self.rejects("row_count_mismatch", path=t, manifest=m)

    def test_unlabeled_synthetic_rejected(self):
        t, m = self.mutated(lambda s: s.replace(",true,", ",false,", 1))
        self.rejects("not_labeled_synthetic", path=t, manifest=m)

    def test_incomplete_manifest_rejected(self):
        m = man(UP); del m["file_checksum"]
        self.rejects("manifest_incomplete", manifest=m)

    def test_submit_is_idempotent_and_records_real_import_state(self):
        from services.data.importer import Pipeline
        pipeline = Pipeline(self.tmp / 'pipeline')
        r = self.run_intake()
        batch, first = intake.submit(r, pipeline); replay, second = intake.submit(r, pipeline)
        self.assertEqual((first, second), (True, False))
        self.assertEqual(r["import_state"], "imported")
        self.assertEqual(batch['batch_id'], replay['batch_id'])
        self.assertEqual(batch['file']['checksum'], r['checksum'])


if __name__ == "__main__":
    unittest.main()
