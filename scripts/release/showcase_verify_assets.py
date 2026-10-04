"""Verify the final presentation bundle against its actual capture evidence."""
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'presentation/aimsigh'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--ffprobe',required=True);args=parser.parse_args()
    build=json.loads((OUT/'build.json').read_text());capture=json.loads((OUT/'capture-verification.json').read_text());slides=json.loads((OUT/'slides-verification.json').read_text())
    assert build['draft'] is False and not build['missing_captures']
    assert capture['passed'] is True and slides['passed'] is True and slides['slide_count']==15
    assert build['duration_seconds']==900
    assert capture['results']['unsupported']['intent']=='unsupported'
    assert all(source['coverage']['state']=='complete' for source in capture['results']['snapshot']['sources'])
    for file,digest in capture['capture_sha256'].items():assert hashlib.sha256((OUT/file).read_bytes()).hexdigest()==digest,file
    with zipfile.ZipFile(OUT/'aimsigh-showcase.pptx') as archive:
        assert archive.testzip() is None
        slide_files=[name for name in archive.namelist() if name.startswith('ppt/slides/slide') and name.endswith('.xml') and '/_rels/' not in name]
        note_files=[name for name in archive.namelist() if name.startswith('ppt/notesSlides/notesSlide') and name.endswith('.xml') and '/_rels/' not in name]
        assert len(slide_files)==len(note_files)==15
        namespace={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
        native_text=sum(len(ET.fromstring(archive.read(name)).findall('.//a:t',namespace)) for name in slide_files)
        assert native_text>100,'Narrative should remain editable native text'
        notes=' '.join(t.text or '' for name in note_files for t in ET.fromstring(archive.read(name)).findall('.//a:t',namespace))
        assert 'nonbinding' in notes and ('model-free' in notes or 'no external model' in notes) and 'https://docs.google.com/' in notes
    video=json.loads(subprocess.check_output([args.ffprobe,'-v','error','-show_format','-show_streams','-of','json',str(OUT/'walkthrough.mp4')],text=True))
    assert 220<=float(video['format']['duration'])<=360
    assert any(s['codec_type']=='video' and s['codec_name']=='h264' for s in video['streams'])
    assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in video['streams'])
    with zipfile.ZipFile(OUT/'exports/september2026.xlsx') as archive:assert archive.testzip() is None
    assert (OUT/'aimsigh-showcase.pdf').read_bytes().startswith(b'%PDF-')
    asset_files=[OUT/'index.html',OUT/'aimsigh-showcase.pdf',OUT/'aimsigh-showcase.pptx',OUT/'walkthrough.mp4',OUT/'exports/september2026.xlsx']
    result={'passed':True,'snapshot_id':capture['snapshot_id'],'slide_count':15,'main_presentation_seconds':900,'narrated_video_seconds':float(video['format']['duration']),'editable_native_text_runs':native_text,'local_only':True,'synthetic':True,'human_accepted':False,'files':{str(p.relative_to(ROOT)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in asset_files}}
    (OUT/'asset-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
