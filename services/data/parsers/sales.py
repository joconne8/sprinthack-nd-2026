"""Source-specific grains; never use a source net/payout field as demo net sales."""
import csv
import io
from datetime import datetime
from zoneinfo import ZoneInfo

from services.data.contracts import DataError, REPORTING_ZONE, canonical, cents, day

ADAPTERS = {
    ("upright_replica", "paid_orders"): ("gross_sales", "refund_amount", "paid_at", ["paid_order_id"], "channel"),
    ("upright_replica", "paid_order_items"): ("gross_sales", "refund_amount", "paid_at", ["paid_order_id", "item_id"], "channel"),
    ("cash_monkey_replica", "orders"): ("item_revenue", "refund_amount", "order_date", ["unit_id"], "channel"),
    ("upright_fixture", "paid_order_items"): ("gross_sales", "refund_amount", "paid_at", ["paid_order_id", "item_id"], "channel"),
    ("shopgoodwill_fixture", "sales"): ("gross_sales", "refund_amount", "sale_date", ["order_id", "item_id"], None),
    ("ebay_fixture", "sales"): ("sale_amount", "refund_amount", "sale_date", ["transaction_id"], None),
    ("cash_monkey_fixture", "orders"): ("item_revenue", "refund_amount", "order_date", ["order_id"], None),
}
PLATFORMS = {"Shopgoodwill": "ShopGoodwill", "ShopGoodwill": "ShopGoodwill", "eBay": "eBay",
             "Goodwillfinds": "GoodwillFinds", "Goodwillbooks": "GoodwillBooks", "Amazon-MF": "Amazon-MF"}


def rows_from_bytes(data, metadata):
    adapter = ADAPTERS.get((metadata["source_name"], metadata["report_type"]))
    if not adapter:
        raise DataError("unsupported_report", "Sales adapter unavailable; expenses/settlements cannot enter revenue")
    try:
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
        fields = reader.fieldnames
        required = {adapter[0], adapter[1], adapter[2], "store_id", "buyer_id", *adapter[3]}
        if metadata["source_name"].endswith("_replica"):
            required.update({"currency", "synthetic", "source_name", "reporting_timezone", "reporting_date", "grain"})
        if adapter[4]:
            required.add(adapter[4])
        if not fields or len(fields) != len(set(fields)) or required - set(fields):
            raise DataError("invalid_headers", "Missing or duplicate required headers")
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as exc:
        raise DataError("malformed_csv", str(exc))
    if len(rows) != metadata["row_count"]:
        raise DataError("row_count_mismatch", f"{len(rows)} != {metadata['row_count']}")
    return rows, adapter


def normalize(row, adapter, metadata, known_stores):
    gross_field, refund_field, date_field, keys, platform_field = adapter
    if None in row or any(value is None for value in row.values()):
        raise DataError("malformed_row", "Column count differs from header")
    if any(not row[key].strip() for key in keys):
        raise DataError("missing_record_id", ",".join(keys))
    gross, refunds = cents(row[gross_field]), cents(row[refund_field])
    if gross < 0 or refunds < 0 or refunds > gross:
        raise DataError("invalid_amount_range", "Require 0 <= refunds <= item sales")
    if "quantity" in row and (not row["quantity"].isdigit() or int(row["quantity"]) < 1):
        raise DataError("invalid_quantity", "Expected a positive integer; item amount is already row-level")
    source_stamp = None
    if "T" in row[date_field]:
        try:
            stamp = datetime.fromisoformat(row[date_field].replace("Z", "+00:00"))
        except ValueError:
            raise DataError("invalid_date", row[date_field])
        if stamp.tzinfo is None:
            raise DataError("timezone_missing", "Timestamp must have an explicit offset")
        source_stamp = stamp.isoformat()
        source_day = stamp.astimezone(ZoneInfo(metadata["reporting_timezone"])).date()
        reporting_day = stamp.astimezone(ZoneInfo(REPORTING_ZONE)).date()
    else:
        source_day = reporting_day = day(row[date_field])
    if not day(metadata["requested_start_date"]) <= source_day <= day(metadata["requested_end_date"]):
        raise DataError("row_outside_period", str(source_day))
    if metadata["source_name"].endswith("_replica"):
        if row["synthetic"] != "true" or row["source_name"] != metadata["source_name"]:
            raise DataError("source_label_mismatch", "Require matching synthetic source identity")
        if row["currency"] != metadata["currency"]:
            raise DataError("currency_mismatch", row["currency"])
        if row["reporting_timezone"] != metadata["reporting_timezone"] or row["reporting_date"] != str(source_day):
            raise DataError("reporting_date_mismatch", "Row metadata conflicts with source timestamp/manifest")
        expected_grain = {"paid_orders": "one row per paid order", "paid_order_items": "one row per paid order item", "orders": "one row per unit"}[metadata["report_type"]]
        if row["grain"] != expected_grain:
            raise DataError("grain_mismatch", row["grain"])
    if platform_field:
        platform = PLATFORMS.get(row[platform_field], row[platform_field])
        if not platform:
            raise DataError("platform_missing", "No platform identity")
    else:
        platform = {"shopgoodwill_fixture": "ShopGoodwill", "ebay_fixture": "eBay", "cash_monkey_fixture": "CashMonkey"}[metadata["source_name"]]
    store = row["store_id"].strip() or None
    buyer = row["buyer_id"].strip() or None
    warnings = []
    if store is None:
        warnings.append("missing_store")
    elif store not in known_stores:
        warnings.append("unmapped_store")
    if buyer is None:
        warnings.append("missing_buyer")
    record = {"record_key": canonical([row[key] for key in keys]), "source": metadata["source_name"],
              "reporting_date": str(reporting_day), "source_date": str(source_day),
              "source_timestamp": source_stamp, "platform": platform,
              "store_id": store, "buyer_id": buyer, "currency": metadata["currency"],
              "item_id": row.get("item_id") or row.get("sku") or None,
              "gross_cents": gross, "refund_cents": refunds, "warnings": warnings}
    return record
