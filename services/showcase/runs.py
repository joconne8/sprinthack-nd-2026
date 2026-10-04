"""Bounded two-source collection and real browser-frame evidence."""
import json
import os
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from acquisition.intake import intake, submit
from acquisition.run_state import execute
from services.data.contracts import DataError, canonical, day, now
from .service import ROOT
from .validation import envelope, keys


class Runs:
    def __init__(self, service):
        self.service, self.pipeline, self.acquisition = service, service.pipeline, service.acquisition
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='showcase-browser')
        self.active = False
        self.closed = False
        with self.pipeline.db() as db:
            for row in db.execute('SELECT record_json FROM showcase_runs'):
                record = json.loads(row[0])
                if record['status'] in ('pending', 'running'):
                    record.update(status='needs_human', stage='failed', cause='Server restarted before collection completed', owner_role='Demo maintainer')
                    db.execute('UPDATE showcase_runs SET record_json=? WHERE id=?', (canonical(record), record['run_id']))

    def _save(self, record):
        with self.pipeline.db() as db:
            db.execute('INSERT OR REPLACE INTO showcase_runs VALUES (?,?)', (record['run_id'], canonical(record)))

    def get(self, identity):
        with self.pipeline.db() as db:
            row = db.execute('SELECT record_json FROM showcase_runs WHERE id=?', (identity,)).fetchone()
        if not row:
            raise DataError('not_found', 'Unknown showcase acquisition run')
        return json.loads(row[0])

    def history(self):
        with self.pipeline.db() as db:
            rows = db.execute('SELECT record_json FROM showcase_runs ORDER BY rowid DESC LIMIT 50').fetchall()
        return envelope(runs=[json.loads(r[0]) for r in rows], runtime_available=bool(self.acquisition and self.acquisition.available))

    def start(self, body):
        keys(body, ('recipe_id', 'start_date', 'end_date', 'mode', 'headed'), ('recipe_id', 'start_date', 'end_date'))
        start, end = day(body['start_date']), day(body['end_date'])
        if start > end or start.year != 2026 or end.year != 2026 or (end - start).days > 30:
            raise DataError('invalid_period', 'Choose an ordered 2026 period of at most 31 days')
        if body.get('mode', 'normal') not in ('normal', 'session-expired', 'changed-label', 'missing-report', 'delayed', 'timeout') or type(body.get('headed', False)) is not bool:
            raise DataError('mode_invalid', 'Unknown failure mode or invalid headed flag')
        self.service.recipes()
        recipe = self.service.recorder.recipe(body['recipe_id'])
        with self.lock:
            if self.active or self.closed:
                raise DataError('collection_busy', 'Wait for the active report collection')
            record = envelope(run_id=uuid4().hex, status='pending', stage='pending', source=recipe['source'],
                              start_date=body['start_date'], end_date=body['end_date'], recipe_id=recipe['recipe_id'],
                              recipe_version=recipe['recipe_version'], attempts=[], cause='', owner_role='', batch_id=None,
                              checksum=None, row_count=None, snapshot_id=None, mode=body.get('mode', 'normal'), headed=body.get('headed', False),
                              import_state='not_submitted', publication_state='not_published', requested_at=now(), finished_at=None)
            self._save(record)
            if not self.acquisition or not self.acquisition.available:
                record.update(status='needs_human', stage='failed', cause='Pinned Node/Playwright runtime unavailable; follow DEMO.md setup', owner_role='Demo maintainer')
                self._save(record)
                return record
            self.active = True
            self.executor.submit(self._collect, record, recipe)
            return record

    def _collect(self, record, recipe):
        began = time.monotonic()
        result = {}
        directory = self.service.root / 'runs' / record['run_id']
        directory.mkdir(parents=True, exist_ok=True)
        skill_path = directory / 'approved-skill.json'
        skill_path.write_text(canonical(recipe['recipe']))
        record.update(status='running', stage='collecting')
        self._save(record)
        try:
            def attempt(n):
                work = directory / ('attempt-%d' % n)
                work.mkdir(exist_ok=True)
                params = dict(baseUrl=self.acquisition.portal_url, startDate=record['start_date'], endDate=record['end_date'],
                              runId=record['run_id'], outputDir=str(work), mode=record['mode'], headed=record['headed'],
                              capture=True, skillPath=str(skill_path), deadlineMs=1000 if record['mode'] == 'timeout' else 40000)
                request = work / 'request.json'
                request.write_text(canonical(params))
                env = dict(os.environ, NODE_PATH=str(Path(self.acquisition.node_modules).resolve()))
                if self.acquisition.chrome_path:
                    env['CHROME_PATH'] = self.acquisition.chrome_path
                try:
                    process = subprocess.run([self.acquisition.node, str(ROOT / 'acquisition/run_skill.cjs'), '--request', str(request)],
                                             cwd=ROOT, env=env, capture_output=True, text=True, timeout=min(45, max(1, 90 - (time.monotonic() - began))))
                    (work / 'runner.log').write_text(process.stdout + process.stderr)
                    acquired = json.loads(process.stdout)
                    if not isinstance(acquired, dict) or type(acquired.get('ok')) is not bool:
                        raise ValueError('Invalid runner response')
                except subprocess.TimeoutExpired:
                    acquired = dict(ok=False, type='timeout', detail='Bounded collection deadline exceeded')
                except (OSError, ValueError):
                    acquired = dict(ok=False, type='runtime_unavailable', detail='Browser runner unavailable')
                result.clear()
                result.update(acquired)
                record['attempts'].append(dict(n=n, ok=acquired['ok'], type=acquired.get('type')))
                self._save(record)
                return acquired

            state = execute(record['run_id'], attempt, max_attempts=2, deadline_s=90, clock=time.monotonic)
            if not state.delivered:
                record.update(status=state.status, stage='failed', cause=state.cause, owner_role=state.owner_role)
                return
            record['stage'] = 'verifying'
            self._save(record)
            verified = intake(result['file'], result['manifest'], record['run_id'], record['start_date'], record['end_date'],
                              recipe['source'], recipe['recipe']['report_type'], directory / 'verified')
            record.update(stage='importing', checksum=verified['checksum'], row_count=verified['row_count'])
            self._save(record)
            batch, _ = submit(verified, self.pipeline)
            record.update(batch_id=batch['batch_id'], import_state=batch['status'], publication_state='blocked' if batch['status'] == 'failed' else 'published')
            if batch['status'] == 'failed':
                record.update(status='needs_human', stage='failed', cause='Import reconciliation failed', owner_role='Data maintainer')
            else:
                record.update(status='succeeded', stage='complete', snapshot_id=self.service.snapshot()['snapshot_id'])
        except Exception as error:
            record.update(status='needs_human', stage='failed', cause=str(error), owner_role='Demo maintainer')
        finally:
            record['finished_at'] = now()
            self._save(record)
            with self.lock:
                self.active = False

    def events(self, identity):
        self.get(identity)
        directory = self.service.root / 'runs' / identity
        events = []
        for path in sorted(directory.glob('attempt-*/events.jsonl')):
            for line in path.read_text().splitlines():
                try:
                    event = json.loads(line)
                    event['frame_url'] = '/api/showcase/v1/runs/%s/frames/%s-%s' % (identity, path.parent.name, event.pop('frame'))
                    events.append(event)
                except (ValueError, KeyError):
                    continue  # writer may have an unfinished final line
        return envelope(events=events)

    def frame(self, identity, name):
        self.get(identity)
        match = re.fullmatch(r'(attempt-[12])-(frame-[0-9]{3}\.png)', name)
        if not match:
            raise DataError('not_found', 'Unknown browser frame')
        file = self.service.root / 'runs' / identity / match[1] / match[2]
        if not file.is_file():
            raise DataError('not_found', 'Browser frame not yet captured')
        return file.read_bytes()

    def close(self):
        self.closed = True
        self.executor.shutdown(wait=True)
