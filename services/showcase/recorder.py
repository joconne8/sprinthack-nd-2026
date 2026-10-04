"""Reviewed recipes compiled from human actions in the two local replicas."""
import json
import re
from urllib.request import urlopen
from uuid import uuid4

from services.data.contracts import DataError, canonical, day, digest, now
from .validation import SOURCES, envelope, keys

PATHS = {'upright_replica': ('/upright', '/upright/reports', '/upright/reports/paid-orders'),
         'cash_monkey_replica': ('/cash-monkey', '/cash-monkey/reports', '/cash-monkey/reports/orders')}
LABELS = {'upright_replica': ('Start date', 'End date', 'Timezone', 'Payment status', 'Channel'),
          'cash_monkey_replica': ('Order Date From:', 'Order Date To:', 'Format:')}
LINKS = {'upright_replica': ('▥ Reports', 'Paid orders'), 'cash_monkey_replica': ('▥ Reports', 'Orders')}
BUTTONS = {'upright_replica': ('Generate report', 'Build export'), 'cash_monkey_replica': ('Submit', 'Build export')}


def cash_skill():
    return dict(skill_id='cash-monkey-orders-replica', skill_version='1.0.0', source_name=SOURCES[1], report_type='orders',
                parameters=['start_date', 'end_date'], allowed_hosts=['localhost', '127.0.0.1'],
                steps=[dict(op='goto', path='/cash-monkey'), dict(op='click', role='link', name='▥ Reports'),
                       dict(op='click', role='link', name='Orders'),
                       dict(op='fill', label='Order Date From:', value='{start_date}'),
                       dict(op='fill', label='Order Date To:', value='{end_date}'),
                       dict(op='click', role='button', name='Submit'),
                       dict(op='wait_state', selector='#messages', ready_class='success', failed_class='error'),
                       dict(op='download', selector='[data-testid="cash-download-link"]')],
                timeouts_ms=dict(step=5000, total=40000), status='reviewed local baseline; synthetic replica only')


