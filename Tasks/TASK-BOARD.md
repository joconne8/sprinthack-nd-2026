# Goodwill build board

Current delivery status uses the newer GOV/ING/DAT/APP/ENG/REL assignments in
`ProjectManagement/agent-assignments/TEAM_ASSIGNMENTS.md`, with combined Jack OC /
Peyton evidence in `reports/integration/completion-status.md`. The G/A/E cards,
scope assumptions and dates below are historical planning, not live completion
state. The acquisition-led scope in `planning/scope.md` governs the current build.

Mock Jira-style board | Prepared Saturday, October 3, 2026 | Five laptops, one small prototype

This is a proposed breakdown, not evidence of work already started. Fill the owner slots, approve the scope card, then move cards as evidence lands. No repo, Replit project or existing file was changed to create this plan.

## Scope and evidence

- **From partner/advisor notes:** recurring fragmented report pulls are the immediate pain; Wicks recommends ingestion, a simple centralized data layer, then a dashboard. His fake Upright/DOM replay is a suggested demo strategy, not approved live access. Reports mention nine source workflows, not nine delivered integrations.
- **Earlier proposed PRD:** four views with synthetic Shop Goodwill and eBay exports, deterministic math, source reconciliation and no live accounting posting.
- **Decision needed (G01):** reconcile these into one small story: simulated Upright date-to-report retrieval feeding the importer, followed by the four-view prototype. Manual synthetic upload remains the safe fallback. The newer judge brief recommends CashMonkey next and more headline KPIs; those do not silently override the PRD.
- **Constraints:** all business records are synthetic; no real sponsor credentials or customer/employee data. Goodwill's tools-already-paid-for and Copilot/authorized-retrieval constraints apply to any future production path. A Replit demo is not proof of approved deployment at Goodwill.
- **Unknowns:** the actual browser tool name is garbled as Jeb/JEV/Jeff; no specific tool capability, speed or zero-token claim is adopted. The available rubric scan is Pod A, not confirmed Pod B. Wicks whiteboard photos were not readable in the earlier inspection; this board uses the written notes.

## Five owner slots

| Lane | Human owner | Responsibility | Separate reviewer |
| --- | --- | --- | --- |
| A | [Name] | Synthetic data, adapters, simulated retrieval | [Name, not A driver] |
| B | [Name] | Revenue, reconciliation, source drilldown | [Name, not B driver] |
| C | [Name] | Platform-local customers | [Name, not C driver] |
| D | [Name] | Listings and snapshot backlog | [Name, not D driver] |
| E | [Name] | Integrator, common shell, deploy, QA/demo | [Name, not E driver] |

These are roles, not assignments to named teammates. Lane A is the bottleneck: others use the frozen fixture/API contract first. Lane E can pair with A on the simulated page after the shell works. Everyone runs tests; a different human signs off each card.

## Plan / dev / review: three agent roles

1. **Plan:** take one card, read its source contract and dependencies, return a tiny implementation plan, allowed files and test list. Human driver approves before build.
2. **Dev:** implement only that card's approved files; run tests and return changed files, test output, source-row/metric checks and remaining gaps. No spending, plan upgrades or live sponsor actions.
3. **Review:** a separate agent checks the diff against the card, shared contract and disclosures. It returns pass/fail findings, not new features. The independent human reviewer checks the evidence and decides whether to integrate.

Use one shared project if the team's actual setup permits it. This file does not assert Replit automatically creates a board or resolves conflicting edits. One writer per shared file; the integrator owns schema/config/common UI. Use small commits or checkpoints and explicit review before applying changes. Check actual plan/concurrency/credit state at E01; do not start five paid background builds on an assumed allowance. Default to short scoped prompts, reusable fixtures and deterministic tests; stop after two failed attempts and ask the human driver to rescope.

## Board columns and movement rules

| Backlog | Todo | In progress | Review | Done |
| --- | --- | --- | --- | --- |
| Optional/deferred cards listed below | Proposed core cards listed below | Empty: no work verified | Empty: no review verified | Empty: no completion verified |

### Initial card placement by lane

