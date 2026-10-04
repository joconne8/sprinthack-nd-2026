"""Generate the v1 schemas from a single structural source (stdlib only)."""
import json
from pathlib import Path

S = {"type": "string"}
TEXT = {"type": "string", "minLength": 1}
N = {"type": "integer", "minimum": 0}
B = {"type": "boolean"}
DATE = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$", "format": "date"}
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
                     "offset": N, "limit": {"type": "integer", "minimum": 1, "maximum": 200}, "total_rows": N, "scope_total": MONEY,
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

QUERY = obj({"start_date": DATE, "end_date": DATE, "source": TEXT,
             "platform": TEXT, "store": TEXT, "run_id": TEXT},
            optional=("platform", "store", "run_id"))
EVIDENCE_QUERY = obj({**QUERY["properties"], "offset": N,
                      "limit": {"type": "integer", "minimum": 1, "maximum": 200}},
                     optional=("platform", "store", "offset", "limit"))
NORMALIZED_ROW = obj({"record_key": TEXT, "source": TEXT, "reporting_date": DATE,
                      "source_date": DATE, "source_timestamp": nullable(TEXT), "platform": TEXT,
                      "store_id": nullable(TEXT), "buyer_id": nullable(TEXT), "currency": {"const": "USD"},
                      "item_id": nullable(TEXT), "gross_cents": {"type": "integer"},
                      "refund_cents": {"type": "integer"}, "warnings": array(TEXT)})
SCHEMAS.update({
    "metrics-query": QUERY,
    "evidence-query": EVIDENCE_QUERY,
    # Preserve vendor/replica metadata; manifest_metadata validates the normalized
    # manifest before any raw-file/database write. This is the transport envelope.
    "import-request": obj({"csv_text": TEXT, "manifest": {"type": "object"},
                           "allow_corrections": B}, optional=("allow_corrections",)),
    "resolution-request": obj({"resolution": {"type": "string", "pattern": r"\S", "minLength": 1}}),
    "imports": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "imports": array(SCHEMAS["batch"])}),
    "staging": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "total_rows": N,
                    "rows": array(obj({"source_row_number": {"type": "integer", "minimum": 1},
                                       "status": enum("accepted", "duplicate", "corrected", "rejected"),
                                       "reason": nullable(TEXT), "file_id": TEXT, "batch_id": TEXT,
                                       "original_row": {"type": "object"},
                                       "normalized_row": nullable(NORMALIZED_ROW)}))}),
    "health": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "status": {"const": "ok"}}),
    "resolution": obj({"contract_version": VERSION, "synthetic": SYNTHETIC, "status": {"const": "resolved"}}),
    # Design-only, read-only tools. These schemas do not activate an assistant,
    # tenant identity, query execution service, or browser action.
    "tool-request": {"anyOf": [obj({"tool": {"const": "get_metrics"}, "arguments": QUERY}),
                               obj({"tool": {"const": "get_evidence"}, "arguments": EVIDENCE_QUERY})]},
    "tool-response": {"anyOf": [SCHEMAS["metrics"], SCHEMAS["evidence"], SCHEMAS["error"]]},
})

TYPE_NAMES = {
    "manifest": "NormalizedManifest", "batch": "BatchResponse", "metrics": "MetricResponse",
    "evidence": "EvidenceResponse", "error": "ErrorResponse", "inventory": "InventoryResponse",
    "metrics-query": "MetricQuery", "evidence-query": "EvidenceQuery", "import-request": "ImportRequest",
    "resolution-request": "ResolutionRequest", "imports": "ImportsResponse", "staging": "StagingResponse",
    "health": "HealthResponse", "resolution": "ResolutionResponse",
    "tool-request": "ToolRequest", "tool-response": "ToolResponse",
}


def typescript(rule):
    """Render our schema subset; client types share the schema's structural source."""
    if "const" in rule:
        base = json.dumps(rule["const"])
    elif "enum" in rule:
        base = " | ".join(json.dumps(value) for value in rule["enum"])
    elif rule.get("type") == "object" or "properties" in rule:
        if not rule.get("properties"):
            base = "Record<string, unknown>"
        else:
            required = set(rule.get("required", ()))
            fields = [f'{key}{"" if key in required else "?"}: {typescript(child)};'
                      for key, child in rule["properties"].items()]
            base = "{ " + " ".join(fields) + " }"
    elif rule.get("type") == "array":
        base = "Array<" + typescript(rule["items"]) + ">"
    else:
        base = {"integer": "number", "boolean": "boolean", "string": "string", "null": "null"}.get(rule.get("type"))
    if "anyOf" in rule:
        union = " | ".join("(" + typescript(child) + ")" for child in rule["anyOf"])
        return "(" + base + ") & (" + union + ")" if base else union
    if base is None:
        raise ValueError("Unsupported TypeScript schema: " + repr(rule))
    return base


def client_types():
    lines = ["/** Generated by contracts/build_schemas.py. Do not edit. */"]
    lines += [f"export type {TYPE_NAMES[name]} = {typescript(rule)};" for name, rule in SCHEMAS.items()]
    lines += ["export type Scope = MetricResponse['filters_applied'];",
              "export type Metric = MetricResponse['metrics'][number];",
              "export type Availability = Metric['availability'];",
              "export type EvidenceRow = EvidenceResponse['rows'][number];"]
    return "\n".join(lines) + "\n"


def main():
    root = Path(__file__).resolve().parent / "v1"
    root.mkdir(exist_ok=True)
    for name, schema in SCHEMAS.items():
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Goodwill v1 " + name, **schema}
        (root / (name + ".schema.json")).write_text(json.dumps(schema, indent=2) + "\n")
    (root / "types.ts").write_text(client_types())


if __name__ == "__main__":
    main()
