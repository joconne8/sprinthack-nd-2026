# GOV-02 Human Decision Request

Task: GOV-02 / issue #11
State: READY_FOR_REVIEW

## Decisions Requested

| Decision | Proposed answer | Evidence basis |
| --- | --- | --- |
| Weekend P0 | One acquisition-led vertical slice: Upright-style replica, parameterized synthetic download, file verification, import/reconciliation, one dashboard evidence view, coverage/exceptions, alternate date and safe failure. | PLAN section 7, GOV-01 REQ-ING-01, REQ-DAT-01, REQ-KPI-01 |
| P1 | Second synthetic source, richer dashboard views, source-linked export, grounded assistant and Jev comparison only after P0 passes. | PLAN section 7 |
| P2 | Universal recorder, nine live integrations, production Copilot, Business Central posting and autonomous operations are deferred. | PLAN, BRIEF, GOV-01 |
| Demo net sales | Item sales minus refunds, excluding shipping, tax and fees. | PLAN, root AGENTS.md, GOV-01 REQ-DAT-05 |
| Reporting timezone | America/New_York for demo until Goodwill confirms another convention. | GOV-01 OQ-05 |
| Strategic KPIs | Track as roadmap/unavailable unless required inputs exist. | BRIEF, PLAN, GOV-01 REQ-KPI-02 |

## Review Checklist

- [ ] P0/P1/P2 split is accepted for weekend execution.
- [ ] Demo net sales convention is accepted for synthetic demo only.
- [ ] Metric dictionary version `GOV-02-metrics-v0.1` can be used by GOV-03 contracts.
- [ ] Missing labor, profit, sell-through and cross-platform identity inputs remain unavailable.
- [ ] No production/live access, credentials, deployment, accounting posting or external business-system action is approved by this packet.

## Known Limits

- GOV-01 is still in review on PR #48; this packet is prepared under the user's orchestration instruction and still requires human acceptance.
- This packet does not publish JSON schemas or API contracts. GOV-03 owns those.
- This packet does not implement app/runtime code or data migrations.
