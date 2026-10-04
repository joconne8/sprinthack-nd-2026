# GOV-02 Metric Dictionary

Version: GOV-02-metrics-v0.1
State: selected synthetic implementation convention under reported Jack OC delegation; independent review remains pending
Source basis: PLAN section 7, GOV-01 requirements, Amanda interview, corrected brief.

## Metric Status Legend

| Status | Meaning |
| --- | --- |
| P0 | Required for the one acquired-file vertical slice. |
| P1 | Optional after P0 passes. |
| Roadmap | Important stakeholder KPI, but missing approved inputs or definitions for weekend implementation. |
| Unavailable | Must display unavailable/partial rather than zero when inputs are missing. |

## P0 Metrics

| Metric ID | Name | Formula | Grain | Required inputs | Source authority | Exclusions | Availability and caveats | Requirement IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-DEMO-NET-SALES | Demo net sales | Sum(item sale amount) - sum(refund amount) | reporting date, source/report, platform if present, store if present, currency | accepted sales rows, accepted refund amounts, currency, reporting date, synthetic flag | GOV-02 demo convention, PLAN | shipping, tax, marketplace fees, settlements, expenses | P0 only for accepted synthetic rows; unknown store remains visible; missing money/currency rejects or marks row unavailable. | REQ-DAT-02, REQ-DAT-04, REQ-DAT-05, REQ-KPI-01 |
| M-SOURCE-COVERAGE | Source coverage | Required source/report periods present vs expected for selected period | source/report, requested period | acquisition/source package metadata, coverage dates, status | PLAN and GOV-01 process map | none | P0; late/missing coverage must be visible and cannot become zero. | REQ-ING-04, REQ-DAT-03, REQ-KPI-01 |
| M-REJECTED-ROWS | Rejected row count | Count rejected rows by reason | import batch, source file, reason | validation output, source row IDs | PLAN | accepted rows | P0; rejected rows must retain row identity and reason. | REQ-DAT-01, REQ-DAT-03 |
| M-DRILLDOWN-ROWS | Supporting source rows | Source rows contributing to a displayed metric run | metric run, source file, source row | lineage from source file to accepted row to metric run | PLAN | rows outside metric scope | P0; limits may apply in UI, but full evidence must be recoverable. | REQ-DAT-01, REQ-KPI-01 |

## P1 Metrics

| Metric ID | Name | Formula | Grain | Required inputs | Source authority | Exclusions | Availability and caveats | Requirement IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-PLATFORM-CUSTOMERS | Platform-local customers | Count distinct non-empty buyer_id | date, platform, optional store/filter | buyer_id, platform, sold_at/reporting date, accepted rows | BRIEF, PLAN | empty buyer IDs; cross-platform identity merges | P1; unavailable/partial if buyer IDs missing for affected source. | REQ-DAT-03, REQ-KPI-01 |
| M-LISTINGS-CREATED | Listings created | Count distinct listing_id events | listed date, platform, store | listing_id, item_id, store_id, listed_at | BRIEF, PLAN | sales rows without listing event | P1 only if listing-event input is accepted. | REQ-KPI-02 |
| M-UNLISTED-BACKLOG | Unlisted backlog | Count unique items in approved unlisted states at complete snapshot | snapshot time, store, workflow state | item_id, store_id, workflow_state, snapshot_at, completeness marker | BRIEF, PLAN | sales-derived inference without inventory snapshot | P1; partial/missing snapshots are unavailable, not zero. | REQ-KPI-02, REQ-DAT-03 |
| M-SUMMARY-EXPORT | Source-linked summary export | Export displayed metric values plus filters, definitions and source refs | selected dashboard scope | metric results, definitions, source references | PLAN | production accounting posting | P1; may be CSV/XLSX-compatible but not Business Central posting. | REQ-FIN-01 |

## Strategic Roadmap Metrics

| Metric ID | Name | Required decision/input before implementation | Current status | Requirement IDs |
| --- | --- | --- | --- | --- |
| R-REVENUE-GROWTH | Revenue growth | Approved comparable periods, source coverage policy and prior-period data. | Roadmap | REQ-KPI-02 |
| R-LABOR-PRODUCTIVITY | Revenue/profit per labor hour | Labor-hour source, matching scope, zero-denominator policy and revenue/profit definition. | Roadmap; unavailable in P0/P1 without labor input. | REQ-KPI-02 |
| R-MARGIN | Gross/net margin | Approved cost, fee, shipping, allocation and revenue definitions. | Roadmap; unavailable until finance approval. | REQ-DAT-04, REQ-KPI-02 |
| R-SELL-THROUGH | E-commerce sell-through | Eligible inventory cohort, time window, relist policy and e-commerce target. | Roadmap; do not use 50-55 percent in-store reference. | REQ-KPI-03 |
| R-CATEGORY-PERFORMANCE | Category performance | Category mapping, item-category coverage and system-of-record. | Roadmap | REQ-KPI-02 |
| R-REPEAT-BUYERS | Repeat/new buyers | Buyer identity policy; cross-platform identity mapping approval if any. | Roadmap; no cross-platform merge in weekend demo. | REQ-DAT-03 |

## Cross-Cutting Metric Rules

- Every displayed number must show metric ID, version, period, filters, coverage and synthetic status.
- Dashboard, SQL, tests, exports and assistant/tool responses must use the same metric ID and formula.
- Missing required inputs produce unavailable/partial states, not zero.
- Financial values must come from deterministic code or SQL, not model-generated arithmetic.
- Any assistant or narrative summary may explain only returned deterministic results and must cite coverage/limitations.
