# AGENT DIVIDING

#6 - Five-Person Codex Assignment Plan

## What & Why

Divide the Goodwill assignment packets among Jack OC, Hugh, Peyton, Landon, and Jack mc so each person can work in their own local VS Code checkout and Codex session without duplicating work or conflicting on shared files. Publish this document in the source repository as ProjectManagement/agent-assignments/TEAM_ASSIGNMENTS.md after verifying the current packets.

Source limitation: The supplied GitHub URL returned HTTP 404 during this review. This draft is based on the uploaded GOODWILL_READY_TO_RUN_AGENT_ASSIGNMENTS snapshot, specifically its INDEX, LAUNCH_GUIDE, agent instructions, and ENG-04 packet. It covers all 36 execution packets and seven coordination packets in that snapshot. Current repository contents, issue claims, accepted changes, and team decisions must be checked before execution. Do not treat snapshot task ownership or completion claims as current facts.

Recommended ownership: This allocation follows workstreams, not assumptions about anyone's experience. Each packet has one primary owner. Coordination packets organize work; they are not additional coding assignments. Owning a packet does not authorize production access or bypass its prerequisites.

## Done looks like

- All five teammates can identify their assignments and start the next eligible packet in their own VS Code/Codex session.
- All 43 snapshot packets have one owner, with weekend priorities separated from optional/pilot work.
- Shared contracts, migrations, runtime configuration, and integration each have a single accountable owner.
- The repository contains a reviewed TEAM_ASSIGNMENTS.md with current task links, setup instructions, handoffs, and approval gates.
- No agents are launched, issue claims posted, or application tasks duplicated merely by publishing this document.

## Out of scope

- Implementing the application or starting the existing Replit build tasks.
- Assuming all 36 execution packets must be completed for the demo.
- Live vendor credentials, production data, paid services, autonomous merging, deployment, or accounting posting.
- Changing accepted task scope, financial definitions, or existing issue ownership without human review.

## Team assignment summary

| Person | Primary responsibility | Coordination packets | Weekend first / core sequence | Optional or later packets |
| --- | --- | --- | --- | --- |
| Jack OC | Team lead, scope/contracts, shared scaffold, human integration | PM-00, E-GOV | GOV-01 -> GOV-02 -> GOV-03; GOV-04; ENG-01, ENG-02; ENG-05 at integration | None; support scope decisions for other lanes |
| Hugh | Report acquisition and browser replay | E-ING | ING-05 source mapping; ING-01 -> ING-02 -> ING-03 | ING-04 is P1 weekend; ING-06 stretch; ING-07 pilot |
| Peyton | Synthetic-fixture validation, ingestion, reconciliation, metrics | E-DAT | DAT-01; DAT-02 -> DAT-03 -> DAT-04 -> DAT-05 -> DAT-06 -> DAT-08 | DAT-07 is P1 weekend; DAT-09 pilot |
| Landon | Operations and leadership UI, metric evidence drilldown | E-APP | APP-01, APP-02 -> APP-03 source-row drilldown | APP-03 exports are P1; APP-04-06 stretch; APP-07 pilot |
| Jack mc | Independent acceptance tests, demo evidence, release preparation | E-ENG, E-REL | ENG-04; REL-01 after integrated acceptance | ENG-03 is P1 weekend; REL-02-04 pilot |

The arrows summarize each lane, not every hard dependency. The individual packet remains authoritative. For example, ING-03 also needs DAT-02, APP-03 needs DAT-06 and DAT-08, and REL-01 needs ENG-05 and APP-03.

## Jack OC - lead and shared setup

Own these packets:

- PM-00 - delivery coordination and shared status.
- E-GOV - requirements and frozen-contract coordination.
- GOV-01 - stakeholder requirements and current-state process map.
- GOV-02 - accepted MVP scope and KPI definitions.
- GOV-03 - acquisition, import, metric, and agent-tool contracts.
- GOV-04 - architecture and live-access security gates.
- ENG-01 - one application scaffold and passing smoke-test baseline.
- ENG-02 - claims, file ownership, and shared-context protocol.
- ENG-05 - human review, dependency-order integration, and feature freeze.

Start with: Review current claims and accepted work, then GOV-01. Reuse accepted foundation/scaffold work rather than rebuilding it.

