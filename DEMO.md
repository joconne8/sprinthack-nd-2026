# Goodwill reporting demo

Deadline supplied by Peyton: **Monday, October 5, 2026, 10:00 a.m. Eastern**.
This is the frozen synthetic P0: acquired file → verified data → connected dashboard.

## Start from a fresh checkout

Prerequisites: Python 3.9+ with timezone data, Node 20+ (tested 22.14.0), npm.

```sh
npm ci --prefix tools/verification --ignore-scripts --no-audit --no-fund
node tools/verification/node_modules/playwright/cli.js install chromium
python3 -m goodwill_app --state-root .runtime/presentation-demo serve --port 8000
```

Open http://127.0.0.1:8000/. The API starts a local synthetic report portal automatically.
Use an unused state directory for a fresh demo. All financial cards query the SQLite-backed API.
Manual CSV/manifest upload remains available if browser collection is unavailable.

## Present the story

Serve the presentation in a second terminal:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory presentation
```

Open http://127.0.0.1:8080/. Arrow keys/Space advance; N shows speaker notes.
The 10-slide deck covers the problem, solution, current delivery, controls, recorded demo and next pilot.
Downloads: [PowerPoint](presentation/goodwill-progress.pptx), [PDF](presentation/goodwill-progress.pdf),
[narrated MP4](presentation/demo.mp4). The video is approximately 2 minutes 11 seconds;
slide 8 plays it locally. HTML works offline with demo.mp4 alongside index.html.

## Live demonstration, about three minutes

1. Report intake: collect Upright paid orders for **2026-09-30** in normal mode.
   Wait for `imported` and verified. This downloads real CSV bytes from the local replica.
2. Leadership pulse: choose September 30 only, Upright. Net sales is **7127.78** from **128 rows**.
   Shipping/tax/fees are excluded. Coverage and missing metric inputs are visible.
3. Open source evidence, inspect a row, then download the exact source CSV. Show checksum,
   batch and pinned metric run. A displayed number stays tied to its supporting rows.
4. Collect **2026-10-01 through 2026-10-02**. The selected two-day total is **14255.20**.
5. Repeat that collection. It becomes `duplicate_noop`; the total does not increase.
6. Choose the session-expired failure mode and collect a different period. Show one bounded attempt,
   owner attention and no published bad data. Reset mode to normal afterward.
7. Show unavailable margin/customer metrics when required inputs are absent. Do not describe them as zero.

## Backup

If the live flow fails, play the recorded MP4; label it a recording. PDF/PPTX contain actual screenshots.
The recording starts with an empty state and shows the same API-driven acquisition/import/evidence flow.
Its captions and narration identify synthetic records and the simulated portal.

## What we can say

We built a working local acquisition-to-dashboard reporting prototype with deterministic financial
calculations, original-file evidence, safe failure, replay/correction controls and missing-data labels.
The financial acceptance uses Jack mc's original handwritten ledger plus an independent raw-byte reader.
Peyton's final-release session added the actual browser checks; human review remains outstanding.
No live vendor/Goodwill data, production deployment, measured ROI, nine connected sources, Jev assistant,
or completed P1 metric export is represented. Source-backed notes live in planning/pitch/slides.json.

Before upload, a team member reviews the story and confirms the organizer's upload destination,
time limit and required filenames. The formats and deadline are user-confirmed; upload details are not.
