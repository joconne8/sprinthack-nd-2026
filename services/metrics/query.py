"""Responses are based exclusively on immutable published metric-run rows."""
import json

from services.data.contracts import (CONTRACT_VERSION, METRIC_VERSION, REPORTING_ZONE,
                                    DataError, day, money, validate)
from services.data.publication.coverage import covered_days

STRATEGIC = {
    "R-LABOR-PRODUCTIVITY": "Matched labor hours and allocation policy are unavailable",
    "R-MARGIN": "Approved costs and allocations are unavailable",
    "R-SELL-THROUGH": "Approved eligible cohort, window and relist policy are unavailable",
    "R-REVENUE-GROWTH": "Comparable prior-year inputs are unavailable",
}


def scope(start, end, source, platform=None, store=None):
    if day(start) > day(end) or (day(end)-day(start)).days > 365:
        raise DataError("invalid_period", "Select an ordered period of at most 366 days")
    if not isinstance(source, str) or not source:
        raise DataError("source_required", "Choose one authoritative source; combined revenue is unavailable")
    return {"start_date": start, "end_date": end, "source": source, "platform": platform,
            "store": store, "reporting_timezone": REPORTING_ZONE}


def published_rows(db, run_id, filters):
    rows = db.execute("SELECT v.*,b.file_id,b.parser_version,b.rule_version FROM metric_run_rows m JOIN sale_versions v ON v.id=m.version_id JOIN import_batches b ON b.id=v.batch_id WHERE m.run_id=? AND v.reporting_date BETWEEN ? AND ? ORDER BY v.reporting_date,v.record_key", (run_id, filters["start_date"], filters["end_date"])).fetchall()
    result = []
    for row in rows:
        normalized = json.loads(row["normalized_json"])
        if filters["platform"] and row["platform"] != filters["platform"]:
            continue
        if filters["store"] == "unknown":
            if not any(w in normalized["warnings"] for w in ("missing_store", "unmapped_store")):
                continue
        elif filters["store"] and row["store_id"] != filters["store"]:
            continue
        result.append(row)
    return result


