Task: ING-04 (P1). State: BLOCKED (needs accepted ING-03, DAT-08).
Delivered: acquisition/run_state.py, acquisition/tests/test_run_state.py, reports/ING-04/fallback-and-schedule.md.
Commands run: python3 -m unittest discover -s acquisition/tests → 23 OK (6 run-state tests: bounded retries, no retry for auth/policy, fail-closed unknown, deadline, no duplicate delivery).
Not done: not wired to runner/UI; no last-success or coverage display; no scheduler. Branch hugh/ING-acquisition, base 15fa25a, uncommitted.
