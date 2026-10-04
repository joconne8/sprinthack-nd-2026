# GOV-04 / ENG-01 local architecture decision

Decision for this authorized combined implementation: Python standard library,
SQLite, local content-addressed raw files, and a loopback JSON API. This replaces
the packet's default Node/Postgres suggestion for the prototype. Python 3.9.6 is
present; Node is absent. Existing portal and acquisition implementations are
Python. No second application or paid infrastructure is introduced.

Peyton reported Jack OC's delegation in chat and requested both lanes be built.
That allows this local implementation decision; it is not client/provider
approval or independent test acceptance. Jack OC's GOV-01/02 proposals are reused
from commit `38120523f60ff9cc0f888146b9450be5be74f674` without merging branches.
Primary Drive access remains unavailable; evidence assertions retain the local
source-register/traceability qualifications.

```text
Existing synthetic portal / verified acquisition run
             ↓ exact bytes + manifest
Immutable raw archive → typed/rejected staging → reconcile
                                               ↓ one transaction
                                   versioned sale facts → metric snapshot
                                               ↓
                                       JSON API → Landon's UI
```

Lineage, source-specific keys, as-of refunds, integer cents, audit history and
last-good publication are implemented. An ordinary query reads immutable run
rows; no claim is made that an ordinary view stores results. SQLite is local
prototype storage, not approval of a production warehouse.

React or another UI can use the same API. Landon owns operations/leadership/
drilldown screens; this session does not replace his application lane. TypeScript
contracts are supplied; completion evidence now includes strict TypeScript
compilation and the unchanged skill in a separate Node/Playwright/Chrome runtime.
Landon's product UI is still not implemented or accepted by this session.
Existing deterministic browser replay remains separate from model-assisted Jev.

Production evaluation should first consider approved file delivery → governed
Power Query/master workbook → existing Power BI. A managed SQL layer is justified
only if measured history, reconciliation, concurrency and access requirements
cannot be met there. Excel is not disqualified by an invented row limit.
Goodwill must designate maintenance/rule/security owners; no staffing cost is
assumed. No database/model/dashboard purchase is required by this decision.

## GOV-04 proposal reconciliation and production comparison

Reviewed Jack OC's GOV-04 proposal `49ac1ad` against merged foundation `610035e`.
Its repo-native Python/SQLite choice, bridge-first production path and conditional
managed storage agree with this implementation. Preserve the actual Python 3.9+
API prerequisites; the proposal's Python 3.10+ and static dashboard describe a
proposed runtime, not an already installed frontend. Landon chooses and builds
the UI in his lane against this API. Browser replay is a separate Node/Playwright
runtime, never evidence that a web host supports browser jobs.

| Control | Approved folder / Power Query / existing Power BI | Managed relational layer |
|---|---|---|
| Setup and cost | Reuses paid-for Microsoft tools; validate actual licenses/refresh path | Requires IT-approved hosting, cost and operational ownership |
| Raw evidence | Retain source files plus manifest/hash/row identifiers | Retain the same archive and row lineage; database alone is insufficient |
| Reconciliation/corrections | Explicit query controls and governed workbook history | Constraints, transactions and versioned facts support auditable changes |
| Concurrency/access | Existing workspace permissions, checked in pilot | Governed identities/roles and tested access boundaries |
| Support | Named workbook/query and Power BI owners | Named platform, rule and incident owners |
| Decision trigger | First production bridge, subject to partner approval | Pilot evidence of unmet lineage/history/concurrency/access/refresh requirements |

A managed service is considered only when a measured gap and named owners justify
it. No universal Excel row threshold or assumed support salary is a decision
criterion. Production leadership stays in existing Power BI until assessed; the
weekend custom application demonstrates the reporting flow and operations needs.

Production process ownership is Amanda with assistant responsibilities unverified;
IT/platform, finance/rule steward and support escalation people are unassigned.
Tenant identities, provider permission, browser session ownership, retention and
Microsoft/finance handoffs remain gates in `reports/GOV-04/approval-gaps.md`.
An approved Copilot route is required before production AI. Jev is optional
probabilistic discovery; model-free replay is the synthetic baseline. Neither is
permission to use a live session. Changes are reviewed and rollback retains the
matching SQLite backup and immutable raw archive.
