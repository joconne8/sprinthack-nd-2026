# Independent showcase QA — review handoff

Base commit: `3a8c734c91a9c86494eb646ec5c9356e220f563e` on the shared
`peyton/aimsigh-showcase` worktree. Verification covers the working diff, not a
later commit or deployment. No commits, external messages, paid calls or live
vendor connections were made by this QA session.

## Financial, source and workbook controls

**27 independent tests pass**, Python 3.9.6, 3.428 seconds in the latest run:

```sh
PYTHONPATH=/private/tmp/goodwill-release-tools/python \
  python3 -m unittest tests.test_showcase -v
```

Actual output: `/private/tmp/aimsigh-showcase-qa-controls-final.log`.
The tests now import the shipped physical September CSVs through `prepare`.

Verified controls include:

- Handwritten two-sale ledger: sales 27.00, fees 3.00, shipping 7.00, one shared
  labor hour, cost 20.00, contribution -3.00 and margin -11.11%. This catches
  multiplied labor from joining one labor row to several sales.
- September 17–23: 60727.56 / 420.00 hours = 144.59 per hour.
- September 24–30: 61706.64 / 588.00 hours = 104.94 per hour.
- Month: net 254059.40, fees 26240.14, shipping 16800.00, hours 1968.00,
  labor cost 39360.00, contribution 171659.26.
- Missing inputs and zero denominators; platform labor remains unknown;
  incomplete sales cannot divide by full-period labor.
- Historical sales, auxiliary versions and coverage remain pinned after changes;
  tampering with a pinned auxiliary artifact stops the query.
- Same-file no-op, non-sales report exclusion, invalid filters, duplicate inputs,
  negative/boolean minutes, bounded recorder actions and approval before review.
- Actual workbook ZIP/XML, thirty daily tabs, cached formulas, daily-to-month
  aggregation, and independently specified monthly totals.
- Read-only pinned question citations; transfer, purchase approval and prediction
  requests are unsupported.
- Missing/malformed fees do not break independently verified sales, and valid
  short fee strings become canonical two-decimal evidence.

A separate direct file inspection checked all six `MANIFEST.json` hashes,
3,840 Upright rows, 960 Cash Monkey unit rows, 1,440 distinct labor
source/store/day keys and 4,800 distinct shipping source/record keys. Source
totals match the independently specified expectations above.

## Actual browser acceptance

`scripts/verify_showcase.py` launches a fresh disposable state through the real
CLI, then executes `tests/showcase_browser.cjs` in installed Chrome with pinned
Node 22.14.0 and Playwright. The final independent run reached all of these:

- Actual manual iframe actions recorded, reviewed and approved for both portals.
- New September 30 dates replayed; actual CSV checksums and importer results
  verified, genuine PNG browser frames downloaded.
- Same-file replay produced `duplicate_noop`.
- Changed-label failure, real operator re-recording of `Build export`, approved
  repair replay, expired-session and missing-report failures, then recovery.
- Dashboard week values, productivity answer, pinned source evidence and
  platform-filtered labor unavailable.
- Actual completed-month XLSX download.

**The final independent run stopped on mobile horizontal overflow in Understand
at 390×844.** The root integrator and UI owner received this defect and own the
repair and final full acceptance. The remaining mobile views, API-failure stale
card clearing and final no-JavaScript-error assertion were not reached in that
run. They must not be described as passed on this report's evidence alone.

Preserved evidence:

- `/private/tmp/aimsigh-showcase-qa/`: first run found a genuine recorder compiler
  defect dropping later observed navigation. Root fixed capture ordering and
  navigation compilation; a new regression test passes.
- `/private/tmp/aimsigh-showcase-qa-second/`: both initial portal flows passed;
  QA then incorrectly selected a historical Complete row during re-training.
  Harness now binds to the exact newly generated job ID.
- `/private/tmp/aimsigh-showcase-qa-third/`: core flow passed; QA's workbook
  request needed absolute URL resolution. The harness was corrected with the
  integrator's explicitly granted extra bounded verification cycle.
- `/private/tmp/aimsigh-showcase-qa-final/`: core flow and workbook passed,
  then identified the mobile overflow. Includes acquired CSVs, real frame PNGs,
  recorder/dashboard/delivery screenshots, `september.xlsx`, and logs.

The harness now persists partial `observed.json` on future failures so recording
and run IDs survive an incomplete acceptance.

## Regression and limits

An existing whole-suite run completed 99 tests with one environment failure:
the prior browser acceptance requires Node >=20 on `PATH`. One existing P0
export test remains skipped; the new actual XLSX is independently exercised.
Root must run the final whole suite with the pinned Node path, `NODE_PATH`,
Chrome and XlsxWriter available. Initial sandbox-denied localhost binding was
re-run with local-server permission; neither environment failure was suppressed.

QA changed only `tests/test_showcase.py`, `tests/showcase_browser.cjs`,
`scripts/verify_showcase.py`, and `reports/SHOWCASE/QA*`. Browser-script syntax
and Python compilation were checked. Presentation/video packaging and overnight
verification are separate root/presentation-owner checks. Human acceptance and
merge remain pending.

## Root integration follow-up

The UI owner repaired the mobile overflow. The root integrator subsequently ran the full browser acceptance successfully, including all three mobile views, stale-card clearing and console checks. Preserved passing evidence is `browser-acceptance.json` and `browser-observations.json` alongside this report. This follow-up supersedes the open mobile blocker above without rewriting its history.
