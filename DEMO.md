# Run the Aimsigh showcase

Peyton’s confirmed deadline: **Monday, October 5, 2026, 10 a.m. Eastern**.
The main presentation is 15 minutes. A real recorder and browser replay feed
verified sample records, Excel, dashboard metrics and a model-free local channel.

## Start from a fresh checkout

Prerequisites: Python 3.9+ with timezone data, Node 20+ and npm. Tested Node:
22.14.0. Install the pinned workbook dependency and Playwright:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-showcase.txt
npm ci --prefix tools/verification --ignore-scripts --no-audit --no-fund
node tools/verification/node_modules/playwright/cli.js install chromium
```

Prepare the rehearsal once, then launch it:

```sh
python3 -m goodwill_app --state-root .runtime/aimsigh-demo demo prepare
python3 -m goodwill_app --state-root .runtime/aimsigh-demo demo serve --port 8000
```

Open **http://127.0.0.1:8000/showcase**. The server starts the local synthetic
vendor portal. Cards and charts query the real SQLite-backed API. The original
reporting workspace remains at http://127.0.0.1:8000/.

Preparation imports verified September 1–29 sales from both simulated portals
and versioned labor/shipping sample inputs. September 30 stays missing so live
collection changes coverage, metrics and the workbook. These are real imported
records, not fixed frontend values. Preparation is idempotent.

If Node or Chromium is not found, check `demo serve --help`; `--node`,
`--node-modules`, and `--chrome-path` select a locally installed runtime.

## Open the presentation

In a second terminal:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory presentation
```

Open **http://127.0.0.1:8080/aimsigh/**. Arrow keys/Space navigate; N shows notes;
Escape closes notes or the recording. The deck has 15 slides, source links and a
timed script. It also works offline with the MP4 beside its HTML.

- [HTML slides](presentation/aimsigh/index.html)
- [PDF](presentation/aimsigh/aimsigh-showcase.pdf)
- [Editable PowerPoint](presentation/aimsigh/aimsigh-showcase.pptx)
- [Narrated recorded walkthrough](presentation/aimsigh/walkthrough.mp4)
- [Sources and presenter notes](planning/pitch/aimsigh-slides.json)

The earlier [P0 recording](presentation/demo.mp4) remains separately available.
Draft builds explicitly state that captures are pending; final rendering/capture
verification establishes readiness.

## Present the connected story

| Segment | Time | Working evidence |
|---|---:|---|
| Problem and people | 2 minutes | Amanda’s workflow, leadership visibility, nine reports |
| Collect | 4 minutes | Real recording, reviewed recipe, two-source new-date replay |
| Verify & deliver | 3 minutes | Snapshot/lineage, actual workbook, data-flow diagram |
| Understand | 4 minutes | Charts, productivity question, underlying evidence |
| Pilot | 2 minutes | Existing Microsoft path, approvals and support ownership |

1. **Collect → Start recording → Upright.** Inside the simulated portal choose
   Reports → Paid orders. Enter **September 29–29**, choose **Eastern Time —
   Indianapolis** and **All** payment statuses. Generate, wait for Complete,
   and download the CSV.
2. Click **Review recording**, inspect actions/date bindings, then **Approve
   recipe**. The reviewed recipe becomes selected for replay.
3. Choose **September 30–30**, Normal collection, and **Run & verify report**.
   Watch genuine browser frames; wait for `succeeded / complete`. Show the run,
   checksum, verified row count and snapshot identifier.
4. Select the approved **Cash Monkey** recipe and run September 30–30. Both
   sources now cover the month. Replaying a report is a duplicate no-op; failed
   runs preserve the last-good publication.
5. Open **Verify & deliver** and download the September workbook. Show monthly
   summary, a daily tab, normalized records, labor inputs and source evidence.
   The supplied preview reads actual exported XLSX cached cell values.
6. Open **Understand**. Show cards, daily chart, comparison, source/store filters,
   coverage and snapshot. Open Supporting records to trace a displayed number.
