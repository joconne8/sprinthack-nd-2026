"""Record takeover evidence; known independent UI placeholder stays a failure."""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--node',default='node')
    parser.add_argument('--node-modules',default=str(ROOT/'tools/verification/node_modules'))
    parser.add_argument('--chrome-path')
    args=parser.parse_args()
    output=ROOT/'reports/takeover/logs';output.mkdir(parents=True,exist_ok=True)
    commands=[]

    def run(command,name):
        started=time.perf_counter()
        process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60)
        (output/name).write_text(process.stdout+process.stderr)
        commands.append({'command':command,'exit_code':process.returncode,'elapsed_seconds':round(time.perf_counter()-started,6),'log':'logs/'+name})
        print(name,'PASS' if process.returncode==0 else 'FAIL',flush=True)
        return process

    run([sys.executable,'-m','compileall','-q','apps','acquisition','services','goodwill_app','contracts','scripts','tests'],'python-syntax.log')
    run([sys.executable,'-m','unittest','tests.test_acquisition_controller','tests.test_pipeline','tests.test_adapters_and_backfill','tests.test_contract_boundaries','tests.test_contract_examples','tests.test_http_integration','tests.test_inventory','-v'],'developer-regression.log')
    run([sys.executable,'-m','unittest','discover','-s','acquisition/tests','-p','test_*.py','-v'],'acquisition-tests.log')
    full=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'all-tests.log')
    run([sys.executable,'reports/DAT-01/review_fixtures.py'],'fixture-review.json')
    run([args.node,str(Path(args.node_modules)/'typescript/bin/tsc'),'--strict','--noEmit','--target','ES2020','--module','commonjs','--lib','ES2020,DOM','contracts/v1/client.ts'],'client-types.log')
    before={path.name:path.read_bytes() for path in (ROOT/'contracts/v1').glob('*.schema.json')}
    before['types.ts']=(ROOT/'contracts/v1/types.ts').read_bytes()
    run([sys.executable,'contracts/build_schemas.py'],'schema-generation.log')
    after={path.name:path.read_bytes() for path in (ROOT/'contracts/v1').glob('*.schema.json')}
    after['types.ts']=(ROOT/'contracts/v1/types.ts').read_bytes()
    browser=[sys.executable,'scripts/verify_dashboard.py','--node',args.node,'--node-modules',args.node_modules]
    if args.chrome_path:browser+=['--chrome-path',args.chrome_path]
    run(browser+['--acquisition-only'],'browser-negatives.log')
    run(browser,'dashboard-browser.log')
    run(['git','diff','--check'],'diff-check.log')
    run(['git','diff','--exit-code','--','goodwill/synthetic-data','tests/acceptance','fixtures/expected-results','reports/ENG-04'],'qa-and-fixtures-unchanged.log')
    hashes={}
    for directory in ['acquisition','apps','goodwill_app','services','contracts','scripts','tests/ui']:
        for path in sorted((ROOT/directory).rglob('*')):
            if path.is_file() and not {'node_modules','__pycache__'}&set(path.parts) and path.suffix!='.pyc':
                hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    owned_pass=before==after and all(command['exit_code']==0 for command in commands if command['log']!='logs/all-tests.log')
    result={'state':'READY_FOR_REVIEW','accepted':False,'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
            'tested_state':'working tree with exact implementation hashes','commands':commands,'implementation_file_sha256':hashes,
            'schema_regeneration_identical':before==after,'owned_checks_passed':owned_pass,'full_suite_passed':full.returncode==0,
            'remaining':['Jack mc independent dashboard acceptance replaces the deliberate placeholder test','Human integration/review/freeze','Remote CI unverified'],
            'deferred':['P1 exports','Assistant/Jev/live connections and production schedules'],
            'authorization':'Peyton explicitly authorized takeover of Hugh/Landon; Jack mc QA lane preserved'}
    (output.parent/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if owned_pass else 1


if __name__=='__main__':raise SystemExit(main())
