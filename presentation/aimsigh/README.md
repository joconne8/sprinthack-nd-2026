# Aimsigh presentation and demonstration

Open `index.html` directly or serve the presentation directory on localhost. The
15-slide main story is timed to 15 minutes: problem 2, recorder 4, data/Excel 3,
dashboard/conversation 4, pilot 2. Arrow keys and Space navigate, N toggles notes,
Escape closes notes or the recording. Source links and full speaker notes are
included. See [DEMO.md](../../DEMO.md) for startup and rehearsal.

The visual reference is the supplied [Aimsigh founder deck](https://docs.google.com/presentation/d/1z-6jdYtqZ3t0SwIbbGc7pAyQ7cWptPXiYY-Tj7PNGLM/edit):
cream, forest green, Georgia headlines, Arial text, spacious diagrams and actual
application evidence. This package does not edit or publish that Drive file.

Final output files are `aimsigh-showcase.pdf`, editable
`aimsigh-showcase.pptx`, and narrated `walkthrough.mp4`. Screenshot media are fitted
fully within their frames; financial UI is never stretched or cropped. The
PowerPoint keeps narrative text, diagrams and speaker notes editable.

The backup is a scripted Playwright walkthrough of actual local-browser
interactions, with offline synthetic narration. It never substitutes invented
metric screenshots or canned API responses. `captures/` contains actual
local-browser recordings of the recorder, collection,
dashboard, comparison, conversation and evidence. The workbook image is a preview
rendered from the exported XLSX cached cell values, explicitly distinguished from
an Excel application screenshot. `exports/september2026.xlsx` is the actual
downloaded workbook. `capture-verification.json` pins the source snapshot and
records assertion results. `slides-verification.json` records rendering checks;
`recording/video-metadata.json` and `recording/timeline.json` document the MP4.

All sales are fictional. Labor and shipping costs are invented, disclosed sample
inputs. The channel is a model-free local Teams-style prototype. Actual Teams,
Copilot, Jev, native Power BI/Superset and hosted database connections remain
conditional pilot work. Amanda's 30–45 minutes is an interview estimate; her LOI
expresses nonbinding interest. No production authorization or measured savings
is represented.

The earlier verified P0 presentation and video remain one directory above as a
separately labelled fallback. A draft Aimsigh build displays capture-pending labels
and is not certified as complete.

## Rebuild

1. Start a fresh prepared rehearsal app as described in `DEMO.md`.
2. Run `python3 scripts/release/showcase_record.py --help`; supply the local base
   URL, Node/Playwright paths, Chrome if required, and local FFmpeg/FFprobe paths.
   Recording uses macOS `say` for offline synthetic narration; other platforms can
   still run the capture script and HTML/PDF/PowerPoint builds.
3. Run `python3 scripts/release/showcase_slides.py`.
4. Run `NODE_PATH=tools/verification/node_modules node scripts/release/showcase_render.cjs`.
5. With `python-pptx==1.0.2` and Pillow installed, run
   `python3 scripts/release/showcase_slides.py --pptx`.
6. Review all rendered slides and the complete narrated recording before submission.

Presentation sources and timing live in `planning/pitch/aimsigh-slides.json` and
`aimsigh-sources.json`. `--allow-draft` exists only for layout inspection while
verified application captures are pending.
