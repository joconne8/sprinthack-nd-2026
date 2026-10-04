# PRD 03: Metrics Dashboard and Source Drilldown

## Primary source basis — Drive-led
- [Goodwill — Three-Phase Solution and Overnight Agent Plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk)
- [Amanda Baumer Goodwill Meeting.md](https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view?usp=drivesdk)
- [goodwill-track-brief-v2.md](https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk)
- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk)
- [Jack explanation.md](https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view?usp=drivesdk)

Relevant plan sections: §6 Dashboard and bounded agentic interaction; §7 Weekend P0/P1/P2.

The corrected brief lists leadership revenue/growth/margin/labor productivity/inventory/customer KPIs. Amanda wants retrieval before visibility and Copilot for AI. Wicks proposes an AI-native application; the plan defines operations, leadership and finance surfaces plus narrow grounded tools and unavailable-input handling.

## Source precedence
Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.


## Status

Proposed P0 workstream PRD. This is the visible sponsor and judge experience after acquisition and data validation.

## Problem

Leadership needs clear e-commerce visibility, but dashboards can be misleading when metrics lack definitions, source coverage, freshness, and row-level evidence. The demo must show usefulness without pretending unverified production data or accounting rules exist.

## Goal

Build a focused dashboard that displays the agreed synthetic metrics with filters, definitions, freshness, source coverage, exceptions, and drilldown to supporting source rows.

## Users

- Debie and leadership reviewing e-commerce visibility
- Amanda and operational users checking report status and exceptions
- Team presenters showing an end-to-end working prototype
- Reviewers validating metric correctness

## In scope

- Shared date, platform, and store filters
- Synthetic disclosure banner
- Daily revenue view
- Daily customers view
- Listings per store per day view
- Unlisted backlog snapshot view
- Source coverage/freshness panel
- Exceptions and rejected-row summary
- Source-row drilldown for at least one key metric
- Source-linked summary export if time permits
- Empty, loading, error, partial, and unavailable states

## Out of scope

- Unverified productivity or sell-through metrics
- Profit or margin if cost/labor definitions are missing
- Cross-platform unique customer count
- Real production Power BI/Copilot embedding
- Live Business Central posting
- A general chatbot as the primary interface

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| DASH-01 | Show synthetic status persistently. | Every view and export includes synthetic demo labeling. |
| DASH-02 | Render accepted P0 view(s); richer four-view dashboard is P1 under PLAN §7. | P0 acquired-file metric and source evidence work; selected P1 views are tested if implemented. |
| DASH-03 | Filters apply consistently. | Same date/store/platform filter affects all applicable views under contract rules. |
| DASH-04 | Display metric definitions. | Each view includes formula, grain, period, unit, exclusions, and caveats. |
| DASH-05 | Display freshness and coverage. | User can see last import time and source coverage for the selected period. |
| DASH-06 | Support source drilldown. | User can trace a displayed revenue value to accepted source rows. |
| DASH-07 | Surface exceptions. | Rejected rows, unknown stores, missing buyers, and partial snapshots are visible. |
| DASH-08 | Avoid unsupported totals. | No cross-platform unique customers or invented accounting totals appear. |
| DASH-09 | Export source-linked summary. | Exported CSV matches displayed values and includes filters, definitions, and source references. |

## View requirements

### Daily revenue — P0 evidence view

- Group by sold-at day, platform, store, and currency.
- Use synthetic `sale_amount - refund_amount` excluding shipping and tax.
- Preserve unknown-store bucket.
- Show source-row drilldown and reconciliation status.

### Daily customers — P1 if scoped

- Count distinct platform-local buyers by day and platform.
- Store-filtered counts are distinct within the filtered subset.
- Missing buyer IDs produce unavailable/partial status for affected inputs.
- Never present a cross-platform unique customer total.

### Listings per store per day — P1 if scoped

- Count deduplicated new listing events.
- Distinguish listings from identified, processed, or sold items.
- Preserve unknown stores and event provenance.

### Unlisted backlog — P1 if scoped

- Count unique items in declared unlisted states at a selected complete snapshot.
- Present snapshot timestamp and completeness.
- Partial or missing snapshots must be labeled partial/unavailable.
- Do not infer backlog from sales exports.

## Design principles

- Practical, operational, and scannable.
- Prioritize controls, status, and evidence over decorative charts.
- Keep synthetic/prototype limitations visible but not noisy.
- Show incomplete data honestly.
- Make the demo path fast to operate under presentation time pressure.

## Dependencies

- PRD 00 metric definitions
- PRD 02 pipeline outputs or stable mocked contract
- Shared shell and route/navigation decisions
- Expected-results ledger for QA

## Risks

| Risk | Mitigation |
| --- | --- |
| UI looks polished but numbers are untrustworthy. | Source-row drilldown and reconciliation are P0. |
| Dashboard implies production integrations. | Only implemented synthetic sources appear enabled. |
| Metric definitions are hidden. | Definition panels or tooltips are required for every view. |
| Empty/missing states look like zero. | Distinct unavailable/partial visual states are required. |

## Evidence required for Done

- Screenshots/recording of accepted P0 view and any actually implemented P1 views
- Filter test evidence
- Revenue drilldown evidence
- Unknown-store and rejected-row evidence
- Export sample, if implemented
- Reviewer confirmation that unsupported claims are absent

## Demo talking point

"The dashboard is useful because the numbers are traceable. We can show where the source file came from, what passed validation, what failed, and exactly which rows support the metric."
