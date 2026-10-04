# Source register — nine reporting sources (ING-05, for human review)

Status: reconciled with the GOV-01 requirement register ([requirements/register.md](requirements/register.md)) and the GOV-03 contracts (contracts/v1, goodwill-v1). GOV-03 acceptance was reported to me by Hugh; I could not see it on GitHub. GOV-01 is in review. Still not an owner-reviewed matrix.

Requirements covered: REQ-ING-01 (parameterized request, same report, new dates: Upright skill), REQ-ING-02 (Upright first, Cash Monkey not equal P0), REQ-ING-03 (no assumed Upright API; restricted API is an unresolved production dependency), REQ-ING-04 (reports are available on demand; the delay is manual retrieval and consolidation), REQ-ING-05 (manual fallback and visible needs-human states, see reports/ING-04).
Basis: [THREE_PHASE_PLAN.md §4](project-management/THREE_PHASE_PLAN.md) table "Nine sources are not nine complete integrations", Drive source register ([DRIVE_SOURCE_REGISTER.md](project-management/DRIVE_SOURCE_REGISTER.md)): Amanda meeting, Wicks plan, Jack explanation, Amanda2.0. Requirement refs: PLAN §4, §7; AMANDA, WICKS, JACK, FOLLOWUP (per BACKLOG.md ING-05).

Every channel below is an **acquisition hypothesis from the brief** unless marked *Confirmed*. "Unknown" means nobody has confirmed it with the source owner. Owner, cadence and access state are unknown for all nine; they must be confirmed with Goodwill before any adapter is promised.

| # | Source (synthetic file) | Acquisition class | Channel evidence | Grain / accounting role | Owner / cadence / access | Special care |
|---|---|---|---|---|---|---|
| 1 | Cash Monkey orders (01) | C2 Portal export | Amanda: "comparatively easy" (*Confirmed* by stakeholder statement) | Order unit; sales + payout | Unknown / unknown / unknown | Dedupe on unit_id, books overlap |
| 2 | Upright paid order items (02) | C2 Portal export (generated report, possibly emailed) | Amanda: API restricted/revoked (*Confirmed* statement, reason unknown); repeated date-only workflow, 30-45 min | Paid order / order item; sales | Unknown / unknown / portal user session | Generation delay; orders vs items; **P0 demo adapter** |
| 3 | Jewelry report (03) | C4 Manual upload / provided report | Plan: requested/provided report | Item enrichment | Unknown | Supplier mappings unconfirmed |
| 4 | OSM/PB/EasyPost shipping (04) | C2 export or C5 lookup | Plan: approved export or lookup | Expense (not revenue) | Unknown | Bank-linked expense data |
| 5 | FedEx charges/refunds (05) | C2 export or C5 lookup | Plan: export or authorized accounting lookup | Expense and refund netting | Unknown | Period/mapping controls |
| 6 | ShopGoodwill periodic reports (06) | C2 Portal export | Plan | Sales, overlaps Upright | Unknown | Overlapping sales; do not add to Upright |
| 7 | Goodwill Books payment statement (07) | C3 Scheduled email/file | Plan: monthly email attachment | Settlement/payout, not transaction revenue | Unknown / monthly | Never sum with sales |
| 8 | eBay listing sales (08) | C1 API (if authorized) or C2 export | Plan: portal download or supported API | Listing/sales; refunds, relists | Unknown | API access not confirmed |
| 9 | Amazon payments summary (09) | C2 async generated report | Plan | Payment summary/settlement | Unknown | Not sales revenue |

Classes (detail in [contracts/sources/acquisition-classes.md](../contracts/sources/acquisition-classes.md)): C1 authorized API, C2 portal export, C3 scheduled email/file, C4 manual upload, C5 monthly/statement or lookup. Classes describe *how a file arrives*; they are not marketplaces and say nothing about accounting meaning (a source's accounting role is a separate column).

## P0 demo adapter decision (draft)
Upright paid orders via C2 portal export, against the synthetic replica only. Rationale: Amanda names it the main pain, it needs repeated date-only work, and the replica already exists (PR #45). Cash Monkey is the P1 second source. The other seven are mapped, **not implemented, not connected**.

## Unknowns to confirm
Per-source owner, cadence, access/authorization, real formats, whether Upright can email reports, why the Upright API was restricted, FedEx/EasyPost system of record.
