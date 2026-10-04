"""Strict additive showcase API and fixed loopback portal transport."""
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from services.data.contracts import DataError, validate
from .validation import envelope, keys
from .runs import Runs
from .service import ROOT

BASE = '/api/showcase/v1'
PREFIX = '/showcase/portal'
PORTAL_PATHS = ('/', '/upright', '/upright/reports', '/upright/reports/paid-orders', '/upright/reports/paid-order-items',
                '/cash-monkey', '/cash-monkey/reports', '/cash-monkey/reports/orders', '/static/app.js', '/static/style.css', '/api/reports')


def dispatch(service, method, path, query, body=None):
    route = path.removeprefix(BASE)
    if method == 'POST':
        request_shape = {'/questions': 'question_request', '/recordings': 'recording_request', '/runs': 'run_request'}.get(route)
        if re.fullmatch(r'/recordings/[a-f0-9]{32}/events', route): request_shape = 'event_request'
        elif re.fullmatch(r'/recordings/[a-f0-9]{32}/(review|approve)', route): request_shape = 'empty_request'
        if request_shape: validate('schema.json', body, ROOT / 'contracts/showcase-v1', request_shape)
    status, result, mime = _dispatch(service, method, path, query, body)
    if isinstance(result, bytes): return status, result, mime
    shape = {'/snapshot': 'snapshot', '/metrics': 'metrics', '/comparison': 'comparison', '/evidence': 'evidence', '/inputs': 'inputs',
             '/summary': 'question', '/questions': 'question', '/sources': 'sources', '/recipes': 'recipes',
             '/recordings': 'recording', '/exports/dictionary': 'dictionary', '/runs': 'runs' if method == 'GET' else 'run'}.get(route)
    if re.fullmatch(r'/runs/[a-f0-9]{32}/events', route): shape = 'events'
    elif re.fullmatch(r'/runs/[a-f0-9]{32}', route): shape = 'run'
    elif re.fullmatch(r'/recordings/[a-f0-9]{32}(/events|/review)?', route): shape = 'recording'
    elif re.fullmatch(r'/recordings/[a-f0-9]{32}/approve', route): shape = 'recipe'
    if shape: validate('schema.json', result, ROOT / 'contracts/showcase-v1', shape)
    return status, result, mime


def _dispatch(service, method, path, query, body=None):
    route = path.removeprefix(BASE)
    with service.lock:
        if service.runner is None:
            service.runner = Runs(service)
    service.recipes()
    mime = 'application/json; charset=utf-8'
    if method == 'GET':
        if route == '/snapshot':
            keys(query, ('snapshot_id',))
            result = service.snapshot(query.get('snapshot_id'))
        elif route == '/metrics': result = service.metrics(query)
        elif route == '/comparison': result = service.comparison(query)
        elif route == '/evidence': result = service.evidence(query)
        elif route == '/inputs': result = service.inputs(query)
        elif route == '/summary': result = service.summary(query)
        elif route == '/sources':
            keys(query, ())
            result = service.sources()
        elif route == '/recipes':
            keys(query, ())
            result = service.recipes()
        elif route == '/runs':
            keys(query, ())
            result = service.runner.history()
        elif route in ('/exports/workbook', '/exports/sales.csv', '/exports/dictionary'):
            keys(query, ('snapshot_id',), ('snapshot_id',))
            if route == '/exports/workbook':
                result, mime = service.workbook(query['snapshot_id']), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif route == '/exports/sales.csv':
                result, mime = service.sales_csv(query['snapshot_id']), 'text/csv; charset=utf-8'
            else: result = service.dictionary(query['snapshot_id'])
        else:
            keys(query, ())
            match = re.fullmatch(r'/runs/([a-f0-9]{32})(/events|/frames/(attempt-[12]-frame-[0-9]{3}\.png))?', route)
            recording = re.fullmatch(r'/recordings/([a-f0-9]{32})', route)
            if match:
                if match[3]: result, mime = service.runner.frame(match[1], match[3]), 'image/png'
                elif match[2]: result = service.runner.events(match[1])
                else: result = service.runner.get(match[1])
            elif recording: result = service.recorder.get(recording[1])
            else: raise DataError('not_found', 'Unknown showcase route')
        return 200, result, mime
    keys(query, ())
    if route == '/questions': return 200, service.question(body), mime
    if route == '/recordings': return 201, service.recorder.start(body), mime
    if route == '/runs': return 202, service.runner.start(body), mime
    match = re.fullmatch(r'/recordings/([a-f0-9]{32})/(events|review|approve)', route)
    if match:
        operation = {'events': service.recorder.event, 'review': service.recorder.review, 'approve': service.recorder.approve}[match[2]]
        return 200, operation(match[1], body), mime
    raise DataError('not_found', 'Unknown showcase write route')


def proxy(service, method, path, body=None):
    if not service.acquisition:
        raise DataError('portal_unavailable', 'Start the local demo server with its synthetic portal')
    relative = urlparse(path).path.removeprefix(PREFIX) or '/'
    if relative not in PORTAL_PATHS and not re.fullmatch(r'/api/reports/[a-f0-9]{32}(/download|/manifest)?', relative):
        raise DataError('path_denied', 'Only the implemented local synthetic portal routes are available')
    if method == 'POST' and relative != '/api/reports':
        raise DataError('path_denied', 'Only report generation is allowed through the portal')
    target = service.acquisition.portal_url.rstrip('/') + relative
    request = Request(target, data=json.dumps(body).encode() if body is not None else None,
                      headers={'Content-Type': 'application/json'}, method=method)
    try:
        response = urlopen(request, timeout=20)
    except HTTPError as error:
        response = error
    except URLError:
        raise DataError('portal_unavailable', 'The configured local replica is not responding')
    with response:
        content = response.read()
        status = response.status
        mime = response.headers.get('Content-Type', 'application/octet-stream')
    if 'text/html' in mime:
        html = content.decode().replace('"/static/', '"' + PREFIX + '/static/')
        app_tag = '<script src="' + PREFIX + '/static/app.js" defer></script>'
        # Install delegated capture before the app makes clickable controls visible.
        # Otherwise a quick click can navigate before the recorder listener exists.
        html = html.replace(app_tag, '<script src="/showcase/assets/portal-recorder.js" defer></script>' + app_tag)
        content = html.encode()
    elif relative == '/static/app.js':
        script = content.decode()
        script = "const portalPrefix='/showcase/portal';\nconst portalUrl=value=>value.startsWith('/')&&!value.startsWith(portalPrefix)?portalPrefix+value:value;\n" + script
        script = script.replace("location.pathname.replace(/\\/$/, '')", "location.pathname.slice(portalPrefix.length).replace(/\\/$/, '')")
        script = script.replace('const response = await fetch(url, options);', 'const response = await fetch(portalUrl(url), options);')
        content = script.encode()
    elif 'application/json' in mime:
        def rewrite(value):
            if isinstance(value, dict):
                return {k: PREFIX + v if k in ('download_url', 'manifest_url') and isinstance(v, str) and v.startswith('/api/reports/') else rewrite(v) for k, v in value.items()}
            if isinstance(value, list): return [rewrite(v) for v in value]
            return value
        content = json.dumps(rewrite(json.loads(content))).encode()
    return status, content, mime
