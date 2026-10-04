"""Verify a synthetic report, archive exact bytes, then submit to the real importer.

Acquisition success means "a verified file is archived", NOT "metrics published".
Import/publication is a separate state recorded later by the importer (DAT-02).
The original manifest is retained, so filters/controls survive the handoff.
Acquisition verification, import and publication have separate recorded states.
write_import_request() preserves the file-based handoff; submit() imports directly.
"""
import csv
import hashlib
import io
import json
import os
import shutil
import stat
import re
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
    if manifest.get('synthetic') is not True or manifest.get('currency') != 'USD':
        raise IntakeRejected('manifest_not_synthetic_usd', 'Require synthetic USD manifest')
    if type(manifest['row_count']) is not int or manifest['row_count'] < 0:
        raise IntakeRejected('invalid_row_count', 'Expected nonnegative integer')
    if 'byte_size' in manifest and manifest['byte_size'] != len(data):
        raise IntakeRejected('byte_size_mismatch', 'Manifest differs from downloaded bytes')
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
    if not rows or rows[0] != expected:
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
    if not isinstance(run_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', run_id):
        raise IntakeRejected('run_id_invalid', 'Use a bounded safe run identity')
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
        "manifest": manifest,
        **facts,
    }
    rec_path = Path(archive_root) / "runs" / f"{run_id}.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    if rec_path.exists():
        raise IntakeRejected("run_id_reused", run_id)
    rec_path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def _verified_bytes(record):
    """Recheck the archived artifact before either importer handoff."""
    if record.get('acquisition_state') != 'acquired_verified' or 'manifest' not in record:
        raise IntakeRejected('intake_incomplete', 'Use a verified run with original manifest')
    data = Path(record['artifact_ref']).read_bytes()
    if _sha256(data) != record['checksum'] or len(data) != record['byte_size']:
        raise IntakeRejected('archive_corrupt', 'Verified artifact changed before submission')
    return data


def write_import_request(record, outbox):
    """Archive → goodwill-v1 request file; publication remains the importer's job."""
    from services.data.contracts import validate
    data = _verified_bytes(record)
    request = {'csv_text': data.decode('utf-8'), 'manifest': record['manifest']}
    validate('import-request.schema.json', request)
    key = f"{record['checksum']}_{record['requested_start_date']}_{record['requested_end_date']}"
    destination = Path(outbox) / f'{key}.import-request.json'
    if destination.exists():
        if json.loads(destination.read_text()) != request:
            raise IntakeRejected('handoff_conflict', 'Existing request differs from the verified handoff')
        return destination, False
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(request) + '\n')
    os.replace(temporary, destination)
    return destination, True


def submit(record, pipeline, allow_corrections=False):
    """Verified run → real batch. Repeated calls on a delivered run reuse its batch."""
    data = _verified_bytes(record)
    if record.get('batch_id'):
        return pipeline.batch(record['batch_id']), False
    manifest = dict(record['manifest'], acquisition_run_id=record['run_id'])
    batch = pipeline.import_bytes(data, manifest, allow_corrections)
    record['batch_id'] = batch['batch_id']
    record['import_state'] = batch['status']
    record['publication_state'] = 'blocked' if batch['status'] == 'failed' else 'published'
    record_path = Path(record['artifact_ref']).parents[1] / 'runs' / (record['run_id'] + '.json')
    temporary = record_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, indent=2) + '\n')
    os.replace(temporary, record_path)
    return batch, True