You alone coordinate changes to: shared contracts/generated interfaces, dependency manifests and lockfiles, app entrypoints, global route registration, and shared status. Codex may propose changes, but you perform the human integration review; ENG-05 is explicitly human-review work.

Handoff: Give everyone the accepted baseline commit, validated fixtures, contract version, exact allowed paths, actual runtime/test commands, and review criteria before feature implementation.

Paste into your Codex session:

```text
I am Jack OC, the lead for the Goodwill team. My lane is PM-00, E-GOV, GOV-01-04, ENG-01-02, and human-led ENG-05. Read the current assignment index, launch guide, repository instructions, and current issue claims. Identify already accepted work before proposing edits. Begin with the next eligible packet, not the entire lane at once. Reserve shared contracts, generated interfaces, manifests/lockfiles, entrypoints, route registration, and status changes to this lane. Stop for missing evidence or approvals. Do not merge or approve your own output autonomously.
```

## Hugh - acquisition

Own these packets:

- E-ING - acquisition coordination.
- ING-01 - supplied-slide review and functional Upright-style replica.
- ING-02 - deterministic browser replay with report/date parameters.
- ING-03 - acquired-file verification and importer handoff.
- ING-04 - bounded retries, run state, manual fallback, and scheduler design; P1 weekend.
- ING-05 - nine-source acquisition-class/adaptor mapping; documentation, not nine live integrations.
- ING-06 - optional Jev evaluation; stretch only.
- ING-07 - reviewed macro capture/repair design; pilot only.

Start with: ING-05 after GOV-01/GOV-03 acceptance, and ING-01 after GOV-03/ENG-01 acceptance. ING-02 follows the accepted replica. Wire ING-03 only when DAT-02 is accepted.

File boundary: Acquisition, replica, source mapping, and their tests in the exact paths Jack OC reserves. No data migrations, global application shell, contract edits, lockfiles, or shared route registration.

Handoff to Peyton: Exact downloaded CSV bytes plus the frozen file manifest, checksum, source/report identity, requested period, synthetic label, and reproducible acquisition/failure evidence.

Paste into your Codex session:

```text
I am Hugh. My lane is E-ING and ING-01-07, prioritizing ING-01-03 and ING-05. Read my next eligible packet and current claims before editing. Build only the approved synthetic replica/replay workflow; do not claim live Upright compatibility. Preserve real file bytes and contract-compliant provenance for Peyton. Coordinate shared API changes with Jack OC. Do not start Jev, live access, or macro/pilot work without explicit approval. Return actual test logs and blockers.
```

## Peyton - trusted data

Own these packets:

- E-DAT - data coordination.
- DAT-01 - validate the existing synthetic-data contribution; do not generate a competing dataset.
- DAT-02 - immutable raw archive, import batches, and row lineage.
- DAT-03 - parser and typed normalization.
- DAT-04 - file/record idempotency, overlapping exports, and corrections.
- DAT-05 - reconciliation and recoverable exceptions.
- DAT-06 - deterministic metric calculations and versioned API.
- DAT-07 - listing/inventory metrics; P1 weekend.
- DAT-08 - completeness, freshness, and last-good publication.
- DAT-09 - DAG, backfill, and performance design; pilot only.

Start with: DAT-01 after GOV-02 acceptance. DAT-02 needs GOV-03 and ENG-01. Then proceed through the accepted data dependencies. Verify the current synthetic-data PR state; the snapshot says it was merged, which has not been independently rechecked here.

File boundary: Assigned ingestion/data/backend modules and their tests. You are the sole migration owner. Jack OC owns shared API schema changes, generated clients, registration, and dependencies.

Handoff to Landon: Reviewed metric/coverage/reconciliation/evidence responses, explicit missing/error states, and source rows that reconcile to the published totals. Calculate money deterministically; demo net sales is item sales minus refunds, excluding shipping, tax, and fees.

Paste into your Codex session:

```text
I am Peyton. My lane is E-DAT and DAT-01-09, prioritizing DAT-01-06 and DAT-08. Validate existing fixtures first, then execute one eligible packet at a time with accepted dependencies. Preserve immutable raw evidence and row lineage. Test duplicates, overlaps, corrections, rejected rows, reconciliation, and last-good publication. Missing inputs must remain unavailable, not zero. I own migrations; coordinate contracts and shared registration with Jack OC. Return actual commands, logs, expected-versus-actual results, and blockers.
```

