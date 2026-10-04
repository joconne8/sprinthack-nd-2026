# Combined setup and trusted-data session

Operator: Peyton with Codex assistance. Branch: `peyton/jackoc-data-foundation`.
Base: `b329c0fece37c1694b4d84c0c55e609dc931f854`.

Authorization: Peyton explicitly instructed this session to combine Jack OC's
tasks and Peyton's tasks and stated that Jack OC approved. This authorizes local
scope/contract/scaffold decisions and data implementation, superseding the
previous instruction to wait for another lane's setup. It is not Goodwill's
production approval, independent QA acceptance, or authorization to push/merge.

Reuse Jack OC's GOV-01/GOV-02 proposals from remote commit
`38120523f60ff9cc0f888146b9450be5be74f674`, with provenance retained. Scope is the
existing P0 synthetic acquired-file vertical slice; P1 inventory is separate.
Pilot work is design only. Do not fabricate historical acceptance records.

Sequential bounded units: GOV-01/02 proposal reuse; GOV-03 contracts; GOV-04 and
ENG-01 runtime; ENG-02 ownership; DAT-01 review policy; DAT-02 archive;
DAT-03 parser; DAT-04 correction handling; DAT-05 reconciliation;
DAT-06 metrics; DAT-08 publication; optional DAT-07; DAT-09 design;
ENG-05 review packet. No child agents or unattended jobs are launched.

Allowed paths: planning requirements/scope/contracts/development/architecture/
ownership/release docs; contracts (except Hugh's existing source-map edits);
services/data/, services/metrics/, goodwill_app/, apps/api/, db/, tests/,
own reports and development CI/config. Existing acquisition/, portal/UI code
and Landon's lane are read/test only. No fixture bytes will be rewritten.

Shared ownership in this session: Peyton owns migrations and delegated
contracts/runtime. Jack OC remains the human integrator after handoff.
No external claims/comments are posted; current issue access returns 404.

Verification: stdlib unittest, independent fixed-cent ledgers, duplicate/overlap/
correction rollback, malformed rows, timezone boundaries, wrong-period/currency,
archive tampering, source lineage, last-good retention, inventory completeness,
contract response validation, HTTP API and exact portal-download integration.
Retain command outputs in reports/integration/logs/.

Runtime found: Python 3.9.6; Node is absent. Reuse existing Python runtime with
local SQLite, no new paid service. Document this deliberate prototype-stack
choice and React UI integration points instead of claiming Node/Postgres tests.
Supervised sequential work only, checkpoint within 60 minutes per unit and at
most two repairs; no spend cap supplied, no unattended runner authorized.

Human integration/independent QA remains pending. Prepare a reviewable local
handoff and tell Peyton when to push; do not push or merge automatically.
