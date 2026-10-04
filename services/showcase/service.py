"""Immutable combined snapshots and deterministic showcase calculations.

Inputs are fictional and explicit. Historical snapshot queries use only their
pinned source metric runs and auxiliary artifacts, never today's active rows.
"""
import csv
import importlib.util
import io
import json
import re
import threading
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import urlencode

from services.data.contracts import DataError, canonical, cents, day, digest, money, now
from services.metrics.query import metric_response, published_rows
from services.data.inventory.store import load_pack
from .validation import SOURCES, envelope, keys, scope

ROOT = Path(__file__).resolve().parents[2]
DEFINITION = 'showcase-september-v1'
BASE = '/api/showcase/v1'


def decimal(value, places=2):
    return format(Decimal(value).quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP), '.%df' % places)


def dates(start, end):
    current = day(start)
    while current <= day(end):
        yield current.isoformat()
        current += timedelta(days=1)


def replica():
    spec = importlib.util.spec_from_file_location('showcase_replica', ROOT / 'data ingestion/server.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ShowcaseService:
    def __init__(self, pipeline, acquisition=None):
        self.pipeline, self.acquisition = pipeline, acquisition
        self.root = pipeline.root / 'showcase'
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.recorder = None
        self.runner = None

    def prepare(self, checkpoint=False):
        """Idempotent seed through Sep29; checkpoint imports the complete month."""
        portal = replica()
        end = '2026-09-30' if checkpoint else '2026-09-29'
        fixture_root = ROOT / 'goodwill/showcase-data'
        fixture_manifest = json.loads((fixture_root / 'MANIFEST.json').read_text())
        for name, expected in fixture_manifest['files'].items():
            if Path(name).name != name or digest((fixture_root / name).read_bytes()) != expected:
                raise DataError('fixture_corrupt', 'Pinned sample data changed: ' + name)
        results = []
        for source in ('upright', 'cash_monkey'):
            spec = portal.validate(dict(source=source, start_date='2026-09-01', end_date=end,
                                       timezone='America/Indiana/Indianapolis' if source == 'upright' else 'UTC',
                                       payment_status='All'))
            if checkpoint:
                payload = (fixture_root / (source + '_september.csv')).read_bytes()
                manifest = json.loads((fixture_root / (source + '_september.manifest.json')).read_text())
            else:
                payload, manifest = portal.create_artifact(spec)
            results.append(self.pipeline.import_bytes(payload, manifest))
        with (fixture_root / 'labor.csv').open(newline='') as stream:
            labor = [dict(row, minutes=int(row['minutes'])) for row in csv.DictReader(stream)]
        with (fixture_root / 'shipping.csv').open(newline='') as stream:
            shipping = [dict(row, amount_cents=int(row['amount_cents'])) for row in csv.DictReader(stream)]
        self.replace_auxiliary(labor, shipping)
        # Original August examples remain independently dated and verified.
        # Their items are never joined to the disjoint September sales feeds.
        load_pack(self.pipeline, ROOT / 'goodwill/synthetic-data')
        self.recipes()
        result = envelope(imports=results, snapshot=self.snapshot(), prepared_through=end)
        (self.root / 'prepared.json').write_text(json.dumps(result, indent=2) + '\n')
        return result

    def replace_auxiliary(self, labor_rows, shipping_rows):
        """Versioned local input loader; used by seed and independent controls."""
        result = []
        with self.lock, self.pipeline.db() as db:
            for kind, rows in [('labor', labor_rows), ('shipping', shipping_rows)]:
                normalized = []
                seen = set()
                for row in rows:
                    allowed = ('source', 'date', 'store_id', 'minutes') if kind == 'labor' else ('source', 'record_key', 'amount_cents')
                    keys(row, allowed, allowed)
                    if row['source'] not in SOURCES:
                        raise DataError('source_invalid', 'Auxiliary inputs require a showcase source')
                    if kind == 'labor':
                        day(row['date'])
                        if not row['date'].startswith('2026-09-') or row['store_id'] not in ['GW-%03d' % n for n in range(1, 25)]:
                            raise DataError('input_scope', 'Labor inputs require September and a known store')
                        amount = row['minutes']
                        row_key = canonical([row['date'], row['store_id']])
                    else:
                        amount = row['amount_cents']
                        if not isinstance(row['record_key'], str) or not row['record_key']:
                            raise DataError('input_key', 'Shipping costs require a source record key')
                        row_key = row['record_key']
                    if type(amount) is not int or not 0 <= amount <= 100000000:
                        raise DataError('input_amount', 'Inputs require a bounded nonnegative integer')
                    identity = (row['source'], row_key)
                    if identity in seen:
                        raise DataError('input_duplicate', 'Duplicate input at its declared grain')
                    seen.add(identity)
                    normalized.append((row_key, dict(row)))
                normalized.sort(key=lambda r: (r[1]['source'], r[0]))
                data = canonical([r[1] for r in normalized]).encode()
                checksum = digest(data)
                input_id = digest((kind + DEFINITION + checksum).encode())
                path = self.root / (input_id + '.json')
                if path.exists() and digest(path.read_bytes()) != checksum:
                    raise DataError('archive_corrupt', 'An immutable auxiliary input artifact changed')
                if not path.exists():
                    path.write_bytes(data)
                db.execute('INSERT OR IGNORE INTO showcase_inputs VALUES (?,?,?,?,?,?)',
                           (input_id, kind, checksum, DEFINITION, now(), str(path)))
                for n, (row_key, row) in enumerate(normalized, 1):
                    db.execute('INSERT OR IGNORE INTO showcase_input_rows VALUES (?,?,?,?,?)',
                               (input_id, n, row['source'], row_key, canonical(row)))
                db.execute('INSERT OR REPLACE INTO showcase_active_inputs VALUES (?,?)', (kind, input_id))
                result.append(input_id)
        return result

    def snapshot(self, snapshot_id=None):
        with self.lock, self.pipeline.db() as db:
            if snapshot_id:
                row = db.execute('SELECT manifest_json FROM showcase_snapshots WHERE id=?', (snapshot_id,)).fetchone()
                if not row:
                    raise DataError('not_found', 'Unknown immutable showcase snapshot')
                return json.loads(row[0])
            source_rows = []
            db.execute('BEGIN')
            for source in SOURCES:
                publication = db.execute('SELECT p.*,b.status FROM source_publications p JOIN import_batches b ON b.id=p.latest_batch_id WHERE p.source=?', (source,)).fetchone()
                run_id = publication['run_id'] if publication else None
                state = 'stale_last_good' if publication and publication['status'] == 'failed' and run_id else 'published' if run_id else 'unpublished'
                source_rows.append(dict(source=source, metric_run_id=run_id,
                                        coverage=self._coverage(source, run_id, '2026-09-01', '2026-09-30'),
                                        latest_import_state=state,
                                        latest_batch_id=publication['latest_batch_id'] if publication else None))
            auxiliary = [dict(r) for r in db.execute('SELECT i.id input_id,i.kind,i.checksum,i.definition_version FROM showcase_active_inputs a JOIN showcase_inputs i ON i.id=a.input_id ORDER BY i.kind')]
            manifest = dict(month='2026-09', definition_version=DEFINITION, sources=source_rows, auxiliary=auxiliary)
            identity = digest(canonical(manifest).encode())
            existing = db.execute('SELECT manifest_json FROM showcase_snapshots WHERE id=?', (identity,)).fetchone()
            if existing:
                return json.loads(existing[0])
            result = envelope(snapshot_id=identity, published_at=now(), **manifest)
            db.execute('INSERT INTO showcase_snapshots VALUES (?,?,?)', (identity, result['published_at'], canonical(result)))
            return result

    def _coverage(self, source, run_id, start, end):
        """Cash Monkey is a UTC DATE report; do not infer missing clock hours.

        These showcase dates mean native report dates: Eastern payment dates for
        Upright and UTC order dates for Cash Monkey. That distinction is exported.
        """
        expected = list(dates(start, end))
        if not run_id:
            complete = []
        elif source == SOURCES[0]:
            complete = metric_response(self.pipeline, start, end, source, run_id=run_id)['coverage']['complete_days']
        else:
            complete = set()
            with self.pipeline.db() as db:
                run = db.execute('SELECT published_at FROM metric_runs WHERE id=? AND source=?', (run_id, source)).fetchone()
                for row in db.execute('SELECT b.request_start,b.request_end,w.scope_json FROM coverage_windows w JOIN import_batches b ON b.id=w.batch_id WHERE w.source=? AND b.recorded_at<=?', (source, run['published_at'])):
                    filters = json.loads(row['scope_json'])
                    full = not any(filters.get(k) for k in ('channels', 'accounts', 'order_ids', 'skus')) and filters.get('payment_status') == 'All'
                    if full:
                        complete.update(dates(row['request_start'], row['request_end']))
            complete = sorted(set(expected) & complete)
        missing = [d for d in expected if d not in complete]
        return dict(state='complete' if not missing else 'partial' if complete else 'unavailable',
                    expected_days=expected, covered_days=complete, missing_days=missing)

    def _context(self, query):
        selected = scope(query)
        snap = self.snapshot(query.get('snapshot_id'))
        facts = []
        missing = set()
        stale = False
        with self.pipeline.db() as db:
            for source in snap['sources']:
                if selected['source'] != 'all' and selected['source'] != source['source']:
                    continue
                missing.update(self._coverage(source['source'], source['metric_run_id'], selected['start_date'], selected['end_date'])['missing_days'])
                stale |= source['latest_import_state'] == 'stale_last_good'
                if not source['metric_run_id']:
                    continue
                filters = dict(selected, source=source['source'], reporting_timezone='America/New_York')
                for row in published_rows(db, source['metric_run_id'], filters):
                    original = json.loads(db.execute('SELECT original_json FROM staging_rows WHERE batch_id=? AND row_number=?', (row['batch_id'], row['row_number'])).fetchone()[0])
                    fee = original.get('marketplace_fee') if row['source'] == SOURCES[0] else original.get('payment_fee')
                    try:
                        fee_cents = cents(fee)
                        fee = money(fee_cents) if fee_cents >= 0 else None
                    except DataError:
                        fee = None
                    facts.append(dict(source=row['source'], record_key=row['record_key'], reporting_date=row['reporting_date'],
                                      platform=row['platform'], store_id=row['store_id'], buyer_id=row['buyer_id'],
                                      gross_item_sales=money(row['gross_cents']), refunds=money(row['refund_cents']),
                                      net_sales=money(row['gross_cents'] - row['refund_cents']),
                                      fee=fee,
                                      file_id=row['file_id'], batch_id=row['batch_id'], source_row_number=row['row_number'],
                                      metric_run_id=source['metric_run_id']))
        facts.sort(key=lambda r: (r['reporting_date'], r['source'], r['record_key']))
        return selected, snap, facts, sorted(missing), stale

    def _inputs(self, snap, selected, facts):
        labor, shipping = [], []
        sale_keys = {(r['source'], r['record_key']) for r in facts}
        with self.pipeline.db() as db:
            for item in snap['auxiliary']:
                artifact = db.execute('SELECT artifact_ref,checksum FROM showcase_inputs WHERE id=?', (item['input_id'],)).fetchone()
                if not artifact or digest(Path(artifact['artifact_ref']).read_bytes()) != item['checksum']:
                    raise DataError('archive_corrupt', 'Pinned auxiliary artifact changed')
                for record in db.execute('SELECT * FROM showcase_input_rows WHERE input_id=? ORDER BY row_number', (item['input_id'],)):
                    row = json.loads(record['payload_json'])
                    meta = dict(input_id=item['input_id'], source_row_number=record['row_number'])
                    if selected['source'] != 'all' and row['source'] != selected['source']:
                        continue
                    if item['kind'] == 'labor':
                        if not selected['start_date'] <= row['date'] <= selected['end_date'] or (selected['store'] and row['store_id'] != selected['store']):
                            continue
                        labor.append(dict(row, labor_cost=decimal(Decimal(row['minutes']) * Decimal(20) / 60), **meta))
                    elif (row['source'], row['record_key']) in sale_keys:
                        shipping.append(dict(source=row['source'], record_key=row['record_key'], amount=money(row['amount_cents']), **meta))
        return labor, shipping

    def metrics(self, query):
        selected, snap, facts, missing, stale = self._context(query)
        labor, shipping = self._inputs(snap, selected, facts)
        coverage = 'partial' if missing else 'complete'
        state = 'partial' if missing or stale else 'available'
        if not facts and missing:
            state = 'unavailable'
        reason = 'Missing reporting days: ' + ', '.join(missing) if missing else 'Latest source import failed; verified last-good data retained' if stale else None
        period_reason = 'Sales coverage is incomplete for the matched labor/cost period' if missing else None
        expected = {(src, date, store) for src in SOURCES if selected['source'] in ('all', src)
                    for date in dates(selected['start_date'], selected['end_date'])
                    for store in ([selected['store']] if selected['store'] else ['GW-%03d' % n for n in range(1, 25)])}
        labor_keys = {(r['source'], r['date'], r['store_id']) for r in labor}
        labor_reason = 'Labor has no platform allocation' if selected['platform'] else 'Matched labor inputs are missing' if not expected <= labor_keys else None
        shipping_reason = 'Matched shipping inputs are missing' if len(shipping) != len(facts) else None
        fee_reason = 'Pinned source fee inputs are missing or invalid' if any(r['fee'] is None for r in facts) else None
        cost_reason = shipping_reason or fee_reason
        gross = sum(cents(r['gross_item_sales']) for r in facts)
        refunds = sum(cents(r['refunds']) for r in facts)
        net = gross - refunds
        minutes = sum(r['minutes'] for r in labor)
        hours = Decimal(minutes) / 60
        labor_cost = sum((Decimal(r['minutes']) * 2000 / 60 for r in labor), Decimal(0))
        fees = sum(cents(r['fee']) for r in facts if r['fee'] is not None)
        shipping_cost = sum(cents(r['amount']) for r in shipping)
        contribution = Decimal(net - fees - shipping_cost) - labor_cost
        metrics = []

        def add(identifier, value, unit, definition, unavailable=None):
            availability = 'unavailable' if unavailable or state == 'unavailable' else state
            metrics.append(dict(metric_id=identifier, value=None if availability == 'unavailable' else value,
                                unit=unit, availability=availability, availability_reason=unavailable or reason, definition=definition))
        add('net_sales', money(net), 'USD', 'Item sales minus refunds; excludes shipping collected, tax, and fees')
        add('labor_hours', decimal(hours), 'hours', 'Invented matched source/store/day minutes divided by 60', labor_reason)
        add('revenue_per_labor_hour', decimal(Decimal(net) / 100 / hours) if hours else None, 'USD/hour',
            'Verified demo net sales divided by matched invented labor hours', labor_reason or period_reason or ('Labor hours are zero' if not hours else None))
        add('fees', money(fees), 'USD', 'Fees on the pinned synthetic source records', fee_reason)
        add('shipping_expense', money(shipping_cost), 'USD', 'Invented shipping expense: $3.50 per sales record', shipping_reason)
        add('labor_cost', decimal(labor_cost / 100), 'USD', 'Invented $20 per hour; excludes payroll burden', labor_reason)
        add('contribution', decimal(contribution / 100), 'USD', 'Net sales less source fees, invented shipping and labor; excludes overhead and tax', labor_reason or cost_reason or period_reason)
        add('contribution_margin', decimal(contribution / net * 100) if net else None, 'percent',
            'Demo contribution divided by net sales; not production net margin', labor_reason or cost_reason or period_reason or ('Net sales is zero' if not net else None))

        def breakdown(field, label):
            totals = {}
            for r in facts:
                key = r[field] or 'unknown'
                totals[key] = totals.get(key, 0) + cents(r['net_sales'])
            return [{label: key, 'net_sales': money(value)} for key, value in sorted(totals.items())]
        by_source = breakdown('source', 'source')
        for row in by_source:
            records = [r for r in facts if r['source'] == row['source']]
            row['records'] = len(records)
            row['orders'] = len({json.loads(r['record_key'])[0].split('-U')[0] for r in records})
        daily = breakdown('reporting_date', 'date')
        daily_map = {r['date']: r['net_sales'] for r in daily}
        daily = [dict(date=d, net_sales=daily_map.get(d) if d in missing else daily_map.get(d, '0.00')) for d in dates(selected['start_date'], selected['end_date'])]
        customers = []
        for src, platform in sorted({(r['source'], r['platform']) for r in facts}):
            records = [r for r in facts if r['source'] == src and r['platform'] == platform]
            known = all(r['buyer_id'] for r in records)
            customers.append(dict(source=src, platform=platform, value=str(len({r['buyer_id'] for r in records})) if known else None,
                                  availability=state if known else 'unavailable'))
        linkquery = dict(selected, snapshot_id=snap['snapshot_id'])
        linkquery = {k: v for k, v in linkquery.items() if v is not None}
        return envelope(snapshot_id=snap['snapshot_id'], scope=selected, coverage=dict(state=coverage, missing_days=missing),
                        freshness=dict(published_at=snap['published_at'], is_last_good=stale), metrics=metrics, daily=daily,
                        by_source=by_source, by_platform=breakdown('platform', 'platform'), by_store=breakdown('store_id', 'store'),
                        customer_counts=customers, evidence_url=BASE + '/evidence?' + urlencode(linkquery),
                        auxiliary_url=BASE + '/inputs?' + urlencode(linkquery))

    def comparison(self, query):
        keys(query, ('snapshot_id', 'source', 'store', 'platform'))
        snap = self.snapshot(query.get('snapshot_id'))
        common = dict(query, snapshot_id=snap['snapshot_id'])
        previous = self.metrics(dict(common, start_date='2026-09-17', end_date='2026-09-23'))
        current = self.metrics(dict(common, start_date='2026-09-24', end_date='2026-09-30'))
        p = {m['metric_id']: m for m in previous['metrics']}
        c = {m['metric_id']: m for m in current['metrics']}
        complete = all(m['availability'] == 'available' for m in [p['revenue_per_labor_hour'], c['revenue_per_labor_hour']])
        explanation = ('September 17–23: $%s sales / %s invented hours = $%s/hour. '
                       'September 24–30: $%s sales / %s invented hours = $%s/hour. '
                       'The change follows the sales and modeled hours shown here. This is an arithmetic comparison, not a verified business cause.' %
                       (p['net_sales']['value'], p['labor_hours']['value'], p['revenue_per_labor_hour']['value'],
                        c['net_sales']['value'], c['labor_hours']['value'], c['revenue_per_labor_hour']['value'])) if complete else 'The comparison is unavailable until both periods have complete sales coverage and matched labor inputs without a platform filter.'
        if complete and Decimal(c['net_sales']['value']) > Decimal(p['net_sales']['value']) and Decimal(c['revenue_per_labor_hour']['value']) < Decimal(p['revenue_per_labor_hour']['value']):
            explanation += ' Sales increased, but invented labor hours increased faster, so revenue per labor hour fell.'
        return envelope(snapshot_id=snap['snapshot_id'], previous=previous, current=current, explanation=explanation, verified_cause=False)

    def evidence(self, query):
        selected, snap, facts, _, _ = self._context(query)
        try:
            offset, limit = int(query.get('offset', 0)), int(query.get('limit', 100))
        except (ValueError, TypeError):
            raise DataError('invalid_pagination', 'Integer pagination required')
        if offset < 0 or not 1 <= limit <= 200:
            raise DataError('invalid_pagination', 'Offset nonnegative; limit 1..200')
        return envelope(snapshot_id=snap['snapshot_id'], scope=selected, total_rows=len(facts), rows=facts[offset:offset + limit],
                        scope_total=money(sum(cents(r['net_sales']) for r in facts)))

    def inputs(self, query):
        selected, snap, facts, _, _ = self._context(query)
        labor, shipping = self._inputs(snap, selected, facts)
        return envelope(snapshot_id=snap['snapshot_id'], labor=labor, shipping=shipping,
                        definitions=['All auxiliary inputs are invented sample data.',
                                     'Labor: source/store/day; Upright 2h/store/day before Sep24, 3h afterwards; Cash Monkey 0.5h/store/day.',
                                     'Shipping: $3.50 per record; labor: $20/hour. Fees remain pinned source values.',
                                     'No platform labor allocation. Overhead, payroll burden and tax are excluded.'])

    def question(self, body):
        keys(body, ('snapshot_id', 'scope', 'question'), ('snapshot_id', 'scope', 'question'))
        keys(body['scope'], ('start_date', 'end_date', 'source', 'store', 'platform'))
        if not isinstance(body['question'], str) or not 1 <= len(body['question']) <= 500:
            raise DataError('question_invalid', 'Question must be 1..500 characters')
        query = dict(body['scope'], snapshot_id=body['snapshot_id'])
        metrics = self.metrics(query)
        text = ' '.join(re.sub(r'[^a-z0-9 ]', ' ', body['question'].lower()).split())
        def has(phrases):
            return any(re.search(r'\b' + re.escape(phrase) + r'\b', text) for phrase in phrases)
        if has(('approve', 'post', 'predict', 'forecast', 'delete', 'write', 'purchase', 'send', 'deploy', 'execute', 'ignore')):
            return envelope(snapshot_id=metrics['snapshot_id'], intent='unsupported', answer='This local prototype supports read-only sales summaries, supporting records, productivity comparisons, and missing inputs. It cannot approve, post, change records, or predict future results.', tools=[], citations=[])
        if has(('labor', 'labour', 'productivity', 'per hour')) and not has(('missing', 'unavailable')):
            intent, tools = 'productivity', ['comparison', 'metrics', 'evidence']
            comparison = self.comparison({k: v for k, v in query.items() if k in ('snapshot_id', 'source', 'store', 'platform')})
            answer = comparison['explanation']
            citations = []
            for label, period in [('Previous period', comparison['previous']), ('Current period', comparison['current'])]:
                citations.extend([dict(label=label + ' sales', url=period['evidence_url']), dict(label=label + ' labor/cost inputs', url=period['auxiliary_url'])])
            return envelope(snapshot_id=metrics['snapshot_id'], intent=intent, answer=answer, tools=tools, citations=citations, comparison=comparison)
        if has(('missing', 'unavailable', 'sell through', 'growth', 'net margin')):
            intent, tools = 'missing', ['metrics']
            answer = 'September sell-through needs an eligible inventory cohort and relist policy; year-over-year growth needs comparable prior-year inputs; production net margin needs approved full costs. The displayed contribution margin uses invented shipping/labor and excludes overhead, payroll burden, and taxes.'
        elif has(('evidence', 'supporting', 'records', 'source', 'behind', 'prove')):
            intent, tools = 'evidence', ['metrics', 'evidence']
            evidence = self.evidence(query)
            answer = '%s supporting sales records produce $%s demo net sales for %s through %s. Inspect the original files and matched auxiliary inputs using the links below.' % (evidence['total_rows'], evidence['scope_total'], metrics['scope']['start_date'], metrics['scope']['end_date'])
        elif has(('sales', 'revenue', 'summary', 'today')):
            intent, tools = 'sales', ['metrics', 'evidence']
            net = next(m for m in metrics['metrics'] if m['metric_id'] == 'net_sales')
            answer = ('%s through %s: %s demo net sales. %s coverage. Item sales minus refunds; shipping collected, tax and fees are excluded. All source data is synthetic.' %
                      (metrics['scope']['start_date'], metrics['scope']['end_date'], '$' + net['value'] if net['value'] else 'unavailable', metrics['coverage']['state']))
        else:
            return envelope(snapshot_id=metrics['snapshot_id'], intent='unsupported', answer='Supported questions: sales summary, supporting records, revenue per labor hour, and missing inputs. This local prototype uses model-free metric tools and cannot answer arbitrary questions.', tools=[], citations=[])
        return envelope(snapshot_id=metrics['snapshot_id'], intent=intent, answer=answer, tools=tools, metrics=metrics,
                        citations=[dict(label='Supporting sales records', url=metrics['evidence_url']), dict(label='Matched labor and cost inputs', url=metrics['auxiliary_url'])])

    def summary(self, query):
        snap = self.snapshot(query.get('snapshot_id'))
        selected = scope(query)
        return self.question(dict(snapshot_id=snap['snapshot_id'], scope=selected, question='sales summary'))

    def sales_csv(self, snapshot_id):
        _, _, facts, _, _ = self._context(dict(snapshot_id=snapshot_id))
        stream = io.StringIO(newline='')
        fields = list(facts[0]) if facts else ['source', 'record_key', 'reporting_date', 'net_sales']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(facts)
        return stream.getvalue().encode()

    def dictionary(self, snapshot_id):
        return envelope(snapshot=self.snapshot(snapshot_id), metrics=self.metrics(dict(snapshot_id=snapshot_id))['metrics'],
                        grains=dict(sales='source/record_key; Upright paid order, Cash Monkey unit', labor='source/store/day', shipping='source/record_key'),
                        reporting_dates='Upright Eastern payment dates; Cash Monkey UTC order dates. No invented intraday Cash Monkey timestamps.',
                        production_path='Import normalized CSV into existing Power BI; tenant access and approved definitions still required')

    def sources(self):
        return envelope(sources=[dict(name=name, kind=kind, status=status, description=description) for name, kind, status, description in [
            ('Upright paid orders', 'Browser report', 'connected', 'Synthetic paid-order acquisition; authoritative for this Upright fixture'),
            ('Cash Monkey orders', 'Browser report', 'connected', 'Synthetic unit-level book sales; distinct from Upright fixture'),
            ('Jewelry', 'Email/report export', 'fixture-only', 'Separate sales report; fixture-only and excluded from the two-source showcase'),
            ('OSM/PB/EasyPost', 'Portal export', 'fixture-only', 'Shipping expense; not additive sales'),
            ('FedEx', 'Portal export', 'fixture-only', 'Shipping expense; not revenue'),
            ('ShopGoodwill', 'Portal/email export', 'fixture-only', 'Standalone sales may overlap Upright; excluded from combined demo'),
            ('Goodwill Books', 'Settlement export', 'fixture-only', 'Payout reconciliation; not additive sales'),
            ('eBay', 'Portal export', 'fixture-only', 'Standalone sales may overlap Upright; excluded from combined demo'),
            ('Amazon', 'Settlement export', 'fixture-only', 'Payout reconciliation; not additive sales')]])

    def workbook(self, snapshot_id):
        from .workbook import build
        return build(self, snapshot_id)

    def recipes(self):
        from .recorder import Recorder
        with self.lock:
            if self.recorder is None:
                self.recorder = Recorder(self)
            return self.recorder.recipes()
