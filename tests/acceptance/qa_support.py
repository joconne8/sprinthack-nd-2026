"""ENG-04 QA helpers. Builds artifacts from the handwritten ledger; never computes expectations.

Deliberately independent of tests/helpers.py and of services/ formulas.
"""
import csv
import hashlib
import importlib.util
import io
import json
import threading
import time
from contextlib import contextmanager
from decimal import Decimal
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
LEDGER = json.loads((ROOT / "fixtures/expected-results/eng04_control_ledger.json").read_text())
SCENARIOS = LEDGER["scenarios"]
FIELDS = ("paid_order_id paid_at item_id store_id channel buyer_id item_title category quantity gross_sales "
          "shipping_collected sales_tax marketplace_fee refund_amount net_sales source_name synthetic grain "
          "reporting_date reporting_timezone currency").split()


def artifact(entries, start="2026-09-30", end=None, timezone="America/New_York"):
    """CSV bytes + replica-v1 manifest. Decoy shipping/tax/fee/net columns are intentionally large."""
    end = end or start
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\r\n")
    writer.writeheader()
    for entry in entries:
        writer.writerow({
            "paid_order_id": entry["key"], "paid_at": entry.get("paid_at", start + "T16:00:00+00:00"),
            "item_id": "ITEM-" + entry["key"], "store_id": entry.get("store", "GW-001"),
            "channel": entry.get("channel", "eBay"), "buyer_id": entry.get("buyer", "BUYER-" + entry["key"]),
            "item_title": "QA synthetic", "category": "Books", "quantity": "1",
            "gross_sales": entry["gross"], "shipping_collected": "500.00", "sales_tax": "400.00",
            "marketplace_fee": "300.00", "refund_amount": entry["refund"], "net_sales": "9999.00",
            "source_name": "upright_replica", "synthetic": "true", "grain": "one row per paid order",
            "reporting_date": entry.get("reporting_date", start), "reporting_timezone": timezone, "currency": "USD"})
    data = output.getvalue().encode()
    return data, {"schema_version": "replica-v1", "source_name": "upright_replica", "report_type": "paid_orders",
                  "requested_start_date": start, "requested_end_date": end, "reporting_timezone": timezone,
                  "file_name": "eng04-qa.csv", "file_checksum": hashlib.sha256(data).hexdigest(),
                  "row_count": len(entries), "currency": "USD", "synthetic": True}


def scenario_file(scenario, name):
    spec = SCENARIOS[scenario]["files"][name]
    if isinstance(spec, list):
        return artifact(spec, SCENARIOS[scenario]["date"])
    return artifact(spec["rows"], spec["start"], spec["end"], spec.get("timezone", "America/New_York"))


def raw_net_by_day(data):
    """QA's own reading of downloaded bytes: item sales minus refunds per reporting_date, in Decimal."""
    totals = {}
    for row in csv.DictReader(io.StringIO(data.decode("utf-8"), newline="")):
        amount = Decimal(row["gross_sales"]) - Decimal(row["refund_amount"])
        totals[row["reporting_date"]] = totals.get(row["reporting_date"], Decimal("0")) + amount
    return {key: format(value, ".2f") for key, value in totals.items()}


def http(url, body=None):
    headers = {"Content-Type": "application/json"} if body is not None else {}
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urlopen(Request(url, data=data, headers=headers), timeout=10) as response:
            return response.status, response.read()
    except HTTPError as response:
        return response.code, response.read()


