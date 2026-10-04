# Task result

Task / issue / source requirement IDs: GOV-03 — [#15](https://github.com/joconne8/sprinthack-nd-2026/issues/15). PLAN §5, §6, §8. GOV-01 REQ-ING-01/03/05, REQ-DAT-01..05, REQ-KPI-01..03, REQ-OPS-01/03, REQ-SEC-01, REQ-AI-01, REQ-FIN-01 (trace in `planning/contracts.md` §11).
State: **READY_FOR_REVIEW**.
Branch / base commit / head commit:
- Branch: `jackoc/GOV-03-contracts`.
- Base: `f36684c4719bdeb714e91c2755cb55abf02e3d2b`, which merges GOV-02 head `0e1fde5` with main `b329c0f`.
- Head: the commit that adds this file.
Changed files and diff summary: All files are new. Nothing existing was edited.
- `contracts/v1/goodwill-contracts.schema.json`: 66 definitions, including 12 top-level contracts.
- `contracts/v1/expected-reports.json`: nine sources, one P0 report.
- `contracts/v1/examples/`: 23 valid and 14 invalid fixtures, plus a README.
- `contracts/tests/validate-contracts.cjs`.
- `contracts/README.md` and `planning/contracts.md`.
- `reports/GOV-03/`: claim, compatibility notes, test results, two run logs, this result and `verification.json`.
Commands actually run, results, logs: `validate-contracts.cjs` gave 58 passed, 0 failed, exit 0 (`contract-run.log`). The negative control gave 57/1, exit 1 (`negative-control-run.log`).
Independent expected-result comparison: The replica's file totals were recomputed with gawk in integer cents (128 rows, 7353.00 − 225.22 = 7127.78) and match its manifest. The SHA-256 was verified separately with `sha256sum` and with Node `crypto`. Example values are illustrative, not an expected-results ledger.
Actual acquisition/file/import/metric artifacts, if relevant: The real replica example file was validated through the documented translation. It fails only on `reporting_timezone`.
Measured elapsed time / usage: About 50 minutes in one interactive session. Token usage was not measured.
Tests NOT run and unsupported behavior: No standard validator (ajv) or type generation, because no dependencies exist yet (ENG-01). No implementation-side API/UI tests (none exist). No Python fixture tests (not installed). The bundled checker implements only the draft-07 subset it uses.
Remaining blockers / exact missing evidence or human decision:
1. Jack OC accepts or amends contracts `1.0.0`. In particular: the `America/New_York` constant, the decimal-string money format, `latest_acquired_wins_with_history`, the refund attribution rule, and the proposed API paths.
2. Hugh: the replica timezone change and runner manifest translation (`compatibility-notes.md` §5). Real replica files pass only after that.
3. ENG-01: a standard validator, type generation, and CI wiring.
4. Still open from E-APP: whether export is required for ENG-04 (B4), and the APP-06 reviewer (B5).
5. GitHub: PR #48 (GOV-01 + GOV-02) is unmerged, so this branch also carries those commits until it merges.
Synthetic/production distinctions: v1 is synthetic-only by construction (`synthetic: true` is a constant). No live systems, credentials or external services were used. Nothing was pushed or posted.
Recommended human review:
1. Read `planning/contracts.md` §3–§6.
2. Check that the fixtures in `contracts/v1/examples/valid/` tell a believable story for the demo.
3. Rerun the checker.

Do not claim accepted/DONE, production readiness, merge or deployment.
