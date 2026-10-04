"""Excel delivery from the exact pinned snapshot, including cached formulas."""
import io
from decimal import Decimal

from services.data.contracts import DataError
from .service import dates


def build(service, snapshot_id):
    try:
        import xlsxwriter
    except ImportError:
        raise DataError('export_unavailable', 'Install the pinned requirements-showcase.txt for Excel delivery')
    snapshot = service.snapshot(snapshot_id)
    response = service.metrics(dict(snapshot_id=snapshot_id))
    if response['coverage']['state'] != 'complete' or response['freshness']['is_last_good']:
        raise DataError('export_incomplete', 'Complete both sources through September 30 before exporting the month')
    stream = io.BytesIO()
    workbook = xlsxwriter.Workbook(stream, {'in_memory': True, 'strings_to_formulas': False, 'strings_to_urls': False})
    heading = workbook.add_format({'bold': True, 'font_color': '#2e7d5b', 'bg_color': '#edf4ef'})
    money_fmt = workbook.add_format({'num_format': '$#,##0.00;[Red]-$#,##0.00'})
    number_fmt = workbook.add_format({'num_format': '0.00'})

    def sheet(name, fields, rows):
        ws = workbook.add_worksheet(name)
        ws.freeze_panes(1, 0)
        ws.set_column(0, len(fields) - 1, 22)
        for col, field in enumerate(fields):
            ws.write(0, col, field, heading)
        for n, row in enumerate(rows, 1):
            for col, field in enumerate(fields):
                value = row.get(field)
                if value is not None:
                    ws.write(n, col, value)
        if rows:
            ws.autofilter(0, 0, len(rows), len(fields) - 1)
        return ws

    definitions = [dict(topic='Classification', definition='All data is synthetic; labor and shipping assumptions are invented.'),
                   dict(topic='Snapshot', definition=snapshot_id),
                   dict(topic='Coverage', definition='September 1–30, 2026; Upright paid orders and Cash Monkey units are disjoint fictional feeds.'),
                   dict(topic='Customers', definition='Distinct buyers computed per source/platform for the full selected period; never sum daily unique counts.'),
                   dict(topic='Daily tabs', definition='Available metrics have formulas and backend-calculated cached results; unavailable inputs leave blank cells.')]
    definitions += [dict(topic=m['metric_id'], definition=m['definition']) for m in response['metrics']]
    sheet('Definitions', ['topic', 'definition'], definitions).set_column(1, 1, 115)
    metric_fields = ['metric_id', 'value', 'unit', 'availability', 'availability_reason']
    month = sheet('Monthly Summary', metric_fields, [{**m, 'value': float(Decimal(m['value'])) if m['value'] is not None else None} for m in response['metrics']])
    month.set_column(0, 0, 29)
    daily_positions = {}
    for date in dates('2026-09-01', '2026-09-30'):
        daily = service.metrics(dict(snapshot_id=snapshot_id, start_date=date, end_date=date))
        daily_positions[date] = {m['metric_id']: i + 2 for i, m in enumerate(daily['metrics'])}
        ws = sheet(date, metric_fields, daily['metrics'])
        for i, metric in enumerate(daily['metrics'], 1):
            if metric['value'] is None:
                ws.write_blank(i, 1, None)
                continue
            value = float(Decimal(metric['value']))
            ws.write_formula(i, 1, '=' + metric['value'], money_fmt if metric['unit'] in ('USD', 'USD/hour') else number_fmt, value)
        row = len(daily['metrics']) + 3
        ws.write(row, 0, 'Source / record grain', heading)
        for n, src in enumerate(daily['by_source'], row + 1):
            ws.write(n, 0, src['source'])
            ws.write_number(n, 1, src['records'])
            ws.write_number(n, 2, src['orders'])
            ws.write(n, 3, 'records / distinct orders')
    additive = {'net_sales', 'labor_hours', 'fees', 'shipping_expense', 'labor_cost', 'contribution'}
    for i, metric in enumerate(response['metrics'], 1):
        if metric['value'] is None:
            continue
        if metric['metric_id'] in additive:
            formula = '=SUM(' + ','.join("'%s'!B%d" % (d, positions[metric['metric_id']]) for d, positions in daily_positions.items()) + ')'
        elif metric['metric_id'] == 'revenue_per_labor_hour':
            formula = '=B2/B3'
        else:
            formula = '=B8/B2*100'
        month.write_formula(i, 1, formula, money_fmt if metric['unit'] in ('USD', 'USD/hour') else number_fmt, float(Decimal(metric['value'])))
    _, _, facts, _, _ = service._context(dict(snapshot_id=snapshot_id))
    fields = list(facts[0]) if facts else ['source', 'record_key']
    sheet('Normalized Sales', fields, facts)
    inputs = service.inputs(dict(snapshot_id=snapshot_id))
    sheet('Labor Inputs', ['source', 'date', 'store_id', 'minutes', 'labor_cost', 'input_id', 'source_row_number'], inputs['labor'])
    sheet('Shipping Inputs', ['source', 'record_key', 'amount', 'input_id', 'source_row_number'], inputs['shipping'])
    sheet('Customer Counts', ['source', 'platform', 'value', 'availability'], response['customer_counts'])
    reconciliation = []
    for source in snapshot['sources']:
        with service.pipeline.db() as db:
            row = db.execute('SELECT b.* FROM metric_runs r JOIN import_batches b ON b.id=r.batch_id WHERE r.id=?', (source['metric_run_id'],)).fetchone()
        reconciliation.append(dict(source=source['source'], metric_run_id=source['metric_run_id'], batch_id=row['id'] if row else None,
                                   state=source['coverage']['state'], controls=row['reconciliation_json'] if row else None))
    sheet('Reconciliation', ['source', 'metric_run_id', 'batch_id', 'state', 'controls'], reconciliation)
    sheet('Source Evidence', ['source', 'record_key', 'file_id', 'batch_id', 'source_row_number', 'metric_run_id'], facts)
    sheet('Source Register', ['name', 'kind', 'status', 'description'], service.sources()['sources'])
    workbook.close()
    return stream.getvalue()
