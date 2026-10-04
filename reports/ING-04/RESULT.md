Task: ING-04; issue #10; requirements: PLAN §4, §7
State: READY_FOR_REVIEW; accepted: false.
Operator: Peyton, authorized takeover of Hugh/Landon; Jack mc retains independent QA.
Branch: peyton/acquisition-dashboard; base: 7f948064146fee91ef573ea11761fec8bd0ae359.
Tested implementation: working-tree hashes in ../takeover/verification.json; delivered commit is the commit containing this report.

Bounded retries, persistent collection/import/publication history, restart recovery, last-success display and CSV+manifest fallback are wired through the API and UI.

Implementation paths: acquisition/run_state.py; acquisition/controller.py; planning/operations/acquisition.md. Shared shell/API/contracts are owned by Peyton under the combined authorization. Existing merged Python/SQLite goodwill-v1 foundation and synthetic replica are reused.

Actual verification: ../takeover/verification.json records exact commands, exit codes, timings, code hashes and logs. Developer backend/controller regression: 48 passed. Acquisition tests: 23 passed. Actual Chrome negative scenarios and dashboard integration: passed. Strict TypeScript, repeatable schema generation and 354-row fixture review: passed. Screenshots were inspected for desktop, operations and mobile layout.

Full Python suite: 73 tests, one failure and one deferred-export skip. Failure is Jack mc's existing test_dashboard_shows_api_values placeholder, which deliberately requires independent acceptance when a dashboard exists. No QA tests/expected results/reports or source CSV fixtures were edited. Developer API/UI comparisons are not independent acceptance.

Evidence: recovery-tests.md; verification.json; ../takeover/browser/; ../takeover/logs/. Primary basis is the registered repository Drive snapshots/three-phase plan, not fresh interviews or issue comments. Historical reports describe their older bases.

Remaining: Jack mc independent UI acceptance; human review/integration/freeze; remote CI unverified. Source-owner review remains required for the nine-source production map. P1 export/assistant/Jev/recorder and live/pilot operations remain deferred under frozen scope. Synthetic/local only; no scheduled collection, live session, external email or accounting posting.
