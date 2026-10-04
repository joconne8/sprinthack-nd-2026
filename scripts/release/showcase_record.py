"""Record the verified Aimsigh application with an offline narrated MP4 track."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PHASES=[
    ('The reporting problem',30,'Real sample inputs produce the dashboard metrics.',
     'Goodwill needs a clearer daily picture of e commerce, but the reporting problem starts before the dashboard. Amanda retrieves recurring reports and hands them into an Excel and Power BI workflow. This is our working local showcase. The portal records are fictional, and labor and shipping costs are invented, explicitly labeled inputs. The numbers you will see come from those sample records through the real verified data pipeline.'),
    ('Teach the task once',35,'Actual DOM actions → operator-reviewed date-parameterized recipe.',
     'We start by teaching the repeated Upright report task. The recorder captures actual actions in this simulated portal. We navigate to paid orders, select September twenty ninth, choose the report settings, generate the report, and download its real CSV file. Then the operator reviews and approves the bounded recipe. The two dates become parameters. This is model free recording and replay, not a Jev call or a video pretending to control the browser.'),
    ('Replay and verify',35,'September 30 completes both fictional source feeds.',
     'Now the same reviewed recipe runs with September thirtieth. These are genuine frames from the automation browser. The downloaded file is verified, archived, reconciled, and imported before publication. We collect the Cash Monkey report too. Its unit rows keep their own grain and source identity. The two disjoint fictional feeds complete the September snapshot. Repeating a report does not double its sales, and a failed collection cannot replace the last good publication.'),
    ('Deliver the workbook',30,'Actual exported XLSX · 30 daily tabs · source-linked month.',
     'Amanda can keep a familiar output. This workbook is downloaded from the published snapshot. The preview reads its actual exported cell values. It contains thirty daily September tabs, a monthly summary, normalized sales, modeled labor and shipping inputs, reconciliation, and source evidence. The workbook and dashboard use the same calculations and publication identifiers. A normalized CSV and data dictionary provide a bridge to an approved Power BI model.'),
    ('Understand the daily picture',30,'Charts and metrics read the same pinned snapshot.',
     'The dashboard now shows the published September sales, daily trends, and source and store breakdowns. Net sales means item sales minus refunds; it excludes shipping collected, taxes, and fees. Labor productivity uses our disclosed source, store, and day allocations. Demo contribution margin subtracts source fees and modeled shipping and labor, and excludes overhead and taxes. The application keeps unsupported production margin, September sell through, and year over year growth unavailable.'),
    ('Inspect the comparison',35,'Sales increased; invented labor hours increased faster.',
     'Here is a question the supplied sample data can actually answer. September seventeenth through twenty third has sixty thousand seven hundred twenty seven dollars and fifty six cents in net sales, and four hundred twenty modeled labor hours. The following week has sixty one thousand seven hundred six dollars and sixty four cents, and five hundred eighty eight hours. Revenue per labor hour falls from one hundred forty four dollars and fifty nine cents to one hundred four dollars and ninety four cents. That is an arithmetic explanation in fictional data, not a verified business cause.'),
    ('Ask beside the dashboard',30,'Local Teams-style channel · deterministic read-only tools.',
     'We ask why revenue per labor hour is down. The local Teams style channel returns the same comparison, definitions, and snapshot as the dashboard. Its evidence links open the underlying sales records and modeled labor inputs. Supported answers use read only metric, comparison, and evidence tools with deterministic templates. There is no external language model. Actual Teams delivery and Copilot integration are later pilot work requiring Goodwill tenant and security approval.'),
    ('A controlled next step',15,'Unsupported questions stay unanswered; pilot approvals remain explicit.',
     'An unsupported request does not invent an answer or post an accounting journal. The next step is one supervised authorized source pilot, compatible Excel and Power BI delivery, and named support owners. Amanda’s letter expresses nonbinding interest. This working synthetic showcase demonstrates progress, not production access or measured savings.'),
]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',required=True);parser.add_argument('--node',required=True);parser.add_argument('--node-modules',required=True);parser.add_argument('--chrome-path');parser.add_argument('--ffmpeg',required=True);parser.add_argument('--ffprobe',required=True);parser.add_argument('--voice',default='Samantha');parser.add_argument('--output',default='presentation/aimsigh');args=parser.parse_args()
    output=(ROOT/args.output).resolve();output.mkdir(parents=True,exist_ok=True);recordings=output/'recording';recordings.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='aimsigh-narration-') as folder:
        temporary=Path(folder);phases=[]
        for index,(title,minimum,caption,narration) in enumerate(PHASES):
            audio=temporary/('%02d.aiff'%index);subprocess.run(['say','-v',args.voice,'-r','175','-o',str(audio),narration],check=True,timeout=60)
            metadata=json.loads(subprocess.check_output([args.ffprobe,'-v','error','-show_entries','format=duration','-of','json',str(audio)],text=True));duration=max(minimum,float(metadata['format']['duration'])+1)
            phases.append(dict(title=title,caption=caption,narration=narration,duration=duration))
        phasefile=temporary/'phases.json';phasefile.write_text(json.dumps(phases))
        env=dict(os.environ,BASE_URL=args.base_url,SHOWCASE_OUTPUT=str(output),DEMO_PHASES=str(phasefile),NODE_PATH=args.node_modules,PYTHON=sys.executable)
        if args.chrome_path:env['CHROME_PATH']=args.chrome_path
        subprocess.run([args.node,str(ROOT/'scripts/release/showcase_capture.cjs')],cwd=ROOT,env=env,check=True,timeout=600)
        capture=json.loads((output/'capture-verification.json').read_text());timeline=capture['timeline'];command=[args.ffmpeg,'-y','-i',str(recordings/'walkthrough-original.webm')]
        for index in range(len(phases)):command+=['-i',str(temporary/('%02d.aiff'%index))]
        filters=['[%d:a]adelay=%d:all=1[a%d]'%(index+1,round(scene['start']*1000),index) for index,scene in enumerate(timeline)]
        filters+=[''.join('[a%d]'%index for index in range(len(phases)))+'amix=inputs=%d:normalize=0,apad[audio]'%len(phases)]
        command+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[audio]','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(output/'walkthrough.mp4')]
        subprocess.run(command,check=True,timeout=300,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    metadata=json.loads(subprocess.check_output([args.ffprobe,'-v','error','-show_format','-show_streams','-of','json',str(output/'walkthrough.mp4')],text=True))
    assert any(s['codec_type']=='audio' for s in metadata['streams']) and any(s['codec_type']=='video' for s in metadata['streams'])
    duration=float(metadata['format']['duration']);assert 220<=duration<=360,'Recording should be approximately four minutes, not a silent or truncated export'
    (recordings/'video-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n');(recordings/'timeline.json').write_text(json.dumps(dict(passed=True,snapshot_id=capture['snapshot_id'],voice='offline macOS synthetic voice: '+args.voice,phases=timeline),indent=2)+'\n')
    (ROOT/'planning/pitch/aimsigh-narration.txt').write_text('\n\n'.join(text for _,_,_,text in PHASES)+'\n')
    for raw in recordings.glob('*.webm'):raw.unlink()
    print('PASS: actual narrated local showcase MP4, %.2f seconds'%duration)


if __name__=='__main__':main()