| Lane | Backlog | Todo | In progress | Review | Done |
| --- | --- | --- | --- | --- | --- |
| A | X01, X05 | A01-A11 | None verified | None verified | None verified |
| B | X03 | B01-B04 | None verified | None verified | None verified |
| C | None | C01-C03 | None verified | None verified | None verified |
| D | X04 | D01-D06 | None verified | None verified | None verified |
| E / scope | E06, X02 | G01-G03, E01-E05, E07-E12 | None verified | None verified | None verified |

Todo means proposed core scope, not dependency-ready. A09-A11 require the G01 retrieval decision before anyone starts them.

- Backlog -> Todo: human lead approves scope and available time.
- Todo -> In progress: dependencies Done, owner/reviewer filled, plan approved. One active dev card per lane is the proposed WIP limit.
- In progress -> Review: implementation plus tests/checkpoint and known gaps attached. Blocked cards keep their status and record blocker/next owner.
- Review -> Done: different human reviewer checks acceptance and integrator confirms the change runs in the shared build. Failed review goes back to In progress.
- P0 = proposed core; P1 = optional preview; P2 = stretch/later. No card is complete just because an agent says so.

## Metric contracts to freeze at G02

These are PRD **demo conventions**, not Goodwill-confirmed accounting definitions. Every implementation, UI, test and export card must carry its relevant contract. All four views and exports say "synthetic demo data".

**Shared day/time rule:** PRD asks for a reporting timezone but does not choose one. Proposed demo choice is `America/New_York`; team must confirm at G02. Derive day from sold_at/listed_at converted to that timezone. Store timestamps with their offsets. Label this choice in UI/exports; do not call it the partner's confirmed timezone. Snapshot time is an instant displayed in that same timezone, not a daily sales window.

**Shared store rule:** originating store gets credit; fictional IDs can represent 24 stores. Missing stores remain in a flagged unknown-store bucket and are never distributed by guesswork. No real store names are fabricated. Filters must not hide unknown data by default.

**R - Daily revenue:** sum accepted synthetic `sale_amount - refund_amount`, excluding shipping and tax, by sold_at day/platform/originating store. Separate currencies without a conversion policy. Under this proposed schema a refund reduces the sale row's day; there is no refund timestamp, so do not imply refund-date cash accounting. Every value traces to accepted source rows.

**C - Daily customers:** distinct platform-local buyer_id within platform/day from accepted sale rows, never cross-platform unique total or order count. Proposed demo clarification to approve: a refunded sale still counts its buyer because the PRD provides no refund-based customer exclusion. If buyer IDs are missing, mark the affected input's metric unavailable rather than silently reporting an undercount. Store-filtered counts are distinct within that subset and cannot be summed to a platform total.

**L - Listings/store/day:** count deduplicated new listing events by listed_at day, platform and originating store. Identified/processed items are not listing events. Freeze event-key/relist treatment at G02. Refunds and customer IDs do not change this count.

**K - Unlisted backlog:** count unique items in declared demo unlisted workflow states at the selected complete inventory snapshot, by originating store. PRD does not supply state names. Proposed fixture states to approve: `awaiting_listing` and `ready_to_list`; document any change before coding. This is point-in-time, not daily flow, and cannot be inferred from sales. Missing or partial snapshots remain unavailable/partial, never a complete count. Refunds and customer IDs do not affect it.

## Proposed milestones, working backward from freeze

Shared `goodwill-track-brief-v2.md` states Sunday, October 4: 4:00 PM freeze and 4:30 PM Pod B presentations, Room 154. Dates were calculated; the schedule is sourced from team notes and must be checked with the facilitator at E10. All targets below use America/New_York. They are team planning targets, not additional official deadlines.

