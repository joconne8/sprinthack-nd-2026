"""Use an isolated real app state to capture or record the complete showcase."""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--node',required=True);parser.add_argument('--node-modules',required=True);parser.add_argument('--chrome-path');parser.add_argument('--record',action='store_true');parser.add_argument('--ffmpeg');parser.add_argument('--ffprobe');args=parser.parse_args()
    if args.record and not(args.ffmpeg and args.ffprobe):parser.error('--record requires --ffmpeg and --ffprobe')
    from tests.acceptance.qa_support import portal_server, serving
    from services.data.importer import Pipeline
    from acquisition.controller import AcquisitionManager
    from apps.api.server import make_server
    with tempfile.TemporaryDirectory(prefix='aimsigh-real-rehearsal-') as temporary:
        with serving(portal_server()) as portal:
            manager=AcquisitionManager(Pipeline(temporary),portal,args.node,args.node_modules,args.chrome_path)
            server=make_server(manager.pipeline,0,manager)
            try:
                server.showcase.prepare()
                with serving(server) as api:
                    env=dict(os.environ,NODE_PATH=args.node_modules,BASE_URL=api,PYTHON=sys.executable)
                    if args.chrome_path:env['CHROME_PATH']=args.chrome_path
                    if args.record:
                        command=[sys.executable,str(ROOT/'scripts/release/showcase_record.py'),'--base-url',api,'--node',args.node,'--node-modules',args.node_modules,'--ffmpeg',args.ffmpeg,'--ffprobe',args.ffprobe]
                        if args.chrome_path:command+=['--chrome-path',args.chrome_path]
                    else:command=[args.node,str(ROOT/'scripts/release/showcase_capture.cjs')]
                    subprocess.run(command,cwd=ROOT,env=env,check=True,timeout=900)
            finally:
                if server.showcase.runner:server.showcase.runner.close()
                manager.close()


if __name__=='__main__':main()
