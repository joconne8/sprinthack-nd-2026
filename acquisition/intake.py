"""ING-03 draft: verify an acquired report file and register it as an immutable artifact.

Acquisition success means "a verified file is archived", NOT "metrics published".
Import/publication is a separate state recorded later by the importer (DAT-02).
The frozen GOV-03 import contract does not exist yet, so submit() writes a
hand-off record into a local outbox that a real importer can replace.
All field names below are draft and must be reconciled with GOV-03.
"""
import csv
import hashlib
import io
import json
import os
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path

INTAKE_VERSION = "intake-draft-v1"

# Expected CSV headers per (source, report_type). Draft; owned by the source/parsing contract.
EXPECTED_HEADERS = {
    ("upright_replica", "paid_orders"): [
        "paid_order_id", "paid_at", "item_id", "store_id", "channel", "buyer_id", "item_title",
        "category", "quantity", "gross_sales", "shipping_collected", "sales_tax", "marketplace_fee",
        "refund_amount", "net_sales", "source_name", "synthetic", "grain", "reporting_date",
        "reporting_timezone", "currency"],
    ("cash_monkey_replica", "orders"): [
        "order_id", "unit_id", "order_date", "sku", "title", "category", "store_id", "buyer_id",
        "account", "channel", "quantity", "item_revenue", "shipping_revenue", "refund_amount",
        "payment_fee", "payout_amount", "source_name", "synthetic", "grain", "reporting_date",
        "reporting_timezone", "currency"],
}
REQUIRED_MANIFEST = [
    "source_name", "report_type", "requested_start_date", "requested_end_date", "file_name",
    "file_checksum", "row_count", "synthetic", "reporting_timezone"]


class IntakeRejected(Exception):
    """File failed verification. Nothing was archived or handed off."""

    def __init__(self, code, detail):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def verify(file_path, manifest, requested_start, requested_end, expected_source, expected_report_type):
    """Return the verified bytes' facts or raise IntakeRejected. Never guesses or repairs."""
    path = Path(file_path)
    if not path.is_file():
        raise IntakeRejected("file_missing", str(path))
    data = path.read_bytes()
    if not data:
        raise IntakeRejected("file_empty", str(path))
    missing = [k for k in REQUIRED_MANIFEST if k not in manifest]
    if missing:
        raise IntakeRejected("manifest_incomplete", ",".join(missing))
    if manifest["source_name"] != expected_source or manifest["report_type"] != expected_report_type:
        raise IntakeRejected("wrong_report", f"{manifest['source_name']}/{manifest['report_type']}")
    if (manifest["requested_start_date"], manifest["requested_end_date"]) != (requested_start, requested_end):
        raise IntakeRejected("wrong_period_in_manifest", f"{manifest['requested_start_date']}..{manifest['requested_end_date']}")
    checksum = _sha256(data)
    if checksum != manifest["file_checksum"]:
        raise IntakeRejected("checksum_mismatch", f"{checksum} != {manifest['file_checksum']}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntakeRejected("not_utf8", str(exc))
    rows = list(csv.reader(io.StringIO(text)))
    expected = EXPECTED_HEADERS.get((expected_source, expected_report_type))
    if expected is None:
        raise IntakeRejected("unknown_schema", f"{expected_source}/{expected_report_type}")
    if rows[0] != expected:
        raise IntakeRejected("unexpected_schema", f"header {rows[0]}")
    body = rows[1:]
    if len(body) != manifest["row_count"]:
        raise IntakeRejected("row_count_mismatch", f"{len(body)} != {manifest['row_count']}")
    col = {name: i for i, name in enumerate(rows[0])}
    for n, row in enumerate(body, start=2):
        if len(row) != len(expected):
            raise IntakeRejected("malformed_row", f"line {n}")
        if row[col["synthetic"]] != "true":
            raise IntakeRejected("not_labeled_synthetic", f"line {n}")
        if not (requested_start <= row[col["reporting_date"]] <= requested_end):
            raise IntakeRejected("row_outside_requested_period", f"line {n}: {row[col['reporting_date']]}")
    dates = sorted(r[col["reporting_date"]] for r in body)
    return {"checksum": checksum, "byte_size": len(data), "row_count": len(body),
            "coverage_start": dates[0] if dates else None, "coverage_end": dates[-1] if dates else None}


def archive(file_path, checksum, archive_root):
    """Content-addressed, read-only copy. Same bytes -> same reference; never overwritten."""
    root = Path(archive_root)
    dest = root / checksum[:2] / f"{checksum}.csv"
    if dest.exists():
        if _sha256(dest.read_bytes()) != checksum:
            raise IntakeRejected("archive_corrupt", str(dest))
        return dest, False
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp")
    shutil.copyfile(file_path, tmp)
    os.chmod(tmp, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    os.replace(tmp, dest)
    return dest, True


def intake(file_path, manifest, run_id, requested_start, requested_end, expected_source,
           expected_report_type, archive_root, now=None):
    """Verify, archive, and write an acquisition record. State is 'acquired_verified' only."""
    facts = verify(file_path, manifest, requested_start, requested_end, expected_source, expected_report_type)
    dest, created = archive(file_path, facts["checksum"], archive_root)
    record = {
        "intake_version": INTAKE_VERSION,
        "run_id": run_id,
        "acquisition_state": "acquired_verified",
        "import_state": "not_submitted",
        "source_name": expected_source,
        "report_type": expected_report_type,
        "requested_start_date": requested_start,
        "requested_end_date": requested_end,
        "reporting_timezone": manifest["reporting_timezone"],
        "artifact_ref": str(dest),
        "newly_archived": created,
        "synthetic": manifest["synthetic"],
        "recorded_at": (now or datetime.now(timezone.utc)).isoformat(),
        **facts,
    }
    rec_path = Path(archive_root) / "runs" / f"{run_id}.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    if rec_path.exists():
        raise IntakeRejected("run_id_reused", run_id)
    rec_path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def submit(record, outbox):
    """Hand the verified artifact to the importer via a local outbox (placeholder for GOV-03).

    Idempotent per checksum+period: resubmission does not create a second hand-off.
    Moves nothing about import_state; the importer owns that transition.
    """
    key = f"{record['checksum']}_{record['requested_start_date']}_{record['requested_end_date']}"
    out = Path(outbox) / f"{key}.json"
    if out.exists():
        return out, False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"run_id": record["run_id"], "artifact_ref": record["artifact_ref"],
                               "checksum": record["checksum"], "source_name": record["source_name"],
                               "report_type": record["report_type"]}, indent=2) + "\n")
    return out, True
