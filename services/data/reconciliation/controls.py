from services.data.contracts import DataError, cents, money


def reconcile(rows, normalized, rejected, duplicate_records, metadata, original_manifest):
    """Unavailable source money stays null. Any rejected row blocks publication."""
    gross = refunds = 0
    controls_available = True
    gross_field = "item_revenue" if metadata["source_name"].startswith("cash_monkey") else (
        "sale_amount" if metadata["source_name"] == "ebay_fixture" else "gross_sales")
    for row in rows:
        try:
            gross += cents(row.get(gross_field))
            refunds += cents(row.get("refund_amount"))
        except DataError:
            controls_available = False
    duplicate_gross = sum(r["gross_cents"] for r in duplicate_records)
    duplicate_refunds = sum(r["refund_cents"] for r in duplicate_records)
    accepted_gross = sum(r["gross_cents"] for r in normalized)-duplicate_gross
    accepted_refunds = sum(r["refund_cents"] for r in normalized)-duplicate_refunds
    duplicates = len(duplicate_records)
    differences = []
    if controls_available:
        for key, actual in (("item_sales", gross), ("refunds", refunds), ("demo_net_sales", gross-refunds)):
            if key in original_manifest and cents(original_manifest[key]) != actual:
                differences.append(key)
    result = {"source_rows": len(rows), "accepted_rows": len(normalized)-duplicates,
              "rejected_rows": len(rejected), "duplicate_rows": duplicates,
              "counts_balanced": len(normalized) + len(rejected) == len(rows),
              "source_gross": money(gross) if controls_available else None,
              "source_refunds": money(refunds) if controls_available else None,
              "accepted_gross": money(accepted_gross), "accepted_refunds": money(accepted_refunds),
              "duplicate_gross": money(duplicate_gross), "duplicate_refunds": money(duplicate_refunds),
              "rejected_gross": money(gross-accepted_gross-duplicate_gross) if controls_available else None,
              "rejected_refunds": money(refunds-accepted_refunds-duplicate_refunds) if controls_available else None,
              "control_differences": differences,
              "state": "verified" if not rejected and not differences and controls_available else "blocked"}
    return result
