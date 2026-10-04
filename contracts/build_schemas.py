"""Generate the v1 schemas from a single structural source (stdlib only)."""
import json
from pathlib import Path

S = {"type": "string"}
TEXT = {"type": "string", "minLength": 1}
N = {"type": "integer", "minimum": 0}
B = {"type": "boolean"}
DATE = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}
MONEY = {"type": "string", "pattern": r"^-?\d+\.\d{2}$"}


def nullable(rule):
    return {"anyOf": [rule, {"type": "null"}]}


def enum(*values):
    return {"type": "string", "enum": list(values)}


def array(rule):
    return {"type": "array", "items": rule}


def obj(properties, optional=()):
    return {"type": "object", "properties": properties,
            "required": [k for k in properties if k not in optional], "additionalProperties": False}


VERSION = {"type": "string", "const": "goodwill-v1"}
SYNTHETIC = {"type": "boolean", "const": True}
FILTERS = obj({"start_date": DATE, "end_date": DATE, "source": TEXT, "platform": nullable(TEXT),
               "store": nullable(TEXT), "reporting_timezone": {"const": "America/New_York"}})
ERROR = obj({"code": TEXT, "detail": S})
COUNTS = obj({k: N for k in ("row_count", "accepted_rows", "rejected_rows", "duplicate_rows", "corrected_rows")})
RECON = obj({"source_rows": N, "accepted_rows": N, "rejected_rows": N, "duplicate_rows": N,
             "counts_balanced": B, "source_gross": nullable(MONEY), "source_refunds": nullable(MONEY),
             "accepted_gross": MONEY, "accepted_refunds": MONEY, "rejected_gross": nullable(MONEY),
             "rejected_refunds": nullable(MONEY), "duplicate_gross": MONEY, "duplicate_refunds": MONEY,
             "control_differences": array(TEXT), "state": enum("verified", "blocked")})
EXCEPTION = obj({"id": TEXT, "batch_id": TEXT, "row_number": nullable(N), "code": TEXT, "detail": S,
                 "owner_role": TEXT, "status": enum("open", "resolved"), "resolution": nullable(S), "resolved_at": nullable(S)})
METRIC = obj({"metric_id": TEXT, "metric_version": TEXT, "value": nullable(S), "unit": TEXT,
              "availability": enum("available", "partial", "unavailable"), "availability_reason": nullable(S), "definition": TEXT})
METRIC["anyOf"] = [
    {"properties": {"availability": {"const": "unavailable"}, "value": {"type": "null"}}},
    {"properties": {"availability": enum("available", "partial"), "metric_id": {"const": "M-DEMO-NET-SALES"}, "unit": {"const": "USD"}, "value": MONEY}},
    {"properties": {"availability": enum("available", "partial"), "metric_id": enum("M-PLATFORM-CUSTOMERS", "M-LISTINGS-CREATED", "M-UNLISTED-BACKLOG"),
                    "value": {"type": "string", "pattern": r"^\d+$"}}},
]

SCHEMAS = {
    "manifest": obj({"schema_version": VERSION, "source_schema_version": enum("replica-v1", "fixture-v1", "goodwill-v1"),
                     "source_name": TEXT, "report_type": TEXT, "requested_start_date": DATE, "requested_end_date": DATE,
                     "reporting_timezone": TEXT, "file_name": TEXT, "file_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                     "row_count": N, "currency": {"const": "USD", "type": "string"}, "synthetic": SYNTHETIC,
                     "filters": obj({"channels": array(TEXT), "accounts": array(TEXT), "order_ids": array(TEXT), "skus": array(TEXT),
                                     "payment_status": enum("All", "Paid", "Refunded")})}),
    "batch": obj({"contract_version": VERSION, "batch_id": TEXT, "source": TEXT, "report_type": TEXT,
                  "status": enum("imported", "duplicate_noop", "failed"), "synthetic": SYNTHETIC,
                  "file": obj({"file_id": TEXT, "checksum": TEXT, "byte_size": N}),
                  "period": obj({"start_date": DATE, "end_date": DATE, "source_timezone": TEXT}),
                  "counts": COUNTS, "reconciliation": nullable(RECON), "error": nullable(ERROR), "exceptions": array(EXCEPTION),
                  "parser_version": TEXT, "rule_version": TEXT, "recorded_at": TEXT}),
    "metrics": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "filters_applied": FILTERS,
                    "metric_run_id": nullable(TEXT), "metrics": array(METRIC),
                    "coverage": obj({"expected_days": array(DATE), "complete_days": array(DATE),
                                     "missing_or_partial_days": array(DATE), "state": enum("complete", "partial", "unavailable")}),
                    "freshness": obj({"published_at": nullable(TEXT), "latest_import_at": nullable(TEXT), "is_last_good": B,
                                      "publication_state": enum("published", "stale_last_good", "unpublished"), "warning": nullable(TEXT)}),
                    "reconciliation_state": enum("verified", "unpublished"),
                    "evidence": obj({"row_count": N, "gross_item_sales": nullable(MONEY), "refunds": nullable(MONEY), "missing_store_rows": N})}),
    "evidence": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "metric_run_id": TEXT, "filters_applied": FILTERS,
                     "offset": N, "limit": N, "total_rows": N, "scope_total": MONEY,
                     "rows": array(obj({"version_id": TEXT, "record_key": TEXT, "file_id": TEXT, "batch_id": TEXT,
                                        "source_row_number": N, "parser_version": TEXT, "rule_version": TEXT, "reporting_date": DATE,
                                        "source_date": DATE, "source_timestamp": nullable(TEXT), "platform": TEXT,
                                        "store_id": nullable(TEXT), "buyer_id": nullable(TEXT), "gross_item_sales": MONEY,
                                        "refunds": MONEY, "demo_net_sales": MONEY, "currency": {"const": "USD"},
                                        "synthetic": SYNTHETIC, "original_row": {"type": "object"}}))}),
    "error": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "error": ERROR}),
    "inventory": obj({"contract_version": VERSION, "synthetic": SYNTHETIC,
                      "start_date": DATE, "end_date": DATE, "snapshot_at": nullable(TEXT),
                      "store": nullable(TEXT), "metrics": array(METRIC), "input_ids": array(TEXT),
                      "coverage_state": enum("complete", "unavailable", "partial")}),
}


def main():
    root = Path(__file__).resolve().parent / "v1"
    root.mkdir(exist_ok=True)
    for name, schema in SCHEMAS.items():
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Goodwill v1 " + name, **schema}
        (root / (name + ".schema.json")).write_text(json.dumps(schema, indent=2) + "\n")


if __name__ == "__main__":
    main()