## Landon - application

Own these packets:

- E-APP - application coordination.
- APP-01 - intake and reporting-status operations view.
- APP-02 - leadership metrics and KPI availability scorecard.
- APP-03 - P0 source-row drilldown; Excel-compatible export is optional P1.
- APP-04 - permission-scoped read-only metric/provenance tools; stretch.
- APP-05 - grounded assistant; stretch.
- APP-06 - assistant injection/permission/unsupported-question evaluation; stretch.
- APP-07 - Copilot/Power BI production integration validation; pilot.

Start with: APP-01 and APP-02, sequentially in your lane, after GOV-03/ENG-01 acceptance. Develop against approved contract fixtures while Peyton builds. APP-03 final wiring waits for DAT-06/DAT-08 and APP-02.

File boundary: Assigned application views/components and their tests, not Hugh's replica, migrations, global routes, generated types, dependencies, or contracts.

Handoff to Jack mc: Reproducible UI flows showing period selection, run/import status, metrics, source evidence, coverage warnings, and loading/empty/error states. Final demo calls real local APIs; no silent mock fallback or separate frontend financial calculations.

Paste into your Codex session:

```text
I am Landon. My lane is E-APP and APP-01-07, prioritizing APP-01-03 source-row drilldown. Work one eligible packet at a time in the reserved application UI paths. Use frozen contracts and approved fixtures during development; do not silently replace failing APIs with mocks. Display synthetic labels, missing inputs, coverage, and errors honestly. Financial values come from Peyton's published API. Coordinate shared changes with Jack OC. Defer exports, tools, assistant, and production integration until explicitly approved.
```

## Jack mc - independent QA and demo

Own these packets:

- E-ENG - test/engineering coordination with Jack OC; Jack OC still owns scaffold and integration.
- E-REL - release/demo coordination.
- ENG-03 - runner budgets, timeouts, cancellation, and reporting design; optional P1 weekend.
- ENG-04 - independent expected totals and end-to-end acceptance tests.
- REL-01 - source-backed pitch, recorded demo, and honest submission evidence.
- REL-02 - workbook parity and gated financial-system validation plan; pilot.
- REL-03 - baseline/conservative ROI evidence; pilot, no invented savings.
- REL-04 - approved pilot/support/handover plan; pilot.

Start with: Read the acceptance requirements and prepare a non-code test checklist. ENG-04 implementation waits for GOV-03, DAT-01, and ENG-01 acceptance. Prepare expected results independently rather than deriving them from Peyton's implementation. REL-01 follows ENG-05 and APP-03 acceptance.

File boundary: Reserved independent test/evidence areas, task-specific reports, and demo documentation. Do not rewrite feature implementations, fixtures, contracts, migrations, or lockfiles to make tests pass. Report a defect to its lane owner.

Handoff to Jack OC: Independent pass/fail evidence for exact-file continuity, alternate dates, duplicate/overlap imports, malformed/wrong-period data, reconciliation, source-row totals, and last-good behavior. Help record the demo only after human acceptance; do not assert production readiness.

Paste into your Codex session:

```text
I am Jack mc. My lane is E-ENG, E-REL, ENG-03-04, and REL-01-04. Prioritize independent ENG-04 acceptance evidence and REL-01 demo preparation. Start implementation only after packet dependencies are accepted. Calculate expected values independently of the application. Do not edit another person's feature code to force passing tests. Return reproducible failures to the owner and acceptance evidence to Jack OC. Runner automation and pilot work are optional and require approval; no autonomous merges, deployment, or fabricated ROI.
```

## Working on your own VS Code and Codex

Each person uses a separate local clone or worktree and their own task branch. All clones target the same product/repository; do not create five independent applications.

Each teammate runs this on their own computer with GitHub access:

```powershell
git clone https://github.com/joconne8/sprinthack-nd-2026.git
cd sprinthack-nd-2026
git fetch origin
git switch main
git pull --ff-only
code .
```

Before your first coding task, confirm the accepted baseline and exact allowed paths with Jack OC. Inspect the actual runtime instructions and manifests; do not assume this repository uses the same commands or stack as the Replit workspace.

For each eligible packet, create a branch from the baseline that contains its accepted dependencies. Example for Hugh, once ING-01 is eligible:

