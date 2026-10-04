"""Read-only fixture review. No importer, generator dependency, or acceptance gate."""
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "goodwill" / "synthetic-data"


def load(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    checks = []

    def check(name, expected, actual):
        checks.append({"check": name, "expected": expected, "actual": actual,
                       "passed": expected == actual})

    check("pack synthetic label", True, manifest["synthetic"])
    tables = {}
    for name, entry in manifest["files"].items():
        tables[name] = load(name)
        check(f"{name}: row count", entry["rows"], len(tables[name]))
        check(f"{name}: checksum", entry["sha256"],
              hashlib.sha256((ROOT / name).read_bytes()).hexdigest())

    metrics = []
    for platform, filename, gross, date_field, source_net in [
        ("ShopGoodwill", "06_shopgoodwill_periodic_reports_aug2026.csv",
         "gross_sales", "sale_date", "net_sales"),
        ("eBay", "08_ebay_listing_sales_aug2026.csv",
         "sale_amount", "sale_date", "payout_amount"),
        ("Upright", "02_upright_paid_order_items_aug2026.csv",
         "gross_sales", "paid_at", "net_sales"),
    ]:
        rows = tables[filename]
        gross_total = sum((Decimal(r[gross]) for r in rows), Decimal(0))
        refunds = sum((Decimal(r["refund_amount"]) for r in rows), Decimal(0))
        metrics.append({"source": platform, "file": filename, "rows": len(rows),
                        "gross_item_sales": str(gross_total), "refunds": str(refunds),
                        "demo_net_sales": str(gross_total - refunds),
                        "source_net_field": source_net,
                        "source_net_total": str(sum((Decimal(r[source_net]) for r in rows), Decimal(0))),
                        "missing_store_rows": sum(not r["store_id"] for r in rows),
                        "missing_buyer_rows": sum(not r["buyer_id"] for r in rows)})
        if platform == "Upright":
            continue  # No daily manifest controls for Upright.
        for day in sorted({r[date_field] for r in rows}):
            selected = [r for r in rows if r[date_field] == day]
            controls = [c for c in manifest["daily_core_metrics"]
                        if c["platform"] == platform and c["day"] == day]
            check(f"{platform}/{day}: exactly one control", 1, len(controls))
            if len(controls) != 1:
                continue
            control = controls[0]
            net = sum((Decimal(r[gross]) - Decimal(r["refund_amount"])
                       for r in selected), Decimal(0))
            check(f"{platform}/{day}: demo net sales", control["net_item_revenue"], str(net))
            check(f"{platform}/{day}: row count", control["rows"], len(selected))
            check(f"{platform}/{day}: buyers", control["distinct_platform_buyers"],
                  len({r["buyer_id"] for r in selected if r["buyer_id"]}))
            check(f"{platform}/{day}: missing stores", control["missing_store_rows"],
                  sum(not r["store_id"] for r in selected))

    missing = set()
    for name, rows in tables.items():
        if name[:2] not in {f"{i:02d}" for i in range(1, 10)}:
            continue
        for number, row in enumerate(rows, 1):
            for field in ("store_id", "buyer_id", "supplier"):
                if field in row and not row[field]:
                    missing.add((name, str(number), field))
    ledger = tables["14_quality_exceptions.csv"]
    declared = {(r["source_file"], r["source_row_id"], r["field"]) for r in ledger}
    # Contract decision: ledger counts root exceptions; related shipping rows
    # retain explicit lineage to the original missing-store order.
    source_orders = {r["order_id"]: (n, r) for n, r in enumerate(tables["06_shopgoodwill_periodic_reports_aug2026.csv"], 1)}
    propagated = []
    for n, r in enumerate(tables["04_shipping_osm_pb_easypost_aug2026.csv"], 1):
        if not r["store_id"]:
            origin = source_orders.get(r["order_id"])
            root_location = ("06_shopgoodwill_periodic_reports_aug2026.csv", str(origin[0]), "store_id") if origin else None
            if origin and not origin[1]["store_id"] and root_location in declared:
                propagated.append({"source_file": "04_shipping_osm_pb_easypost_aug2026.csv", "source_row_number": n,
                                   "record_id": r["order_id"], "root_source_file": root_location[0],
                                   "root_source_row_number": origin[0], "field": "store_id"})
    propagated_locations = {(r["source_file"], str(r["source_row_number"]), r["field"]) for r in propagated}
    check("root exceptions plus explicit propagated lineage cover source gaps", sorted(declared | propagated_locations), sorted(missing))
    check("exception ledger count", manifest["expected_exceptions"], len(ledger))
    check("exception ledger unique locations", len(ledger), len(declared))

    snapshots = tables["12_inventory_snapshots_aug2026.csv"]
    check("unique item/snapshot keys", len(snapshots),
          len({(r["snapshot_at"], r["item_id"]) for r in snapshots}))
    snapshot_summaries = []
    unlisted = {"received", "awaiting_inspection", "awaiting_photography", "ready_to_list"}
    for cutoff, control in manifest["inventory_controls"].items():
        selected = [r for r in snapshots if r["snapshot_at"] == cutoff]
        states = dict(Counter(r["workflow_state"] for r in selected))
        backlog = sum(r["workflow_state"] in unlisted for r in selected)
        check(f"{cutoff}: inventory", control["total_inventory"], len(selected))
        check(f"{cutoff}: backlog", control["unlisted_backlog"], backlog)
        check(f"{cutoff}: states", control["workflow_states"], states)
        snapshot_summaries.append({"snapshot_at": cutoff, "inventory": len(selected), "backlog": backlog})

    listings = tables["11_listing_events_aug2026.csv"]
    months = dict(Counter(datetime.fromisoformat(r["listed_at"]).strftime("%Y-%m") for r in listings))
    result = {"scope": "preparatory fixture review; not importer or task acceptance",
              "expected_result_basis": "existing generated manifest; not independent QA ledger",
              "currency": manifest["currency"], "metrics_by_source": metrics,
              "combined_revenue": None,
              "combined_revenue_reason": "source authority/overlap decisions are unresolved",
              "listing_month_counts": months, "snapshots": snapshot_summaries,
              "propagated_store_rows": propagated,
              "exception_fields": dict(Counter(r["field"] for r in ledger)),
              "checks": checks, "passed": all(c["passed"] for c in checks)}
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
