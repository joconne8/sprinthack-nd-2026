import csv
import io

from services.data.contracts import digest

FIELDS = ["paid_order_id", "paid_at", "item_id", "store_id", "channel", "buyer_id", "item_title",
          "category", "quantity", "gross_sales", "shipping_collected", "sales_tax", "marketplace_fee",
          "refund_amount", "net_sales", "source_name", "synthetic", "grain", "reporting_date", "reporting_timezone", "currency"]


def row(key="A", gross="10.00", refund="1.00", day="2026-09-30", **changes):
    result = dict(zip(FIELDS, [key, day+"T16:00:00+00:00", "ITEM-"+key, "GW-001", "eBay", "BUYER-"+key,
                              "Synthetic item", "Books", "1", gross, "99.00", "88.00", "77.00", refund, "9999.00",
                              "upright_replica", "true", "one row per paid order", day, "America/New_York", "USD"]))
    result.update(changes)
    return result


def payload(rows, start="2026-09-30", end="2026-09-30", **changes):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\r\n")
    writer.writeheader()
    writer.writerows(rows)
    data = output.getvalue().encode()
    manifest = {"schema_version": "replica-v1", "source_name": "upright_replica", "report_type": "paid_orders",
                "requested_start_date": start, "requested_end_date": end, "reporting_timezone": "America/New_York",
                "file_name": "test.csv", "file_checksum": digest(data), "row_count": len(rows), "currency": "USD", "synthetic": True}
    manifest.update(changes)
    return data, manifest
