"""Transactional archive → staging → reconciliation → curated → metric snapshot."""
import json
from pathlib import Path
from uuid import uuid4

from services.data.contracts import (CONTRACT_VERSION, METRIC_VERSION, PARSER_VERSION, RULE_VERSION,
                                    DataError, canonical, digest, manifest_metadata, now, validate)
from services.data.database import connect
from services.data.parsers.sales import normalize, rows_from_bytes
from services.data.publication.coverage import source_window
from services.data.raw.archive import archive
from services.data.reconciliation.controls import reconcile


class Pipeline:
    def __init__(self, state_root):
        self.root = Path(state_root).resolve()
        self.db_path = self.root / "goodwill.sqlite3"
        self.archive_root = self.root / "raw"

    def db(self):
        return connect(self.db_path)

    def import_file(self, path, manifest, allow_corrections=False):
        return self.import_bytes(Path(path).read_bytes(), manifest, allow_corrections)

    def import_bytes(self, data, manifest, allow_corrections=False):
        if not isinstance(data, bytes) or len(data) > 8 * 1024 * 1024:
            raise DataError("file_size", "Expected at most 8 MiB of CSV bytes")
        if type(allow_corrections) is not bool:
            raise DataError("correction_flag", "Explicit boolean required")
        metadata = manifest_metadata(manifest)
        batch_id = uuid4().hex
        timestamp = now()
        checksum, artifact = archive(data, self.archive_root)
        db = self.db()
        try:
            # One SQLite write transaction serializes identity checks and publication.
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT OR IGNORE INTO source_files VALUES(?,?,?,?,?,1)",
                       (checksum, checksum, artifact, len(data), timestamp))
            db.execute("INSERT INTO import_batches(id,file_id,source,report_type,request_start,request_end,source_timezone,manifest_json,parser_version,rule_version,status,recorded_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                       (batch_id, checksum, metadata["source_name"], metadata["report_type"], metadata["requested_start_date"], metadata["requested_end_date"], metadata["reporting_timezone"], canonical(manifest), PARSER_VERSION, RULE_VERSION, "running", timestamp))
            source = metadata["source_name"]
            current = db.execute("SELECT run_id FROM source_publications WHERE source=?", (source,)).fetchone()
            previous_run = current["run_id"] if current else None
            db.execute("INSERT INTO source_publications VALUES(?,?,?) ON CONFLICT(source) DO UPDATE SET latest_batch_id=excluded.latest_batch_id", (source, previous_run, batch_id))
            try:
                if db.execute("SELECT 1 FROM import_batches WHERE source=? AND report_type<>? AND status IN ('imported','duplicate_noop')", (source, metadata["report_type"])).fetchone():
                    raise DataError("source_report_conflict", "Do not mix different report grains as authoritative source revenue")
                if checksum != metadata["file_checksum"]:
                    raise DataError("checksum_mismatch", "Downloaded bytes do not match manifest")
                if "byte_size" in manifest and (type(manifest["byte_size"]) is not int or manifest["byte_size"] != len(data)):
                    raise DataError("byte_size_mismatch", "Manifest differs from exact bytes")
                rows, adapter = rows_from_bytes(data, metadata)
                # Fixture store mapping is declared; retain unknown stores without guessing.
                import csv
                store_file = Path(__file__).resolve().parents[2] / "goodwill/synthetic-data/10_stores.csv"
                with store_file.open(newline="") as handle:
                    known_stores = {r["store_id"] for r in csv.DictReader(handle)}
                known_stores.update(f"GW-{n:03d}" for n in range(1, 25))
                normalized, rejected, pending, duplicate_records = [], [], [], []
                seen = {}
                duplicates = corrections = 0
                for number, row in enumerate(rows, 1):
                    original = {k: v for k, v in row.items() if k is not None}
                    if None in row:
                        original["_extra_columns"] = row[None]
                    try:
                        record = normalize(row, adapter, metadata, known_stores)
                        fingerprint = digest(canonical(record).encode())
                        old = db.execute("SELECT v.* FROM active_sales a JOIN sale_versions v ON v.id=a.version_id WHERE a.source=? AND a.record_key=?", (source, record["record_key"])).fetchone()
                        prior = seen.get(record["record_key"])
                        if prior and prior != fingerprint:
                            raise DataError("conflicting_rows", "Same key has differing rows in one file")
                        if prior or (old and old["fingerprint"] == fingerprint):
                            status = "duplicate"
                            duplicates += 1
                            duplicate_records.append(record)
                        elif old:
                            if not allow_corrections:
                                raise DataError("correction_requires_approval", record["record_key"])
                            status = "corrected"
                            corrections += 1
                            pending.append((number, record, fingerprint, old["id"]))
                        else:
                            status = "accepted"
                            pending.append((number, record, fingerprint, None))
                        seen[record["record_key"]] = fingerprint
                        normalized.append(record)
                        db.execute("INSERT INTO staging_rows VALUES(?,?,?,?,?,NULL)", (batch_id, number, canonical(original), canonical(record), status))
                        for warning in record["warnings"]:
                            db.execute("INSERT INTO exceptions(id,batch_id,row_number,code,detail,owner_role,status) VALUES(?,?,?,?,?,?,?)", (uuid4().hex, batch_id, number, warning, "Preserve missing/unmapped input; no inferred replacement", "Data maintainer", "open"))
                    except DataError as exc:
                        rejected.append({"row_number": number, "code": exc.code, "detail": exc.detail})
                        db.execute("INSERT INTO staging_rows VALUES(?,?,?,NULL,?,?)", (batch_id, number, canonical(original), "rejected", exc.code))
                        db.execute("INSERT INTO exceptions(id,batch_id,row_number,code,detail,owner_role,status) VALUES(?,?,?,?,?,?,?)", (uuid4().hex, batch_id, number, exc.code, exc.detail, "Data maintainer", "open"))
                controls = reconcile(rows, normalized, rejected, duplicate_records, metadata, manifest)
                db.execute("UPDATE import_batches SET row_count=?,accepted_rows=?,rejected_rows=?,duplicate_rows=?,corrected_rows=?,reconciliation_json=? WHERE id=?", (len(rows), len(normalized)-duplicates, len(rejected), duplicates, corrections, canonical(controls), batch_id))
                if controls["state"] != "verified":
                    self._fail(db, batch_id, "reconciliation_blocked", canonical(controls))
                else:
                    # Overlap and correction handling changes only source-specific identity keys.
                    for number, record, fingerprint, supersedes in pending:
                        version_id = uuid4().hex
                        db.execute("INSERT INTO sale_versions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                   (version_id, source, record["record_key"], batch_id, number,
                                    record["reporting_date"], record["source_date"], record["source_timestamp"],
                                    record["platform"], record["store_id"], record["buyer_id"], record["currency"],
                                    record["item_id"], record["gross_cents"], record["refund_cents"], fingerprint,
                                    canonical(record), supersedes))
                        db.execute("INSERT INTO active_sales VALUES(?,?,?) ON CONFLICT(source,record_key) DO UPDATE SET version_id=excluded.version_id", (source, record["record_key"], version_id))
                    starts_at, ends_at = source_window(metadata)
                    same_window = db.execute("SELECT 1 FROM coverage_windows WHERE source=? AND starts_at=? AND ends_at=? AND scope_json=?", (source, starts_at, ends_at, canonical(metadata["filters"]))).fetchone()
                    if not same_window:
                        db.execute("INSERT INTO coverage_windows VALUES(?,?,?,?,?)", (source, batch_id, starts_at, ends_at, canonical(metadata["filters"])))
                    duplicate_only = not pending and previous_run and same_window
                    status = "duplicate_noop" if duplicate_only else "imported"
                    db.execute("UPDATE import_batches SET status=? WHERE id=?", (status, batch_id))
                    if not duplicate_only:
                        run_id = uuid4().hex
                        db.execute("INSERT INTO metric_runs VALUES(?,?,?,?,?)", (run_id, source, batch_id, METRIC_VERSION, timestamp))
                        db.execute("INSERT INTO metric_run_rows SELECT ?,version_id FROM active_sales WHERE source=?", (run_id, source))
                        db.execute("UPDATE source_publications SET run_id=? WHERE source=?", (run_id, source))
                    db.execute("INSERT INTO audit_events(recorded_at,action,reference,detail_json) VALUES(?,?,?,?)", (timestamp, status, batch_id, canonical({"explicit_corrections": allow_corrections, "correction_count": corrections})))
            except DataError as exc:
                self._fail(db, batch_id, exc.code, exc.detail)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        return self.batch(batch_id)

    @staticmethod
    def _fail(db, batch_id, code, detail):
        db.execute("UPDATE import_batches SET status='failed',error_code=?,error_detail=? WHERE id=?", (code, detail, batch_id))
        db.execute("INSERT INTO audit_events(recorded_at,action,reference,detail_json) VALUES(?,?,?,?)", (now(), "import_failed", batch_id, canonical({"code": code, "detail": detail})))

    def batch(self, batch_id):
        with self.db() as db:
            row = db.execute("SELECT b.*,f.checksum,f.artifact_ref,f.byte_size FROM import_batches b LEFT JOIN source_files f ON b.file_id=f.id WHERE b.id=?", (batch_id,)).fetchone()
            if row is None:
                raise DataError("not_found", "Unknown batch")
            exceptions = [dict(r) for r in db.execute("SELECT * FROM exceptions WHERE batch_id=? ORDER BY row_number,code", (batch_id,))]
            response = {"contract_version": CONTRACT_VERSION, "batch_id": batch_id, "source": row["source"],
                        "report_type": row["report_type"], "status": row["status"], "synthetic": True,
                        "file": {"file_id": row["file_id"], "checksum": row["checksum"], "byte_size": row["byte_size"]},
                        "period": {"start_date": row["request_start"], "end_date": row["request_end"], "source_timezone": row["source_timezone"]},
                        "counts": {key: row[key] for key in ("row_count", "accepted_rows", "rejected_rows", "duplicate_rows", "corrected_rows")},
                        "reconciliation": json.loads(row["reconciliation_json"]) if row["reconciliation_json"] else None,
                        "error": {"code": row["error_code"], "detail": row["error_detail"]} if row["error_code"] else None,
                        "exceptions": exceptions, "parser_version": row["parser_version"], "rule_version": row["rule_version"], "recorded_at": row["recorded_at"]}
            return validate("batch.schema.json", response)

    def batches(self):
        with self.db() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM import_batches ORDER BY recorded_at DESC,id DESC")]
        return [self.batch(batch_id) for batch_id in ids]

    def resolve_exception(self, exception_id, resolution):
        if not isinstance(resolution, str) or not resolution.strip():
            raise DataError("resolution_missing", "Human resolution note required")
        with self.db() as db:
            old = db.execute("SELECT * FROM exceptions WHERE id=?", (exception_id,)).fetchone()
            if not old:
                raise DataError("not_found", "Unknown exception")
            if old["status"] == "resolved":
                raise DataError("already_resolved", "Resolution is append-only")
            db.execute("UPDATE exceptions SET status='resolved',resolution=?,resolved_at=? WHERE id=?", (resolution, now(), exception_id))
            db.execute("INSERT INTO audit_events(recorded_at,action,reference,detail_json) VALUES(?,?,?,?)", (now(), "exception_resolved", exception_id, canonical({"resolution": resolution})))
