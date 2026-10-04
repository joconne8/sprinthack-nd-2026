# GOV-01 Current-State Process Map

Task: GOV-01 / issue #13
State: draft for human review
Scope: current reported workflow and approval gaps, not a production design.

## Current Evidence Summary

Amanda describes a manual e-commerce reporting workflow centered on Upright and Cash Monkey, with Upright as the hard retrieval path. She can pull reports whenever needed, but the work is manual and interruption-prone. The output is manually aggregated into Excel, sent to Sonia for a weekly summary that includes store sales, and then feeds existing visibility such as Power BI. The later follow-up says the e-commerce manager assumption is stale: Amanda is now on her own with an assistant.

## Workflow Map

```text
Marketplace / source portals and reports
  |
  | Manual login, report selection, date selection, generation, download
  | - Upright: main pain point
  | - Cash Monkey: still a source, but described as easier
  | - Other sources: jewelry, shipping, FedEx, ShopGoodwill, eBay, Amazon, Books, etc.
  v
Downloaded reports / emailed files / exported spreadsheets
  |
  | Manual consolidation and manipulation
  v
Master Excel reporting sheet
  |
  | Amanda / operations sends summary inputs onward
  v
Sonia weekly summary
  |
  | Combined with store sales and other internal reporting
  v
Existing reporting / Power BI visibility and finance/accounting handoffs
  |
  | Later, partially validated Business Central workflow may be explored
  v
Leadership decisions and month-end close inputs
```

## Step Detail

| Step | Current owner / actor | Evidence | Inputs | Actions | Outputs | Known gaps / risks |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Identify needed reports | Amanda / operations; formerly e-commerce manager may have helped | AMANDA, FOLLOWUP | Reporting date, report type, platform/source | Decide which reports to pull; repeat same reports with changed dates | Pull list for the day or period | Exact report inventory, owner and cadence not fully validated |
| 2. Pull Upright reports | Amanda / operations | AMANDA, WICKS, PLAN | Upright session, report name, date range, product/filter choices | Log in, navigate to reports, choose report/date/product, generate, download | Upright report export | API access restricted; production browser automation not approved; exact report names/fields need confirmation |
| 3. Pull Cash Monkey reports | Amanda / operations | AMANDA, BRIEF | Cash Monkey report parameters | Pull report from Cash Monkey | Cash Monkey export | Amanda says Cash Monkey is much easier; do not over-prioritize before scope review |
| 4. Pull or receive other source data | E-commerce staff / source owners / maybe manager role | AMANDA, BRIEF, PLAN | Jewelry, shipping, FedEx, ShopGoodwill, eBay, Amazon, Books and other reports | Download, request, receive by email or copy from platform | Source files or values | Source ownership, overlap and grain unresolved; some may be expense or settlement, not revenue |
| 5. Manual consolidation | Amanda / operations | AMANDA, JACK | Exported files and values | Manipulate files and enter/copy values into master Excel | Master Excel sheet | Error-prone, interrupted, stale or missing inputs can corrupt downstream visibility |
| 6. Send to Sonia | Amanda / operations | AMANDA, PLAN | Master Excel summary | Send e-commerce summary to Sonia | Weekly summary inputs | Sonia's workbook/process not inspected; acceptance owner pending |
| 7. Combine with store sales | Sonia / admin summary process | AMANDA, PLAN | E-commerce summary, store sales | Add to weekly summary with store sales | Combined weekly view | Definitions, formulas and review criteria pending |
| 8. Publish or view in Power BI / reports | Existing internal reporting owners | AMANDA, PLAN | Consolidated data | Feed or review existing reporting | Leadership visibility | Existing Power BI should be assessed before replacement; route and refresh details unknown |
| 9. Finance / Business Central handoff | Finance/accounting | BRIEF, PLAN | Month-end outputs, source records | Re-enter or prepare accounting data | Business Central / close inputs | No import schema, test environment or accounting approval established |

## Current Pain Points

| Pain point | Evidence | Impact | Requirement IDs |
| --- | --- | --- | --- |
| Upright retrieval is repeated manual work, mainly changing dates. | AMANDA, WICKS | Consumes operator time and delays reliable visibility. | REQ-ING-01, REQ-ING-02 |
| Upright API/key access is restricted. | AMANDA, PLAN | API-first demo would assume unavailable access. | REQ-ING-03 |
| Manual Excel consolidation is a source of error and staleness. | AMANDA, JACK, PLAN | Dashboard or AI built on incorrect data would mislead users. | REQ-DAT-01, REQ-DAT-02, REQ-DAT-03 |
| Leadership wants visibility while operators need retrieval relief first. | AMANDA, BRIEF, PLAN, WICKS | A dashboard alone misses Amanda's upstream bottleneck. | REQ-KPI-01, REQ-OPS-03 |
| Staffing changed. | FOLLOWUP | Support/run-state assumptions cannot depend on the departed e-commerce manager. | REQ-OPS-01 |
| Finance/accounting handoff is unvalidated. | BRIEF, PLAN | Business Central claims would be unsafe without accounting review. | REQ-FIN-01 |

## Weekend Design Implications

- P0 should prove the acquisition-led vertical slice: simulated Upright-style retrieval, verified source file, validated import, metric evidence and safe failure.
- The demo must label replica portal, synthetic records, scripted/model-assisted behavior and unconnected sources honestly.
- Human approval is still needed before live access, real credentials, real data, production browser automation, Copilot integration or Business Central posting.
- Scope freeze belongs to GOV-02 and contracts belong to GOV-03; this process map only records evidence and open decisions.

## Validation Gaps

| Gap ID | Gap | Needed for |
| --- | --- | --- |
| GAP-01 | Exact report names, fields and date parameter semantics from Amanda's PowerPoint/screenshots. | Replica and acquisition contract |
| GAP-02 | Sonia's summary workbook and Power BI feed path. | Downstream handoff and production fit |
| GAP-03 | Goodwill finance metric definitions and Business Central import schema. | Accounting roadmap and finance-safe exports |
| GAP-04 | Source overlap and system-of-record decisions for revenue, settlements, shipping, fees and refunds. | Reconciliation and metric dictionary |
| GAP-05 | Assistant role and support ownership. | Run-state, exception routing and production readiness |
| GAP-06 | Goodwill/provider authorization for live browser automation and approved AI surface. | Production pilot planning |
