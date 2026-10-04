"""Small strict request boundaries, independent of unchanged goodwill-v1."""
from services.data.contracts import DataError, day

SOURCES = ('upright_replica', 'cash_monkey_replica')
VERSION = 'showcase-v1'


def envelope(**data):
    return dict(contract_version=VERSION, synthetic=True, **data)


def keys(value, allowed, required=()):
    if not isinstance(value, dict) or set(value) - set(allowed) or set(required) - set(value):
        raise DataError('request_invalid', 'Expected documented keys: ' + ', '.join(allowed))
    return value


def scope(query):
    keys(query, ('snapshot_id', 'start_date', 'end_date', 'source', 'store', 'platform', 'offset', 'limit'))
    result = {k: query.get(k) or default for k, default in
              [('start_date', '2026-09-01'), ('end_date', '2026-09-30'),
               ('source', 'all'), ('store', None), ('platform', None)]}
    start, end = day(result['start_date']), day(result['end_date'])
    if start > end or start.isoformat() < '2026-09-01' or end.isoformat() > '2026-09-30':
        raise DataError('invalid_period', 'Showcase metrics cover ordered September 2026 dates')
    if result['source'] not in ('all',) + SOURCES:
        raise DataError('source_invalid', 'Only the two disjoint synthetic showcase feeds are combined')
    if result['store'] and result['store'] not in ['GW-%03d' % n for n in range(1, 25)]:
        raise DataError('store_invalid', 'Choose a known synthetic store')
    if result['platform'] and result['platform'] not in ('ShopGoodwill', 'eBay', 'GoodwillFinds', 'Amazon-MF', 'GoodwillBooks'):
        raise DataError('platform_invalid', 'Choose a known showcase platform')
    return result
