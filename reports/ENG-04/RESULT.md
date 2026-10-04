> Current release update: the dashboard placeholder has been replaced with actual browser acceptance. See ../release/verification.json and ../integration/human-review-checklist.md for current checks and pending human review. The report below preserves the earlier session.

# Task result

Task / issue / source requirement IDs: ENG-04 / #42 (parent E-ENG #5) / PLAN §8 independent
expected totals and QA, §9 synthetic data and realistic coverage.
State: READY_FOR_REVIEW (partial: ledger, negative, seeded-defect and portal→API demo
sequence are done; dashboard and export acceptance are BLOCKED/deferred, see below).

Branch / base commit / head commit: `jack-mc/eng-04-preflight` / `610035e` (main, merged
PR #52) / see the PR for the head commit. Operator: Claude Code assisting Jack mc.

Changed files (QA lane only, no implementation or fixture edits elsewhere):

- `fixtures/expected-results/eng04_control_ledger.json`: handwritten expected ledger with arithmetic
- `tests/acceptance/__init__.py`: makes the suite run under CI's `discover -s tests`
- `tests/acceptance/qa_support.py`: artifact builder, QA raw-byte reader, demo-sequence driver
- `tests/acceptance/test_independent_ledger.py`: 11 ledger/contract/negative tests
- `tests/acceptance/test_seeded_defects.py`: 7 mutation tests
- `tests/acceptance/test_demo_sequence.py`: 5 passing end-to-end tests + 2 explicit skips
- `reports/ENG-04/`: this result, regression report, verification.json, logs, demo evidence and downloaded files

Commands actually run (Python 3.9.6, macOS, 2026-10-04 03:47 UTC):

| Command | Result | Log |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/acceptance -p 'test_*.py' -v` | 25 run, OK, 2 skipped | logs/acceptance.log |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` (CI command) | 61 run, OK, 2 skipped | logs/tests-all.log |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s acquisition/tests -p 'test_*.py'` | 23 run, OK | logs/acquisition.log |
| `run_demo_sequence(..., keep_files='reports/ENG-04/artifacts')` | evidence below | demo-sequence-evidence.json |

The first acceptance run had 1 failure (2 reports). The cause was my own assertion:
`correction_requires_approval` appears as a row exception while the batch error is
`reconciliation_blocked`. I corrected the test to check the exceptions. This was not an implementation defect.

Independent expected-result comparison:

- Handwritten ledger totals (10.01 → 15.76 → 14.76, gross/refund splits, date edges 9.00/2.50/11.50,
  buyer/store splits 24.00/18.00/6.00/14.00/5.00) all match the implementation.
- Decoy shipping 500.00, tax 400.00, fees 300.00 and source net 9999.00 are excluded.
- Missing days, sources and buyers return null/unavailable, never 0.00. A UTC-zone report only partially
  covers a New York day.
- Seeded defects are each caught by the same checks that pass on the real code: refunds ignored,
  shipping/tax/fees included, source net field used, unstable duplicate key, forced-complete
  coverage and guessed store mapping.

Actual acquisition/file/import/metric artifacts (replica portal, synthetic):

| Step | File (SHA-256) | Import | QA raw sum | API | Portal manifest |
|---|---|---|---|---|---|
| 09-29 | `upright_paid_orders_2026-09-29_2026-09-29_synthetic.csv` (`e79cb1e7…a6cb`) | imported, verified | 7127.90 | 7127.90 | 7127.90 |
| 09-29 replay | same bytes | duplicate_noop | 7127.90 | 7127.90 unchanged | — |
| 09-29..09-30 overlap | `upright_paid_orders_2026-09-29_2026-09-30_synthetic.csv` (`f51b7287…3869`) | imported, 128 accepted / 128 duplicate | 7127.90 + 7127.78 | 14255.68 | 14255.68 |

Archived bytes served by `/api/v1/files/{id}` equal the downloaded bytes in every step. Hand-evaluated
spot rows are UP-20260929-0001 = 23.14, UP-20260930-0001 = 23.82 and UP-20260930-0002 = 49.75, and all
three match the evidence API.

Measured elapsed time / usage: acceptance suite about 4.7 s; one interactive session; no paid services.

Tests NOT run and unsupported behavior:

- Dashboard/browser acceptance: no UI in main (`apps/dashboard/` absent; Landon's E-APP branch is docs only). Skipped with reason.
- Export: deferred from P0 (planning/development.md). Skipped with reason, not waived.
- Remote CI (Python 3.9/3.12 matrix) runs on the PR; local run was 3.9.6 only.
- Drive source documents and live issue comments were not read in this session.

Remaining blockers / exact missing evidence or human decision:

- APP-01..03 merged UI is needed to finish the dashboard step, and ENG-05 integration is needed before REL-01.
- QA lane mapping (`tests/acceptance/`, `fixtures/expected-results/`) is used as proposed. Jack OC to confirm.

Synthetic/production distinctions: all data is synthetic (replica portal and handwritten QA rows). No live
vendor, Goodwill data, credentials or production access.

Recommended human review: check the fixture derivations by hand and the seeded-defect list for missing
defect classes. Note that the importer reports unapproved corrections as `reconciliation_blocked` with a
row exception.

Do not claim accepted/DONE, production readiness or deployment.
