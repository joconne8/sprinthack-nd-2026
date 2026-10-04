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
contracts are supplied but Node/type/build/browser checks remain unrun here.
Existing deterministic browser replay remains separate from model-assisted Jev.

Production evaluation should first consider approved file delivery → governed
Power Query/master workbook → existing Power BI. A managed SQL layer is justified
only if measured history, reconciliation, concurrency and access requirements
cannot be met there. Excel is not disqualified by an invented row limit.
Goodwill must designate maintenance/rule/security owners; no staffing cost is
assumed. No database/model/dashboard purchase is required by this decision.
