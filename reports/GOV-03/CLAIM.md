# Task claim — GOV-03

Task / GitHub issue: GOV-03 — publish frozen acquisition, import, metric and agent-tool contracts — [#15](https://github.com/joconne8/sprinthack-nd-2026/issues/15)
Operator/session and designated human reviewer: A Claude Code session on Landon's machine. The session user stated they were acting as Jack OC, and commits are authored as Landon. Reviewer: Jack OC.
Primary source and requirement IDs: PLAN §5, §6, §8; GOV-01 REQ-ING-01/03/05, REQ-DAT-01..05, REQ-KPI-01..03, REQ-OPS-01/03, REQ-SEC-01, REQ-AI-01, REQ-FIN-01.
Branch / worktree / base commit: `jackoc/GOV-03-contracts`, created from `0e1fde5` (GOV-01 + GOV-02). Main `b329c0f` was merged in as `f36684c` so the contracts could reconcile Hugh's PR #49 drafts.
Dependency accepted commits and evidence inspected:
- **GOV-02**, accepted at `3812052` (GOV-02 commit) / branch head `0e1fde53fe290f1b1730f0d93e496314e1d1165c`.
  - The user, acting as Jack OC, replied "accept" on 2026-10-04 (~02:50Z). The question was: "acting as Jack OC, do you accept GOV-02 now and want me to start GOV-03 and GOV-04 from the GOV-01 branch head (`0e1fde5`)?"
  - Inspected first: all five required outputs exist, the commit stayed in its file lane, and on my reading it meets the three acceptance tests.
  - Four gaps were reported to the user. GOV-03 closes three: refund attribution and the `net_sales` column (`planning/contracts.md` §5), and the expected-report schedule (`contracts/v1/expected-reports.json`). The fourth, the replica timezone, is fixed in the contract but needs Hugh's replica change.
  - **Not recorded in GitHub:** PR #48 (GOV-01, which carries GOV-02) is still unmerged, and no reviewer identity is verified beyond the session.
Frozen schema/API/metric versions: consumes `GOV-02-scope-v0.1` and `GOV-02-metrics-v0.1`; publishes contracts `1.0.0`.
Exact allowed files; shared-file owner agreement: `contracts/**`, `planning/contracts.md`, `reports/GOV-03/**`. Hugh's `contracts/sources/acquisition-classes.md` is read, not edited.
Commands to run / independent expected results: `node contracts/tests/validate-contracts.cjs`, run through VS Code's bundled runtime because Node is not installed. Replica totals were recomputed independently with gawk in integer cents.
Elapsed deadline / max 2 repairs / runner spend-token cap: 60 minutes; 2 repairs (1 used); supervised interactive session, no separate spend cap set.
Human gates / unsupported runtime / stop conditions: No live systems. Contract acceptance stays with Jack OC.
Reports directory: `reports/GOV-03/`

Not posted to GitHub.
