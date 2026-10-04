"""Record bounded release checks, including a clean exported checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--node', default='node')
    p.add_argument('--node-modules', default=str(ROOT/'tools/verification/node_modules'))
    p.add_argument('--chrome-path')
    args = p.parse_args()
    output = ROOT/'reports/release'; logs=output/'logs';logs.mkdir(parents=True,exist_ok=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GOODWILL_NODE=args.node,GOODWILL_NODE_MODULES=args.node_modules,
             GOODWILL_QA_OUTPUT=str(output/'browser'))
    if args.chrome_path:env['CHROME_PATH']=args.chrome_path
    commands=[]
    def run(command,name,cwd=ROOT,environment=env):
        start=time.monotonic()
        try:
            result=subprocess.run(command,cwd=cwd,env=environment,capture_output=True,text=True,timeout=90)
            code=result.returncode; stdout=result.stdout; message=stdout+result.stderr
        except subprocess.TimeoutExpired as e:
            code=124;stdout='';message='TIMEOUT after 90 seconds\n'+str(e.stdout or '')+str(e.stderr or '')
        (logs/name).write_text(message)
        commands.append({'command':command,'cwd':str(cwd),'exit_code':code,'elapsed_seconds':round(time.monotonic()-start,3),'log':'logs/'+name})
        print(name,'PASS' if code==0 else 'FAIL',flush=True)
        return code,stdout
    schema=lambda:{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in list((ROOT/'contracts/v1').glob('*.schema.json'))+[ROOT/'contracts/v1/types.ts']}
    before=schema()
    run([sys.executable,'contracts/build_schemas.py'],'schemas.log');identical=before==schema()
    run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'all-tests.log')
    run([sys.executable,'-m','unittest','discover','-s','acquisition/tests','-p','test_*.py','-v'],'acquisition.log')
    run([sys.executable,'reports/DAT-01/review_fixtures.py'],'fixture-review.json')
    run([sys.executable,'scripts/check_completion_artifacts.py'],'task-artifacts.json')
    with tempfile.TemporaryDirectory(prefix='goodwill-release-clean-') as temporary:
        archive=subprocess.check_output(['git','archive',commit],cwd=ROOT)
        subprocess.run(['tar','-xf','-','-C',temporary],input=archive,check=True)
        clean_env=dict(env,GOODWILL_QA_OUTPUT=str(output/'clean-browser'))
        run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'clean-checkout-tests.log',Path(temporary),clean_env)
        run([sys.executable,'-m','unittest','discover','-s','goodwill/synthetic-data','-p','test_*.py','-v'],'fixture-regeneration.log',Path(temporary))
    with tempfile.TemporaryDirectory(prefix='goodwill-release-cli-') as temporary:
        cli=[sys.executable,'-m','goodwill_app','--state-root',temporary]
        run(cli+['init'],'cli-init.json')
        run(cli+['import','--csv','data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv',
                 '--manifest','data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.manifest.json'],'cli-import.json')
        code,stdout=run(cli+['metrics','--start-date','2026-09-30','--end-date','2026-09-30','--source','upright_replica'],'cli-metrics.json')
        cli_matches=code==0 and json.loads(stdout)['metrics'][0]['value']=='7127.78'
    with tempfile.TemporaryDirectory(prefix='goodwill-release-client-') as temporary:
        run([args.node,str(Path(args.node_modules)/'typescript/bin/tsc'),'--strict','--target','ES2020','--module','commonjs','--lib','ES2020,DOM','--outDir',temporary,'contracts/v1/client.ts'],'client-build.log')
        run([args.node,'tests/client.test.cjs',temporary],'client-tests.log')
    browser=[sys.executable,'scripts/verify_dashboard.py','--node',args.node,'--node-modules',args.node_modules]
    if args.chrome_path:browser+=['--chrome-path',args.chrome_path]
    run(browser+['--acquisition-only'],'acquisition-browser.log')
    run(['git','diff','--check'],'diff-check.log')
    run(['git','diff','--exit-code','127bd7f17d532c008a3d1de6bf25a9a5ed26d915','--','goodwill/synthetic-data','fixtures/expected-results','acquisition','apps','services','contracts','data ingestion'],'implementation-and-ledger-unchanged.log')
    hashes={}
    for folder in ['apps','services','acquisition','goodwill_app','contracts','tests','scripts/release']:
        for f in sorted((ROOT/folder).rglob('*')):
            if f.is_file() and not {'__pycache__','node_modules'}&set(f.parts):hashes[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
    result={'state':'READY_FOR_REVIEW','accepted':False,'tested_commit':commit,'tested_state':'working tree hashes plus clean Git archive of tested_commit',
            'python':sys.version,'commands':commands,'schema_regeneration_identical':identical,'cli_expected_result_matches':cli_matches,
            'implementation_file_sha256':hashes,'passed':identical and cli_matches and all(c['exit_code']==0 for c in commands),
            'expected_basis':'Original handwritten ENG-04 ledger and separate QA Decimal raw-CSV sums; new browser checks authored under Peyton final-release takeover.',
            'limits':['No independent human acceptance','No second physical device tested','Synthetic local replica only','P1 metric exports deferred'],
            'deadline':'2026-10-05T10:00:00-04:00','spend':'Local checks; no paid/model calls'}
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