| Target | Evidence required | If missed |
| --- | --- | --- |
| Sat 7:30 PM | G01-G03 contracts/owners agreed; E01 existing setup checked | Cut recorder/chatbot/extra KPI work |
| Sat 10:00 PM | Upload -> normalized rows -> revenue -> source trace runs | Keep manual synthetic uploads; pause simulated retrieval polish |
| Sun 10:00 AM | Four views, idempotency and exception paths working | Pair to finish core; do not add extras |
| Sun 12:00 PM | Full regression and second-laptop run pass | Cut optional preview/AI/recorder; fix truth and data quality first |
| Sun 1:30 PM | Feature stop; stable deployed version | Bug fixes only |
| Sun 2:30 PM | Rehearsal, pitch disclosures and backup recording ready | Use known-good labeled replay as backup, not live-access claim |
| Sun 3:30 PM | Submission assets and links checked | Human lead submits with time to correct receipt/link issues |
| Sun 4:00 PM | Freeze and verified receipt under confirmed requirements | No unapproved changes after freeze |
| Sun 4:30 PM | Pod B presentation, subject to facilitator confirmation | Show only what runs; recording remains ready |

## Critical path

`G01 -> G02/G03 -> E01/E02 -> A02/A03 -> A04 -> A05/A06 -> A07 -> A08 -> E04 -> four views -> E05/E07 -> E08 -> E11 -> E12`

The proposed Wicks proof branches through `A09 -> A10 -> A11`; if chosen as the lead demo story, it joins E07's acceptance gate. Parallel UI work uses mocked interfaces only until real importer integration passes. Do not mark dependencies Done without evidence.

## Card index

| ID | Lane | Card | Priority | Status | Depends on |
| --- | --- | --- | --- | --- | --- |
| G01 | E | Choose and record the weekend scope | P0 | Todo | None |
| G02 | E | Freeze metric and import contracts | P0 | Todo | G01 |
| G03 | E | Assign five owners and independent reviewers | P0 | Todo | G01 |
| E01 | E | Check the existing Replit project and safe preview | P0 | Todo | G01,G03 |
| E02 | E | Scaffold the smallest runnable shell | P0 | Todo | G02,E01 |
| A01 | A | Map source workflows to adapter types | P0 | Todo | G01 |
| A02 | A | Generate synthetic sales fixtures | P0 | Todo | G02 |
| A03 | A | Generate synthetic listing and inventory fixtures | P0 | Todo | G02 |
| A04 | A | Create shared deterministic validation | P0 | Todo | A02,A03,E02 |
| A05 | A | Build Shop Goodwill synthetic CSV adapter | P0 | Todo | A04 |
| A06 | A | Build eBay synthetic CSV adapter | P0 | Todo | A04 |
| A07 | A | Persist import batches with repeat-import protection | P0 | Todo | A05,A06 |
| A08 | A | Build import results and exceptions API | P0 | Todo | A07 |
| A09 | A | Create one simulated Upright report page | P0 | Todo | G01,A02 |
| A10 | A | Replay date-to-CSV retrieval on the simulation | P0 | Todo | A09,A05,A07 |
| A11 | A | Connect simulated retrieval to report intake | P0 | Todo | A10,A08,E03 |
| B01 | B | Implement deterministic daily revenue query | P0 | Todo | G02,A07 |
| B02 | B | Build revenue view and metric definition panel | P0 | Todo | B01,A08,E03 |
| B03 | B | Reconcile revenue to source rows | P0 | Todo | B01,A08 |
| B04 | B | Test revenue drilldown and next-day update | P0 | Todo | B02,B03,A02 |
| C01 | C | Implement platform-local daily customer query | P0 | Todo | G02,A07 |
| C02 | C | Build customers view and definition panel | P0 | Todo | C01,A08,E03 |
| C03 | C | Test customer identities and missing data | P0 | Todo | C01,C02,A02 |
| D01 | D | Import listing events and snapshots | P0 | Todo | A03,A04,A07 |
| D02 | D | Implement listings per store per day | P0 | Todo | D01,G02 |
| D03 | D | Build listings view | P0 | Todo | D02,A08,E03 |
| D04 | D | Implement selected-snapshot backlog | P0 | Todo | D01,G02 |
| D05 | D | Build backlog view and snapshot selector | P0 | Todo | D04,A08,E03 |
| D06 | D | Test listings and backlog boundary cases | P0 | Todo | D03,D05,A03 |
| E03 | E | Build common controls and disclosure shell | P0 | Todo | E02,G02 |
| E04 | E | Build manual upload flow | P0 | Todo | E03,A08 |
| E05 | E | Export source-linked summary CSV | P0 | Todo | B03,C03,D06,E04 |
| E06 | E | Business Central mapping preview: proposal only | P1 | Backlog | E05 |
| E07 | E | Run integrated demo regression | P0 | Todo | B04,C03,D06,E04,E05 |
| E08 | E | Deploy and check from a second laptop | P0 | Todo | E07 |
| E09 | E | Write honest pitch and maintenance handoff | P0 | Todo | G01,E07 |
| E10 | E | Confirm Pod B format and submission checklist | P0 | Todo | G01 |
| E11 | E | Rehearse, cut and record backup | P0 | Todo | E08,E09,E10 |
| E12 | E | Freeze, submit and verify receipt | P0 | Todo | E11 |
| X01 | A | Generic macro-recorder UI and second retrieval source | P2 | Backlog | A11 |
| X02 | E | Grounded narrative or Copilot-compatible query | P2 | Backlog | E07 |
| X03 | B | Revenue/profit per labor hour and net margin | P2 | Backlog | G02 |
| X04 | D | Sell-through and other marketplace metrics | P2 | Backlog | G02 |
| X05 | A | Real-source and accounting pilot gate | P2 | Backlog | A01,E09 |