@contextmanager
def serving(server):
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:%d" % server.server_port
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def portal_server():
    """Hugh's replica portal, loaded unmodified from its own lane."""
    spec = importlib.util.spec_from_file_location("eng04_portal", ROOT / "data ingestion/server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return ThreadingHTTPServer(("127.0.0.1", 0), module.Handler)


def download(portal, start, end):
    status, body = http(portal + "/api/reports", {"source": "upright", "start_date": start, "end_date": end,
                                                  "timezone": "America/Indiana/Indianapolis", "payment_status": "All"})
    if status != 202:
        raise AssertionError("portal refused report: %s %s" % (status, body[:200]))
    job = json.loads(body)
    deadline = time.monotonic() + 10
    while job["status"] == "pending" and time.monotonic() < deadline:
        time.sleep(0.1)
        job = json.loads(http(portal + "/api/reports/" + job["id"])[1])
    if job["status"] != "ready":
        raise AssertionError("portal job not ready: %s" % job["status"])
    data = http(portal + job["download_url"])[1]
    manifest = json.loads(http(portal + job["manifest_url"])[1])
    return data, manifest


def run_demo_sequence(state_dir, keep_files=None):
    """Acquire actual replica files over HTTP -> POST import -> reconcile -> metrics/evidence/raw API.

    Returns observed evidence only; the caller compares it with independent expectations.
    """
    from apps.api.server import make_server
    from services.data.importer import Pipeline

    pipeline = Pipeline(state_dir)
    steps = []
    with serving(portal_server()) as portal, serving(make_server(pipeline, 0)) as api:
        def metrics(start, end):
            query = urlencode({"start_date": start, "end_date": end, "source": "upright_replica"})
            return json.loads(http(api + "/api/v1/metrics?" + query)[1])

        for label, start, end in (("sep29", "2026-09-29", "2026-09-29"),
                                  ("sep29_replay", "2026-09-29", "2026-09-29"),
                                  ("sep29_sep30_overlap", "2026-09-29", "2026-09-30")):
            data, manifest = download(portal, start, end)
            if keep_files:
                Path(keep_files).mkdir(parents=True, exist_ok=True)
                (Path(keep_files) / manifest["file_name"]).write_bytes(data)
            status, body = http(api + "/api/v1/imports", {"csv_text": data.decode("utf-8"), "manifest": manifest})
            batch = json.loads(body)
            raw = http(api + "/api/v1/files/" + batch["file"]["file_id"])[1]
            after = {day: metrics(day, day) for day in ("2026-09-29", "2026-09-30")}
            whole = metrics(start, end)
            evidence = json.loads(http(api + "/api/v1/evidence?" + urlencode({
                "start_date": start, "end_date": end, "source": "upright_replica",
                "run_id": whole["metric_run_id"], "limit": 200}))[1])
            steps.append({
                "step": label, "request": {"start_date": start, "end_date": end},
                "download": {"file_name": manifest["file_name"], "sha256": hashlib.sha256(data).hexdigest(),
                             "manifest_checksum": manifest["file_checksum"], "byte_size": len(data),
                             "row_count": manifest["row_count"], "portal_demo_net_sales": manifest["demo_net_sales"]},
                "qa_raw_net_by_day": raw_net_by_day(data),
                "import": {"http_status": status, "batch_id": batch["batch_id"], "status": batch["status"],
                           "file_id": batch["file"]["file_id"], "counts": batch["counts"],
                           "reconciliation_state": (batch["reconciliation"] or {}).get("state")},
                "raw_download_matches": raw == data,
                "metrics_by_day": {day: {"value": m["metrics"][0]["value"], "availability": m["metrics"][0]["availability"],
                                         "coverage": m["coverage"]["state"], "rows": m["evidence"]["row_count"],
                                         "run_id": m["metric_run_id"]} for day, m in after.items()},
                "range_metric": {"value": whole["metrics"][0]["value"], "availability": whole["metrics"][0]["availability"],
                                 "run_id": whole["metric_run_id"], "reconciliation_state": whole["reconciliation_state"]},
                "evidence": {"total_rows": evidence["total_rows"], "scope_total": evidence["scope_total"],
                             "file_ids": sorted({r["file_id"] for r in evidence["rows"]}),
                             "spot": {r["record_key"]: r["demo_net_sales"] for r in evidence["rows"]
                                      if r["record_key"] in ('["UP-20260929-0001"]', '["UP-20260930-0001"]', '["UP-20260930-0002"]')}},
            })
    return steps
