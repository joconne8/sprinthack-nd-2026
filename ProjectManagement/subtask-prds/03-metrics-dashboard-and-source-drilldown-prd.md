# PRD 03: Metrics Dashboard and Source Drilldown

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
| DASH-02 | Render four agreed views. | User can navigate to revenue, customers, listings, and backlog. |
| DASH-03 | Filters apply consistently. | Same date/store/platform filter affects all applicable views under contract rules. |
| DASH-04 | Display metric definitions. | Each view includes formula, grain, period, unit, exclusions, and caveats. |
| DASH-05 | Display freshness and coverage. | User can see last import time and source coverage for the selected period. |
| DASH-06 | Support source drilldown. | User can trace a displayed revenue value to accepted source rows. |
| DASH-07 | Surface exceptions. | Rejected rows, unknown stores, missing buyers, and partial snapshots are visible. |
| DASH-08 | Avoid unsupported totals. | No cross-platform unique customers or invented accounting totals appear. |
| DASH-09 | Export source-linked summary. | Exported CSV matches displayed values and includes filters, definitions, and source references. |

## View requirements

### Daily revenue

- Group by sold-at day, platform, store, and currency.
- Use synthetic `sale_amount - refund_amount` excluding shipping and tax.
- Preserve unknown-store bucket.
- Show source-row drilldown and reconciliation status.

### Daily customers

- Count distinct platform-local buyers by day and platform.
- Store-filtered counts are distinct within the filtered subset.
- Missing buyer IDs produce unavailable/partial status for affected inputs.
- Never present a cross-platform unique customer total.

### Listings per store per day

- Count deduplicated new listing events.
- Distinguish listings from identified, processed, or sold items.
- Preserve unknown stores and event provenance.

### Unlisted backlog

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

- Screenshots or recording of all four views
- Filter test evidence
- Revenue drilldown evidence
- Unknown-store and rejected-row evidence
- Export sample, if implemented
- Reviewer confirmation that unsupported claims are absent

## Demo talking point

"The dashboard is useful because the numbers are traceable. We can show where the source file came from, what passed validation, what failed, and exactly which rows support the metric."
