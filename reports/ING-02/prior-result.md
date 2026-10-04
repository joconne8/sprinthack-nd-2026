Task / issue / source requirement IDs: ING-02 (issue #16); PLAN §4, §7
State: BLOCKED on process gates only (GOV-03 and ING-01 acceptance, claim not posted); technical work runs and is ready for human review once gates clear.
Branch / base commit / head commit: hugh/ING-acquisition / 15fa25a / uncommitted working tree
Changed files: acquisition/run_skill.cjs, acquisition/skills/upright-paid-orders.skill.json, acquisition/tests/failure_modes.cjs, acquisition/tests/test_skill_config.py, reports/ING-02/*
Commands actually run (Node v24.21.0, Playwright 1.62.1 via 'data ingestion' node_modules installed with --no-package-lock, installed Chrome, replica on :4173):
- node --check acquisition/run_skill.cjs: ok
- node acquisition/tests/failure_modes.cjs: two_ranges pass (128 rows for 2026-09-30, 256 rows for 2026-10-01..02, different SHA-256, checksum equals manifest); expired_session pass; changed_label pass; host_not_allowed pass; reversed_dates (bad_params) pass; delayed generation still succeeds pass; missing_report pass but classified wrong_page (no dedicated type; imprecise).
- node 'data ingestion/tests/browser.test.cjs': all PASS lines shown (replica's own suite; I only saw the last 8 lines of output).
- python3 -m unittest discover -s acquisition/tests: 23 OK. python3 -m unittest discover -s 'data ingestion/tests': 9 OK.
- End to end: skill download for 2026-10-01..02 fed into acquisition/intake.py: acquired_verified, import_state not_submitted, 256 rows, checksum matches.
Independent expected results: row counts and coverage from the ING-01 README/VERIFICATION figures.
Tests NOT run: no wrong-page-by-redirect case; timeout (total deadline) case not exercised; logs print run id and skill version to stderr but log content was not asserted; Upright only, not Cash Monkey; real Upright untested and unclaimed.
Remaining blockers: GOV-03/ING-01 acceptance, orchestrator lane mapping, claim posting.
Synthetic/production: replica only. Tests use a hook that sets the replica's sessionStorage mode.
Not accepted, not merged, not DONE.