7. Ask **“Why is revenue per labor hour down?”** Inspect the September 17–23
   versus September 24–30 answer and its labor evidence. An unsupported question
   returns supported alternatives rather than an invented answer.
8. If time permits, choose Changed control label under the failure demonstration.
   Review the stopped run, record the changed local workflow, review/approve its
   updated recipe, and retry. Restore Normal before continuing.

## Sample inputs produce the actual metrics

The fictional feeds are disjoint by construction. Labor is allocated at
source/store/day grain: 2 h/day per Upright store through September 23, then
3 h/day; Cash Monkey uses 0.5 h/day throughout. There are 24 modeled stores.
Shipping expense is invented at $3.50 per sales record; labor cost is invented
at $20/h. Marketplace fees come from the synthetic source records.

| Period | Net sales | Modeled hours | Revenue/labor hour |
|---|---:|---:|---:|
| September 17–23 | $60,727.56 | 420 | $144.59 |
| September 24–30 | $61,706.64 | 588 | $104.94 |
| September 1–30, both sources | $254,059.40 | 1,968 | $129.10 |

Net sales is item sales minus refunds, excluding shipping collected, tax and
fees. Demo contribution margin subtracts fees plus modeled shipping/labor,
excluding overhead and taxes. Full-month modeled contribution is $171,659.26;
demonstrated contribution margin is 67.57%.

The comparison explains an arithmetic change in fictional data, not a verified
business cause. Platform filters make labor-dependent metrics unavailable
because labor has no platform allocation. Customer counts stay source/platform-
local. The original August inventory example stays separately dated and is never
joined to September sales.

## Reset and known-good checkpoint

Stop the rehearsal server before resetting its isolated state:

```sh
python3 -m goodwill_app --state-root .runtime/aimsigh-demo demo reset
python3 -m goodwill_app --state-root .runtime/aimsigh-demo demo serve --port 8000
```

For a separate, fully populated recovery state:

```sh
python3 -m goodwill_app --state-root .runtime/aimsigh-checkpoint demo prepare --checkpoint
python3 -m goodwill_app --state-root .runtime/aimsigh-checkpoint demo serve --port 8001
```

Open http://127.0.0.1:8001/showcase for the complete workbook/dashboard. Identify it
as prepared sample state. Use the incomplete baseline rehearsal for teach/replay.
Reset is restricted to a marked isolated showcase state; keep unrelated data
elsewhere. If live collection fails, play the labelled walkthrough or switch to
the checkpoint. Do not describe recorded footage as a current live run.

## Honest claims and handoff

Working scope: two synthetic local portals, actual DOM recording/review/replay,
verified imports, immutable source evidence, Excel, connected charts and supported
model-free answers. The channel is a local Teams-style prototype. Production
Teams/Copilot/Jev, native Power BI/Superset and hosted database integration remain
conditional pilot work. September sell-through, prior-year growth and production
net margin stay unavailable without the required inputs.

Amanda’s 30–45 minutes is an interview estimate, not measured savings. Her LOI
expresses nonbinding interest, not a purchased or authorized production pilot.
Live access, accounting-close automation and Microsoft connections require
partner validation and named owners.

Review capture, slide, video and integrated QA verification before submission.
The root release package includes the new deck/workbook/walkthrough, original P0
fallback and source notes. Human acceptance and organizer upload remain explicit.

## Offline application handoff

Build the inspected application-and-presentation ZIP with:

```sh
python3 scripts/release/package_release.py --showcase
```

`.runtime/aimsigh-submission.zip` includes runnable source, contracts, migrations, physical sample CSVs, slides, workbook and narrated video. `presentation/aimsigh/PACKAGE-MANIFEST.json` pins every included file by SHA-256. Extract into a fresh folder, install the prerequisites above, then use the same prepare/serve commands. The package does not include installed dependencies; obtain those before an offline rehearsal.

For complete metrics immediately, use `demo prepare --checkpoint` in a separate marked demo state. The primary rehearsal deliberately begins with September 30 missing, then live collection completes both feeds and unlocks the workbook.