## Granular cards

### G01 - Choose and record the weekend scope

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** None
- **Acceptance:** Human team lead signs off: four PRD views, two synthetic marketplace exports; proposed Wicks path is one simulated Upright date-to-CSV retrieval feeding the same importer. Upright is a report interface, not a third marketplace. Do not quietly switch the second platform to CashMonkey. If retrieval takes too long, retain manual synthetic upload and disclose that gap.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### G02 - Freeze metric and import contracts

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01
- **Acceptance:** Write shared typed schemas for Sale, Listing event, Inventory snapshot and Import batch using PRD fields. Record revenue/refunds, timezone, currency, store attribution, buyer counting and unlisted-state choices below. Human lead approves before parallel coding; unresolved production definitions stay labeled unconfirmed.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### G03 - Assign five owners and independent reviewers

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01
- **Acceptance:** Fill lane owner slots. Each card gets one driver and a different human reviewer. Reserve an integrator for shared files. No claim that anyone has started or completed these cards.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E01 - Check the existing Replit project and safe preview

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01,G03
- **Acceptance:** Identify the actual shared project, current collaborator access, plan, credits and deployment state before making changes. Use synthetic data only. Record run/test/deploy commands. Do not buy credits or change plans as part of this board.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E02 - Scaffold the smallest runnable shell

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02,E01
- **Acceptance:** App opens from a reproducible command with upload route, four placeholder view routes and a mocked contract. Pick one simple existing data store, not a new warehouse initiative. One integrator owns package/config/schema files.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A01 - Map source workflows to adapter types

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01
- **Acceptance:** Create a short source/type matrix from Wicks notes: CSV export, manual dashboard pull, email delivery and other unknown types. Label nine-source coverage as roadmap, not implemented. Record source shapes still unknown; no live credentials or unattended report delivery.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A02 - Generate synthetic sales fixtures

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02
- **Acceptance:** Create Shop Goodwill and eBay exports with fictional store IDs from a 24-store dimension, platform-local buyer IDs and known expected totals. Include refunds, duplicate rows, missing stores, missing buyers, malformed values and midnight-boundary cases. Every file/header/fixture is labeled synthetic demo data.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A03 - Generate synthetic listing and inventory fixtures

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02
- **Acceptance:** Separate new listing events from identified/processed items. Build complete snapshots using the approved demo unlisted states, plus partial/missing snapshots, repeated snapshots and unknown-store cases. Include selected fictional stores for the demo, and label all fixtures synthetic.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A04 - Create shared deterministic validation

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A02,A03,E02
- **Acceptance:** Validate required fields, timestamp parsing, numeric amounts, platform, currency, row IDs and synthetic flag. Reject malformed rows with reasons; retain unknown-store rows visibly. Missing buyer IDs make customer metrics unavailable for that affected input. Keep accepted/rejected counts and date coverage.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A05 - Build Shop Goodwill synthetic CSV adapter

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A04
- **Acceptance:** Map every proposed Sale field; preserve source_file_id and source_row_id. Unit tests compare normalized rows to fixtures. UI calls this a synthetic export import, never a live connector.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A06 - Build eBay synthetic CSV adapter

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A04
- **Acceptance:** Normalize the second fixture shape to the same schema; preserve platform-local buyer/order keys and source provenance. Pass the same contract tests without pretending the synthetic fields are verified production fields.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A07 - Persist import batches with repeat-import protection

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A05,A06
- **Acceptance:** Fingerprint files; re-uploading the same file leaves counts and totals unchanged. Freeze a row-key policy and test repeated rows/overlapping files without silently losing valid records. Store import time, validation results, date coverage, synthetic flag and row counts.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A08 - Build import results and exceptions API

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A07
- **Acceptance:** Return accepted/rejected rows, unknown-store bucket, missing-data flags, batch freshness and source-row drilldowns. Expose typed endpoints for the four views. Do not conceal rejected rows or report incomplete data as complete.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A09 - Create one simulated Upright report page

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01,A02
- **Acceptance:** Use authorized reference screenshots only as visual guidance. Build a real DOM with clearly marked simulation, paid-orders/date/report/download steps and no real sponsor sign-in. A date produces a synthetic CSV accepted by the importer. No logo or screen implies live access.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A10 - Replay date-to-CSV retrieval on the simulation

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A09,A05,A07
- **Acceptance:** Implement a narrow deterministic script against the mock DOM. A reviewer can choose a supported fixture date, download the labeled CSV and import it. Unsupported dates and missing elements fail visibly. Record timing only as measured simulation timing, never a Goodwill saving claim.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### A11 - Connect simulated retrieval to report intake

