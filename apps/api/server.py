"""Loopback-only synthetic API. No authentication or production deployment claim."""
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from services.data.contracts import CONTRACT_VERSION, DataError, canonical, digest, validate
from services.data.inventory.store import inventory_response
from services.metrics.query import evidence_response, metric_response

MAX_BODY = 8 * 1024 * 1024


def make_server(pipeline, port=8000):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, code, body, content_type="application/json; charset=utf-8"):
            data = canonical(body).encode() if not isinstance(body, bytes) else body
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            origin = self.headers.get("Origin")
            if origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(data)

        def error(self, exc):
            self.send(404 if exc.code == "not_found" else 400,
                      {"contract_version": CONTRACT_VERSION, "synthetic": True,
                       "error": {"code": exc.code, "detail": exc.detail}})

        def local_request(self):
            host = self.headers.get("Host", "").split(":")[0]
            if host not in ("localhost", "127.0.0.1"):
                raise DataError("host_denied", "This synthetic API serves loopback hosts only")

        def do_GET(self):
            try:
                self.local_request()
                parsed = urlparse(self.path)
                query = parse_qs(parsed.query, keep_blank_values=True)
                if any(len(values) != 1 for values in query.values()):
                    raise DataError("duplicate_query", "Query keys must be unique")
                q = {k: v[0] for k, v in query.items()}
                path = parsed.path
                if path == "/api/v1/health":
                    if q:
                        raise DataError("query_invalid", "Health takes no query parameters")
                    return self.send(200, validate("health.schema.json", {"contract_version": CONTRACT_VERSION, "synthetic": True, "status": "ok"}))
                if path in ("/api/v1/metrics", "/api/v1/evidence"):
                    schema = "metrics-query" if path.endswith("metrics") else "evidence-query"
                    typed_query = dict(q)
                    for key in ("offset", "limit"):
                        if key in typed_query:
                            if not re.fullmatch(r"\d+", typed_query[key]):
                                raise DataError("invalid_pagination", "Pagination requires unsigned integers")
                            typed_query[key] = int(typed_query[key])
                    validate(schema + ".schema.json", typed_query)
                    args = (pipeline, q["start_date"], q["end_date"], q["source"], q.get("platform"), q.get("store"))
                    if path.endswith("metrics"):
                        return self.send(200, metric_response(*args, run_id=q.get("run_id")))
                    if not q.get("run_id"):
                        raise DataError("run_required", "Evidence requires the displayed metric_run_id")
                    return self.send(200, evidence_response(pipeline, q["run_id"], *args[1:], offset=int(q.get("offset", 0)), limit=int(q.get("limit", 100))))
                if path == "/api/v1/imports":
                    if q:
                        raise DataError("query_invalid", "Imports list takes no query parameters")
                    return self.send(200, validate("imports.schema.json", {"contract_version": CONTRACT_VERSION, "synthetic": True, "imports": pipeline.batches()}))
                match = re.fullmatch(r"/api/v1/imports/([a-f0-9]{32})(/rows)?", path)
                if match:
                    batch = pipeline.batch(match[1])
                    if not match[2]:
                        if q:
                            raise DataError("query_invalid", "Batch detail takes no query parameters")
                        return self.send(200, batch)
                    if set(q) - {"offset", "limit", "status"}:
                        raise DataError("query_invalid", "Rows support offset, limit and status only")
                    offset, limit = int(q.get("offset", 0)), int(q.get("limit", 100))
                    if not 0 <= offset or not 1 <= limit <= 200:
                        raise DataError("invalid_pagination", "Limit 1..200; nonnegative offset")
                    status = q.get("status")
                    if status and status not in ("accepted", "duplicate", "corrected", "rejected"):
                        raise DataError("invalid_row_status", status)
                    with pipeline.db() as db:
                        rows = db.execute("SELECT * FROM staging_rows WHERE batch_id=? ORDER BY row_number", (match[1],)).fetchall()
                        selected = [r for r in rows if status is None or r["status"] == status]
                        items = [{"source_row_number": r["row_number"], "status": r["status"], "reason": r["reason"],
                                  "file_id": batch["file"]["file_id"], "batch_id": match[1],
                                  "original_row": json.loads(r["original_json"]),
                                  "normalized_row": json.loads(r["normalized_json"]) if r["normalized_json"] else None}
                                 for r in selected[offset:offset+limit]]
                    return self.send(200, validate("staging.schema.json", {"contract_version": CONTRACT_VERSION, "synthetic": True, "total_rows": len(selected), "rows": items}))
                match = re.fullmatch(r"/api/v1/files/([a-f0-9]{64})", path)
                if match:
                    if q:
                        raise DataError("query_invalid", "Raw-file download takes no query parameters")
                    with pipeline.db() as db:
                        row = db.execute("SELECT artifact_ref,checksum FROM source_files WHERE id=?", (match[1],)).fetchone()
                        if not row:
                            raise DataError("not_found", "Unknown source file")
                        from pathlib import Path
                        data = Path(row["artifact_ref"]).read_bytes()
                        if digest(data) != row["checksum"]:
                            raise DataError("archive_corrupt", "Archived bytes changed")
                    return self.send(200, data, "text/csv; charset=utf-8")
                if path == "/api/v1/inventory":
                    if not {"start_date", "end_date"} <= set(q) or set(q)-{"start_date", "end_date", "snapshot_at", "store"}:
                        raise DataError("query_invalid", "Inventory requires start_date/end_date and known filters")
                    return self.send(200, inventory_response(pipeline, q["start_date"], q["end_date"], q.get("snapshot_at"), q.get("store")))
                raise DataError("not_found", "Unknown versioned API route")
            except DataError as exc:
                self.error(exc)
            except (ValueError, TypeError, UnicodeError) as exc:
                self.error(DataError("request_invalid", str(exc)))

        def do_OPTIONS(self):
            try:
                self.local_request()
                if self.headers.get("Origin") not in ("http://localhost:5173", "http://127.0.0.1:5173"):
                    raise DataError("origin_denied", "Unknown development origin")
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()
            except DataError as exc:
                self.error(exc)

        def do_POST(self):
            try:
                self.local_request()
                origin = self.headers.get("Origin")
                local_origins = {"http://" + self.headers.get("Host", ""), "http://localhost:5173", "http://127.0.0.1:5173"}
                if origin and origin not in local_origins:
                    raise DataError("origin_denied", "Cross-origin write denied")
                if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                    raise DataError("content_type", "Require application/json")
                size = int(self.headers.get("Content-Length", 0))
                if not 0 < size <= MAX_BODY:
                    raise DataError("request_size", "Body must be 1 byte..8 MiB")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise DataError("request_invalid", "Expected JSON object")
                path = urlparse(self.path).path
                if path == "/api/v1/imports":
                    validate("import-request.schema.json", body)
                    result = pipeline.import_bytes(body["csv_text"].encode(), body["manifest"], body.get("allow_corrections", False))
                    return self.send(422 if result["status"] == "failed" else 201, result)
                match = re.fullmatch(r"/api/v1/exceptions/([a-f0-9]{32})/resolve", path)
                if match:
                    validate("resolution-request.schema.json", body)
                    pipeline.resolve_exception(match[1], body["resolution"])
                    return self.send(200, validate("resolution.schema.json", {"contract_version": CONTRACT_VERSION, "synthetic": True, "status": "resolved"}))
                raise DataError("not_found", "Unknown write route")
            except DataError as exc:
                self.error(exc)
            except (ValueError, TypeError, UnicodeError) as exc:
                self.error(DataError("request_invalid", str(exc)))

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
