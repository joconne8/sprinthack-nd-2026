# Shared Goodwill agent context — Drive-led revision

## Mandatory reading and authority
Read [Drive source register](DRIVE_SOURCE_REGISTER.md), [the actual Drive three-phase solution](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk), its [repo snapshot](THREE_PHASE_PLAN.md), [source traceability](SOURCE_TRACEABILITY.md), your assigned issue/comments and root AGENTS.md.

Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.

[Delivery hub](https://github.com/joconne8/sprinthack-nd-2026/issues/7) · [Backlog](BACKLOG.md) · [Registry](backlog.json) · [Workstream PRDs](https://github.com/joconne8/sprinthack-nd-2026/tree/main/ProjectManagement/subtask-prds).

## Organizing solution
**Acquire reports → make data trustworthy → make it useful to people and approved agents.** Amanda’s report retrieval is upstream of Debie’s leadership visibility and finance handoffs. Do not substitute a dashboard-only feature checklist for the end-to-end operating problem.

## Phase 1: report acquisition
Prioritize Upright because Amanda says it is the difficult repetitive date-only workflow; Cash Monkey is easier. Map nine sources into shared acquisition types and keep per-source parser rules. Demonstrate one screenshot-informed functional HTML replica and real downloadable synthetic CSV. Verify dates/content/checksum before import. Deterministic replay is P0; Jev comparison is optional, correctly described probabilistic AI; recorder is deferred. No provider restriction bypass.

## Phase 2: trusted data
Grain before joins: distinct sales/refunds/expenses/settlements/listing events/inventory snapshots/labor inputs. Use raw→typed staging→curated→versioned metric outputs with source-row lineage and deterministic SQL/code. Handle same-file and overlapping-file duplicates, malformed rows, corrections and missing/stale sources. Never sum all nine source amounts as revenue. Publish only verified runs; retain last-good with warning.

Use the simplest tool meeting confirmed controls. Excel/Power Query→existing Power BI is a viable production bridge; a managed SQL layer is conditional, not automatic. Demo net sales = item sales minus refunds excluding shipping/tax/fees as explicitly proposed by PLAN §5. Finance approves production definitions. Missing labor/cost/cohort/targets/prior periods produce unavailable KPIs, not zeros or estimates.

## Phase 3: application and agentic interaction
Operations view: expected files, ready/failed states, coverage, exceptions and ownership. Leadership: verified daily pulse and strategic KPI availability, comparisons, filters, definitions and evidence. Finance: reconciliation and optional source-linked exports; accounting later. Approved read-only tools supply exact metrics and provenance; an optional assistant explains results, not arithmetic or unproved causation. Copilot production approval/identity/tenant integration remains gated; Teams styling is not an integration.

## Weekend priorities — not inherited old scope
- P0: replica→actual acquisition artifact→validated/reconciled import→same-file dashboard; coverage/freshness/exceptions, source evidence, alternate date and failure.
- P1: second synthetic source, richer/four-view dashboard, listing/backlog if scoped, export, grounded assistant, Jev comparison if access/time/policy allow.
- P2/pilot: recorder, nine live feeds, production Copilot, automated accounting close, pricing/staffing/marketplace actions.

Old four-view/two-platform language is not a binding customer constraint. GOV-02 freezes scope from current Drive evidence and PLAN §7; GOV-03 freezes shared contracts. Optional exports or extra views must not prevent a passing P0 slice.

## Current evidence and ownership
PR #1 remains an open/unmerged draft expanded synthetic-data contribution at the check; DAT-01 validates its relevant artifacts without duplicating it. Its tests are not app verification. Later Amanda2.0 says the former e-commerce manager left; support ownership must be confirmed with Amanda/assistant. No new agents/jobs, live connections, deployments or posting are authorized by this planning revision.

## Overnight engineering — PLAN §8
Freeze scope/contracts and build a passing vertical slice before handoff. Start with 3–4 bounded workers: replica/acquisition, data, frontend against frozen mocks, independent QA. Assistant is a later wave only after checkpoint. Use isolated branches/worktrees and file lanes; one owner for schemas/migrations/lockfiles/entrypoints. Verify an actual runner, budget/deadline/network/action limits and cancellation. At most two repair attempts before escalation. Do not buy services, change credentials, merge unattended or disable tests. Write reports/<TASK-ID>/; one human orchestrator updates shared state. Human morning review checks financial logic/source authenticity/permissions and the complete integrated demo.

## Claim template
```text
Task ID / issue and primary source requirement:
Operator/session, branch/worktree, base commit:
Accepted predecessor evidence:
Allowed files / shared-file conflicts:
Frozen contracts and version:
Tests, independent expected results and artifact paths:
Deadline / spend cap / max 2 repairs:
Human gates / stop conditions:
```

## Return template
```text
Task and primary requirements covered:
Branch / commit / changed files:
Commands actually run + pass/fail/logs:
Downloaded/imported/source/metric evidence:
Measured runtime/usage, not assumed:
Unsupported behavior / tests not run:
Remaining blockers and next human review:
```

## Workflow and Projects limitation
Claim before edits. Dependencies require verified accepted artifacts, not only issue state. All cards remain unclaimed; human acceptance closes them. Current connection cannot access native Projects (403); issue refs are explicit dependency links, not native dependency objects. The bootstrap script attaches these existing issues using authorized Projects access, without launching agents.
