# GOV-01 Source-To-Requirement Matrix

Task: GOV-01 / issue #13
Purpose: show how each requirement in `planning/requirements/register.md` maps to Drive evidence or an unresolved decision.

## Source Coverage

| Source ID | Evidence used for GOV-01 | Requirement IDs |
| --- | --- | --- |
| PLAN | Governing synthesis: acquisition-led workflow; corrections about report availability, API restriction, Cash Monkey priority, staffing, Jev, Excel, Power BI, sell-through and no production claims; P0/P1/P2 split; planning artifacts required before unattended work. | REQ-ING-01, REQ-ING-02, REQ-ING-03, REQ-ING-04, REQ-ING-05, REQ-DAT-01, REQ-DAT-03, REQ-DAT-04, REQ-DAT-05, REQ-KPI-01, REQ-KPI-02, REQ-KPI-03, REQ-OPS-01, REQ-OPS-02, REQ-OPS-03, REQ-AI-01, REQ-AI-02, REQ-FIN-01, REQ-FIN-02, REQ-SEC-01 |
| AMANDA | Operator interview: manual Upright retrieval, same reports with changed dates, reports can be pulled whenever needed, Upright API/key restricted, Cash Monkey easier, master Excel, Sonia summary, existing Power BI, AI through Copilot, 30-45 minute estimate with interruptions. | REQ-ING-01, REQ-ING-02, REQ-ING-03, REQ-ING-04, REQ-DAT-01, REQ-DAT-02, REQ-OPS-02, REQ-OPS-03, REQ-AI-01, REQ-FIN-02 |
| FOLLOWUP | Later correction: e-commerce manager moved to Grand Rapids; Amanda is now on her own with an assistant. | REQ-OPS-01 |
| WICKS | Mentor plan: three layers, map source types instead of nine one-off integrations, screenshot/DOM Upright replica, low-maintenance data layer, acquisition enables dashboard. | REQ-ING-01, REQ-ING-02, REQ-KPI-01 |
| BRIEF | Business brief: leadership visibility, 24 stores, manual platform pulls, Business Central desire, Copilot approval constraint, synthetic weekend data, no online sell-through target, event constraints. | REQ-KPI-01, REQ-KPI-02, REQ-KPI-03, REQ-AI-01, REQ-FIN-01, REQ-FIN-02, REQ-SEC-01 |
| JACK | Internal walkthrough: manual six-step process, deterministic SQL/code for calculations, source aggregation idea; corrected by PLAN where unsupported. | REQ-DAT-01, REQ-DAT-02, REQ-AI-02 |

## Acceptance Criteria Mapping

| Issue acceptance criterion | GOV-01 artifact evidence |
| --- | --- |
| Every requirement links to Drive evidence, not merely the legacy repo PRD. | `planning/requirements/register.md` uses PLAN, AMANDA, FOLLOWUP, WICKS, BRIEF and JACK source IDs; this matrix lists source coverage. |
| Later Amanda follow-up overrides the departed-manager staffing assumption. | `REQ-OPS-01` and `planning/process-map.md` mark the departed e-commerce manager assumption as stale and require assistant-role validation. |
| Report availability is distinct from Monday distribution. | `REQ-ING-04` records that Amanda can pull reports whenever needed; workflow delay is manual retrieval/consolidation/distribution. |
| Operator retrieval need and leadership visibility are connected. | `REQ-ING-01`, `REQ-KPI-01`, `REQ-OPS-03` and the process-map weekend implications connect acquisition to trusted dashboard visibility. |
| Finance/IT/Sonia validation remains explicitly pending. | Open questions `OQ-03`, `OQ-06`, `OQ-08`; process-map gaps `GAP-02`, `GAP-03`, `GAP-06`; requirements `REQ-FIN-01`, `REQ-SEC-01`. |

## Negative Checks Performed

| Check | Result |
| --- | --- |
| Did GOV-01 freeze GOV-02/GOV-03 scope or contracts? | No. The register explicitly says GOV-02 freezes scope and GOV-03 publishes contracts. |
| Did GOV-01 claim live access, production data or Business Central posting? | No. Requirements and process map label those as approval gates or out of bounds. |
| Did GOV-01 treat missing source inputs as zero? | No. `REQ-DAT-03` requires unavailable/partial states. |
| Did GOV-01 make Cash Monkey equal priority with Upright? | No. `REQ-ING-02` records Amanda's prioritization of Upright. |
| Did GOV-01 adopt a 50-55 percent e-commerce sell-through target? | No. `REQ-KPI-03` records that as unresolved for e-commerce. |

## Human Review Request

Please review whether the requirement IDs are sufficient for GOV-02 to freeze weekend scope and for GOV-03 to publish contracts. Human reviewers should especially confirm:

- exact P0 story and which optional P1 items to defer;
- whether Amanda's PowerPoint/screenshots establish enough report detail for ING-01;
- who can validate Sonia, finance/accounting, IT/security and assistant-role assumptions.
