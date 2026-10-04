#!/usr/bin/env python3
"""Local synthetic reporting portals. Python standard library only."""
import argparse
import csv
import hashlib
import io
import json
import threading
import time
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
JOBS = {}
LOCK = threading.Lock()
CHANNELS = {'upright': ['Shopgoodwill', 'eBay', 'Goodwillfinds'], 'cash_monkey': ['Amazon-MF', 'eBay', 'Goodwillbooks']}
ACCOUNTS = ['276 - Goodwill Michiana', '277 - Goodwill Michiana (Stores)']
ZONES = ['America/Los_Angeles', 'America/Indiana/Indianapolis', 'UTC']
MODES = ['normal', 'delayed', 'missing-report', 'session-expired', 'changed-label']


def money(cents):
    return f'{cents // 100}.{cents % 100:02d}'


@lru_cache(maxsize=2)
def ledger(source):
    """Fictional records with stable IDs; generated once for each portal."""
    rows = []
    day = date(2026, 1, 1)
    for offset in range(365):
        current = day + timedelta(days=offset)
        count = 128 if source == 'upright' else 30
        for n in range(count):
            gross = (1500 if source == 'upright' else 500) + ((offset * 137 + n * 211) % 8500)
            refund = gross // 2 if n % 17 == 0 else 0
            shipping = 399 + (n % 5) * 100
            fee = gross // 10
            order_id = f'{"UP" if source == "upright" else "CM"}-{current:%Y%m%d}-{n + 1:04d}'
            base = {
                'order_id': order_id, 'source_name': f'{source}_replica',
                'paid_at': f'{current.isoformat()}T{18 + n % 4:02d}:00:00+00:00',
                'order_date': current.isoformat(),
                'channel': CHANNELS[source][n % 3], 'account': ACCOUNTS[n % 2],
                'store_id': f'GW-{n % 24 + 1:03d}', 'buyer_id': f'DEMO-{source.upper()}-{n % 89 + 1:04d}',
                'item_id': f'DEMO-ITEM-{current:%Y%m%d}-{n + 1:04d}',
                'sku': f'DEMO-{source.upper()}-{current:%Y%m%d}-{n + 1:04d}',
                'item_title': ['Vintage ceramic vase', 'Wool cardigan, size S', 'Framed landscape print', 'Silver-tone necklace'][n % 4] if source == 'upright' else ['Engineering reference manual', 'Hardcover regional cookbook', 'Collected short stories', 'Paperback history'][n % 4],
                'category': ['Home', 'Apparel', 'Art', 'Jewelry'][n % 4] if source == 'upright' else 'Books',
                'payment_status': 'Refunded' if refund else 'Paid',
                'gross_sales': money(gross), 'shipping_collected': money(shipping),
                'sales_tax': money(gross * 7 // 100), 'marketplace_fee': money(fee),
                'refund_amount': money(refund), 'net_sales': money(gross - refund),
                'synthetic': 'true', 'currency': 'USD',
            }
            if source == 'upright':
                base.update(paid_order_id=order_id, grain='one row per paid order', quantity=1)
                rows.append(base)
            else:
                # The photographed report says one line per unit, not per customer.
                for unit in range(2 if n % 15 == 0 else 1):
                    r = dict(base)
                    r.update(unit_id=f'{order_id}-U{unit + 1}', quantity=1,
                             item_revenue=money(gross), shipping_revenue=money(shipping),
                             payment_fee=money(fee), payout_amount=money(gross + shipping - refund - fee),
                             title=base['item_title'], grain='one row per unit')
                    rows.append(r)
    return rows


def validate(spec):
    source = spec.get('source')
    if source not in CHANNELS:
        raise ValueError('Choose Upright or Cash Monkey.')
    report_type = spec.get('report_type', 'paid_orders' if source == 'upright' else 'orders')
    if report_type not in (['paid_orders', 'paid_order_items'] if source == 'upright' else ['orders']):
        raise ValueError('That report is not implemented in this replica.')
    try:
        start = date.fromisoformat(spec.get('start_date', ''))
        end = date.fromisoformat(spec.get('end_date', ''))
    except (ValueError, TypeError):
        raise ValueError('Enter valid start and end dates.') from None
    if start > end:
        raise ValueError('The start date must be on or before the end date.')
    if start.year != 2026 or end.year != 2026:
        raise ValueError('Synthetic reports cover 2026 only.')
    if (end - start).days > 30:
        raise ValueError('Select no more than 31 days per report.')
    zone = spec.get('timezone', 'UTC' if source == 'cash_monkey' else 'America/Los_Angeles')
    if zone not in ZONES or (source == 'cash_monkey' and zone != 'UTC'):
        raise ValueError('Use an available reporting timezone; Cash Monkey uses UTC.')
    channels = spec.get('channels', [])
    accounts = spec.get('accounts', [])
    if not isinstance(channels, list) or any(c not in CHANNELS[source] for c in channels):
        raise ValueError('Choose an available channel.')
    if not isinstance(accounts, list) or any(a not in ACCOUNTS for a in accounts):
        raise ValueError('Choose an available account.')
    payment_status = spec.get('payment_status', 'All')
    if payment_status not in ['All', 'Paid', 'Refunded']:
        raise ValueError('Choose an available payment status.')
    mode = spec.get('mode', 'normal')
    if mode not in MODES:
        raise ValueError('Choose an available test mode.')
    fmt = spec.get('format', 'CSV')
    if fmt != 'CSV':
        raise ValueError('Only CSV is supported in this replica.')
    for key in ['order_ids', 'skus']:
        if not isinstance(spec.get(key, []), list) or any(not isinstance(v, str) for v in spec.get(key, [])):
            raise ValueError('Order IDs and SKUs must be lists of text values.')
    return dict(source=source, report_type=report_type, start_date=start.isoformat(), end_date=end.isoformat(),
                timezone=zone, channels=channels, accounts=accounts, payment_status=payment_status,
                mode=mode, format=fmt, order_ids=spec.get('order_ids', []), skus=spec.get('skus', []))


def create_artifact(spec):
    start, end = date.fromisoformat(spec['start_date']), date.fromisoformat(spec['end_date'])
    zone = ZoneInfo(spec['timezone'])
    rows = []
    for row in ledger(spec['source']):
        reporting_date = datetime.fromisoformat(row['paid_at']).astimezone(zone).date()
        if not start <= reporting_date <= end:
            continue
        if spec['channels'] and row['channel'] not in spec['channels']:
            continue
        if spec['accounts'] and row['account'] not in spec['accounts']:
            continue
        # "Paid" includes partially refunded orders, as their original payment exists.
        if spec['payment_status'] == 'Refunded' and row['payment_status'] != 'Refunded':
            continue
        if spec['order_ids'] and row['order_id'] not in spec['order_ids']:
            continue
        if spec['skus'] and row['sku'] not in spec['skus']:
            continue
        rows.append(dict(row, reporting_date=reporting_date.isoformat(), reporting_timezone=spec['timezone']))
    common = ['source_name', 'synthetic', 'grain', 'reporting_date', 'reporting_timezone', 'currency']
    fields = (['paid_order_id', 'paid_at', 'item_id', 'store_id', 'channel', 'buyer_id', 'item_title', 'category', 'quantity', 'gross_sales', 'shipping_collected', 'sales_tax', 'marketplace_fee', 'refund_amount', 'net_sales'] if spec['source'] == 'upright' else ['order_id', 'unit_id', 'order_date', 'sku', 'title', 'category', 'store_id', 'buyer_id', 'account', 'channel', 'quantity', 'item_revenue', 'shipping_revenue', 'refund_amount', 'payment_fee', 'payout_amount']) + common
    if spec['report_type'] == 'paid_order_items':
        rows = [dict(row, grain='one row per paid order item') for row in rows]
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore', lineterminator='\r\n')
    writer.writeheader()
    writer.writerows(rows)
    payload = output.getvalue().encode('utf-8')
    checksum = hashlib.sha256(payload).hexdigest()
    file_name = f'{spec["source"]}_{spec["report_type"]}_{spec["start_date"]}_{spec["end_date"]}_synthetic.csv'
    gross_cents = sum(int(Decimal(r['gross_sales']) * 100) for r in rows)
    refund_cents = sum(int(Decimal(r['refund_amount']) * 100) for r in rows)
    manifest = {
        'schema_version': 'replica-v1', 'source_package_id': f'{spec["source"]}-{checksum[:16]}',
        'source_name': f'{spec["source"]}_replica', 'report_type': spec['report_type'],
        'requested_start_date': spec['start_date'], 'requested_end_date': spec['end_date'],
        'reporting_timezone': spec['timezone'], 'channels': spec['channels'], 'accounts': spec['accounts'],
        'payment_status': spec['payment_status'], 'order_ids': spec['order_ids'], 'skus': spec['skus'],
        'generated_at': datetime.now(timezone.utc).isoformat(), 'file_name': file_name,
        'file_checksum': checksum, 'checksum_algorithm': 'SHA-256', 'row_count': len(rows),
        'order_count': len({r['order_id'] for r in rows}), 'platform_local_buyer_count': len({(r['channel'], r['buyer_id']) for r in rows}),
        'coverage_start_date': min((r['reporting_date'] for r in rows), default=None),
        'coverage_end_date': max((r['reporting_date'] for r in rows), default=None),
        'currency': 'USD', 'item_sales': money(gross_cents), 'refunds': money(refund_cents),
        'demo_net_sales': money(gross_cents - refund_cents),
        'revenue_definition': 'item sales minus refunds; excludes shipping, tax and fees',
        'synthetic': True, 'status': 'success',
        'replay_version': None, 'note': 'Replica artifact; not a live vendor export. No downstream import has occurred.'
    }
    return payload, manifest


def job_view(job):
    elapsed = time.monotonic() - job['started']
    if elapsed < job['delay']:
        return {'id': job['id'], 'status': 'pending', 'spec': job['spec']}
    if job['spec']['mode'] == 'missing-report':
        return {'id': job['id'], 'status': 'failed', 'spec': job['spec'], 'error': 'The report is unavailable. Retry or use a manual export.', 'error_category': 'missing_report'}
    return {'id': job['id'], 'status': 'ready', 'spec': job['spec'], 'manifest': job['manifest'],
            'download_url': f'/api/reports/{job["id"]}/download', 'manifest_url': f'/api/reports/{job["id"]}/manifest'}


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, mime='application/json; charset=utf-8', headers=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == '/api/health':
            return self.send(200, {'status': 'ok', 'synthetic': True})
        if path == '/api/reports':
            with LOCK:
                jobs = [job_view(j) for j in reversed(list(JOBS.values()))]
            return self.send(200, jobs)
        if path.startswith('/api/reports/'):
            bits = path.split('/')
            with LOCK:
                job = JOBS.get(bits[3])
            if not job:
                return self.send(404, {'error': 'Report not found. Generate it again.'})
            state = job_view(job)
            if len(bits) == 4:
                return self.send(200, state)
            if state['status'] != 'ready':
                return self.send(409, {'error': 'Report is not ready for download.', 'status': state['status']})
            if len(bits) == 5 and bits[4] == 'download':
                return self.send(200, job['payload'], 'text/csv; charset=utf-8', {'Content-Disposition': f'attachment; filename="{job["manifest"]["file_name"]}"'})
            if len(bits) == 5 and bits[4] == 'manifest':
                return self.send(200, job['manifest'], headers={'Content-Disposition': f'attachment; filename="{job["manifest"]["file_name"].replace(".csv", ".manifest.json")}"'})
            return self.send(404, {'error': 'Unknown report operation.'})
        if path.startswith('/api/'):
            return self.send(404, {'error': 'Unknown API route.'})
        if path in ['/static/app.js', '/static/style.css']:
            file = ROOT / path.lstrip('/')
            return self.send(200, file.read_bytes(), 'text/javascript; charset=utf-8' if file.suffix == '.js' else 'text/css; charset=utf-8')
        if path in ['/', '/upright', '/upright/reports', '/upright/reports/paid-orders', '/upright/reports/paid-order-items', '/cash-monkey', '/cash-monkey/reports', '/cash-monkey/reports/orders']:
            return self.send(200, (ROOT / 'static/index.html').read_bytes(), 'text/html; charset=utf-8')
        self.send(404, 'Page not found.', 'text/plain; charset=utf-8')

    def do_POST(self):
        if urlparse(self.path).path != '/api/reports':
            return self.send(404, {'error': 'Unknown API route.'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size < 1 or size > 16384:
                raise ValueError('Request body must be between 1 and 16384 bytes.')
            spec = validate(json.loads(self.rfile.read(size)))
            if spec['mode'] == 'session-expired':
                return self.send(401, {'error': 'Demo session expired. Choose Normal in the test controls to resume.', 'error_category': 'session_expired'})
            payload, manifest = create_artifact(spec)
            job = {'id': uuid.uuid4().hex, 'spec': spec, 'payload': payload, 'manifest': manifest,
                   'started': time.monotonic(), 'delay': 6.0 if spec['mode'] == 'delayed' else 0.8}
            with LOCK:
                if len(JOBS) >= 200:
                    # Bound local demo memory. Expired jobs return a visible 404.
                    JOBS.pop(next(iter(JOBS)))
                JOBS[job['id']] = job
            self.send(202, job_view(job))
        except (ValueError, TypeError, AttributeError, json.JSONDecodeError) as error:
            self.send(400, {'error': str(error)})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--host', default='127.0.0.1')
    args = parser.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Synthetic portal replicas: http://{args.host}:{args.port}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
