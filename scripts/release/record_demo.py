"""Record the actual local dashboard and export a narrated H.264 MP4 backup."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.acceptance.qa_support import portal_server, serving
from acquisition.controller import AcquisitionManager
from apps.api.server import make_server
from services.data.importer import Pipeline

PHASES = [
    ('The problem', 'Trusted reporting starts before the dashboard.', 'Goodwill needs useful numbers for decisions. But first, someone has to retrieve and consolidate reports. We built a synthetic prototype that connects that upstream work to a dashboard. This recording uses fictional records and a simulated portal.'),
    ('Acquire', 'Choose dates. Collect the report. Verify and import the exact file.', 'The operator requests a paid orders report for September thirtieth. A versioned browser skill selects the dates and downloads the report. The file is checked, archived and sent through the real importer. Collection, import and publication remain separate states.'),
    ('Understand', 'The dashboard reads published data through the API.', 'The leadership view now shows seven thousand, one hundred twenty seven dollars and seventy eight cents in demo net sales. That means item sales minus refunds. It excludes shipping, taxes and fees. Coverage, definitions and freshness sit beside the value.'),
    ('Keep the proof', 'Metric run → supporting rows → original CSV and import batch.', 'We can follow the number back to its supporting rows, original source fields, file checksum and import batch. The view is pinned to the metric run we opened. It is evidence for the displayed number, rather than a separate mock dashboard.'),
    ('Change the dates', 'The same workflow collects October 1–2 without code changes.', 'Now we request October first through second. The same workflow imports two hundred fifty six rows. The dashboard changes to fourteen thousand, two hundred fifty five dollars and twenty cents. No code or fixture is edited to produce the alternate date result.'),
    ('Replay safely', 'Repeating a report keeps published totals unchanged.', 'Collecting the same report again is a duplicate no-op. It remains visible in history, but it does not double the published totals. Corrections use a separate, explicit approval control.'),
    ('Fail safely', 'An expired synthetic session stops and names the next owner.', 'An expired synthetic session stops after one attempt. The dashboard shows the cause and the operator who needs to act. Nothing is imported from this failed collection. Manual CSV and manifest upload remains available as a fallback.'),
    ('State of play', 'Working synthetic prototype. Live connections and advanced inputs are next.', 'The acquisition, verification and dashboard flow works. Missing margin and labor inputs stay unavailable. Real Goodwill access, source mappings, Microsoft integration and production ownership are next steps. This is demonstrated prototype progress, not a live integration or a measured savings claim.'),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--node', required=True); p.add_argument('--node-modules', required=True)
    p.add_argument('--chrome-path'); p.add_argument('--ffmpeg', required=True); p.add_argument('--ffprobe', required=True)
    p.add_argument('--output', default='presentation')
    args = p.parse_args()
    output = (ROOT / args.output).resolve(); output.mkdir(parents=True, exist_ok=True)
    recordings = output / 'recording'; recordings.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='goodwill-demo-recording-') as temporary:
        temp = Path(temporary); phases = []
        for i, (title, caption, narration) in enumerate(PHASES):
            audio = temp / f'{i}.aiff'
            subprocess.run(['say', '-r', '165', '-o', str(audio), narration], check=True, timeout=45)
            probe = subprocess.check_output([args.ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(audio)], text=True)
            phases.append({'title': title, 'caption': caption, 'narration': narration, 'duration': float(json.loads(probe)['format']['duration'])})
        phase_path = temp / 'phases.json'; phase_path.write_text(json.dumps(phases))
        with serving(portal_server()) as portal:
            manager = AcquisitionManager(Pipeline(temp / 'state'), portal, args.node, args.node_modules, args.chrome_path)
            try:
                with serving(make_server(manager.pipeline, 0, manager)) as api:
                    env = dict(os.environ, BASE_URL=api, DEMO_OUTPUT=str(recordings), DEMO_PHASES=str(phase_path), NODE_PATH=args.node_modules)
                    if args.chrome_path: env['CHROME_PATH'] = args.chrome_path
                    subprocess.run([args.node, str(ROOT / 'scripts/release/record_demo.cjs')], env=env, check=True, timeout=360)
            finally: manager.close()
        timeline = json.loads((recordings / 'timeline.json').read_text())
        command = [args.ffmpeg, '-y', '-i', str(recordings / 'demo-original.webm')]
        for i in range(len(phases)): command += ['-i', str(temp / f'{i}.aiff')]
        filters = [f'[{i+1}:a]adelay={round(item["start"]*1000)}:all=1[a{i}]' for i, item in enumerate(timeline['phases'])]
        filters += [''.join(f'[a{i}]' for i in range(len(phases))) + f'amix=inputs={len(phases)}:normalize=0,apad[audio]']
        command += ['-filter_complex', ';'.join(filters), '-map', '0:v', '-map', '[audio]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', str(output / 'demo.mp4')]
        subprocess.run(command, check=True, timeout=240, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        # Keep the presentation package compact; the MP4 and timestamps are the backup.
        for path in recordings.glob('*.webm'): path.unlink()
    (ROOT / 'planning/pitch/narration.txt').write_text('\n\n'.join(text for _, _, text in PHASES)+'\n')
    metadata = json.loads(subprocess.check_output([args.ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(output / 'demo.mp4')], text=True))
    (recordings / 'video-metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print('Recorded MP4:', output / 'demo.mp4')


if __name__ == '__main__': main()
