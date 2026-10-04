"""Run real UI/browser tests against isolated portal/controller/API state."""
import argparse
import importlib.util
import os
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from acquisition.controller import AcquisitionManager
from apps.api.server import make_server
from services.data.importer import Pipeline


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--node',default='node')
    parser.add_argument('--node-modules',default=str(ROOT/'tools/verification/node_modules'))
    parser.add_argument('--chrome-path')
    parser.add_argument('--output',default='reports/takeover/browser')
    parser.add_argument('--acquisition-only',action='store_true')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='goodwill-ui-') as temporary:
        pipeline=Pipeline(Path(temporary)/'state')
        spec=importlib.util.spec_from_file_location('ui_portal',ROOT/'data ingestion/server.py')
        portal=importlib.util.module_from_spec(spec);spec.loader.exec_module(portal)
        replica=ThreadingHTTPServer(('127.0.0.1',0),portal.Handler)
        manager=AcquisitionManager(pipeline,f'http://127.0.0.1:{replica.server_port}',args.node,args.node_modules,args.chrome_path)
        server=make_server(pipeline,0,manager)
        servers=[replica,server];threads=[]
        try:
            for item in servers:
                thread=threading.Thread(target=item.serve_forever,daemon=True);thread.start();threads.append(thread)
            env=dict(os.environ,BASE_URL=f'http://127.0.0.1:{server.server_port}',NODE_PATH=str(Path(args.node_modules).resolve()),
                     OUTPUT_DIR=str(Path(args.output).resolve()),QA_TEMP=temporary,REPLICA_URL=manager.portal_url)
            if args.chrome_path:env['CHROME_PATH']=args.chrome_path
            script='acquisition.test.cjs' if args.acquisition_only else 'dashboard.test.cjs'
            process=subprocess.run([args.node,str(ROOT/'tests/ui'/script)],cwd=ROOT,env=env,timeout=60)
            return process.returncode
        finally:
            manager.close()
            for item,thread in zip(servers,threads):item.shutdown();thread.join();item.server_close()


if __name__=='__main__':raise SystemExit(main())
