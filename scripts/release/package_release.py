"""Package the offline presentation and retain inspectable file hashes."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    files = [p for p in (ROOT/'presentation').rglob('*') if p.is_file() and p.name != 'MANIFEST.json']
    files += [ROOT/'DEMO.md'] + [p for p in (ROOT/'planning/pitch').rglob('*') if p.is_file()]
    manifest = {str(p.relative_to(ROOT)): {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
    (ROOT/'presentation/MANIFEST.json').write_text(json.dumps({'files':manifest,'synthetic':True,'human_accepted':False},indent=2)+'\n')
    output=ROOT/'.runtime/goodwill-submission.zip';output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files+[ROOT/'presentation/MANIFEST.json']:archive.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert all(hashlib.sha256(archive.read(p)).hexdigest()==item['sha256'] for p,item in manifest.items())
    print(json.dumps({'path':str(output),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'zip_roundtrip_verified':True},indent=2))


if __name__=='__main__':main()
