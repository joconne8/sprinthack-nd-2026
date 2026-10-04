import importlib.util
import json
import tempfile
import threading
import time
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from apps.api.server import make_server
from services.data.contracts import digest, validate
from services.data.importer import Pipeline
from tests.helpers import payload, row


def request(url, body=None, headers=None):
    hdr = {"Content-Type": "application/json"} if body is not None else {}
    hdr.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urlopen(Request(url, data=data, headers=hdr), timeout=10) as response:
            return response.status, response.read()
    except HTTPError as response:
        return response.code, response.read()


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pipeline = Pipeline(self.temp.name)
        self.server = make_server(self.pipeline, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def stop_server(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def test_json_upload_metric_evidence_and_exact_raw_download(self):
        data, manifest = payload([row(), row("B", "20.00", "2.00")])
        status, body = request(self.base+"/api/v1/imports", {"csv_text": data.decode(), "manifest": manifest})
        self.assertEqual(status, 201)
        batch = json.loads(body)
        validate("batch.schema.json", batch)
        query = urlencode({"start_date": "2026-09-30", "end_date": "2026-09-30", "source": "upright_replica"})
        status, body = request(self.base+"/api/v1/metrics?"+query)
        self.assertEqual(status, 200)
        metrics = json.loads(body)
        self.assertEqual(metrics["metrics"][0]["value"], "27.00")
        validate("metrics.schema.json", metrics)
        _, body = request(self.base+"/api/v1/evidence?"+query+"&run_id="+metrics["metric_run_id"]+"&limit=1")
        evidence = json.loads(body)
        validate("evidence.schema.json", evidence)
        self.assertEqual(evidence["total_rows"], 2)
        self.assertEqual(len(evidence["rows"]), 1)
        self.assertEqual(evidence["scope_total"], "27.00")
        _, raw = request(self.base+"/api/v1/files/"+batch["file"]["file_id"])
        self.assertEqual(raw, data)
        _, listed = request(self.base+"/api/v1/imports")
        self.assertEqual(len(json.loads(listed)["imports"]), 1)

    def test_bad_input_and_cross_origin_write_fail_safely(self):
        for path in ("/api/v1/metrics", "/api/v1/not-found", "/api/v1/metrics?start_date=bad&end_date=bad&source=upright_replica"):
            status, body = request(self.base+path)
            self.assertIn(status, (400, 404))
            validate("error.schema.json", json.loads(body))
        data, manifest = payload([row()])
        status, _ = request(self.base+"/api/v1/imports", {"csv_text": data.decode(), "manifest": manifest}, {"Origin": "https://example.invalid"})
        self.assertEqual(status, 400)
        status, _ = request(self.base+"/api/v1/health", headers={"Host": "example.invalid"})
        self.assertEqual(status, 400)

    def test_failed_batch_exposes_rejected_rows(self):
        data, manifest = payload([row(gross="broken")])
        status, body = request(self.base+"/api/v1/imports", {"csv_text": data.decode(), "manifest": manifest})
        self.assertEqual(status, 422)
        batch = json.loads(body)
        _, body = request(self.base+f"/api/v1/imports/{batch['batch_id']}/rows?status=rejected")
        rejected = json.loads(body)
        self.assertEqual(rejected["rows"][0]["source_row_number"], 1)
        self.assertEqual(rejected["rows"][0]["reason"], "invalid_money")

    def test_real_portal_download_alternate_dates_and_failure(self):
        path = Path(__file__).resolve().parents[1]/"data ingestion/server.py"
        spec = importlib.util.spec_from_file_location("test_portal", path)
        portal = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(portal)
        server = ThreadingHTTPServer(("127.0.0.1", 0), portal.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            for day in ("2026-09-29", "2026-09-30"):
                status, body = request(base+"/api/reports", {"source": "upright", "start_date": day, "end_date": day,
                                                            "timezone": "America/Indiana/Indianapolis", "payment_status": "All"})
                self.assertEqual(status, 202)
                job = json.loads(body)
                deadline = time.monotonic()+8
                while job["status"] == "pending" and time.monotonic() < deadline:
                    time.sleep(0.1)
                    _, body = request(base+"/api/reports/"+job["id"])
                    job = json.loads(body)
                self.assertEqual(job["status"], "ready")
                _, data = request(base+job["download_url"])
                _, manifest_body = request(base+job["manifest_url"])
                manifest = json.loads(manifest_body)
                self.assertEqual(digest(data), manifest["file_checksum"])
                batch = self.pipeline.import_bytes(data, manifest)
                self.assertEqual(batch["status"], "imported")
                query = urlencode({"start_date": day, "end_date": day, "source": "upright_replica"})
                _, response_body = request(self.base+"/api/v1/metrics?"+query)
                metrics = json.loads(response_body)
                self.assertEqual(metrics["metrics"][0]["value"], manifest["demo_net_sales"])
                self.assertEqual(metrics["coverage"]["state"], "complete")
                self.assertEqual(metrics["evidence"]["row_count"], 128)
                _, raw = request(self.base+"/api/v1/files/"+batch["file"]["file_id"])
                self.assertEqual(raw, data)
            status, body = request(base+"/api/reports", {"source": "upright", "start_date": "2026-09-30", "end_date": "2026-09-30", "mode": "session-expired"})
            self.assertEqual(status, 401)
            self.assertEqual(json.loads(body)["error_category"], "session_expired")
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
