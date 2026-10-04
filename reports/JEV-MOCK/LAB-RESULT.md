# Recorded workflow lab — READY_FOR_REVIEW

User requested the ambitious synthetic Jev demo. Branch peyton/jev-mockup,
base 3a8c734; uncommitted working-tree deliverable. No merge or live deployment.

New lab files: experiments/jev/lab.cjs, lab.html, lab-ui.js, recorder.cjs,
recipe.cjs, handoff.py, lab.test.cjs, recipe.test.cjs. Existing experiment run.cjs
adds optional recipe path and repair approval hook; README documents launch and
rehearsal. Reports remain in reports/JEV-MOCK/. Shared portal, acquisition,
contracts, migrations and dashboard code are unchanged.

Delivered:
- Record actual synthetic-portal browser actions with before/after observations.
- Require verified current-job recording download and explicit date-parameter review.
- Save and restore bounded versioned recipes; reject expanded hosts/reports/actions.
- Replay the captured journey with different dates and verify actual CSV bytes.
- Jev mode uses the existing actual API provider; changed-label decisions highlight
  the replacement and require single-run human approval within 15 seconds.
- Approval rejection/expiry stops; verified repair proposals never silently replace
  saved recipes. Cancel closes the active page.
- Operator-triggered handoff calls existing verified intake and importer, using
  an isolated SQLite state root. Pulse and evidence come from existing metric API
  functions, not hardcoded display totals. Duplicate imports leave totals unchanged.
- Live screenshot stream plus labeled final capture, model usage/decision trail,
  evidence, last-good retention and persistent synthetic/unconnected disclosures.

Actual checks (Node 22.14.0/Playwright from /private/tmp/goodwill-completion-tools;
installed Chrome; local Python portal on 4187):
- `node --test experiments/jev/provider.test.cjs experiments/jev/recipe.test.cjs`:
  12/12 passed; log /private/tmp/jev-lab-unit.log.
- `node experiments/jev/lab.test.cjs`: passed six scenario groups; log
  /private/tmp/jev-lab-test.log. Real recorded events and real downloaded/imported
  CSVs; model responses are explicitly injected-test-only, with no external calls.
- Browser test checks 128 rows / 7127.78 for September 30 and 256 rows / 14255.20
  for October 1–2 against the existing independent ledger values.
- Tested date review rejection, no-session-token denial, replay drift stop,
  reviewed renamed-button recovery, rejection/no-import, duplicate_noop,
  last-good retention, expired session and pulse UI rendering.
- `node --check` for lab.cjs, recipe.cjs, lab-ui.js: pass.
- Python handoff compilation: pass with PYTHONPYCACHEPREFIX=/private/tmp/jev-lab-pycache.
- `git diff --check`: pass; new lane files remain untracked.
- Screenshot visually inspected after image-route/final-capture repair.

Reproducible test artifacts:
/var/folders/1t/r8vbq2ns31z3ld8d_36zw3s40000gn/T/jev-lab-tests-9QlUZH/
contains lab.png, recipe.json, verification.json, runs/ and pipeline/.
Convenience preview: .runtime/jev-lab-preview.png.

Observed failures retained in the session: initial Python compile targeted a
nonwritable system cache; fixed by specifying a writable cache. Screenshot had
a query-route mismatch/no final image; fixed and tested image decode. Repeated
tests encountered multiple old Download links; test now uses generated job ID,
and recording verification rejects downloads from any older job.

Limitations: actual lab Jev quality is untested because user-terminal credentials
are not inherited by agent tools. Real Jev may still fail confidence guards.
Human headed recording was exercised with browser-generated actions in tests;
manual usability rehearsal remains needed. Approval timeout and cancel paths
exist but were not independently exercised. Not a universal recorder or Chrome
extension; only the ordered scoped paid-orders journey is supported. The lab's
queried pulse uses its isolated database, not the main application's running DB.
No real Upright session, production approval, external messaging or schedules.
