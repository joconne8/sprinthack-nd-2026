"""Actual browser acceptance using Jack mc's independently authored QA ledger."""
import hashlib
import io
import csv
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from tests.acceptance.qa_support import ROOT, SCENARIOS, artifact, scenario_file, raw_net_by_day, portal_server, serving


def run_dashboard_acceptance():
    from acquisition.controller import AcquisitionManager
    from apps.api.server import make_server
    from services.data.importer import Pipeline

    node = os.environ.get('GOODWILL_NODE') or shutil.which('node')
    if not node:
        raise AssertionError('Browser acceptance requires Node >=20; follow DEMO.md. It is never silently skipped.')
    modules = os.environ.get('GOODWILL_NODE_MODULES', str(ROOT / 'tools/verification/node_modules'))
    output_setting = os.environ.get('GOODWILL_QA_OUTPUT')
    with tempfile.TemporaryDirectory(prefix='goodwill-dashboard-acceptance-') as temporary:
        temp = Path(temporary)
        output = Path(output_setting).resolve() if output_setting else temp / 'browser'
        output.mkdir(parents=True, exist_ok=True)
        inputs = {}
        for name in ['initial', 'overlap', 'correction']:
            data, manifest = scenario_file('core_ledger', name)
            inputs[name] = (data, manifest)
        # Nonfinancial source text is untrusted; the ledger arithmetic is unchanged.
        data, manifest = inputs['initial']
        rows = list(csv.DictReader(io.StringIO(data.decode())))
        rows[0]['item_title'] = '<img src=x onerror="window.__qaInjection=true">'
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\r\n')
        writer.writeheader(); writer.writerows(rows)
        data = stream.getvalue().encode()
        manifest['file_checksum'] = hashlib.sha256(data).hexdigest()
        inputs['initial'] = data, manifest
        inputs['keys'] = artifact(SCENARIOS['buyer_store_keys']['files']['keys'], start='2026-10-03')
        inputs['invalid'] = scenario_file('invalid_rows', 'three_decimals')
        for name, (data, manifest) in inputs.items():
            (temp / (name + '.csv')).write_bytes(data)
            (temp / (name + '.json')).write_text(json.dumps(manifest))
        (temp / 'expected.json').write_text(json.dumps(SCENARIOS))
        with serving(portal_server()) as portal:
            manager = AcquisitionManager(Pipeline(temp / 'state'), portal, node, modules, os.environ.get('CHROME_PATH'))
            try:
                with serving(make_server(manager.pipeline, 0, manager)) as api:
                    env = dict(os.environ, BASE_URL=api, QA_INPUT=str(temp), QA_OUTPUT=str(output), NODE_PATH=modules)
                    process = subprocess.run([node, str(ROOT / 'tests/acceptance/dashboard_browser.cjs')],
                                             cwd=ROOT, env=env, capture_output=True, text=True, timeout=85)
                    (output / 'browser.log').write_text(process.stdout + process.stderr)
                    if process.returncode:
                        raise AssertionError('Browser acceptance failed:\n' + process.stdout + process.stderr)
            finally:
                manager.close()
        observed = json.loads((output / 'observed.json').read_text())
        # Genuine browser-acquired values are checked by QA's independent raw CSV reader,
        # never by asking the metric implementation to produce the expected result.
        for item in observed['acquired']:
            data = (output / item['raw_file']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == item['checksum']
            totals = raw_net_by_day(data)
            from decimal import Decimal
            expected = format(sum((Decimal(value) for value in totals.values()), Decimal('0')), '.2f')
            assert item['displayed_value'] == expected, (item, expected)
            item['qa_raw_expected'] = expected
        observed.update(passed=True, expectation_basis='Jack mc handwritten ledger plus independent QA raw CSV reader',
                        human_accepted=False, second_physical_device_verified=False)
        (output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
        return observed
