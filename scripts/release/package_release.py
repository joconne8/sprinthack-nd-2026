"""Package the offline presentation and retain inspectable file hashes."""
import hashlib
import json
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--showcase', action='store_true', help='Include the runnable application and its sample data')
    args = parser.parse_args()
    files = [p for p in (ROOT/'presentation').rglob('*') if p.is_file() and p.name != 'MANIFEST.json']
    files += [ROOT/'DEMO.md'] + [p for p in (ROOT/'planning/pitch').rglob('*') if p.is_file()]
    if args.showcase:
        roots = ['apps', 'services', 'contracts', 'db', 'acquisition', 'goodwill_app',
                 'data ingestion', 'goodwill/showcase-data', 'goodwill/synthetic-data',
                 'scripts', 'tests', 'tools/verification', 'reports/SHOWCASE']
        for name in roots:
            files.extend(p for p in (ROOT/name).rglob('*') if p.is_file()
                         and not any(part in {'node_modules', '__pycache__', '.runtime', '.venv', '.DS_Store'} for part in p.relative_to(ROOT).parts)
                         and p.suffix not in {'.pyc', '.pyo'})
        files += [ROOT/'README.md', ROOT/'requirements-showcase.txt']
    files = sorted(set(p for p in files if p.name != 'PACKAGE-MANIFEST.json'))
    manifest = {str(p.relative_to(ROOT)): {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
    manifest_path = ROOT/('presentation/aimsigh/PACKAGE-MANIFEST.json' if args.showcase else 'presentation/MANIFEST.json')
    manifest_path.write_text(json.dumps({'files':manifest,'synthetic':True,'human_accepted':False,'runnable_application':args.showcase},indent=2)+'\n')
    output=ROOT/'.runtime'/('aimsigh-submission.zip' if args.showcase else 'goodwill-submission.zip');output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files+[manifest_path]:archive.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert all(hashlib.sha256(archive.read(p)).hexdigest()==item['sha256'] for p,item in manifest.items())
    print(json.dumps({'path':str(output),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'zip_roundtrip_verified':True},indent=2))


if __name__=='__main__':main()
