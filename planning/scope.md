# GOV-02 Scope Packet

Task: GOV-02 / issue #11
State: ready for human scope review
Version: GOV-02-scope-v0.1
Base requirement source: GOV-01 register and process map

## Authority

Current user and human scope decisions govern. This packet operationalizes Drive evidence and the three-phase plan. It does not approve live Goodwill data, production credentials, provider bypass, production deployment, Copilot/Jev production use, or accounting posting.

## P0 Weekend Scope

P0 is one acquisition-led vertical slice:

1. Functional Upright-style simulated portal based on supplied material.
2. Parameterized report request for one selected report and date range.
3. Real downloadable synthetic source file from that flow.
4. File verification with source identity, requested period, coverage, checksum, row count and synthetic flag.
5. Import/validation/reconciliation of that exact file.
6. One dashboard evidence view updated from that exact file.
7. Source coverage, freshness, rejected/exception state and source-row drilldown.
8. Alternate date run proving parameterization.
9. Safe failure demonstration for missing/unavailable/expired/unsupported source state.

P0 success is working evidence for the control pattern, not proof of live Upright compatibility or production readiness.

## P1 After P0 Passes

P1 items may be added only after P0 is demonstrated end to end:

- Second synthetic source using the same intake contract.
- Richer four-view dashboard: daily revenue, platform-local customers, listings, unlisted backlog.
- Excel-compatible source-linked summary export.
- Read-only grounded assistant over deterministic metric results.
- Jev/model-assisted comparison only if approved access exists and deterministic replay remains the baseline.

## P2 Deferred

Deferred work is not part of the weekend commitment:

- Universal recorder or browser extension.
- Nine live integrations.
- Production Copilot deployment.
- Live Business Central posting.
- Fully automated close/accounting workflow.
- Autonomous pricing, staffing, listing, purchasing, external messaging or production deployment.
- Predictive inventory models.

## Non-Goals And Prohibited Claims

- Do not claim every stakeholder approved the design.
- Do not claim the replica is a live Upright integration.
- Do not claim all nine sources are integrated.
- Do not use real Goodwill data or credentials.
- Do not state Monday install readiness.
- Do not claim measured ROI or guaranteed savings from Amanda's estimate.
- Do not use the physical-store 50-55 percent sell-through reference as an e-commerce target.
- Do not merge buyer identities across platforms.
- Do not present missing inputs as zero.

## Frozen Demo Conventions

| Convention | Decision | Requirement IDs |
| --- | --- | --- |
| Data status | Synthetic/local demo data only. | REQ-SEC-01 |
| Reporting timezone | America/New_York unless a later human decision changes it. | REQ-DAT-03 |
| Demo net sales | Item sales minus refunds, excluding shipping, tax and fees. | REQ-DAT-05 |
| Currency | Do not aggregate unlike currencies without an explicit conversion policy. | REQ-DAT-04 |
| Buyer count | Platform-local distinct non-empty buyer IDs only. Cross-platform unique customers are unavailable. | REQ-DAT-03 |
| Unknown store | Preserve unknown or unmapped store rows visibly. | REQ-DAT-03 |
| Labor/productivity | Unavailable until matched labor-hour inputs exist for the same scope. | REQ-KPI-02 |
| Profit/margin | Unavailable until cost, fee, shipping and allocation definitions are approved. | REQ-KPI-02 |
| Sell-through | Unavailable until eligible cohort, window, relist and denominator rules are approved. | REQ-KPI-03 |
| Business Central | Proposed export/mapping only; no posting action. | REQ-FIN-01 |
| AI | Optional read-only synthetic demo only; production AI requires approved Copilot path. | REQ-AI-01 |

## Critical Dependencies

| Downstream task | Can start after | Scope note |
| --- | --- | --- |
| GOV-03 | GOV-02 human review | Publish schemas and examples matching this packet. |
| GOV-04 | GOV-02 human review | Record architecture/security gates and live-access boundaries. |
| DAT-01 | GOV-02 human review | Validate merged synthetic fixtures against this scope and metric dictionary. |
| ENG-01 | GOV-02 and GOV-04 human review | Establish one scaffold/runtime after scope/security choices are reviewed. |
| DAT-02 | GOV-03 and ENG-01 human review | Implement raw/archive/lineage only after contracts and scaffold exist. |

## Human Decision Request

Reviewers should confirm:

- P0/P1/P2 split is accepted for the weekend.
- Demo net sales convention is acceptable for synthetic demo only.
- America/New_York reporting timezone is acceptable until Goodwill confirms otherwise.
- Strategic KPIs are tracked as roadmap/unavailable, not forced into the demo without inputs.
- GOV-03 can treat this packet as the source for contract version `GOV-02-scope-v0.1`.