class Recorder:
    def __init__(self, service):
        self.service, self.pipeline = service, service.pipeline

    def recipes(self):
        from .service import ROOT
        upright = json.loads((ROOT / 'acquisition/skills/upright-paid-orders.skill.json').read_text())
        upright['status'] = 'reviewed local baseline under approved showcase plan; synthetic replica only'
        with self.pipeline.db() as db:
            for identity, skill in [('upright-baseline', upright), ('cash-monkey-baseline', cash_skill())]:
                db.execute('INSERT OR IGNORE INTO showcase_recipes VALUES (?,?,?,?,?)',
                           (identity, skill['source_name'], skill['skill_version'], now(), canonical(skill)))
            rows = db.execute('SELECT * FROM showcase_recipes ORDER BY approved_at').fetchall()
        return envelope(recipes=[self._recipe(r) for r in rows])

    def _recipe(self, row):
        return envelope(recipe_id=row['id'], source=row['source'], recipe_version=row['version'], approved=True, recipe=json.loads(row['skill_json']))

    def recipe(self, recipe_id):
        with self.pipeline.db() as db:
            row = db.execute('SELECT * FROM showcase_recipes WHERE id=?', (recipe_id,)).fetchone()
        if not row:
            raise DataError('not_found', 'Unknown approved recipe')
        return self._recipe(row)

    def start(self, body):
        keys(body, ('source',), ('source',))
        if body['source'] not in SOURCES:
            raise DataError('source_invalid', 'Choose a synthetic Upright or Cash Monkey journey')
        identity = uuid4().hex
        with self.pipeline.db() as db:
            db.execute('INSERT INTO showcase_recordings VALUES (?,?,?,?,?,?)', (identity, body['source'], 'recording', '[]', None, None))
        return self.get(identity)

    def get(self, identity):
        with self.pipeline.db() as db:
            row = db.execute('SELECT * FROM showcase_recordings WHERE id=?', (identity,)).fetchone()
        if not row:
            raise DataError('not_found', 'Unknown recording')
        return envelope(recording_id=identity, source=row['source'], status=row['status'], events=json.loads(row['events_json']),
                        recipe=json.loads(row['recipe_json']) if row['recipe_json'] else None)

    def event(self, identity, body):
        keys(body, ('event',), ('event',))
        event = body['event']
        keys(event, ('op', 'path', 'role', 'name', 'label', 'value', 'observation'), ('op', 'path', 'observation'))
        if any(not isinstance(value, str) or len(value) > 2000 for value in event.values()):
            raise DataError('recording_invalid', 'Recording fields are bounded strings')
        with self.service.lock:
            record = self.get(identity)
            if record['status'] != 'recording' or len(record['events']) >= 25:
                raise DataError('recording_closed', 'Recording is closed or exceeds 25 actions')
            source = record['source']
            if event['path'] not in PATHS[source]:
                raise DataError('path_denied', 'Only the implemented local report paths can be recorded')
            op = event['op']
            if op not in ('navigate', 'click', 'fill', 'select', 'ready', 'download'):
                raise DataError('operation_denied', 'Unknown recording action')
            if op == 'click':
                role, name = event.get('role'), event.get('name')
                if not (role == 'link' and name in LINKS[source] or role == 'button' and name in BUTTONS[source]):
                    raise DataError('control_denied', 'This control is outside the reviewed report journey')
            if op in ('fill', 'select'):
                label, value = event.get('label'), event.get('value')
                if label not in LABELS[source] or value is None:
                    raise DataError('control_denied', 'Unrecognized report field')
                if op == 'fill':
                    day(value)
                elif value not in ('America/Indiana/Indianapolis', 'All', 'CSV', ''):
                    raise DataError('filter_denied', 'Teach the full-source Eastern/UTC report without channel filters')
            record['events'].append(event)
            with self.pipeline.db() as db:
                db.execute('UPDATE showcase_recordings SET events_json=? WHERE id=?', (canonical(record['events']), identity))
            return self.get(identity)

    def review(self, identity, body):
        keys(body, ())
        with self.service.lock:
            record = self.get(identity)
            if record['status'] != 'recording':
                raise DataError('recording_closed', 'Only an active recording can be reviewed')
            source, events = record['source'], record['events']
            labels = {e.get('label'): e.get('value') for e in events if e['op'] in ('fill', 'select')}
            starts, ends = LABELS[source][:2]
            if starts not in labels or ends not in labels or not any(e['op'] == 'download' for e in events) or not any(e['op'] == 'ready' for e in events):
                raise DataError('recording_incomplete', 'Teach both date fields, wait for report-ready, and download the CSV before review')
            if source == SOURCES[0] and (labels.get('Timezone') != 'America/Indiana/Indianapolis' or labels.get('Payment status') != 'All'):
                raise DataError('recording_incomplete', 'Select Eastern Time and All payment statuses for complete Upright coverage')
            if self.service.acquisition:
                download = next(e for e in reversed(events) if e['op'] == 'download')
                job_id = download.get('value', '')
                if not re.fullmatch(r'[a-f0-9]{32}', job_id):
                    raise DataError('recording_incomplete', 'Download the newly generated report so its exact job can be verified')
                base = self.service.acquisition.portal_url.rstrip('/') + '/api/reports/' + job_id
                try:
                    with urlopen(base + '/manifest', timeout=10) as response:
                        manifest = json.load(response)
                    with urlopen(base + '/download', timeout=10) as response:
                        payload = response.read()
                except (OSError, ValueError):
                    raise DataError('training_artifact', 'Training download is unavailable; generate and record a new report')
                if (manifest.get('file_checksum') != digest(payload) or manifest.get('source_name') != source
                        or manifest.get('requested_start_date') != labels[starts] or manifest.get('requested_end_date') != labels[ends]
                        or manifest.get('synthetic') is not True or manifest.get('payment_status') != 'All'
                        or any(manifest.get(k) for k in ('channels', 'accounts', 'order_ids', 'skus'))):
                    raise DataError('training_artifact', 'The downloaded training file does not match the taught dates and full-source report')
                directory = self.service.root / 'recordings' / identity
                directory.mkdir(parents=True, exist_ok=True)
                (directory / 'training.csv').write_bytes(payload)
                (directory / 'training.manifest.json').write_text(canonical(manifest))
            steps = []
            generated = False
            for event in events:
                op = event['op']
                if op == 'navigate':
                    steps.append(dict(op='goto', path=event['path']))
                elif op == 'click':
                    step = dict(op='click', role=event['role'], name=event['name'])
                    if source == SOURCES[0] and event['name'] == '▥ Reports':
                        step['within'] = dict(role='navigation', name='Upright navigation')
                    steps.append(step)
                    generated |= event['role'] == 'button'
                elif op in ('fill', 'select'):
                    value = '{start_date}' if event['label'] == starts else '{end_date}' if event['label'] == ends else event['value']
                    steps.append(dict(op=op, label=event['label'], value=value))
                elif op == 'ready':
                    if not steps or steps[-1]['op'] != 'wait_state':
                        steps.append(dict(op='wait_state', selector='#messages', ready_class='success', failed_class='error'))
                elif op == 'download':
                    steps.append(dict(op='download', selector='[data-testid="download-{job_id}"]' if source == SOURCES[0] else '[data-testid="cash-download-link"]'))
                    break
            if not steps or steps[0]['op'] != 'goto' or not generated:
                raise DataError('recording_incomplete', 'Start recording at the portal landing page and generate a report')
            skill = dict(skill_id=identity, skill_version='1.0.0', source_name=source,
                         report_type='paid_orders' if source == SOURCES[0] else 'orders',
                         allowed_hosts=['localhost', '127.0.0.1'], parameters=['start_date', 'end_date'], steps=steps,
                         timeouts_ms=dict(step=5000, total=40000), status='human action recording; awaiting recipe approval')
            with self.pipeline.db() as db:
                db.execute('UPDATE showcase_recordings SET status=?,recipe_json=? WHERE id=?', ('review', canonical(skill), identity))
            return self.get(identity)

    def approve(self, identity, body):
        keys(body, ())
        with self.service.lock:
            record = self.get(identity)
            if record['status'] != 'review':
                raise DataError('review_required', 'Review the actual recorded actions before approving')
            skill = dict(record['recipe'], status='operator-approved local recipe; synthetic replica only')
            with self.pipeline.db() as db:
                db.execute('INSERT INTO showcase_recipes VALUES (?,?,?,?,?)', (identity, record['source'], skill['skill_version'], now(), canonical(skill)))
                db.execute('UPDATE showcase_recordings SET status=?,recipe_id=? WHERE id=?', ('approved', identity, identity))
            return self.recipe(identity)
