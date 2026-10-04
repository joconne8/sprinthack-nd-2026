"""Explicit fixture/intake handoffs; production formats are not asserted."""
import csv
import json
from pathlib import Path

from services.data.contracts import DataError, digest

FIXTURE_SOURCES = {
    "01_cash_monkey_orders_aug2026.csv": ("cash_monkey_fixture", "orders"),
    "02_upright_paid_order_items_aug2026.csv": ("upright_fixture", "paid_order_items"),
    "06_shopgoodwill_periodic_reports_aug2026.csv": ("shopgoodwill_fixture", "sales"),
    "08_ebay_listing_sales_aug2026.csv": ("ebay_fixture", "sales"),
}


def fixture_manifest(csv_path, start, end, source, report_type):
    path = Path(csv_path)
    data = path.read_bytes()
    with path.open(newline="", encoding="utf-8") as handle:
        count = len(list(csv.DictReader(handle)))
    return {"schema_version": "fixture-v1", "source_name": source, "report_type": report_type,
            "requested_start_date": start, "requested_end_date": end, "reporting_timezone": "America/Indiana/Indianapolis",
            "file_name": path.name, "file_checksum": digest(data), "byte_size": len(data), "row_count": count,
            "currency": "USD", "synthetic": True}


def import_intake(pipeline, record_path, allow_corrections=False):
    """Consume Hugh's full acquisition run record, not its incomplete outbox stub."""
    record = json.loads(Path(record_path).read_text())
    if record.get("acquisition_state") != "acquired_verified" or record.get("synthetic") is not True:
        raise DataError("intake_not_verified", "Require verified synthetic acquisition record")
    required = ("artifact_ref", "checksum", "byte_size", "row_count", "source_name", "report_type",
                "requested_start_date", "requested_end_date", "reporting_timezone")
    if any(key not in record for key in required):
        raise DataError("intake_incomplete", "Use the full runs/<run_id>.json record")
    path = Path(record["artifact_ref"])
    if "manifest" in record:
        from acquisition.intake import submit
        return submit(record, pipeline, allow_corrections)[0]
    metadata = {key: record[key] for key in ("source_name", "report_type", "requested_start_date", "requested_end_date", "reporting_timezone", "row_count", "byte_size")}
    metadata.update(schema_version="goodwill-v1", file_name=path.name,
                    file_checksum=record["checksum"], currency="USD", synthetic=True,
                    acquisition_run_id=record.get("run_id"))
    # Intake's original record omits query filters/control totals. Conservatively
    # mark that scope unknown until the complete portal manifest is supplied.
    metadata["payment_status"] = "Paid"
    return pipeline.import_file(path, metadata, allow_corrections)
