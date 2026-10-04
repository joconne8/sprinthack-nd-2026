# PRD 00: Scope, Contracts, and Operating Rules

## Status

Proposed P0 project-management PRD. This should be completed before parallel implementation begins.

## Primary source basis — Drive-led
- [Goodwill — Three-Phase Solution and Overnight Agent Plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk)
- [Amanda Baumer Goodwill Meeting.md](https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view?usp=drivesdk)
- [Amanda2.0](https://docs.google.com/document/d/1yveSPTDJ4PUVi1MjMvCP6ovVtyVy-M7UGOeDdDngz7g/edit?usp=drivesdk)
- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk)
- [goodwill-track-brief-v2.md](https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk)

Relevant plan sections: §1 Evidence, chronology and corrections; §2 ESTEEM requirements; §15 Immediate decisions.

Amanda prioritizes retrieval and requires Copilot; the follow-up corrects staffing. Wicks connects retrieval to executive visibility in three layers. The corrected brief provides business/mission/KPI constraints. The plan turns these into requirements, frozen interfaces and human decisions.

## Source precedence
Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.


## Problem

The team has several strong source documents, but parallel builders need one frozen operating frame. Without a signed scope, metric contract, and safety boundary, different subtasks may optimize for different demos, invent incompatible data shapes, or overclaim production readiness.

## Goal

Create the single authoritative scope packet that every implementation, QA, pitch, and demo artifact follows for the Goodwill hackathon build.

## Users

- Team lead and integrator
- Subtask owners for acquisition, data, dashboard, QA, and pitch
- Reviewers checking whether work is truthful and in scope
- Judges and sponsors indirectly, through consistent claims and demo behavior

## In scope

- Final weekend scope decision
- Requirement register with IDs and acceptance tests
- Frozen metric definitions for the hackathon demo
- Shared import and API contracts
- File ownership and branch/worktree rules
- Synthetic-data disclosures and non-goals
- Agent/task packet template
- Stop rules for scope creep, failed tasks, and model/automation limits

## Out of scope

- Building product features
- Choosing new paid services
- Production Goodwill deployment approval
- Final accounting mappings
- Real vendor credentials or report access

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| SCOPE-01 | Record the weekend story as acquisition-led: report retrieval, validation, import, metrics, and evidence. | PRD packet states the story in one paragraph and all workstream PRDs reference it. |
| SCOPE-02 | Freeze P0/P1/P2 scope. | P0 tasks are clearly distinct from optional and deferred tasks. |
| SCOPE-03 | Define shared entities: source file, import batch, sale, listing event, inventory snapshot, metric run, exception. | Contracts or schema examples exist before implementation lanes begin. |
| SCOPE-04 | Freeze demo metric rules for revenue, customer count, listings, and backlog. | Dashboard and tests use the same metric language. |
| SCOPE-05 | Define synthetic labels and prohibited claims. | Every PRD includes the rule that data is synthetic and not production-validated. |
| SCOPE-06 | Assign one owner per shared file class. | Contracts, migrations, generated types, app shell, and task status each have a single owner. |
| SCOPE-07 | Create a reusable task packet. | Each subtask can be handed to a builder with allowed files, forbidden actions, tests, and evidence fields. |

## Metric conventions to freeze

- Reporting timezone: proposed `America/New_York`, unless the team records a different decision.
- Revenue: synthetic `sale_amount - refund_amount`, excluding shipping and tax, grouped by sold-at day, platform, store, and currency.
- Customers: distinct platform-local `buyer_id` within platform and day. Do not claim cross-platform unique customers.
- Listings: deduplicated listing events by listed-at day, platform, and originating store.
- Backlog: unique items in declared unlisted states at a complete selected snapshot.
- Unknown store rows remain visible and selectable.
- Missing buyer IDs make the affected customer metric unavailable, not estimated.

## Non-goals and permission boundaries

- No real Goodwill data.
- No real marketplace credentials.
- No production browser automation.
- No live Business Central posting.
- No autonomous listing, pricing, staffing, or accounting decisions.
- No unlabeled synthetic data.
- No claims of measured ROI, Monday install readiness, nine live integrations, or Copilot/Jev production approval.

## Deliverables

- `SPEC.md` or equivalent authoritative scope file
- `contracts/` examples or typed interfaces
- `TASKS.md` or task-board update with owners and reviewers
- `DEMO.md` or final demo script
- Metric dictionary
- Non-goals and disclosure checklist
- Agent task packet template

## Dependencies

None. This is the root workstream.

## Risks

| Risk | Mitigation |
| --- | --- |
| Team begins parallel work before contracts are frozen. | No task starts until this PRD is accepted. |
| Scope drifts toward nine integrations or a chatbot. | P0/P1/P2 labels and stop rules are visible in every task packet. |
| Different builders compute metrics differently. | Shared metric dictionary and expected-results ledger are required. |
| Synthetic demo is mistaken for production integration. | Persistent labels and pitch disclaimers are required. |

## Evidence required for Done

- Link to the authoritative scope packet
- List of approved P0 features
- Metric contract version
- Owners and reviewers assigned
- Stop rules acknowledged by each subtask owner

## Handoff packet for builders

```text
Task ID:
Business requirement IDs:
Goal:
Allowed files:
Forbidden files/actions:
Frozen interfaces:
Fixtures and expected results:
Acceptance tests:
Commands to run:
Runtime/cost/retry limits:
Stop and escalation rules:
Output location:
```
