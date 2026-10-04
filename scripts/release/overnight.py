"""Bounded local verification of a frozen checkout; never edits or merges code."""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def parse_deadline(value):
    deadline = datetime.fromisoformat(value)
    if deadline.tzinfo is None:
        raise ValueError('Deadline must include an explicit timezone offset')
    return deadline.astimezone(timezone.utc)


def source_hashes(source):
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=source).decode().split('\0')
    return {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in paths if name and (source / name).is_file()}


def run_bounded(command, source, log, env, timeout, stop_file):
    if stop_file.exists(): return {'exit_code': 130, 'cause': 'cancelled'}
    if timeout <= 0: return {'exit_code': 124, 'cause': 'deadline'}
    started = time.monotonic()
    with log.open('w') as output:
        child = subprocess.Popen(command, cwd=source, env=env, stdin=subprocess.DEVNULL,
                                 stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
        while child.poll() is None:
            cause = 'cancelled' if stop_file.exists() else 'timeout' if time.monotonic()-started >= timeout else None
            if cause:
                os.killpg(child.pid, signal.SIGTERM)
                try: child.wait(timeout=5)
                except subprocess.TimeoutExpired: pass
                try: os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                child.wait()
                return {'exit_code': 130 if cause == 'cancelled' else 124, 'cause': cause}
            time.sleep(0.25)
    return {'exit_code': child.returncode, 'elapsed_seconds': round(time.monotonic()-started, 3)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    p.add_argument('--node', required=True); p.add_argument('--node-modules', required=True); p.add_argument('--chrome-path')
    p.add_argument('--until', required=True); p.add_argument('--interval-seconds', type=int, default=3600)
    p.add_argument('--max-cycles', type=int, default=36); p.add_argument('--dry-run', action='store_true')
    p.add_argument('--showcase', action='store_true', help='Include the real Aimsigh browser/Excel/conversation acceptance')
    p.add_argument('--command-timeout-seconds', type=int, default=90)
    args = p.parse_args(); deadline = parse_deadline(args.until)
    if not 60 <= args.interval_seconds <= 7200 or not 1 <= args.max_cycles <= 36:
        p.error('Use a 60–7200 second interval and 1–36 cycles')
    if not 10 <= args.command_timeout_seconds <= 300:
        p.error('Command timeout must be 10–300 seconds')
    if deadline <= datetime.now(timezone.utc): p.error('Deadline must be in the future')
    source = args.source.resolve(); output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=source): p.error('Frozen source checkout must be clean')
    original = source_hashes(source)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    status = {'pid': os.getpid(), 'source': str(source), 'commit': commit, 'deadline_utc': deadline.isoformat(),
              'interval_seconds': args.interval_seconds, 'max_cycles': args.max_cycles, 'state': 'planned',
              'cycles': [], 'spend': 'No model/paid-service calls; local tests only', 'changes_code': False}
    stop_file = output / 'STOP'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GOODWILL_NODE=args.node, GOODWILL_NODE_MODULES=args.node_modules)
    env['PATH'] = str(Path(args.node).resolve().parent) + os.pathsep + env.get('PATH', '')
    env['NODE_PATH'] = args.node_modules
    if args.chrome_path: env['CHROME_PATH'] = args.chrome_path
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'acquisition/tests', '-p', 'test_*.py', '-v'],
        [sys.executable, 'scripts/check_completion_artifacts.py'],
    ]

    def save():
        status['updated_at_utc'] = datetime.now(timezone.utc).isoformat()
        temporary = output / 'status.tmp'; temporary.write_text(json.dumps(status, indent=2)+'\n'); temporary.replace(output / 'status.json')

    def cancel(signum, frame): stop_file.touch()
    signal.signal(signal.SIGTERM, cancel); signal.signal(signal.SIGINT, cancel)
    if args.dry_run:
        status.update(state='dry_run', commands=commands); save(); print(json.dumps(status, indent=2)); return 0
    failures = 0
    for number in range(1, args.max_cycles+1):
        if stop_file.exists(): status['state']='cancelled'; break
        if (deadline-datetime.now(timezone.utc)).total_seconds()<20: status['state']='deadline_reached'; break
        if source_hashes(source) != original: status['state']='stopped_source_changed'; break
        status['state']='running'; folder=output/f'cycle-{number:02d}';folder.mkdir(exist_ok=True)
        cycle={'number':number,'started_at_utc':datetime.now(timezone.utc).isoformat(),'commands':[]};status['cycles'].append(cycle);save()
        cycle_env=dict(env,GOODWILL_QA_OUTPUT=str(folder/'browser'))
        cycle_commands = list(commands)
        if args.showcase:
            acceptance = [sys.executable, 'scripts/verify_showcase.py', '--node', args.node,
                          '--node-modules', args.node_modules, '--output', str(folder/'showcase')]
            if args.chrome_path: acceptance += ['--chrome-path', args.chrome_path]
            cycle_commands.append(acceptance)
        for index, command in enumerate(cycle_commands):
            remaining=(deadline-datetime.now(timezone.utc)).total_seconds()
            result=run_bounded(command,source,folder/f'{index+1}.log',cycle_env,min(args.command_timeout_seconds,max(0,remaining)),stop_file)
            cycle['commands'].append({'command':command,**result});save()
            if result['exit_code'] != 0: break
        cycle['passed']=len(cycle['commands'])==len(cycle_commands) and all(c['exit_code']==0 for c in cycle['commands'])
        cycle['finished_at_utc']=datetime.now(timezone.utc).isoformat()
        failures=0 if cycle['passed'] else failures+1
        if stop_file.exists(): status['state']='cancelled';save();break
        if failures >= 2:status['state']='stopped_two_failures';save();break
        status['state']='waiting';save()
        next_run=time.monotonic()+args.interval_seconds
        while time.monotonic()<next_run and datetime.now(timezone.utc)<deadline and not stop_file.exists(): time.sleep(min(1,max(0,next_run-time.monotonic())))
    else: status['state']='cycle_limit_reached'
    if status['state']=='waiting':status['state']='cancelled' if stop_file.exists() else 'deadline_reached'
    save(); return 1 if status['state'].startswith('stopped') else 0


if __name__ == '__main__': raise SystemExit(main())
