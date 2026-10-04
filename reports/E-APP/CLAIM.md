# Task claim — E-APP (coordination only)

Task / GitHub issue: E-APP — Dashboard, metric tools and bounded agentic interaction — [#6](https://github.com/joconne8/sprinthack-nd-2026/issues/6)
Operator/session and designated human reviewer: Landon (operator), Claude Code session in VS Code. Proposed reviewer: Jack OC (PM-00 orchestrator).
Primary source and requirement IDs: PLAN §6, §7, §8; PRD 03 DASH-01–09; PRD 04 AI-01–07; PLAN §2 REQ-DAT-01, REQ-KPI-01, REQ-AI-01.
Branch / worktree / base commit: `landon/E-APP` in the main checkout. Started on `15fa25ad31f1720320dbb4b9fe073796436e2dce` (merge of PR #45). Fast-forwarded before commit to `b329c0f` (merge of PR #49); the reports were refreshed for that state.
Dependency accepted commits and evidence inspected: None required for E-APP. Children's dependencies inspected; none are accepted (see workstream-readiness.md).
Frozen schema/API/metric versions: None exist on any branch at base commit.
Exact allowed files; shared-file owner agreement: `reports/E-APP/**` only. No application, contract, fixture, migration or lockfile edits.
Commands to run / independent expected results: git state commands; read-only inspection of packets, plan and fixtures; one awk column check (`reports/E-APP/netcheck.awk`). No app tests exist to run.
Elapsed deadline / max 2 repairs / runner spend-token cap: 60 minutes; 2 repairs; spend cap not set by orchestrator — supervised interactive session, not unattended.
Human gates / unsupported runtime / stop conditions: No child implementation. Python and Node are not installed on this machine, so `select_assignment.py` and fixture tests could not run here.
Reports directory: `reports/E-APP/`

This is a claim proposal; resolve conflicting claims with the orchestrator before editing.
It has **not** been posted to issue #6. Landon will post it if the orchestrator wants it on GitHub.
