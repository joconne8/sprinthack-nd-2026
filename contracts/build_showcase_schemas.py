"""Generate the additive showcase contract; goodwill-v1 is untouched."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'showcase-v1'
S = {'type': 'string'}
DEC = {'type': 'string', 'pattern': r'^-?\d+\.\d{2}$'}
DATE = {'type': 'string', 'format': 'date'}
BOOL = {'type': 'boolean'}
INT = {'type': 'integer', 'minimum': 0}
NULL = {'type': 'null'}
SOURCE = {'type': 'string', 'enum': ['upright_replica', 'cash_monkey_replica']}


def array(value): return {'type': 'array', 'items': value}
def ref(name): return {'$ref': '#/$defs/' + name}
def nullable(value): return {'anyOf': [value, NULL]}
def obj(properties, required=None):
    return {'type': 'object', 'additionalProperties': False, 'properties': properties, 'required': list(properties) if required is None else required}
def env(properties, required=None):
    base = {'contract_version': {'const': 'showcase-v1'}, 'synthetic': {'const': True}}
    return obj(dict(base, **properties), list(base) + (list(properties) if required is None else required))


D = {}
D['scope'] = obj(dict(start_date=DATE, end_date=DATE, source={'enum': ['all', 'upright_replica', 'cash_monkey_replica']}, store=nullable(S), platform=nullable(S)))
D['scope_request'] = obj(D['scope']['properties'], [])
D['event'] = obj(dict(op={'enum': ['navigate', 'click', 'fill', 'select', 'ready', 'download']}, path=S,
                       role=S, name=S, label=S, value=S, observation=S), ['op', 'path', 'observation'])
D['step'] = obj(dict(op={'enum': ['goto', 'assert', 'click', 'fill', 'select', 'wait_state', 'download']}, path=S, role=S, name=S,
                      label=S, value=S, within=obj(dict(role=S, name=S)), selector=S, ready_class=S, failed_class=S), ['op'])
D['skill'] = obj(dict(skill_id=S, skill_version=S, status=S, source_name=SOURCE, report_type={'enum': ['paid_orders', 'orders']},
                       target=S, allowed_hosts=array(S), parameters=array(S), steps=array(ref('step')),
                       timeouts_ms=obj(dict(step=INT, total=INT)), stop_on=array(S), secrets=S),
                 ['skill_id', 'skill_version', 'status', 'source_name', 'report_type', 'allowed_hosts', 'parameters', 'steps', 'timeouts_ms'])
D['coverage'] = obj(dict(state={'enum': ['complete', 'partial', 'unavailable']}, expected_days=array(DATE), covered_days=array(DATE), missing_days=array(DATE)))
D['snapshot'] = env(dict(snapshot_id=S, published_at=S, definition_version=S, month={'const': '2026-09'},
                         sources=array(obj(dict(source=SOURCE, metric_run_id=nullable(S), coverage=ref('coverage'), latest_import_state=S, latest_batch_id=nullable(S)))),
                         auxiliary=array(obj(dict(input_id=S, kind={'enum': ['labor', 'shipping']}, checksum=S, definition_version=S)))))
D['metric'] = obj(dict(metric_id={'enum': ['net_sales', 'labor_hours', 'revenue_per_labor_hour', 'contribution_margin', 'contribution', 'fees', 'shipping_expense', 'labor_cost']},
                       value=nullable(DEC), unit={'enum': ['USD', 'hours', 'USD/hour', 'percent']}, availability={'enum': ['available', 'partial', 'unavailable']},
                       availability_reason=nullable(S), definition=S))
D['metrics'] = env(dict(snapshot_id=S, scope=ref('scope'), coverage=obj(dict(state={'enum': ['complete', 'partial']}, missing_days=array(DATE))),
                        freshness=obj(dict(published_at=S, is_last_good=BOOL)), metrics=array(ref('metric')),
                        daily=array(obj(dict(date=DATE, net_sales=nullable(DEC)))),
                        by_source=array(obj(dict(source=SOURCE, net_sales=DEC, records=INT, orders=INT))),
                        by_platform=array(obj(dict(platform=S, net_sales=DEC))), by_store=array(obj(dict(store=S, net_sales=DEC))),
                        customer_counts=array(obj(dict(source=SOURCE, platform=S, value=nullable(S), availability={'enum': ['available', 'partial', 'unavailable']}))),
                        evidence_url=S, auxiliary_url=S))
D['comparison'] = env(dict(snapshot_id=S, previous=ref('metrics'), current=ref('metrics'), explanation=S, verified_cause={'const': False}))
D['fact'] = obj(dict(source=SOURCE, record_key=S, reporting_date=DATE, platform=S, store_id=nullable(S), buyer_id=nullable(S),
                     gross_item_sales=DEC, refunds=DEC, net_sales=DEC, fee=nullable(DEC), file_id=S, batch_id=S, source_row_number=INT, metric_run_id=S))
D['evidence'] = env(dict(snapshot_id=S, scope=ref('scope'), total_rows=INT, rows=array(ref('fact')), scope_total=DEC))
D['inputs'] = env(dict(snapshot_id=S, labor=array(obj(dict(source=SOURCE, date=DATE, store_id=S, minutes=INT, labor_cost=DEC, input_id=S, source_row_number=INT))),
                      shipping=array(obj(dict(source=SOURCE, record_key=S, amount=DEC, input_id=S, source_row_number=INT))), definitions=array(S)))
D['question'] = env(dict(snapshot_id=S, intent={'enum': ['sales', 'evidence', 'productivity', 'missing', 'unsupported']}, answer=S,
                        tools=array({'enum': ['metrics', 'comparison', 'evidence']}), citations=array(obj(dict(label=S, url=S))), comparison=ref('comparison'), metrics=ref('metrics')),
                    ['snapshot_id', 'intent', 'answer', 'tools', 'citations'])
D['question_request'] = obj(dict(snapshot_id=S, scope=ref('scope_request'), question={'type': 'string', 'minLength': 1}))
D['recording_request'] = obj(dict(source=SOURCE))
D['event_request'] = obj(dict(event=ref('event')))
D['empty_request'] = obj({})
D['recording'] = env(dict(recording_id=S, source=SOURCE, status={'enum': ['recording', 'review', 'approved']}, events=array(ref('event')), recipe=nullable(ref('skill'))))
D['recipe'] = env(dict(recipe_id=S, source=SOURCE, recipe_version=S, approved={'const': True}, recipe=ref('skill')))
D['recipes'] = env(dict(recipes=array(ref('recipe'))))
D['run_request'] = obj(dict(recipe_id=S, start_date=DATE, end_date=DATE, mode={'enum': ['normal', 'session-expired', 'missing-report', 'changed-label', 'delayed', 'timeout']}, headed=BOOL), ['recipe_id', 'start_date', 'end_date'])
D['run'] = env(dict(run_id=S, status={'enum': ['pending', 'running', 'succeeded', 'needs_human']}, stage={'enum': ['pending', 'collecting', 'verifying', 'importing', 'complete', 'failed']}, source=SOURCE,
                    start_date=DATE, end_date=DATE, recipe_id=S, recipe_version=S, attempts=array(obj(dict(n=INT, ok=BOOL, type=S))),
                    cause=S, owner_role=S, batch_id=nullable(S), checksum=nullable(S), row_count=nullable(INT), snapshot_id=nullable(S),
                    mode=S, headed=BOOL, import_state=S, publication_state=S, requested_at=S, finished_at=nullable(S)))
D['runs'] = env(dict(runs=array(ref('run')), runtime_available=BOOL))
D['events'] = env(dict(events=array(obj(dict(step=INT, op=S, detail=S, observed_at=S, frame_url=S)))))
D['sources'] = env(dict(sources=array(obj(dict(name=S, kind=S, status={'enum': ['connected', 'fixture-only', 'awaiting-access']}, description=S)))))
D['dictionary'] = env(dict(snapshot=ref('snapshot'), metrics=array(ref('metric')), grains=obj(dict(sales=S, labor=S, shipping=S)), reporting_dates=S, production_path=S))


def main():
    ROOT.mkdir(exist_ok=True)
    (ROOT / 'schema.json').write_text(json.dumps({'$schema': 'https://json-schema.org/draft/2020-12/schema', '$defs': D}, indent=2) + '\n')
    def name(key): return ''.join(part.title() for part in key.split('_'))
    def ts(rule):
        if '$ref' in rule: return name(rule['$ref'].split('/')[-1])
        if 'anyOf' in rule: return '(' + ' | '.join(ts(r) for r in rule['anyOf']) + ')'
        if 'const' in rule: return json.dumps(rule['const'])
        if 'enum' in rule: return ' | '.join(json.dumps(v) for v in rule['enum'])
        if rule.get('type') == 'array': return 'Array<' + ts(rule['items']) + '>'
        if rule.get('type') == 'object':
            return '{ ' + '; '.join(json.dumps(k) + ('' if k in rule.get('required', []) else '?') + ': ' + ts(v) for k, v in rule['properties'].items()) + ' }'
        return {'string': 'string', 'integer': 'number', 'boolean': 'boolean', 'null': 'null'}[rule['type']]
    (ROOT / 'types.ts').write_text('// Generated by contracts/build_showcase_schemas.py.\n' + '\n'.join('export type %s = %s;' % (name(k), ts(v)) for k, v in D.items()) + '\n')


if __name__ == '__main__': main()
