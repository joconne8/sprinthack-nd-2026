# Goodwill presentation package

Open index.html directly, or serve this directory on localhost as described in ../DEMO.md.
Arrow keys/Space navigate, N toggles notes, Home/End jump. Slide 8 plays demo.mp4 locally.
Files: ten-slide HTML/PDF/PowerPoint, a narrated 2:11 MP4, slide PNGs and recording evidence.
The HTML embeds its screenshots and styles; keep demo.mp4 beside it for offline playback.
PowerPoint uses raster slide images with speaker notes. Financial screenshots are actual local API-driven
browser captures of synthetic data; narrative charts are not substituted for measured results.

Sources and speaker notes: ../planning/pitch/slides.json. Offline voiceover: macOS say (synthetic speech).
Video encoding: FFmpeg 6.1.1 from the publisher's [portable build](https://github.com/eugeneware/ffmpeg-static),
local H.264/AAC, no network video service. Browser recording: pinned Playwright 1.62.1 and installed Chrome.

Rebuild: python3 scripts/release/record_demo.py --help; python3 scripts/release/build_slides.py;
NODE_PATH=tools/verification/node_modules node scripts/release/render_slides.cjs;
python3 scripts/release/build_slides.py --pptx with python-pptx==1.0.2 installed.
Actual verification: slides-verification.json and recording/video-metadata.json.
No final human approval or organizer upload is represented by this package.

Package the offline handoff ZIP: `python3 scripts/release/package_release.py`.
The verified ZIP is written to `.runtime/goodwill-submission.zip`; file hashes are in MANIFEST.json.