- **Lane / priority / status:** A / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A10,A08,E03
- **Acceptance:** One run hands the generated synthetic file into the same validation/provenance path used for manual uploads. Repeating the date does not double totals. A broken replay leaves prior results intact and offers manual upload. No live email/shared-folder delivery claim.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### B01 - Implement deterministic daily revenue query

- **Lane / priority / status:** B / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02,A07
- **Acceptance:** Apply R definition below: sum synthetic sale_amount minus refund_amount, excluding shipping/tax, grouped by sold_at day in approved demo timezone, platform and originating store. Preserve unknown stores, separate unlike currencies and link accepted source rows. Tests include refunds and day boundaries.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### B02 - Build revenue view and metric definition panel

- **Lane / priority / status:** B / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** B01,A08,E03
- **Acceptance:** Render daily revenue with date/platform/store filters, currency and R definition visible. Every chart/card is labeled synthetic. Unknown-store bucket is selectable; freshness and incomplete imports are visible. Do not call this confirmed Goodwill accounting.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### B03 - Reconcile revenue to source rows

- **Lane / priority / status:** B / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** B01,A08
- **Acceptance:** For each platform/store/day and currency, source accepted rows sum exactly to the displayed net revenue. Show rejected rows and discrepancies. Seeded refund and unknown-store cases pass; discrepancies cannot be silently rounded away.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### B04 - Test revenue drilldown and next-day update

- **Lane / priority / status:** B / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** B02,B03,A02
- **Acceptance:** Reviewer traces a filtered value to source rows, reimports unchanged data without inflation, then imports the next synthetic day without changing code or templates. Verify R refund, timezone, store and currency rules at the UI boundary.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### C01 - Implement platform-local daily customer query

- **Lane / priority / status:** C / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02,A07
- **Acceptance:** Apply C definition below: distinct buyer_id within each platform and sold_at day in approved timezone, on accepted sale rows. Refunds do not automatically remove a buyer under this demo convention. No cross-platform identity merge or summed unique total. Missing buyer IDs make affected input unavailable, never order count.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### C02 - Build customers view and definition panel

- **Lane / priority / status:** C / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** C01,A08,E03
- **Acceptance:** Show platform counts separately using the same date/platform/store controls; for store-filtered results count distinct buyers within that filtered subset, do not sum store counts. Display C definition, synthetic label, unavailable state and batch freshness.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### C03 - Test customer identities and missing data