```powershell
git switch main
git pull --ff-only
# Confirm Jack OC's accepted baseline and required commits are present first.
git switch -c hugh/ING-01
python3 ProjectManagement/agent-assignments/select_assignment.py ING-01 `
  --acceptance /absolute/path/to/reviewed-acceptance.json
```

Use the repository's verified Python runtime. If it is unavailable, open the packet Markdown directly; this does not waive any acceptance checks. The acceptance record must contain real human-reviewed evidence, not placeholders. The selector validates record structure only; it does not prove the checks actually ran or that commits are present. Jack OC and the operator must verify those facts.

Copy the emitted packet into one Codex session rooted in that checkout, along with your lane prompt above. Keep one execution packet per session. Use the current coordination/ and tasks/ files under ProjectManagement/agent-assignments/ once their existence is verified in your checkout.

Before working, record your name, task ID, branch/base commit, allowed paths, checked dependencies, expected tests, deadline, and approved spend cap using the repository's claim template. Re-read current issue comments and ask Jack OC to resolve conflicting claims; do not impersonate another teammate or automatically post external messages.

When finished, submit a commit/PR for human review with changed files, commands actually run, pass/fail logs, artifacts, contract version, limitations, and blockers. Write task-specific evidence under reports/<TASK-ID>/ and do not concurrently edit shared status. Pull accepted changes between packets, not mid-task without reviewing their impact.

## Execution order and handoffs

1. Agree the baseline: Jack OC checks current scope/claims and completes or reuses accepted GOV-01-04, ENG-01, and ENG-02 outputs. Peyton validates DAT-01 after GOV-02. Everyone may read packets and prepare questions before implementation is eligible.
2. Verify a thin vertical slice: Supervise one synthetic acquired file through verification/import to a displayed total before an unattended feature wave. Do not regard five passing isolated tasks as proof of integration.
3. Run three feature lanes: Hugh builds acquisition, Peyton builds data, and Landon builds UI against frozen interfaces. Keep at most three concurrent feature-build sessions as required by the snapshot launch guide. Jack OC coordinates/reviews; Jack mc prepares independent evidence. If QA requires a concurrent coding slot, serialize it with a feature lane or approve an updated concurrency policy explicitly.
4. Respect cross-lane gates: Hugh's ING-03 waits for Peyton's DAT-02; Landon's APP-03 final integration waits for DAT-06/DAT-08. Jack mc runs independent checks when dependencies and real outputs are available. A placeholder is not accepted completion.
5. Human integration and freeze: Jack OC leads ENG-05 reviews and dependency-ordered integration. Jack mc completes REL-01 with a working recorded backup and truthful synthetic/live limitations. Do not add optional assistants or extra sources before the core demonstration passes.

Stop rules: Missing contracts/acceptance, overlapping edits, failed checks, contradictory evidence, or exhausted time/spend limits mean report BLOCKED. Suggested packet checkpoints are 60 minutes and at most two repair attempts; ENG-04 allows 90 minutes. These are instructions, not automatic enforcement. Do not run unattended unless your actual tooling supports approved limits and cancellation.

## Steps

1. Verify current assignment sources - Obtain an authorized current checkout of the linked repository and compare its assignment index, launch guidance, issue claims, and acceptance evidence with this snapshot-based allocation; report inaccessible sources rather than infer their contents.
2. Finalize the five ownership lanes - Confirm the recommended named owners, retain one primary owner per packet, and adjust only for current claims or explicit team decisions while preserving dependency and scope gates.
3. Publish the team guide - Add the reviewed Markdown guide to the repository's assignment directory with person-specific task IDs, local VS Code/Codex instructions, file reservations, handoffs, and weekend-versus-later priorities.
4. Check coverage and usability - Verify every current packet is assigned exactly once, all referenced packet paths and selector flags exist, setup commands match the actual repository, and no agents or external actions are started by documentation publication.

## Relevant files

- attached_assets/GOODWILL_READY_TO_RUN_AGENT_ASSIGNMENTS_1791073850610.zip
- docs/goodwill/FOUNDATION.md
- .local/tasks/goodwill-foundation.md
- .local/tasks/goodwill-acquisition.md
- .local/tasks/goodwill-trusted-data.md
- .local/tasks/goodwill-application.md
- .local/tasks/goodwill-integration.md
