# Jev-assisted reporting demo

Default mode is model-free replay. Explicit `--provider jev` sends synthetic DOM
controls to the official TypeSafe API and uses actual Jev decisions. Browser actions
remain bounded by the local paid-orders workflow. DOM observations are data, never
instructions. No live Upright integration or production approval is represented.

Install the repository's existing browser dependency:

```sh
npm ci --prefix tools/verification --ignore-scripts --no-audit --no-fund
node tools/verification/node_modules/playwright/cli.js install chromium
```

Start the standalone synthetic portal in another terminal:

```sh
python3 "data ingestion/server.py" --host 127.0.0.1 --port 4173
```

If using the full application from `DEMO.md`, set BASE_URL to its portal URL
(the portal is separate from the dashboard).

```sh
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/mockup.cjs 2026-09-30 --headed
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/mockup.cjs 2026-10-01 2026-10-02
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/mockup.cjs 2026-09-30 --mode session-expired
```

## Run actual Jev

Configure `TYPESAFE_API_KEY` privately in the process environment or an approved
secret manager. Do not paste it into chat, recipes, screenshots, or source files.
After authorizing an API testing budget, use:

```sh
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/mockup.cjs 2026-09-30 --provider jev --headed
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/mockup.cjs 2026-10-01 2026-10-02 --provider jev --mode changed-label --headed
```

Direct endpoint: https://api.typesafe.ai/v1/systemone; pinned model `jev-1.13.0`.
There are no automatic API retries. Maximum 20 calls and 60 seconds per provider
run; the existing acquisition runner imposes its tighter 40-second browser limit.
Each call times out after at most 10 seconds. Confidence and chosen probability
must both reach 0.90. These are provisional demo thresholds, not validated safety
guarantees. API failure stops; it never silently switches to scripted decisions.

For the comparison, run `--mode changed-label` with the default provider first:
it should stop. Then run the same dates and mode with `--provider jev`. Successful
adaptation requires Jev to choose the observed Build export control and the final
CSV to pass independent deterministic checks. Actual Jev accuracy remains untested
until a key and budget are supplied; injected tests are labeled separately.

Optional: BASE_URL, OUTPUT_DIR, CHROME_PATH (installed Chrome executable).
Each run writes trace.jsonl and result.json to a unique evidence directory.
Success retains the downloaded CSV, source.manifest.json and manifest in result.json.
Validation checks checksum, source, report type, selected parameters, row count,
required CSV headers, every row's reporting date, and every row's synthetic flag.
Financial import
and dashboard publication are separate; this script does not perform them.
Unavailable reports, expired sessions and ambiguous controls stop the replay.
Successful clicks are distinct from final file verification. Request/response
traces include model, probabilities, confidence, token usage and timing; API
headers and credentials are excluded. Missing usage is unknown, never zero.

## Amanda's handoff

Select the requested start/end dates in the commands above. After a successful run,
the terminal prints the evidence directory: retain its original CSV and
source.manifest.json for the existing import process. If automation stops, open
http://127.0.0.1:4173/upright, choose Reports → Paid orders, enter dates, choose
Eastern/Indianapolis and payment status All, generate, then download CSV and
Manifest manually. A failed run's CSV is unverified and must not be imported.

The provider and DOM collector are separate from the portal adapter in run.cjs.
An authorized real-Upright pilot must first inspect actual DOM/report formats,
obtain Goodwill/provider browser and AI permission, assign session/support ownership,
and validate real exports. Do not point this demo at a live portal by extending
the host list. Credentials are never entered by this runner. The CLI excludes
recorder UI, automatic import and dashboard publication; the workflow lab below
adds recording and an operator-triggered isolated pipeline handoff. Neither
entrypoint provides unattended scheduling.

## Offline verification

```sh
node --test experiments/jev/provider.test.cjs
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/browser.test.cjs
```

Browser tests require the synthetic portal on port 4187 (or set BASE_URL). They
inject fixture responses without an external API call and explicitly do not
prove real Jev decision quality. Tests exercise normal/alternate dates, renamed
controls, delays, failure states, stale controls and content rejection.

## Record-once live workflow lab