- **Lane / priority / status:** C / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** C01,C02,A02
- **Acceptance:** Same buyer twice on a platform/day counts once; same text ID on two platforms stays separate. Test timezone boundary, missing IDs, unknown stores and repeat imports. Refund treatment matches the documented demo convention; no unsupported unique-customer claim.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D01 - Import listing events and snapshots

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A03,A04,A07
- **Acceptance:** Preserve event/snapshot provenance, IDs, store and timestamps. Freeze unique listing-event and inventory-item policies. Validate completeness per snapshot and retain missing/unknown stores. Repeated inputs cannot inflate listings or backlog.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D02 - Implement listings per store per day

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** D01,G02
- **Acceptance:** Apply L definition below: count deduplicated new listing events by originating store, platform and listed_at day in approved timezone. Identified/processed items are not listings. Refunds/customer IDs do not affect this metric. Unknown stores remain flagged, not dropped or redistributed.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D03 - Build listings view

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** D02,A08,E03
- **Acceptance:** Show L definition, count unit, day/store/platform filters, source rows and freshness; label synthetic throughout. Test multiple listings and repeated events under the chosen event-key policy.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D04 - Implement selected-snapshot backlog

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** D01,G02
- **Acceptance:** Apply K definition below: count unique items in approved demo unlisted states at a selected complete snapshot, grouped by originating store. Point-in-time, not daily flow and never inferred from sales. Missing/partial snapshots are labeled, no fabricated complete count. Refunds and buyer IDs are irrelevant.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D05 - Build backlog view and snapshot selector

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** D04,A08,E03
- **Acceptance:** Display snapshot timestamp in approved timezone, declared unlisted states, completeness, unknown-store bucket and provenance. Keep partial counts labeled partial or unavailable; synthetic labels appear on card/chart/export. Do not imply historical backlog from daily sales.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### D06 - Test listings and backlog boundary cases

- **Lane / priority / status:** D / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** D03,D05,A03
- **Acceptance:** Check new-listing dates versus identified/processed timestamps, event dedupe, unknown stores, complete/partial/missing snapshots and repeated item rows. Verify L/K definitions in the UI, not only unit tests.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E03 - Build common controls and disclosure shell

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E02,G02
- **Acceptance:** Share date/platform/store controls, view navigation, loading/error/empty states and synthetic banner. Only implemented platforms appear enabled. Keep common components integrator-owned; metric drivers use agreed props, not concurrent edits.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E04 - Build manual upload flow

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E03,A08
- **Acceptance:** Accept the two synthetic sales files plus listing/inventory inputs; show progress, result counts, validation reasons and coverage. A user can retry a failed import without losing accepted data. No live marketplace/accounting permission is implied.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E05 - Export source-linked summary CSV

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** B03,C03,D06,E04
- **Acceptance:** CSV carries synthetic flag, metric-definition/version, filters, timezone, currency or count unit, snapshot time where relevant, source batch/row references and missing-data flags. Values match displayed R/C/L/K semantics, with platform-local customer counts kept separate.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E06 - Business Central mapping preview: proposal only

- **Lane / priority / status:** E / P1 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E05
- **Acceptance:** Optional: show a proposed source-to-field mapping labeled UNVALIDATED / PROPOSAL ONLY and synthetic demo data. No verified import schema exists in the PRD. No posting/upload button, accounting compatibility claim, or guessed production account codes.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E07 - Run integrated demo regression

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** B04,C03,D06,E04,E05
- **Acceptance:** Clean-start test performs uploads, four views, filters, source drilldown, refund, unknown-store, malformed-row rejection, duplicate reimport and next-day update. If simulated retrieval is selected, A11 also passes. Save pass/fail evidence; independent human reviewer signs off.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E08 - Deploy and check from a second laptop

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E07
- **Acceptance:** Human integrator deploys using existing approved setup; another laptop tests clean entry, supported files/date and four views. Verify no secrets or real personal data are bundled. Capture deployed URL and version; do not assume plan-change redeploys already happened.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E09 - Write honest pitch and maintenance handoff

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01,E07
- **Acceptance:** Describe what runs, what is simulated/synthetic and what is borrowed. Attribute Wicks/partner claims to notes, not measured baselines. Explain simple data storage, broken-source recovery and real-data approval gates. No savings, security/customer-logo, pilot, Monday rollout or nine-source coverage claims without evidence.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E10 - Confirm Pod B format and submission checklist

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G01
- **Acceptance:** Check facilitator requirements: actual Pod B rubric, recording/GitHub-link submission, whether live demonstration is allowed and presentation length. Schedule below comes from shared notes, not live event confirmation. Prepare recording regardless; do not assume the Pod A scorecard is official for Pod B.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E11 - Rehearse, cut and record backup

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E08,E09,E10
- **Acceptance:** Run the exact finished workflow with one supported new date/file chosen by a teammate. Time to confirmed slot; seven minutes is only the PRD proposal. Record working evidence and retain labeled local replay. Cut extras before weakening provenance or synthetic disclosures.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### E12 - Freeze, submit and verify receipt

