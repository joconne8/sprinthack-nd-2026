# Goodwill Project Management PRDs

## Primary source basis — Drive-led
- [Goodwill — Three-Phase Solution and Overnight Agent Plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk)
- [Amanda Baumer Goodwill Meeting.md](https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view?usp=drivesdk)
- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk)
- [Jack explanation.md](https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view?usp=drivesdk)
- [goodwill-track-brief-v2.md](https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk)
- [Amanda2.0](https://docs.google.com/document/d/1yveSPTDJ4PUVi1MjMvCP6ovVtyVy-M7UGOeDdDngz7g/edit?usp=drivesdk)

Relevant plan sections: §§1–15 across all three phases.

The primary solution is acquire reports → make data trustworthy → make it useful to people and approved agents. Requirements come from current Drive evidence, not the older repo feature list.

## Source precedence
Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.


Prepared from the actual Drive plan linked above and its planning/project-management/THREE_PHASE_PLAN.md snapshot and the Drive source `GOODWILL_THREE_PHASE_SOLUTION_AND_OVERNIGHT_AGENT_PLAN.md`.

These PRDs break the Goodwill hackathon build into bounded workstreams. They are written for project management: each file identifies the user need, owner lane, dependencies, acceptance criteria, evidence required, and explicit non-goals.

## Recommended execution order

1. [00 - Scope, Contracts, and Operating Rules](subtask-prds/00-scope-contracts-and-operating-rules-prd.md)
2. [01 - Report Acquisition and Upright Replica](subtask-prds/01-report-acquisition-and-upright-replica-prd.md)
3. [02 - Data Pipeline, Validation, and Reconciliation](subtask-prds/02-data-pipeline-validation-and-reconciliation-prd.md)
4. [03 - Metrics Dashboard and Source Drilldown](subtask-prds/03-metrics-dashboard-and-source-drilldown-prd.md)
5. [04 - Read-Only AI Interaction and Metric Explanation](subtask-prds/04-read-only-ai-interaction-and-metric-explanation-prd.md)
6. [05 - QA, Demo, Release, and Evidence](subtask-prds/05-qa-demo-release-and-evidence-prd.md)
7. [06 - Finance and Production Roadmap](subtask-prds/06-finance-and-production-roadmap-prd.md)

## Shared truth that applies to every subtask

- The weekend prototype uses synthetic demo data only.
- The strongest story is acquisition-led: collect a report, verify it, import it, calculate consistently, then display and explain the result.
- The Upright-style page is a replica for demonstration and testing, not proof of live Upright access.
- Browser automation must be deterministic first. Jev or other model-assisted behavior is optional and must be labeled separately.
- No production credentials, real customer data, employee data, accounting posting, or vendor restriction bypass is in scope.
- Missing, stale, partial, or malformed data must be visible; it must never be silently converted to zero or hidden.
- Every metric must identify its definition, period, coverage, freshness, and supporting records.
- Accounting and Business Central work remains a gated roadmap item unless Goodwill validates schemas, mappings, and controls.

## Workstream dependency map

```text
00 Scope/contracts
      |
      +--> 01 Report acquisition
      |         |
      |         v
      +--> 02 Data pipeline -----> 03 Dashboard/source drilldown
      |                                |
      |                                v
      +----------------------------> 04 AI explanation, optional after metrics pass
                                       |
                                       v
                                  05 QA/demo/release
                                       |
                                       v
                                  06 Production/accounting roadmap
```

## Project management usage

For each PRD, fill these fields before work starts:

- Owner
- Reviewer
- Target date/time
- Current status
- Branch or task link
- Evidence location

A subtask moves to Done only when a different reviewer verifies its acceptance criteria and evidence. Agent or developer messages saying "done" are not sufficient.

## Ready-to-run assignment package
[All 43 task/coordination packets](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/INDEX.md) and [launch guide](https://github.com/joconne8/sprinthack-nd-2026/blob/main/ProjectManagement/agent-assignments/LAUNCH_GUIDE.md) provide explicit preflight, dependencies, file lanes, outputs, tests and stop rules. Packaging does not launch agents or clear human gates. At package publication PR #1 is merged (GitHub reports 2026-10-04T00:13:02Z); validate its merged fixtures rather than duplicate or reintegrate them. Earlier open-draft descriptions are historical; tests must still be run independently.
