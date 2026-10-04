"""Supervised synthetic collection, durable run history and real importer handoff."""
import json
import os
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from acquisition.intake import IntakeRejected, intake, submit
from acquisition.run_state import execute
from services.data.contracts import CONTRACT_VERSION, DataError, day, now, validate

ROOT = Path(__file__).resolve().parents[1]


class AcquisitionManager:
    def __init__(self, pipeline, portal_url, node=None, node_modules=None, chrome_path=None, attempt_fn=None):
        from urllib.parse import urlparse
        address = urlparse(portal_url)
        if address.scheme != 'http' or address.hostname not in ('localhost', '127.0.0.1') or address.username or address.password:
            raise DataError('host_denied', 'Collection targets only the local synthetic replica')
        self.pipeline, self.portal_url = pipeline, portal_url
        self.node = node or shutil.which('node')
        self.node_modules = node_modules or str(ROOT / 'tools/verification/node_modules')
        self.chrome_path = chrome_path or os.environ.get('CHROME_PATH')
        self.attempt_fn = attempt_fn
        self.root = pipeline.root / 'acquisition'
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='synthetic-collection')
        self.active = False
        self.closed = False
        for path in self.root.glob('*.json'):
            record = json.loads(path.read_text())
            if record['status'] in ('pending', 'running'):
                record.update(status='needs_human', stage='failed', cause='Server restarted before this run completed.',
                              owner_role='Demo maintainer', finished_at=now())
                self._save(record)

    @property
    def available(self):
        return bool(self.attempt_fn or (self.node and Path(self.node_modules, 'playwright/package.json').exists()))

    def _save(self, record):
        path = self.root / (record['run_id'] + '.json')
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(record, indent=2) + '\n')
        os.replace(temp, path)

    def get(self, run_id):
        if len(run_id) != 32 or any(char not in '0123456789abcdef' for char in run_id):
            raise DataError('not_found', 'Unknown acquisition run')
        with self.lock:
            path = self.root / (run_id + '.json')
            if not path.is_file():
                raise DataError('not_found', 'Unknown acquisition run')
            return validate('acquisition-run.schema.json', json.loads(path.read_text()))

    def history(self):
        with self.lock:
            records = sorted((json.loads(path.read_text()) for path in self.root.glob('*.json')),
                             key=lambda record: record['requested_at'], reverse=True)[:50]
        success = next((record for record in records if record['status'] == 'succeeded'), None)
        return validate('acquisition-history.schema.json', {
            'contract_version': CONTRACT_VERSION, 'synthetic': True, 'runtime_available': self.available,
            'runs': records, 'last_success_at': success['finished_at'] if success else None,
            'schedule': 'Manual request only; no production schedule or email delivery'})

    def start(self, request):
        validate('acquisition-request.schema.json', request)
        start, end = day(request['start_date']), day(request['end_date'])
        if start > end or (end-start).days > 30 or start.year != 2026 or end.year != 2026:
            raise DataError('invalid_period', 'Choose an ordered synthetic 2026 period of at most 31 days')
        with self.lock:
            if self.active or self.closed:
                raise DataError('collection_busy', 'A report is already being collected; wait for its result')
            record = {'contract_version': CONTRACT_VERSION, 'synthetic': True, 'run_id': uuid4().hex,
                      'source': 'upright_replica', 'report_type': 'paid_orders', 'start_date': str(start), 'end_date': str(end),
                      'mode': request.get('mode', 'normal'), 'requested_at': now(), 'finished_at': None,
                      'status': 'pending', 'stage': 'pending', 'attempts': [], 'cause': '', 'owner_role': '',
                      'import_state': 'not_submitted', 'publication_state': 'not_published',
                      'batch_id': None, 'checksum': None, 'row_count': None, 'coverage_state': None,
                      'max_attempts': 2, 'deadline_seconds': 90}
            self._save(record)
            if not self.available:
                record.update(status='needs_human', stage='failed', finished_at=now(),
                              cause='Report collection is not configured here. Upload the CSV and manifest, or ask the demo maintainer.',
                              owner_role='Demo maintainer')
                self._save(record)
                return record
            self.active = True
            self.executor.submit(self._collect, record)
            return dict(record)

    def _attempt(self, record, number, remaining):
        if self.attempt_fn:
            return self.attempt_fn(record, number)
        work = self.root / record['run_id']
        work.mkdir(exist_ok=True)
        params = {'baseUrl': self.portal_url, 'startDate': record['start_date'], 'endDate': record['end_date'],
                  'runId': record['run_id'], 'outputDir': str(work), 'mode': record['mode'],
                  'deadlineMs': 1000 if record['mode'] == 'timeout' else min(40000, int(remaining*1000))}
        request_path = work / 'request.json'
        request_path.write_text(json.dumps(params))
        env = dict(os.environ, NODE_PATH=str(Path(self.node_modules).resolve()))
        if self.chrome_path:
            env['CHROME_PATH'] = self.chrome_path
        try:
            process = subprocess.run([self.node, str(ROOT / 'acquisition/run_skill.cjs'), '--request', str(request_path)],
                                     cwd=ROOT, env=env, text=True, capture_output=True, timeout=min(45, remaining))
            (work / f'attempt-{number}.log').write_text(process.stdout + process.stderr)
            result = json.loads(process.stdout)
            if not isinstance(result, dict) or type(result.get('ok')) is not bool:
                raise ValueError('Invalid runner result')
            return result
        except subprocess.TimeoutExpired:
            return {'ok': False, 'type': 'timeout', 'detail': 'Collection deadline exceeded'}
        except (OSError, ValueError):
            return {'ok': False, 'type': 'runtime_unavailable', 'detail': 'Collection runtime failed; use manual upload or contact the demo maintainer'}

    def _collect(self, record):
        started = time.monotonic()
        acquired = {}
        try:
            with self.lock:
                record.update(status='running', stage='collecting')
                self._save(record)

            def attempt(number):
                result = self._attempt(record, number, max(0.1, 90-(time.monotonic()-started)))
                acquired.clear()
                acquired.update(result)
                with self.lock:
                    record['attempts'].append({'n': number, 'type': result.get('type', 'unknown'), 'ok': bool(result.get('ok'))})
                    self._save(record)
                return result

            state = execute(record['run_id'], attempt, max_attempts=2, deadline_s=90, clock=time.monotonic)
            if not state.delivered:
                with self.lock:
                    record.update(status=state.status, cause=state.cause, owner_role=state.owner_role, stage='failed')
                return
            with self.lock:
                record['stage'] = 'verifying'
                self._save(record)
            verified = intake(acquired['file'], acquired['manifest'], record['run_id'], record['start_date'], record['end_date'],
                              'upright_replica', 'paid_orders', self.root / 'verified')
            with self.lock:
                record.update(stage='importing', checksum=verified['checksum'], row_count=verified['row_count'])
                self._save(record)
            batch, _ = submit(verified, self.pipeline)
            with self.lock:
                record.update(batch_id=batch['batch_id'], import_state=batch['status'],
                              publication_state='blocked' if batch['status'] == 'failed' else 'published')
                self._save(record)
            from services.metrics.query import metric_response
            metrics = metric_response(self.pipeline, record['start_date'], record['end_date'], 'upright_replica')
            with self.lock:
                record.update(batch_id=batch['batch_id'], import_state=batch['status'], coverage_state=metrics['coverage']['state'],
                              publication_state='blocked' if batch['status'] == 'failed' else 'published',
                              status='needs_human' if batch['status'] == 'failed' else 'succeeded',
                              stage='failed' if batch['status'] == 'failed' else 'complete',
                              cause='Import reconciliation failed; review source rows and controls.' if batch['status'] == 'failed' else '',
                              owner_role='Data maintainer' if batch['status'] == 'failed' else '')
        except Exception as error:
            with self.lock:
                record.update(status='needs_human', stage='failed', cause=str(error), owner_role='Data / acquisition maintainer')
        finally:
            with self.lock:
                record['finished_at'] = now()
                self._save(record)
                self.active = False

    def close(self):
        with self.lock:
            self.closed = True
        self.executor.shutdown(wait=True)
