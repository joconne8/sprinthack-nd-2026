# DAT-01 preparatory review reservation

Operator: Peyton, assisted by Codex in this local session.
Task: DAT-01 / GitHub issue #25; PLAN sections 5 and 9; PIPE-06, PIPE-09.
Branch: `peyton/DAT-01-fixture-review`.
Base/tested commit: `b329c0fece37c1694b4d84c0c55e609dc931f854`.
Merged fixture commit: `ee7291d515a10da51be0ee9e887dfa53b73b5650` (PR #1).

Permitted edits: `reports/DAT-01/` only. This is a local preparatory
reservation; no GitHub claim was posted and issue ownership is unverified.
No fixture, shared contract, migration, entrypoint, or other lane is edited.

Dependency status: GOV-02 acceptance not located. Its remote branch contains
proposals marked ready for human review. This reservation authorizes baseline
review artifacts only; it does not clear DAT-01 acceptance or implementation gates.

Planned commands:

- Run the supplied fixture suite in a temporary directory extracted from the
  exact tested commit, retaining stdout/stderr and runtime. The suite regenerates
  fixtures; it must not run against the user's working files.
- `python3 reports/DAT-01/review_fixtures.py`: read-only cross-checks using CSV
  data and manifest controls without importing generator code.
- Run DAT-01/DAT-02 selectors and retain their actual blocked exit codes.
- `git diff --check`, `git status --short --branch`.

Review scope: cent-exact demo sales versus source payout fields, daily control
totals, declared exceptions, listing dates, snapshot grain, and provenance gaps.
Expected values: existing manifest controls; these were generated with the
fixtures and are not an independent QA acceptance ledger.

Session limits: supervised preparation only, maximum 60 minutes, maximum two
repair attempts; no unattended build or new paid service. No spend cap has been
provided, so this document does not authorize unattended execution.
Human reviewer: not yet designated; Jack OC's prerequisite decisions are needed.

Stop conditions: missing accepted scope/contracts/scaffold prevents data feature
implementation. Unavailable issue comments or Drive sources are recorded as
limitations, never treated as approved or read.
