import csv
import hashlib
import io
import json
import sys
import threading
import unittest
import urllib.request
import urllib.error
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


def spec(source='upright', **changes):
    result = dict(source=source, report_type='paid_orders' if source == 'upright' else 'orders', start_date='2026-09-30', end_date='2026-09-30', timezone='America/Los_Angeles' if source == 'upright' else 'UTC', payment_status='Paid', channels=[], accounts=[], mode='normal', format='CSV')
    result.update(changes)
    return server.validate(result)


def read_rows(payload):
    return list(csv.DictReader(io.StringIO(payload.decode())))


class ReportTests(unittest.TestCase):
    def test_upright_control_totals_and_repeat_fingerprint(self):
        payload, manifest = server.create_artifact(spec())
        rows = read_rows(payload)
        self.assertEqual(128, len(rows))
        self.assertEqual(128, manifest['order_count'])
        # Expected amount calculated independently from the disclosed fixture rule.
        day_number = (date(2026, 9, 30) - date(2026, 1, 1)).days
        expected_cents = sum((1500 + ((day_number * 137 + n * 211) % 8500)) - ((1500 + ((day_number * 137 + n * 211) % 8500)) // 2 if n % 17 == 0 else 0) for n in range(128))
        self.assertEqual(Decimal(expected_cents) / 100, Decimal(manifest['demo_net_sales']))
        self.assertEqual({r['synthetic'] for r in rows}, {'true'})
        self.assertEqual({r['reporting_date'] for r in rows}, {'2026-09-30'})
        self.assertEqual(hashlib.sha256(payload).hexdigest(), manifest['file_checksum'])
        self.assertEqual(payload, server.create_artifact(spec())[0])

    def test_alternate_dates_and_inclusive_range(self):
        a, _ = server.create_artifact(spec())
        b, m = server.create_artifact(spec(start_date='2026-10-01', end_date='2026-10-02'))
        self.assertNotEqual(a, b)
        self.assertEqual(256, len(read_rows(b)))
        self.assertEqual('2026-10-01', m['coverage_start_date'])
        self.assertEqual('2026-10-02', m['coverage_end_date'])

    def test_channel_and_refund_filters(self):
        payload, m = server.create_artifact(spec(channels=['eBay'], payment_status='Refunded'))
        rows = read_rows(payload)
        self.assertEqual(2, len(rows))  # n=34 and n=85 are eBay + partial refunds.
        self.assertEqual({'eBay'}, {r['channel'] for r in rows})
        self.assertTrue(all(Decimal(r['refund_amount']) > 0 for r in rows))

    def test_cash_monkey_grain_accounts_and_ids(self):
        payload, m = server.create_artifact(spec('cash_monkey'))
        self.assertEqual(32, m['row_count'])
        self.assertEqual(30, m['order_count'])
        rows = read_rows(payload)
        self.assertEqual(32, len({r['unit_id'] for r in rows}))
        filtered, fm = server.create_artifact(spec('cash_monkey', accounts=['276 - Goodwill Michiana'], channels=['Amazon-MF'], order_ids=['CM-20260930-0001']))
        self.assertEqual(2, fm['row_count'])
        self.assertEqual({'CM-20260930-0001'}, {r['order_id'] for r in read_rows(filtered)})
        empty, em = server.create_artifact(spec('cash_monkey', order_ids=['nonexistent']))
        self.assertEqual(0, em['row_count'])
        self.assertIsNone(em['coverage_start_date'])
        self.assertEqual([], read_rows(empty))

    def test_reject_invalid_inputs(self):
        for changes in [dict(start_date='2026-10-01', end_date='2026-09-30'), dict(start_date='2025-09-30'), dict(start_date='2026-01-01', end_date='2026-03-01'), dict(source='fake'), dict(report_type='inventory'), dict(timezone='Not/AZone'), dict(channels=['Other']), dict(format='XLSX')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                spec(**changes)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.httpd.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def request(self, path, data=None):
        request = urllib.request.Request(self.base + path, data=json.dumps(data).encode() if data else None, headers={'Content-Type': 'application/json'})
        return urllib.request.urlopen(request)

    def test_async_download_and_manifest(self):
        with self.request('/api/reports', spec()) as r:
            self.assertEqual(202, r.status)
            job = json.load(r)
        self.assertEqual('pending', job['status'])
        with self.assertRaises(urllib.error.HTTPError) as err:
            self.request(f'/api/reports/{job["id"]}/download')
        self.assertEqual(409, err.exception.code)
        server.JOBS[job['id']]['started'] -= 10
        with self.request(f'/api/reports/{job["id"]}/download') as r:
            body = r.read()
            self.assertIn('attachment;', r.headers['Content-Disposition'])
        with self.request(f'/api/reports/{job["id"]}/manifest') as r:
            manifest = json.load(r)
        self.assertEqual(hashlib.sha256(body).hexdigest(), manifest['file_checksum'])
        self.assertEqual(128, manifest['row_count'])

    def test_missing_report_never_downloads(self):
        with self.request('/api/reports', spec(mode='missing-report')) as r:
            job = json.load(r)
        server.JOBS[job['id']]['started'] -= 10
        with self.request(f'/api/reports/{job["id"]}') as r:
            state = json.load(r)
        self.assertEqual('failed', state['status'])
        with self.assertRaises(urllib.error.HTTPError) as err:
            self.request(f'/api/reports/{job["id"]}/download')
        self.assertEqual(409, err.exception.code)

    def test_expired_session_and_unknown_routes(self):
        with self.assertRaises(urllib.error.HTTPError) as err:
            self.request('/api/reports', spec(mode='session-expired'))
        self.assertEqual(401, err.exception.code)
        for path in ['/api/reports/unknown/download', '/static/../server.py', '/api/unknown']:
            with self.subTest(path=path), self.assertRaises(urllib.error.HTTPError) as err:
                self.request(path)
            self.assertEqual(404, err.exception.code)

    def test_screens_serve(self):
        for path in ['/', '/upright', '/upright/reports/paid-orders', '/cash-monkey/reports/orders']:
            with self.request(path) as r:
                self.assertIn(b'HACKATHON REPLICA', r.read())


if __name__ == '__main__':
    unittest.main()