The expanded lab records actual actions in a separate visible browser, requires
date-parameter review, replays the resulting recipe, presents Jev drift repairs
for human approval, verifies downloads and imports the exact file through the
existing pipeline. Its pulse cards query an isolated demo database; these are
not the main dashboard's database. Other sources remain unconnected.

Start the portal on 4173 as above. In your key-configured terminal:

```sh
NODE_PATH=/private/tmp/goodwill-completion-tools/packages/node_modules \
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
/private/tmp/goodwill-completion-tools/node-v22.14.0-darwin-arm64/bin/node \
experiments/jev/lab.cjs
```

Open http://127.0.0.1:4190. Alternatively use your installed Node and repository
Playwright dependency. The /private/tmp runtime is a verified local convenience,
not a portable installation. BASE_URL and LAB_PORT configure local ports;
`--headless` is for tests, not manual recording.

1. Click **Open & record**. In the portal window, open Reports → Paid orders.
2. Set BOTH dates (change the initial values), choose Eastern/Indianapolis,
   select All payments, click Generate report, wait for completion, then Download
   from the row for the report you just generated, rather than an older report.
   Avoid preview/test controls while recording; this recorder supports only the
   scoped eight-action workflow and rejects extra actions.
3. Click **Finish recording** in the control panel. Review the actions, check
   **Make Start date and End date reusable inputs**, and **Approve recipe**.
4. Choose different dates and run Saved replay. Click **Import verified file**
   after verification; inspect the pulse and source evidence. Import again to
   demonstrate duplicate_noop with unchanged totals.
5. Choose the renamed-button scenario and run Saved replay; it stops on drift.
6. Choose Jev and run the same scenario. If confidence passes, the control panel
   asks you to approve the highlighted replacement. Approve within 15 seconds.
   The file must still pass verification before import is enabled.
7. Inspect a session-expired run; the pulse retains the last-good publication.

The live viewport is a screenshot stream, not a video recording. Jev does not
see screenshots; it receives control metadata. Recorded before/after observations,
recipe, trace, CSV, manifest, publication and repair proposals are retained under
`.runtime/jev-lab/`. Successful repairs do not overwrite the reviewed recipe.
The new lab uses at most 20 calls and a 60-second browser/provider deadline;
the existing CLI still retains its 40-second browser limit. Approval expires at
15 seconds; rejection or expiry stops the run. API and confidence failures never
fall back silently. Real Jev reliability remains subject to actual API evaluation.

Offline full-lab test (portal on 4187):

```sh
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/lab.test.cjs
```

Tests inject labeled responses and exercise recorder → recipe → replay →
verified importer → queried pulse plus approved/rejected drift repair. This is
not a universal recorder, Chrome extension, or approved real-Upright pilot.

## Presentation: walkthrough then first-run Jev

Restart the lab after updating its server code. At the top of the page, play
**Report walkthrough**, select dates and a scenario below, then click
**Run with Jev**. No recorded recipe is needed: this uses the existing predefined
paid-orders workflow. Jev chooses observed controls live; it does not watch or
learn from the video. Confidence/file checks and repair approval still apply.
The video is a staged manual-paced browser demonstration with scripted clicks,
not footage of a person or an actual Jev run. The Run log distinguishes live
Jev from replay and injected test responses. Runtime is not a speed guarantee.

Generate or replace the local walkthrough (portal running on 4173):

```sh
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/walkthrough.cjs
```

Playwright's video encoder must be installed (`playwright install ffmpeg`). On
this machine it is installed under `/private/tmp/goodwill-completion-tools/browsers`;
set `PLAYWRIGHT_BROWSERS_PATH` to that path when regenerating. Artifacts:
`.runtime/jev-lab/walkthrough.webm`, walkthrough.csv and walkthrough-evidence.json.
The current generated video verifies 256 synthetic rows for October 1–2, 2026.
Live API evaluation remains separate from the injected presentation-path tests.

## Hosted / Replit version

See [hosted setup and limits](hosted/README.md). The hosted entrypoint adds
password protection, one active predefined run, browser screenshots and verified
CSV/manifest/trace downloads. Jev keys stay server-side. The portal remains
loopback-only inside the host. Replit deployment and live API rehearsal have not
been performed. Local upload bundle: `.runtime/jev-replit-demo.zip`.