- **Lane / priority / status:** E / P0 / Todo
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E11
- **Acceptance:** Before scheduled freeze, record stable app version/link, accessible GitHub artifact and video/Slides link as required by confirmed instructions. Human team lead submits to verified form and saves receipt. This card does not perform GitHub writes or create a submission now.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### X01 - Generic macro-recorder UI and second retrieval source

- **Lane / priority / status:** A / P2 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A11
- **Acceptance:** Stretch only after E07: decide recorder scope, verify the garbled tool name separately, and test only against synthetic mock sources. CashMonkey is a future retrieval/source decision, not a secretly working connector.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### X02 - Grounded narrative or Copilot-compatible query

- **Lane / priority / status:** E / P2 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** E07
- **Acceptance:** Stretch only: explanation cites computed source-linked facts; no LLM math or causal certainty. Partner AI approval and Copilot constraint remain production gates. No general chatbot promise.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### X03 - Revenue/profit per labor hour and net margin

- **Lane / priority / status:** B / P2 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02
- **Acceptance:** Deferred sponsor priorities. Revenue per labor hour = agreed scope/window revenue divided by matched labor hours; zero/missing hours is unavailable. Profit basis/costs/fees/labor allocation must be confirmed. Net margin has no approved demo contract here; do not invent costs.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### X04 - Sell-through and other marketplace metrics

- **Lane / priority / status:** D / P2 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** G02
- **Acceptance:** Deferred: sold items from a defined eligible cohort / eligible items in that same cohort over a stated window. Confirm relists and cross-platform item treatment. Never use sales today / listings today or the physical-store 50-55% as an online target.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

### X05 - Real-source and accounting pilot gate

- **Lane / priority / status:** A / P2 / Backlog
- **Owner:** [Name] | **Reviewer:** [Different name]
- **Dependencies:** A01,E09
- **Acceptance:** Later only: authorized access, verified source formats/terms, confirmed metric definitions, reconciliation to partner reports, security/data-handling review and accounting validation. Real data, automation permissions, production delivery and Business Central posting require separate approvals.
- **Evidence / checkpoint:** [Link or test output]
- **Blocker / next action:** [Fill only if blocked]

## Source trail

Read live from SprintHack on October 3, 2026. These files are source notes/specifications, not permission to access sponsor systems or external proof that a product claim is current.

- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [02-prd-goodwill-ops-reports.md](https://drive.google.com/file/d/1aFNo7lVR-R0o7ck9quw6SNPMHLLY8dSb/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [05-agentic-build-plan.md](https://drive.google.com/file/d/1a0uAIOZse1spLOaYKPP2qEp8EZ3xvhdH/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [judge-brief-pod-b.md](https://drive.google.com/file/d/16t4AaJcXgJgq842jyxAj6w011_h82TiL/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [goodwill-track-brief-v2.md](https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [horacio-chat.md](https://drive.google.com/file/d/15SRZd0BjL-jqf2tJjz8AAEM_QBMtRaNi/view?usp=drivesdk&authuser=joconne6%40nd.edu)
- [Jack explanation.md](https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view?usp=drivesdk&authuser=joconne6%40nd.edu)

No measured savings, confirmed pilot, full nine-source coverage, current Replit entitlement, real-data access or validated Business Central import is claimed in this board.
