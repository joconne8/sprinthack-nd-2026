# Goodwill — five-person VS Code / Codex assignment guide

## Current Hugh/Landon takeover

Peyton explicitly authorized taking over Hugh and Landon's remaining core work
while Jack mc finishes independent QA. Branch `peyton/acquisition-dashboard` is
based on merged main `7f94806`. ING-02/03/04/05 and APP-01/02/03 now have
implementation and review artifacts; see [handoff](../../reports/takeover/RESULT.md)
and [exact verification](../../reports/takeover/verification.json).

The app serves real operations, leadership and source-evidence screens and wires
synthetic acquisition to verified import/publication. The targeted developer
checks pass. Jack mc retains his acceptance tests, expected results and ENG-04
reports. His deliberate dashboard placeholder is the single full-suite failure;
independent UI acceptance and human ENG-05/REL-01 integration/freeze remain.

This handoff supersedes older missing-UI/backend and separate Hugh/Landon lane
statements below. It does not assert human acceptance or GitHub issue closure.
Optional exports, APP-04–07 assistant work, ING-06 Jev and ING-07 live/pilot
work remain deferred under frozen scope. Nine-source live owners/access still
need confirmation. The older allocation table is retained as the original plan.

## Current combined-lane handoff

The shared foundation is merged into main at `610035e` (PR #52), after the
historical package check below. Peyton's authorized combined completion branch
is `peyton/jackoc-data-completion`. See
[current task-by-task status](../../reports/integration/completion-status.md),
[verification](../../reports/integration/completion-verification.json) and
[runtime/API guide](../../planning/development.md). This is implementation
delivery status, not human acceptance or verified GitHub issue closure.

GOV-01–04, ENG-01/02 and DAT-01–09 have review artifacts and regression evidence.
The old GOV-03/GOV-04 branch proposals are reconciled with the merged API; use
`goodwill-v1`. Final ENG-05 integration/freeze still needs Landon's APP-01/02/03
UI and Jack mc's independent ENG-04 evidence. Acquisition source mapping and
automated submission stay in Hugh's lane. Several older reports mention missing
contracts/backend or unmerged PRs; those statements describe their original base.

## Historical status and source verification

Reviewed against authorized GitHub `main` on **October 4, 2026**, commit
`3b5060fe91229a89b6556d9332ddbaff892699c3`. This is a documentation-only ownership
proposal for **Jack OC, Hugh, Peyton, Landon, and Jack mc**. Jack OC must confirm
the allocation, resolve the existing acquisition contribution, and record
accepted dependencies before coding starts. Publication is not an issue claim,
scope approval, task acceptance, agent launch, merge, or production authorization.

The earlier unauthenticated 404 is superseded: authorized repository access
succeeded. The recursive tree was complete; all **57 assignment-package files**
matched the uploaded `GOODWILL_READY_TO_RUN_AGENT_ASSIGNMENTS` archive by Git blob
hash. The current manifest/index contain **36 execution packets and 7 coordination
packets**. All 43 corresponding issues were open and had no GitHub assignees;
the repository-wide issue-comment response was empty and neither list was
paginated. This does **not** establish that no work has begun.

Important current work:

- [Synthetic-data PR #1](https://github.com/joconne8/sprinthack-nd-2026/pull/1)
  is merged, at `2026-10-04T00:13:02Z`, and its fixtures are on main.
  DAT-01 validates those fixtures; do not recreate or re-merge them.
- [Draft acquisition PR #45](https://github.com/joconne8/sprinthack-nd-2026/pull/45)
  is open, unmerged, and had no submitted reviews at this check. Its branch,
  `codex/reporting-decoy`, contains `reports/ING-01/CLAIM.md` reserving
  `data ingestion/**` and `reports/ING-01/**`, plus reported verification.
  Its claim explicitly does not assert GOV-03/ENG-01 acceptance. **Hugh and
  Jack OC must coordinate review/reuse with that contributor before ING-01 edits.**
  Do not override this existing reservation or infer the contributor's identity
  from the five display names. The reported tests were inspected, not rerun here.
- That PR uses a separate generated dataset and different dates/grain/manifest
  from the August merged fixtures and the Replit foundation. It is not an
  accepted importer handoff. Review compatibility and an explicit adapter
  through GOV-03 before adopting it; do not silently mix datasets or duplicate
  its replica/replay work.
- Current source `main` contains planning and Python synthetic fixtures, but no
  application dependency/runtime manifest, accepted-task evidence record, or
  merged feature scaffold was found in its tree. The Replit foundation is a
  separate working implementation, not automatically present in these local
  clones. Jack OC must select and record one accepted baseline/scaffold, not
  ask each teammate to create an application.

Read the current [index](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/INDEX.md),
[launch guide](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/LAUNCH_GUIDE.md),
[root instructions](https://github.com/joconne8/sprinthack-nd-2026/blob/main/AGENTS.md),
and [source register](https://github.com/joconne8/sprinthack-nd-2026/blob/main/planning/project-management/DRIVE_SOURCE_REGISTER.md).
Primary Drive evidence and current accepted decisions govern; legacy dashboard-first
scope does not override them. This guide checks assignment sources, not a fresh
review of every linked Drive document. Recheck issues, PRs, comments and accepted
commits before each packet; this dated observation is not live status.

## Team summary

| Person | Responsibility | Coordination | Core weekend order | Optional / later |
|---|---|---|---|---|
| Jack OC | Scope, contracts, scaffold, human integration | PM-00, E-GOV | GOV-01 → GOV-02 → GOV-03; GOV-04; ENG-01/02; ENG-05 at integration | Support other lanes' scope decisions |
| Hugh | Acquisition and replay | E-ING | ING-05; review existing ING-01 contribution → ING-02 → ING-03 | ING-04 P1 weekend; ING-06 stretch; ING-07 pilot |
| Peyton | Fixture validation, ingestion, reconciliation, metrics | E-DAT | DAT-01; DAT-02 → DAT-03 → DAT-04 → DAT-05 → DAT-06 → DAT-08 | DAT-07 P1 weekend; DAT-09 pilot |
| Landon | Operations/leadership UI and source evidence | E-APP | APP-01, APP-02 → APP-03 drilldown | APP-03 exports P1; APP-04–06 stretch; APP-07 pilot |
| Jack mc | Independent acceptance and demo/release evidence | E-ENG, E-REL | ENG-04; REL-01 after integrated acceptance | ENG-03 P1 weekend; REL-02–04 pilot |

Arrows describe lanes, not every hard dependency. The full register below retains
all dependencies. Coordination is organizational work, not seven extra coding jobs.
Named primary owners are recommended accountability, not modifications to existing
GitHub assignees or authority to replace a claim.

## Jack OC — lead and shared setup

**Own:** PM-00 delivery/status; E-GOV requirements coordination; GOV-01 stakeholder
requirements/process; GOV-02 scope/KPIs; GOV-03 contracts; GOV-04 architecture/security;
ENG-01 scaffold/smoke baseline; ENG-02 claims/reservations; human-led ENG-05 integration/freeze.

**Start:** Check current claims and accepted work, then GOV-01 or its outstanding
evidence. Review PR #45 with its contributor and Hugh before reserving acquisition
paths. Reuse accepted foundation work rather than reconstructing it.

**Exclusive shared ownership:** Contracts/generated interfaces, manifests/lockfiles,
global configuration, runtime commands, app entrypoints, route registration,
shared status and human integration. Codex proposes patches; it cannot accept or
merge its own output.

**Handoff:** Accepted baseline commit and dependency commits, approved fixtures,
contract/metric version, exact allowed paths, actual runtime/test commands, human
reviewer, deadline and spend cap. Reservation proposals in packets must be mapped
to that actual scaffold before anyone edits.

**Paste alongside one eligible packet:**
> I am Jack OC. My lane is PM-00, E-GOV, GOV-01–04, ENG-01–02 and human-led ENG-05. Read current index, launch guide, AGENTS.md, source context and issue claims. Identify accepted work and the existing acquisition PR before proposing edits. Begin with one eligible packet. Coordinate contracts/generated types, manifests/lockfiles, entrypoints, routes, runtime configuration and shared status in my lane. Stop for missing evidence/approval. Do not autonomously approve or merge output.

## Hugh — acquisition

**Own:** E-ING coordination; ING-01 screenshot-informed synthetic replica; ING-02
date/report-parameterized browser replay; ING-03 file verification/intake; ING-04
bounded retries/run state/manual fallback/scheduler design; ING-05 nine-source
acquisition-class mapping; ING-06 optional Jev evaluation; ING-07 macro/repair design.

**Start:** Coordinate the existing PR #45 claim first, without rewriting it.
ING-05 needs GOV-01/GOV-03; ING-01 needs GOV-03/ENG-01. ING-02 follows accepted
ING-01. ING-03 additionally waits for DAT-02. Mapping sources is documentation,
not nine live integrations.

**Boundary:** Only lead-reserved acquisition/replica/source-map modules and tests.
PR #45's `data ingestion/**` remains reserved to its current contributor until an
explicit handoff. No migrations, global shell/routes, contracts or lockfile edits.

**Handoff to Peyton:** Exact downloaded bytes and frozen manifest: run/source/report
identity, requested dates/timezone, checksum/byte size, artifact reference,
download time, synthetic label/version, and reproducible success/failure evidence.
Success means a verified acquired file, not published metrics.

**Paste alongside one eligible packet:**
> I am Hugh. My lane is E-ING and ING-01–07, prioritizing ING-01–03 and ING-05. Read current claims and coordinate PR #45 review/reuse with Jack OC and its contributor before edits. Execute one eligible packet in reserved paths. Build only approved synthetic acquisition; never claim live Upright compatibility. Preserve exact bytes and contract-compliant provenance for Peyton. Propose shared API changes to Jack OC. No Jev, live access or pilot work without approval. Return actual logs and blockers.

## Peyton — trusted data

**Own:** E-DAT; DAT-01 existing-fixture validation; DAT-02 immutable archive/batches/
lineage; DAT-03 parsing/normalization; DAT-04 duplicates/overlaps/corrections;
DAT-05 reconciliation/exceptions; DAT-06 deterministic metrics/versioned API;
DAT-07 listing/inventory metrics; DAT-08 completeness/freshness/last-good;
DAT-09 DAG/backfill/performance design.

**Start:** DAT-01 after GOV-02, validating merged PR #1, not generating a competing
dataset. DAT-02 needs GOV-03/ENG-01; DAT-03 needs both DAT-01 and DAT-02.
Continue through the accepted dependencies.

**Boundary:** Lead-reserved ingestion/data/backend modules and tests. **Sole
migration owner: Peyton.** Jack OC still owns shared API schemas/generated clients,
registration and dependencies. Do not adapt PR #45's separate dataset without a
reviewed contract decision.

**Handoff to Landon:** Reviewed metric/coverage/reconciliation/evidence responses,
source rows reconciling to totals, and explicit missing/error states. Money uses
deterministic decimal/minor-unit arithmetic. Demo net sales = item sales − refunds,
excluding shipping, tax and fees; missing inputs are unavailable, never zero.

**Paste alongside one eligible packet:**
> I am Peyton. My lane is E-DAT and DAT-01–09, prioritizing DAT-01–06 and DAT-08. Validate merged fixtures first; execute one eligible packet with accepted dependencies. Preserve immutable raw bytes and row lineage. Test duplicates, overlaps, corrections, rejected rows, reconciliation and last-good behavior. Missing inputs stay unavailable. I alone own migrations; Jack OC coordinates contracts/generated types/shared registration. Return actual commands/logs, independent expected-versus-actual results and blockers.

## Landon — application

**Own:** E-APP; APP-01 operations intake/status; APP-02 leadership/KPI availability;
APP-03 P0 source-row drilldown (exports optional P1); APP-04 read-only permission-
scoped tools; APP-05 grounded assistant; APP-06 assistant safety evaluation;
APP-07 Microsoft production-integration validation.

**Start:** APP-01 and APP-02 sequentially after GOV-03/ENG-01, using approved
contract fixtures during development. APP-03 final wiring requires DAT-06,
DAT-08 and APP-02 acceptance.

**Boundary:** Lead-reserved views/components and tests. Not Hugh's replica,
migrations, global routes/shell, generated types, dependencies or contracts.
Final demo uses actual local APIs, not silent mock fallback or separate frontend
financial calculations. Exports/tools/assistant/production work need explicit approval.

**Handoff to Jack mc:** Reproducible period selection, run/import status, metrics,
source-row evidence, coverage warnings, and loading/empty/error flows. Role views
do not imply real access control unless signed-in roles are separately accepted.

**Paste alongside one eligible packet:**
> I am Landon. My lane is E-APP and APP-01–07, prioritizing APP-01–03 drilldown. Work one eligible packet in reserved UI paths. Use frozen contracts and approved fixtures during development, never silently replace failing APIs with mocks. Show synthetic labels, missing inputs, coverage and errors honestly. Financial values come from Peyton's published API. Coordinate shared changes with Jack OC. Defer exports, tools, assistant and production integration until approved.

## Jack mc — independent QA and demo

**Own:** E-ENG testing coordination (Jack OC retains scaffold/integration); E-REL;
ENG-03 runner limits/cancellation/reporting design; ENG-04 independent acceptance;
REL-01 source-backed pitch/recorded backup/honest evidence; REL-02 workbook parity/
gated financial validation plan; REL-03 evidenced conservative ROI; REL-04 pilot/
support/handover plan.

**Start:** Read acceptance requirements and prepare a non-code checklist. ENG-04
implementation needs GOV-03/DAT-01/ENG-01; final end-to-end checks need real lane
outputs. REL-01 needs ENG-05/APP-03. Independently derive expected results, rather
than copying Peyton's implementation.

**Boundary:** Reserved independent tests, expected-result fixtures and own reports/
demo docs. Packet proposals include `tests/acceptance/`, `fixtures/expected-results/`
and `reports/ENG-04/`; confirm the actual mapping first. Do not change feature
code, source fixtures, contracts, migrations or lockfiles to force passing tests.
If you contributed a feature under review, disclose that and have Jack OC designate
a different independent checker for that feature.

**Handoff to Jack OC:** Exact-file continuity, alternate dates, repeat/overlap
imports, malformed/wrong-period inputs, reconciliation, source-row sums, missing
coverage and last-good pass/fail evidence. Do not assert production readiness.
ENG-04 currently mentions export in its demo sequence although APP-03 export is P1:
Jack OC must record whether export is deferred or required before QA acceptance;
do not silently waive the packet or make optional export block the P0 demo.

**Paste alongside one eligible packet:**
> I am Jack mc. My lane is E-ENG, E-REL, ENG-03–04 and REL-01–04. Prioritize independent ENG-04 evidence and REL-01 preparation. Start coding only with accepted dependencies. Derive expected values independently. Disclose any feature contribution that affects reviewer independence. Do not edit another lane's implementation to force tests to pass. Return defects to owners and evidence to Jack OC. Runner automation/pilot work require approval; no autonomous merges, deployment or fabricated ROI.

## Local VS Code / Codex setup

Each person uses their own authorized clone or worktree, branch, and Codex session,
all targeting **one product/repository**, not five applications. GitHub access,
Git, VS Code (`code` command optional), and Python **3.10+** for fixture tests are
required. Python 3.13.11 was available for this guide's selector checks.

```bash
git clone https://github.com/joconne8/sprinthack-nd-2026.git
cd sprinthack-nd-2026
git fetch origin
git switch main
git pull --ff-only
code .
python3 --version
python3 ProjectManagement/agent-assignments/select_assignment.py --list
# Inspect the first requirements packet; this does not approve or launch work.
python3 ProjectManagement/agent-assignments/select_assignment.py GOV-01
```

If `code` is unavailable, open the folder in VS Code. If Python is unavailable,
open the Markdown packet directly, but do not waive dependencies. Do not guess
`npm`, `pnpm`, database or application startup commands: read the accepted ENG-01
runtime guide and actual manifests after the lead's scaffold is integrated.
The verified existing fixture command, from repository root, is:

```bash
python3 -m unittest discover -s goodwill/synthetic-data -p 'test_*.py' -v
```

That tests fixtures, not importer/UI correctness. Do not run `generate.py` merely
to start: it overwrites CSVs/manifest. PR #45's optional runtime instructions are
branch-specific and not valid on current main.

For each eligible packet, branch from a baseline containing accepted prerequisites.
Example for Hugh, **only after ING-01 review/claim resolution and dependencies**:

```bash
git switch main
git pull --ff-only
git rev-parse HEAD
# For EACH actual dependency commit from the reviewed acceptance record:
# git merge-base --is-ancestor <actual-accepted-commit> HEAD
# A nonzero result means STOP; do not auto-merge missing dependencies.
git switch -c hugh/ING-01
python3 ProjectManagement/agent-assignments/select_assignment.py ING-01 \
  --acceptance /absolute/path/to/reviewed-acceptance.json
```

Use a unique task branch if one already exists. The acceptance record must use
real human-reviewed evidence, not the empty example. `accepted_tasks` maps IDs to
`accepted: true`, reviewer, full 40-character `accepted_commit`, non-empty evidence
and tests arrays; each test has command, `result: "pass"` and log.
The selector validates **structure only**, not identity, artifact truth, ancestry,
test execution, deadlines, budgets or actual approval.

Missing acceptance exits **2** with BLOCKED. `--emit-blocked` prints a review copy
and still exits 2; it cannot clear a gate. No selector invocation launches an agent,
changes Git or posts external messages.

Copy the emitted packet plus your lane prompt into **one Codex session rooted in
that checkout**. Keep one execution packet per session. Before edits, use
[CLAIM_TEMPLATE.md](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/templates/CLAIM_TEMPLATE.md)
to record operator, task/issue, branch/base, exact paths, dependencies/versions,
tests/independent expectations, deadline, reviewer and approved spend cap. Read
current comments and branch-local claims; Jack OC resolves collisions. Any external
claim message must be explicitly authorized and sent by the actual operator, not
automatically posted or impersonated by this guide.

Return a commit/PR for human review with changed files, actual commands and logs,
pass/fail, artifacts, contract version, limits, tests not run and blockers. Use
[RESULT_TEMPLATE.md](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/templates/RESULT_TEMPLATE.md)
and `reports/<TASK-ID>/`. Do not concurrently edit shared status. Pull accepted
changes between packets, not mid-task without reviewing their impact.

## Full packet ownership and dependency register

This is the single primary-owner register: **9 Jack OC + 8 Hugh + 10 Peyton +
8 Landon + 8 Jack mc = 43**. Packet and issue links were verified against current
main/issue records. P1 weekend is optional after core acceptance; stretch/pilot
needs explicit approval. Even P0 work must satisfy dependency and human gates.

| Packet | Primary owner | Issue | Priority / scope | Hard dependencies |
|---|---|---|---|---|
| [PM-00](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/PM-00.md) | Jack OC | [#7](https://github.com/joconne8/sprinthack-nd-2026/issues/7) | P0 / weekend coordination | None |
| [E-GOV](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-GOV.md) | Jack OC | [#4](https://github.com/joconne8/sprinthack-nd-2026/issues/4) | P0 / weekend coordination | None |
| [E-ING](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-ING.md) | Hugh | [#2](https://github.com/joconne8/sprinthack-nd-2026/issues/2) | P0 / weekend coordination | None |
| [E-DAT](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-DAT.md) | Peyton | [#8](https://github.com/joconne8/sprinthack-nd-2026/issues/8) | P0 / weekend coordination | None |
| [E-APP](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-APP.md) | Landon | [#6](https://github.com/joconne8/sprinthack-nd-2026/issues/6) | P0 / weekend coordination | None |
| [E-ENG](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-ENG.md) | Jack mc | [#5](https://github.com/joconne8/sprinthack-nd-2026/issues/5) | P0 / weekend coordination | None |
| [E-REL](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/coordination/E-REL.md) | Jack mc | [#3](https://github.com/joconne8/sprinthack-nd-2026/issues/3) | P0 / weekend coordination | None |
| [GOV-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/GOV-01.md) | Jack OC | [#13](https://github.com/joconne8/sprinthack-nd-2026/issues/13) | P0 / weekend | None |
| [GOV-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/GOV-02.md) | Jack OC | [#11](https://github.com/joconne8/sprinthack-nd-2026/issues/11) | P0 / weekend | GOV-01 |
| [GOV-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/GOV-03.md) | Jack OC | [#15](https://github.com/joconne8/sprinthack-nd-2026/issues/15) | P0 / weekend | GOV-02 |
| [GOV-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/GOV-04.md) | Jack OC | [#9](https://github.com/joconne8/sprinthack-nd-2026/issues/9) | P0 / weekend | GOV-01, GOV-02 |
| [ING-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-01.md) | Hugh | [#14](https://github.com/joconne8/sprinthack-nd-2026/issues/14) | P0 / weekend | GOV-03, ENG-01 |
| [ING-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-02.md) | Hugh | [#16](https://github.com/joconne8/sprinthack-nd-2026/issues/16) | P0 / weekend | ING-01, GOV-03 |
| [ING-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-03.md) | Hugh | [#17](https://github.com/joconne8/sprinthack-nd-2026/issues/17) | P0 / weekend | ING-02, DAT-02, GOV-03 |
| [ING-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-04.md) | Hugh | [#10](https://github.com/joconne8/sprinthack-nd-2026/issues/10) | P1 / weekend | ING-03, DAT-08 |
| [ING-05](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-05.md) | Hugh | [#12](https://github.com/joconne8/sprinthack-nd-2026/issues/12) | P0 / weekend | GOV-01, GOV-03 |
| [ING-06](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-06.md) | Hugh | [#18](https://github.com/joconne8/sprinthack-nd-2026/issues/18) | P1 / stretch | ING-02, GOV-04 |
| [ING-07](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ING-07.md) | Hugh | [#28](https://github.com/joconne8/sprinthack-nd-2026/issues/28) | P2 / pilot | ING-02, ING-05, GOV-04 |
| [DAT-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-01.md) | Peyton | [#25](https://github.com/joconne8/sprinthack-nd-2026/issues/25) | P0 / weekend | GOV-02 |
| [DAT-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-02.md) | Peyton | [#22](https://github.com/joconne8/sprinthack-nd-2026/issues/22) | P0 / weekend | GOV-03, ENG-01 |
| [DAT-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-03.md) | Peyton | [#27](https://github.com/joconne8/sprinthack-nd-2026/issues/27) | P0 / weekend | DAT-01, DAT-02 |
| [DAT-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-04.md) | Peyton | [#19](https://github.com/joconne8/sprinthack-nd-2026/issues/19) | P0 / weekend | DAT-03 |
| [DAT-05](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-05.md) | Peyton | [#26](https://github.com/joconne8/sprinthack-nd-2026/issues/26) | P0 / weekend | DAT-03, DAT-04 |
| [DAT-06](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-06.md) | Peyton | [#23](https://github.com/joconne8/sprinthack-nd-2026/issues/23) | P0 / weekend | DAT-05, GOV-03 |
| [DAT-07](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-07.md) | Peyton | [#24](https://github.com/joconne8/sprinthack-nd-2026/issues/24) | P1 / weekend | DAT-01, DAT-02, DAT-06 |
| [DAT-08](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-08.md) | Peyton | [#20](https://github.com/joconne8/sprinthack-nd-2026/issues/20) | P0 / weekend | DAT-05, DAT-06 |
| [DAT-09](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/DAT-09.md) | Peyton | [#21](https://github.com/joconne8/sprinthack-nd-2026/issues/21) | P1 / pilot | DAT-08, GOV-04 |
| [APP-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-01.md) | Landon | [#38](https://github.com/joconne8/sprinthack-nd-2026/issues/38) | P0 / weekend | GOV-03, ENG-01 |
| [APP-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-02.md) | Landon | [#32](https://github.com/joconne8/sprinthack-nd-2026/issues/32) | P0 / weekend | GOV-03, ENG-01 |
| [APP-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-03.md) | Landon | [#34](https://github.com/joconne8/sprinthack-nd-2026/issues/34) | P0 / weekend | DAT-06, DAT-08, APP-02 |
| [APP-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-04.md) | Landon | [#35](https://github.com/joconne8/sprinthack-nd-2026/issues/35) | P1 / stretch | DAT-06, DAT-08, GOV-04 |
| [APP-05](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-05.md) | Landon | [#29](https://github.com/joconne8/sprinthack-nd-2026/issues/29) | P1 / stretch | APP-04, GOV-04 |
| [APP-06](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-06.md) | Landon | [#31](https://github.com/joconne8/sprinthack-nd-2026/issues/31) | P1 / stretch | APP-04, APP-05, ENG-04 |
| [APP-07](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/APP-07.md) | Landon | [#36](https://github.com/joconne8/sprinthack-nd-2026/issues/36) | P2 / pilot | GOV-04, APP-04 |
| [ENG-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ENG-01.md) | Jack OC | [#33](https://github.com/joconne8/sprinthack-nd-2026/issues/33) | P0 / weekend | GOV-02, GOV-04 |
| [ENG-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ENG-02.md) | Jack OC | [#37](https://github.com/joconne8/sprinthack-nd-2026/issues/37) | P0 / weekend | GOV-03 |
| [ENG-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ENG-03.md) | Jack mc | [#30](https://github.com/joconne8/sprinthack-nd-2026/issues/30) | P1 / weekend | ENG-01, ENG-02, ING-03, DAT-06 |
| [ENG-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ENG-04.md) | Jack mc | [#42](https://github.com/joconne8/sprinthack-nd-2026/issues/42) | P0 / weekend | GOV-03, DAT-01, ENG-01 |
| [ENG-05](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/ENG-05.md) | Jack OC | [#44](https://github.com/joconne8/sprinthack-nd-2026/issues/44) | P0 / weekend | ENG-04, ING-03, DAT-08, APP-01, APP-02 |
| [REL-01](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/REL-01.md) | Jack mc | [#43](https://github.com/joconne8/sprinthack-nd-2026/issues/43) | P0 / weekend | ENG-05, APP-03 |
| [REL-02](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/REL-02.md) | Jack mc | [#41](https://github.com/joconne8/sprinthack-nd-2026/issues/41) | P2 / pilot | GOV-01, DAT-05, GOV-04 |
| [REL-03](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/REL-03.md) | Jack mc | [#40](https://github.com/joconne8/sprinthack-nd-2026/issues/40) | P1 / pilot | GOV-01, ING-04 |
| [REL-04](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/tasks/REL-04.md) | Jack mc | [#39](https://github.com/joconne8/sprinthack-nd-2026/issues/39) | P2 / pilot | GOV-04, ING-05, DAT-09, APP-07, REL-03 |

## Execution and approval gates

1. **Agree one baseline.** Jack OC checks scope, existing claims/PRs and accepts or
   reuses GOV-01–04/ENG-01–02 outputs. Peyton validates DAT-01 after GOV-02.
   Reading packets/preparing questions is allowed before implementation eligibility.
2. **Verify a supervised thin slice.** One acquired file must reach verification,
   import/reconciliation and a displayed total before unattended feature work.
   Five isolated passing tasks are not integration evidence.
3. **Run at most three concurrent build sessions.** Acquisition, data and UI use
   frozen interfaces and disjoint exact paths. Lead coordination and non-code QA
   preparation are separate. A QA coding session consumes a build slot: serialize
   it with a feature lane unless humans explicitly update the concurrency policy.
4. **Respect cross-lane handoffs.** ING-03 needs DAT-02; APP-03 needs DAT-06/DAT-08.
   A download is not publication, a fixture is not an API, and a placeholder is
   not accepted completion.
5. **Human integration/freeze.** Jack OC reviews and integrates in dependency order
   under ENG-05. Jack mc provides independent acceptance and REL-01's recorded
   backup after ENG-05/APP-03. Confirm the event deadline with organizers; no
   date/time is inferred as current authorization.
6. **Optional work only after P0 passes.** Nine-source mapping is not nine revenue
   feeds. No assistant, export, extra source or recorder should displace the core
   controls. Pilot packets draft reviewed plans; they do not permit live execution.

**Stop and report BLOCKED** on missing acceptance/contracts, conflicting edits,
failed checks, contradictory evidence, financial disagreement, provider denial,
or exhausted time/spend. Suggested checkpoint: 60 minutes per packet, 90 for
ENG-04, at most two repair attempts. These are instruction limits, not automatic
enforcement. Unattended execution requires verified deadline/budget/cancellation
controls, per-task and total caps, and named human reviewers; otherwise supervise.

No live credentials/data, paid services, vendor restriction bypass, autonomous
merges, deployment, external messaging, or accounting posting is authorized here.
No issue claims or agents are started by publishing this guide. Human team
allocation confirmation, exact file reservations, baseline acceptance and existing
PR review remain explicit gates rather than fabricated completion claims.
