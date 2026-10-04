"""Browser-downloaded bytes → unchanged intake → importer → API → exact archive.

Shared implementation regression, not independent ENG-04 or Landon's UI acceptance.
Dependencies are explicit; missing Node/browser is a failing check, never a skip.
"""
import argparse
import csv
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
from datetime import datetime
from decimal import Decimal
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from acquisition.intake import intake
from apps.api.server import make_server
from services.data.contracts import digest, validate
from services.data.importer import Pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node', default='node')
    parser.add_argument('--node-modules')
    parser.add_argument('--chrome-path')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('handoff_portal', ROOT / 'data ingestion/server.py')
    portal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(portal)
    with tempfile.TemporaryDirectory(prefix='goodwill-browser-handoff-') as temporary:
        root = Path(temporary)
        pipeline = Pipeline(root / 'state')
        servers = [ThreadingHTTPServer(('127.0.0.1', 0), portal.Handler), make_server(pipeline, 0)]
        threads = []
        try:
            for server in servers:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                threads.append(thread)
            env = dict(os.environ, BASE_URL=f'http://127.0.0.1:{servers[0].server_port}', OUTPUT_DIR=str(root / 'downloads'))
            if args.node_modules:
                env['NODE_PATH'] = args.node_modules
            if args.chrome_path:
                env['CHROME_PATH'] = args.chrome_path
            process = subprocess.run([args.node, str(ROOT / 'scripts/browser_handoff.cjs')], env=env,
                                     capture_output=True, text=True, timeout=60)
            sys.stderr.write(process.stderr)
            if process.returncode:
                raise RuntimeError(process.stdout + process.stderr)
            acquired = json.loads(process.stdout)
            summaries = []
            for result in acquired['results']:
                manifest = result['manifest']
                raw = Path(result['file']).read_bytes()
                record = intake(result['file'], manifest, result['run_id'], manifest['requested_start_date'],
                                manifest['requested_end_date'], manifest['source_name'], manifest['report_type'], root / 'intake')
                assert record['checksum'] == digest(raw) == result['sha256']
                assert Path(record['artifact_ref']).read_bytes() == raw
                # Use the full original manifest to retain filters and controls.
                batch = pipeline.import_bytes(raw, manifest)
                assert batch['status'] == 'imported', batch
                query = {"start_date": manifest['requested_start_date'], "end_date": manifest['requested_end_date'], "source": manifest['source_name']}
                base = f'http://127.0.0.1:{servers[1].server_port}'
                with urlopen(base + '/api/v1/metrics?' + urlencode(query), timeout=10) as response:
                    metrics = validate('metrics.schema.json', json.load(response))
                # Independent arithmetic within this implementation session;
                # this does not substitute for a different reviewer's QA.
                ledger = Decimal('0')
                expected_rows = 0
                for row in csv.DictReader(io.StringIO(raw.decode())):
                    reporting_day = str(datetime.fromisoformat(row['paid_at']).astimezone(ZoneInfo('America/New_York')).date())
                    if query['start_date'] <= reporting_day <= query['end_date']:
                        ledger += Decimal(row['gross_sales']) - Decimal(row['refund_amount'])
                        expected_rows += 1
                assert metrics['metrics'][0]['value'] == format(ledger, '.2f'), metrics
                with urlopen(base + '/api/v1/evidence?' + urlencode({**query, 'run_id': metrics['metric_run_id'], 'limit': 200}), timeout=10) as response:
                    evidence = validate('evidence.schema.json', json.load(response))
                assert evidence['total_rows'] == expected_rows
                assert evidence['scope_total'] == format(ledger, '.2f')
                with urlopen(base + '/api/v1/files/' + batch['file']['file_id'], timeout=10) as response:
                    assert response.read() == raw
                replay = pipeline.import_bytes(raw, manifest)
                assert replay['status'] == 'duplicate_noop'
                summaries.append({'run_id': result['run_id'], 'period': query, 'checksum': digest(raw),
                                  'byte_size': len(raw), 'source_rows': manifest['row_count'], 'reporting_rows': expected_rows,
                                  'expected_net_sales': format(ledger, '.2f'), 'api_net_sales': metrics['metrics'][0]['value'],
                                  'coverage': metrics['coverage']['state'], 'same_bytes_verified': True,
                                  'intake_verified': True, 'replay': replay['status']})
            print(json.dumps({'passed': True, 'synthetic': True, 'runs': summaries,
                              'expired_session': acquired['expired_session']['type'],
                              'limits': ['No product UI', 'Not independent ENG-04 acceptance', 'No live source compatibility']}, indent=2))
        finally:
            for server, thread in zip(servers, threads):
                server.shutdown()
                thread.join()
                server.server_close()


if __name__ == '__main__':
    main()