def metric_response(pipeline, start, end, source, platform=None, store=None, run_id=None):
    filters = scope(start, end, source, platform, store)
    with pipeline.db() as db:
        publication = db.execute("SELECT p.*,r.published_at FROM source_publications p LEFT JOIN metric_runs r ON r.id=p.run_id WHERE p.source=?", (source,)).fetchone()
        chosen_run = run_id or (publication["run_id"] if publication else None)
        if run_id:
            historical = db.execute("SELECT * FROM metric_runs WHERE id=? AND source=?", (run_id, source)).fetchone()
            if not historical:
                raise DataError("not_found", "Unknown metric run for selected source")
        else:
            historical = None
        rows = published_rows(db, chosen_run, filters) if chosen_run else []
        latest_batch = db.execute("SELECT * FROM import_batches WHERE id=?", (publication["latest_batch_id"],)).fetchone() if publication else None
        stale = bool(latest_batch and latest_batch["status"] == "failed" and chosen_run)
        windows = []
        # A historical run's coverage must not borrow windows from future imports.
        run_time = historical["published_at"] if historical else (publication["published_at"] if publication else None)
        for row in db.execute("SELECT w.*,b.recorded_at FROM coverage_windows w JOIN import_batches b ON b.id=w.batch_id WHERE w.source=? AND b.recorded_at<=?", (source, run_time or "")):
            report_filters = json.loads(row["scope_json"])
            full = not any(report_filters.get(k) for k in ("channels", "accounts", "order_ids", "skus")) and report_filters.get("payment_status") == "All"
            if full:
                windows.append(row)
        coverage = covered_days(windows, start, end)
        availability = "available" if chosen_run and coverage["state"] == "complete" else "partial" if rows else "unavailable"
        warning = "Latest import failed; retaining verified last-good data" if stale else None
        if warning and availability == "available":
            availability = "partial"
        reason = warning or ("Required reporting days or full-source report coverage are missing" if availability != "available" else None)
        value = money(sum(r["gross_cents"]-r["refund_cents"] for r in rows)) if availability != "unavailable" else None
        buyers = {(r["platform"], r["buyer_id"]) for r in rows if r["buyer_id"]}
        platforms = {r["platform"] for r in rows}
        buyer_missing = any(not r["buyer_id"] for r in rows)
        buyer_state = "unavailable" if buyer_missing or len(platforms) > 1 else availability
        buyer_reason = "Buyer IDs missing; affected customer metric is unavailable" if buyer_missing else "Select one platform; cross-platform unique customers are unavailable" if len(platforms) > 1 else reason
        metrics = [
            {"metric_id": "M-DEMO-NET-SALES", "metric_version": METRIC_VERSION, "value": value,
             "unit": "USD", "availability": availability, "availability_reason": reason,
             "definition": "Item sales minus refunds; excludes shipping, tax and fees"},
            {"metric_id": "M-PLATFORM-CUSTOMERS", "metric_version": "platform-customers-v1",
             "value": str(len(buyers)) if buyer_state != "unavailable" else None, "unit": "buyers",
             "availability": buyer_state, "availability_reason": buyer_reason,
             "definition": "Distinct non-empty buyer IDs within one platform and selected period"},
        ]
        metrics.extend({"metric_id": key, "metric_version": "roadmap-v1", "value": None, "unit": "unavailable",
                        "availability": "unavailable", "availability_reason": detail,
                        "definition": "Requires approved matching inputs and definitions"} for key, detail in STRATEGIC.items())
        response = {"contract_version": CONTRACT_VERSION, "synthetic": True, "filters_applied": filters,
                    "metric_run_id": chosen_run, "metrics": metrics, "coverage": coverage,
                    "freshness": {"published_at": run_time, "latest_import_at": latest_batch["recorded_at"] if latest_batch else None,
                                  "is_last_good": stale, "publication_state": "stale_last_good" if stale else "published" if chosen_run else "unpublished",
                                  "warning": warning},
                    "reconciliation_state": "verified" if chosen_run else "unpublished",
                    "evidence": {"row_count": len(rows), "gross_item_sales": money(sum(r["gross_cents"] for r in rows)) if chosen_run else None,
                                 "refunds": money(sum(r["refund_cents"] for r in rows)) if chosen_run else None,
                                 "missing_store_rows": sum("missing_store" in json.loads(r["normalized_json"])["warnings"] for r in rows)}}
        return validate("metrics.schema.json", response)


def evidence_response(pipeline, run_id, start, end, source, platform=None, store=None, offset=0, limit=100):
    filters = scope(start, end, source, platform, store)
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 200:
        raise DataError("invalid_pagination", "Nonnegative offset and limit 1..200 required")
    with pipeline.db() as db:
        if not db.execute("SELECT 1 FROM metric_runs WHERE id=? AND source=?", (run_id, source)).fetchone():
            raise DataError("not_found", "Unknown metric run")
        selected = published_rows(db, run_id, filters)
        result = []
        for row in selected[offset:offset+limit]:
            original = db.execute("SELECT original_json FROM staging_rows WHERE batch_id=? AND row_number=?", (row["batch_id"], row["row_number"])).fetchone()
            result.append({"version_id": row["id"], "record_key": row["record_key"], "file_id": row["file_id"],
                           "batch_id": row["batch_id"], "source_row_number": row["row_number"],
                           "parser_version": row["parser_version"], "rule_version": row["rule_version"],
                           "reporting_date": row["reporting_date"], "source_date": row["source_date"],
                           "source_timestamp": row["source_timestamp"], "platform": row["platform"],
                           "store_id": row["store_id"], "buyer_id": row["buyer_id"],
                           "gross_item_sales": money(row["gross_cents"]), "refunds": money(row["refund_cents"]),
                           "demo_net_sales": money(row["gross_cents"]-row["refund_cents"]),
                           "currency": row["currency"], "synthetic": True, "original_row": json.loads(original[0])})
        response = {"contract_version": CONTRACT_VERSION, "synthetic": True, "metric_run_id": run_id,
                    "filters_applied": filters, "offset": offset, "limit": limit, "total_rows": len(selected),
                    "rows": result, "scope_total": money(sum(r["gross_cents"]-r["refund_cents"] for r in selected))}
        return validate("evidence.schema.json", response)
