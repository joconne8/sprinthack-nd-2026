# Hugh and Landon takeover handoff

Peyton authorized this combined implementation while Jack mc finishes independent QA. Branch: peyton/acquisition-dashboard; base main: 7f94806. State: READY_FOR_REVIEW, not human accepted/merged.

| Task | Delivered for review |
|---|---|
| ING-02 | Versioned bounded synthetic report replay and browser failure cases |
| ING-03 | Verified exact-byte/full-manifest intake to real importer and checksum chain |
| ING-04 | Persistent bounded recovery/status/manual fallback and operating runbook |
| ING-05 | Nine-source acquisition/authority map with unknown live owners/access |
| APP-01 | Operations intake, collection/import status, controls and exception evidence |
| APP-02 | API-backed leadership filters/cards/coverage/freshness/unavailable inputs |
| APP-03 | Pinned metric-run drilldown to original acquired file/row/batch |

[Exact verification](verification.json): 48 developer regression tests and 23 acquisition tests passed; actual Chrome negative and full-dashboard integration checks passed; strict client/schema/354-row fixture checks passed. Desktop, operations and mobile screenshots were inspected. Implementation hashes and actual command timings/logs are retained. No source fixture or independent QA lane changed.

The full Python suite ran 73 tests with one failure and one deferred-export skip. Failure: tests/acceptance/test_demo_sequence.py::test_dashboard_shows_api_values deliberately requires Jack mc's independent acceptance once the dashboard exists. It is retained unchanged. Remote CI, human integration/freeze and issue closure are unverified.

Jack mc handoff: run the app from [development guide](../../planning/development.md); evaluate operations→collection→verified import→leadership→source evidence, alternate dates, duplicate replay and failure/last-good; replace his deliberate placeholder with independent UI assertions; provide ENG-04/REL-01 evidence. Human review/merge remains required before ordinary main pulls include this branch.

P1 exports, assistant APP-04–07, Jev ING-06 and live/pilot ING-07 remain deferred under the scope freeze. Existing design reports remain historical/reviewable. No live vendor, production email, model, unattended schedule, accounting posting or deployment was activated. Source-owner confirmation is still required for live matrix decisions. Actual work used Python 3.9.6, Node 22.14.0, TypeScript 5.6.3, Playwright 1.62.1 and installed Chrome; paths/versions are reproducible from the verification record. No paid-service calls were made; overall token/cost usage unavailable.
