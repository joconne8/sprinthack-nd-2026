"""Record fresh combined-lane regression evidence, without self-acceptance."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node', default='node')
    parser.add_argument('--node-modules', default=str(ROOT / 'tools/verification/node_modules'))
    parser.add_argument('--chrome-path')
    args = parser.parse_args()
    output = ROOT / 'reports/integration/completion-logs'
    output.mkdir(parents=True, exist_ok=True)
    commands = []
    started_session = time.perf_counter()

    def run(command, name, cwd=ROOT, env=None):
        started = time.perf_counter()
        process = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
        (output / name).write_text(process.stdout + process.stderr)
        commands.append({'command': command, 'cwd': str(cwd), 'exit_code': process.returncode,
                         'elapsed_seconds': round(time.perf_counter() - started, 6),
                         'log': 'completion-logs/' + name})
        print(name, 'PASS' if process.returncode == 0 else 'FAIL', flush=True)
        if process.returncode:
            print(process.stdout + process.stderr, flush=True)
        return process

    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    before = {p.name: p.read_bytes() for p in (ROOT / 'contracts/v1').glob('*.schema.json')}
    before['types.ts'] = (ROOT / 'contracts/v1/types.ts').read_bytes()
    run([sys.executable, 'contracts/build_schemas.py'], 'schema-client-generation.log')
    after = {p.name: p.read_bytes() for p in (ROOT / 'contracts/v1').glob('*.schema.json')}
    after['types.ts'] = (ROOT / 'contracts/v1/types.ts').read_bytes()
    same = before == after
    run([sys.executable, '-m', 'compileall', '-q', 'apps', 'services', 'goodwill_app', 'contracts', 'scripts', 'tests'], 'python-syntax.log')
    run([sys.executable, 'scripts/check_completion_artifacts.py'], 'task-artifacts.json')
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'foundation-tests.log')
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'acquisition/tests', '-p', 'test_*.py', '-v'], 'acquisition-tests.log')
    run([sys.executable, 'reports/DAT-01/review_fixtures.py'], 'fixture-review.json')
    run([sys.executable, 'scripts/benchmark_data.py'], 'benchmark.json')
    with tempfile.TemporaryDirectory(prefix='goodwill-completion-fixtures-') as temporary:
        archive = subprocess.check_output(['git', 'archive', commit, 'goodwill/synthetic-data'], cwd=ROOT)
        subprocess.run(['tar', '-xf', '-', '-C', temporary], input=archive, check=True)
        run([sys.executable, '-m', 'unittest', 'discover', '-s', 'goodwill/synthetic-data', '-p', 'test_*.py', '-v'], 'fixture-suite.log', Path(temporary))
    with tempfile.TemporaryDirectory(prefix='goodwill-completion-cli-') as temporary:
        command = [sys.executable, '-m', 'goodwill_app', '--state-root', temporary]
        run(command + ['init'], 'cli-init.json')
        run(command + ['import', '--csv', 'data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv',
                       '--manifest', 'data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.manifest.json'], 'cli-import.json')
        process = run(command + ['metrics', '--start-date', '2026-09-30', '--end-date', '2026-09-30', '--source', 'upright_replica'], 'cli-metrics.json')
        cli_expected = process.returncode == 0 and json.loads(process.stdout)['metrics'][0]['value'] == '7127.78'
    run([args.node, '--version'], 'node-version.log')
    compiler = str(Path(args.node_modules) / 'typescript/bin/tsc')
    run([args.node, compiler, '--version'], 'typescript-version.log')
    run([args.node, '-e', "console.log(require(process.argv[1]).version)", str(Path(args.node_modules) / 'playwright/package.json')], 'playwright-version.log')
    with tempfile.TemporaryDirectory(prefix='goodwill-completion-client-') as temporary:
        run([args.node, compiler, '--strict', '--target', 'ES2020', '--module', 'commonjs', '--lib', 'ES2020,DOM',
             '--outDir', temporary, 'contracts/v1/client.ts'], 'client-build.log')
        run([args.node, 'tests/client.test.cjs', temporary], 'client-tests.log')
    browser = [sys.executable, 'scripts/verify_browser_handoff.py', '--node', args.node, '--node-modules', args.node_modules]
    if args.chrome_path:
        browser += ['--chrome-path', args.chrome_path]
    run(browser, 'browser-handoff.log')
    run(['git', 'diff', '--check'], 'diff-check.log')
    run(['git', 'diff', '--exit-code', commit, '--', 'goodwill/synthetic-data', 'acquisition', 'data ingestion'], 'other-lanes-unchanged.log')
    hashes = {}
    for directory in ('apps/api', 'services', 'goodwill_app', 'db', 'contracts', 'scripts', 'tests', 'tools/verification'):
        for path in sorted((ROOT / directory).rglob('*')):
            if path.is_file() and not {'__pycache__', 'node_modules'} & set(path.parts) and path.suffix != '.pyc':
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {'state': 'READY_FOR_REVIEW', 'accepted': False, 'independent_acceptance': False,
              'base_commit': commit, 'tested_state': 'working tree; exact implementation hashes below',
              'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
              'python': sys.version, 'commands': commands, 'schema_and_client_regeneration_identical': same,
              'cli_expected_result_matches': cli_expected, 'elapsed_seconds': round(time.perf_counter()-started_session, 6),
              'implementation_file_sha256': hashes,
              'not_run': ['Landon product UI acceptance', 'Independent ENG-04 review', 'Remote GitHub CI', 'Live Goodwill/provider/Microsoft integrations'],
              'eng05_remaining': ['APP-01/02/03 integrated UI', 'ENG-04 independent evidence', 'human acceptance/freeze on reviewed commit'],
              'spend': 'No paid service or model calls; token totals are not exposed',
              'authorization': 'User requested completion of Peyton and delegated Jack OC lanes; no human acceptance invented'}
    result['passed'] = same and cli_expected and all(command['exit_code'] == 0 for command in commands)
    (output.parent / 'completion-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
