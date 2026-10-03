# Goodwill Michiana Project Brief

Source deck: https://innovationsprintlab.com/sprinthack-deck/sprinthack.html#16

This document extracts the Goodwill Michiana material from the SprintHack deck and expands it into a practical build brief for a hackathon team. Items marked as "From deck" are directly grounded in the deck. Items marked as "Build guidance" are implementation-oriented recommendations derived from the deck material.

## 1. Track Context

### From deck

- Partner: Goodwill Michiana
- Track: Goodwill Michiana
- Sunday demo pod: Pod B, Room 154
- Saturday presenter: Debie Coble, Chief Executive Officer
- Sunday partner judge: Amanda Baumer
- Sunday judges:
  - Amanda Baumer, Goodwill partner judge, in person
  - Michael Wicks, Notre Dame, in person
  - Shreya Kumar, Notre Dame, in person
  - Tim Connors, PivotNorth, remote
  - Horacio Lopez, Replit, remote
  - Dustin Goodman, ClickUp, remote
  - Reece Atkinson, ClickUp, remote

### Problem framing

Goodwill's stated theme is:

> From manual reporting to management visibility.

The project opportunity is to convert fragmented e-commerce reporting, spreadsheet-based controls, and manual Business Central entry work into a controlled operating view and/or automation workflow.

## 2. Primary Business Problem

### From deck

Goodwill's current e-commerce reporting and close process depends on manual report pulls, portal downloads, emailed files, spreadsheet rules, finance lookups, and manual Business Central entries.

The process has two related needs:

1. Daily operating visibility: marketplace revenue and customer counts by day.
2. Month-end close automation: source reports, allocation rules, journal entries, AR invoice outputs, and reconciliation evidence.

### Build guidance

The strongest project should not merely visualize uploaded CSVs. It should show that the team understands the operational control problem:

- Data arrives from multiple sources.
- Each source has different timing, naming, report format, and business rules.
- The allocation workbook is currently the control layer.
- Business Central needs balanced, traceable outputs.
- Missing reports, failed transformations, and posting exceptions must be visible.

## 3. Current Daily Reporting Workflow

### Upright reporting steps from deck

1. Open Reports.
2. Click Paid orders.
3. Set date range.
4. Generate report.
5. Download.
6. Customer count equals rows minus the title row. These numbers are entered on the Daily Summary Spreadsheet.

### Cash Monkey / Books reporting steps from deck

1. Books: open Cash Monkey reports.
2. Open Orders Report.
3. Select dates from the drop-down.
4. Click the link; the report downloads.

### Build guidance

Potential system behavior:

- Upload or ingest downloaded reports.
- Detect source type.
- Parse report date range.
- Calculate customer count where the current process uses row count.
- Normalize daily revenue and customer counts.
- Write results into a shared daily summary table.
- Flag missing source reports for the selected date.
- Show a run log for each import.

## 4. Nightly Channel Breakdown

### From deck

Each nightly report should show revenue and customer count by marketplace, followed by enterprise totals.

| Revenue Source | Daily Revenue | Daily Customers |
| --- | --- | --- |
| ShopGoodwill | Revenue for the day | Customers for the day |
| Amazon | Revenue for the day | Customers for the day |
| eBay | Revenue for the day | Customers for the day |
| Other e-commerce channels | Revenue for the day | Customers for the day |
| Total e-commerce | Total revenue for the day | Total customers for the day |

Other marketplaces can be added as separate rows as the channel mix evolves.

### Build guidance

Suggested normalized table:

| Field | Type | Notes |
| --- | --- | --- |
| report_date | date | Business date for the daily report |
| source | string | ShopGoodwill, Amazon, eBay, Other, Cash Monkey, Upright, etc. |
| marketplace | string | Public-facing marketplace/channel |
| gross_revenue | decimal | Revenue before adjustments if available |
| net_revenue | decimal | Revenue after refunds/fees if available |
| customers | integer | Buyer/customer count |
| orders | integer | Optional but useful if report provides it |
| units_sold | integer | Optional |
| file_name | string | Source file used |
| imported_at | datetime | Import timestamp |
| import_status | enum | imported, warning, failed |
| exception_reason | string | Human-readable issue |

Suggested dashboard widgets:

- Daily revenue by channel
- Daily customers by channel
- Total e-commerce revenue
- Total e-commerce customers
- Missing reports
- Import exceptions
- Revenue trend over last 7 or 30 days
- Customer trend over last 7 or 30 days

## 5. Monthly Management Dashboard

### From deck

The monthly e-commerce dashboard should balance:

- Growth
- Profitability
- Productivity
- Inventory management
- Customer engagement

The deck positions this as a shift from manual reporting to management visibility.

### Build guidance

The dashboard should be designed for a COO or operating leader, not just an analyst. The user should quickly answer:

- Is e-commerce revenue growing?
- Is e-commerce profitable?
- Are labor hours producing enough revenue and profit?
- Is inventory moving fast enough?
- Are listings being created at the required pace?
- Which categories are driving revenue and margin?
- Are buyers returning?
- What needs attention before month-end close?

## 6. KPI Framework

### Financial metrics from deck

- Total E-Commerce Revenue
- Revenue Growth % YOY
- Gross Margin %
- Net Margin %
- Revenue per Labor Hour
- Profit per Labor Hour

### Listing and production metrics from deck

- Items Identified for E-Commerce
- Items Sent to E-Commerce
- Listings Created per Day
- Listings per Employee
- Average Time to List an Item
- Unlisted Inventory Backlog

### Sales effectiveness metrics from deck

- Average Selling Price (ASP)
- Median Sale Price
- Sell-Through Rate
- Days to Sell
- Unsold Inventory %
- Relisted Inventory %

### Category performance metrics from deck

- Sales by Category
- Margin by Category
- Units Sold by Category
- Sell-Through Rate by Category
- Average Selling Price by Category
- Top 10 Categories by Revenue
- Top 10 Categories by Margin

### Customer and marketplace metrics from deck

- Number of Buyers
- Repeat Buyer Rate
- New Buyers
- Customer Satisfaction Rating
- Net Promoter Score, if available
- Marketplace Conversion Metrics

## 7. COO Scorecard

### From deck

A monthly scorecard should combine outcomes, operating drivers, and early warning indicators.

| Area | KPI 1 | KPI 2 | KPI 3 |
| --- | --- | --- | --- |
| Financial | Total E-Commerce Revenue | Revenue Growth % | Net Margin % |
| Productivity | Listings Created | Revenue per Labor Hour | Listings per Employee |
| Inventory | Days from Donation to Listing | Unlisted Inventory Backlog | Unsold Inventory % |
| Sales | Average Selling Price | Sell-Through Rate | Sales per Employee |
| Category + Customer | Top 10 Categories by Revenue | Top 10 Categories by Margin | Repeat Buyer Rate |

Monthly cadence: one page, with trend and target context added as data becomes available.

### Build guidance

For a weekend build, prioritize a one-page COO scorecard with:

- Current month value
- Prior month value
- Change
- Status color
- Small trend line
- Target, if available
- Source freshness
- Exceptions affecting confidence in the number

## 8. 2027 Plan Anchor Metrics

### From deck

Three KPIs anchor the 2027 plan:

1. Increase e-commerce net margin annually.
2. Increase revenue per labor hour annually.
3. Increase sell-through rate annually.

These connect profitability, workforce productivity, and the speed at which inventory converts to cash.

### Build guidance

Use these three as the top-level executive scorecard:

- Net Margin %
- Revenue per Labor Hour
- Sell-Through Rate

The dashboard can visually connect each top-level KPI to its operational drivers:

- Net Margin %: revenue, refunds, fees, shipping, category mix, gross margin.
- Revenue per Labor Hour: listings created, sales per employee, labor hours, productivity.
- Sell-Through Rate: listings, inventory age, days to sell, unsold inventory, relisted items.

## 9. Month-End Close Problem

### From deck

The current month-end close combines:

- Portal downloads
- Emailed reports
- Bank activity
- Spreadsheet rules
- Manual Business Central entries

High-level flow:

1. Source reports
2. Allocation + rules
3. Business Central

### Build guidance

This is the more sophisticated automation track. A good solution can simulate Business Central output if real credentials and APIs are unavailable.

Minimum credible month-end build:

- Accept a monthly close period.
- Collect or upload source reports.
- Confirm all required sources are present.
- Normalize data into a common staging model.
- Apply source-specific rules.
- Generate journal-entry-like output.
- Generate AR-invoice-like output.
- Show reconciliation totals.
- Show exceptions requiring review.
- Preserve source file references and run history.

## 10. Source Workflows

### From deck

Nine source workflows feed one month-end close.

| Source | Month-End Input | Acquisition / Rule |
| --- | --- | --- |
| Cash Monkey | Orders, full month | Submit/download CSV; save as Excel |
| Upright | Paid order items, full month | Generate; email delivery; save as Excel |
| Jewelry | Jewelry Report | Request report; Co-Pivot populates Supplier |
| OSM / PB / EasyPost | Shipping amounts | 1st Source account 0101; GL 10009 |
| FedEx | Shipping charges + refunds | BC GL 40356; Dept 180; V00122; net BNKDEPOSIT refunds |
| ShopGoodwill | Periodic marketplace reports | Filter year/month; Period 1 periodic only; Period 3 all reports |
| Goodwill Books | Prior-month payment statement | Monthly email attachment |
| eBay | Listing sales report | Seller Center; change date; generate/download |
| Amazon | Payments summary | Seller Central; request/refresh/download |

Current state: each source has its own access path, timing, and business rule.

### Build guidance

Represent sources with metadata:

| Field | Example |
| --- | --- |
| source_id | ebay |
| display_name | eBay |
| input_type | portal_download |
| expected_frequency | monthly |
| required_for_close | true |
| expected_file_format | csv/xlsx/pdf/email attachment |
| acquisition_owner | finance/e-commerce/accounting |
| business_rule_group | ebay_sales_mapping |
| target_bc_account | configured mapping |
| target_department | configured mapping |
| due_day | day of month or relative timing |

## 11. Allocation Workbook

### From deck

The allocation workbook is the manual control layer.

Process:

1. Archive inputs: save all files under Accounting / Month End / year / month / Journal Entries / E-Commerce JEs.
2. Roll workbook: open the prior-month E-Commerce Allocation file and save a current-month copy.
3. Populate tabs: enter report data into orange-highlighted fields on matching source tabs.
4. Generate entries: workbook logic flows data into Journal Entry tabs for each report.
5. Post General Journal: copy and paste journal-entry output into a Business Central General Journal.
6. Create AR Invoice: use the final Invoices tab to create the Business Central AR invoice entry.

The dependency is broader than a single upload: month-end rules, source-specific timing, shipping lookups, journal creation, and invoice creation all sit inside the manual process.

### Build guidance

The workbook should be treated as the source of truth for current business rules until validated.

Suggested approach:

- Inventory workbook tabs.
- Identify orange input fields.
- Extract formulas and named ranges.
- Map workbook tabs to source reports.
- Reproduce calculated totals in code.
- Compare generated outputs to workbook outputs.
- Keep workbook-equivalent totals visible during early cutover.

## 12. Target Close

### From deck

The target close should automate the rules, not just the downloads.

Target flow:

1. Acquire
   - Portal reports
   - Email attachments
   - Bank and Business Central lookups
2. Archive
   - Consistent year/month
   - Source file naming
   - Run history
3. Enrich
   - Supplier assignment
   - Source labels
   - Period metadata
4. Apply rules
   - Monthly date range
   - Shipping and refunds
   - Period-specific reports
5. Create Business Central output
   - General Journal lines
   - AR invoice entry
   - Control totals
6. Post + reconcile
   - Import/API status
   - Source-to-BC totals
   - Owned exceptions

Control principle: Business Central receives balanced, traceable journal and invoice payloads; missing reports, failed rules, and posting errors remain visible for review.

### Build guidance

The target system should include:

- Source intake status
- File archive location
- Transformation status
- Journal output preview
- Invoice output preview
- Control totals
- Reconciliation checks
- Exception queue
- Owner assignment
- Audit log

## 13. Workstreams

### From deck

| Workstream | Work to Complete | Deliverable |
| --- | --- | --- |
| 1. Source Intake | Confirm access and automate downloads/email pickup for Cash Monkey, Upright, ShopGoodwill, Books, eBay, and Amazon. | Reliable monthly source package |
| 2. Shipping + Enrichment | Ingest bank activity; reproduce FedEx filters/refund netting; automate Jewelry Supplier enrichment. | Complete expense and enrichment dataset |
| 3. Rules + Mapping | Document orange-field inputs, workbook formulas, control totals, and source-to-account/dimension mapping. | Approved transformation and BC mapping |
| 4. Business Central Outputs | Build General Journal and AR invoice payloads; capture import/API validation and posting response. | Tested journal and invoice interfaces |
| 5. Close Controls + Support | Reconcile source, workbook-equivalent, and posted totals; define exceptions, approvals, archive, and ownership. | Auditable month-end operating model |

Discovery must confirm:

- Credentials
- Report availability
- Business Central destinations
- Existing workbook formulas

## 14. Implementation Waves

### From deck

Automation should be introduced source by source, then proven against the existing allocation workbook before manual posting is retired.

1. Baseline the close
   - Inventory files, owners, timing, workbook tabs, formulas, journal output, and invoice output.
2. Automate acquisition
   - Prioritize stable portal/email feeds.
   - Add shipping lookups and enrichment after core reports.
3. Reproduce + validate
   - Generate Business Central-ready outputs.
   - Compare every source, total, journal line, and invoice to the workbook.
4. Cut over + operate
   - Approve production posting.
   - Monitor each close.
   - Route exceptions to named owners.

Definition of done:

- Every required source is captured.
- Period and shipping rules are reproduced.
- Journal lines reconcile.
- AR invoice output reconciles.
- Posting status and exceptions are retained.

## 15. Suggested Hackathon MVP Options

### MVP A: Daily E-Commerce Pulse

Best if the team wants a strong, demoable dashboard.

Core features:

- Upload sample marketplace reports.
- Normalize daily revenue and customers.
- Show nightly channel breakdown.
- Calculate total e-commerce revenue and customers.
- Flag missing reports.
- Show trends over time.
- Export a daily summary CSV.

Why it fits:

- Directly addresses manual reporting.
- Easy to demo.
- Shows management visibility.
- Lower integration complexity.

### MVP B: COO Scorecard

Best if the team wants an executive-facing management system.

Core features:

- Monthly KPI dashboard.
- 15 KPI scorecard.
- Top 3 2027 anchor metrics.
- Trend and target context.
- Source freshness and confidence indicators.
- Drilldowns by category, marketplace, and source.

Why it fits:

- Aligns tightly with strategic plan material.
- Useful for leadership.
- Can work with mock or uploaded data.

### MVP C: Month-End Close Control Center

Best if the team wants a deeper workflow automation project.

Core features:

- Monthly close checklist.
- Required source report tracker.
- File upload by source.
- Source-to-close status.
- Rule application preview.
- General Journal output.
- AR invoice output.
- Reconciliation totals.
- Exception queue.

Why it fits:

- Addresses the highest-value operational pain.
- Shows understanding of controls.
- Strong judging story if the prototype reconciles outputs.

### MVP D: Hybrid

Recommended if the team can move quickly.

Build a single app with two tabs:

- Daily Pulse
- Month-End Close

This shows both operating visibility and finance process automation without trying to fully replace Business Central.

## 16. Suggested Data Model

### source_files

| Field | Type | Purpose |
| --- | --- | --- |
| id | uuid | Primary key |
| source | string | Report source |
| period_start | date | Start date |
| period_end | date | End date |
| file_name | string | Original file |
| file_type | string | csv, xlsx, pdf, email |
| uploaded_by | string | User or system |
| uploaded_at | datetime | Timestamp |
| status | enum | pending, parsed, warning, failed |
| checksum | string | Duplicate detection |

### marketplace_daily_metrics

| Field | Type | Purpose |
| --- | --- | --- |
| date | date | Reporting date |
| marketplace | string | ShopGoodwill, Amazon, eBay, etc. |
| revenue | decimal | Daily revenue |
| customers | integer | Daily customer count |
| orders | integer | Optional |
| units | integer | Optional |
| source_file_id | uuid | Traceability |

### monthly_kpis

| Field | Type | Purpose |
| --- | --- | --- |
| month | date | Reporting month |
| kpi_name | string | KPI label |
| kpi_group | string | Financial, Productivity, Inventory, Sales, Category + Customer |
| value | decimal | KPI value |
| target | decimal | Optional target |
| prior_period_value | decimal | Trend context |
| status | enum | green, yellow, red, unknown |
| source_confidence | enum | high, medium, low |

### close_sources

| Field | Type | Purpose |
| --- | --- | --- |
| month | date | Close month |
| source | string | Cash Monkey, Upright, etc. |
| required | boolean | Required for close |
| received | boolean | File/report received |
| received_at | datetime | Receipt timestamp |
| owner | string | Responsible person/team |
| rule_group | string | Transformation rule set |
| exceptions_count | integer | Active exceptions |

### journal_lines

| Field | Type | Purpose |
| --- | --- | --- |
| month | date | Close month |
| line_number | integer | Journal line sequence |
| source | string | Source report |
| account | string | Business Central account |
| department | string | Dimension/department |
| vendor | string | Vendor ID where applicable |
| debit | decimal | Debit amount |
| credit | decimal | Credit amount |
| description | string | Human-readable line description |
| control_total_group | string | Reconciliation group |

### exceptions

| Field | Type | Purpose |
| --- | --- | --- |
| id | uuid | Primary key |
| month | date | Close month |
| source | string | Source related to issue |
| severity | enum | info, warning, blocker |
| type | string | Missing file, parse error, reconciliation mismatch, posting failure |
| message | string | Explanation |
| owner | string | Assigned reviewer |
| status | enum | open, in_review, resolved |
| created_at | datetime | Timestamp |
| resolved_at | datetime | Timestamp |

## 17. Business Central Output Considerations

### From deck

Business Central output needs:

- General Journal lines
- AR invoice entry
- Control totals
- Import/API validation and posting response

### Build guidance

For hackathon purposes, a mock Business Central export can be enough if it is credible and traceable.

Suggested export columns:

- Posting Date
- Document Number
- Account Type
- Account Number
- Description
- Department
- Vendor
- Debit Amount
- Credit Amount
- Source
- External Document Number
- Control Group

Validation checks:

- Debits equal credits.
- Required dimensions are present.
- Required source reports are received.
- Each journal line ties back to a source file.
- AR invoice total matches calculated source total.
- Refunds and shipping adjustments are separately visible.

## 18. Exception Handling

### Build guidance

Potential exception types:

- Missing source report
- Wrong date range
- Duplicate file
- Unrecognized report format
- Customer count mismatch
- Revenue total mismatch
- Missing supplier assignment
- Missing Business Central account mapping
- Debits and credits do not balance
- AR invoice total does not reconcile
- Posting/API failure

Each exception should include:

- Source
- Period
- Severity
- Owner
- Suggested resolution
- Current status

## 19. Demo Story

### Recommended narrative

1. "Goodwill currently spends time pulling reports from different portals and moving numbers into spreadsheets."
2. "Our prototype creates one controlled intake layer for those reports."
3. "For daily operations, it produces a channel-level revenue and customer pulse."
4. "For month-end, it tracks source readiness, applies rules, and generates Business Central-ready outputs."
5. "Every number traces back to a source file, and exceptions stay visible instead of being hidden in spreadsheets."

### Demo flow

1. Select a reporting date or close month.
2. Show required sources and which have arrived.
3. Upload or simulate receiving a source report.
4. Show parsed metrics.
5. Show daily channel breakdown.
6. Show COO scorecard.
7. Show month-end close status.
8. Generate journal lines and AR invoice preview.
9. Show reconciliation and exceptions.
10. Export Business Central-ready CSV.

## 20. Judging Alignment

### Working evidence

Show the prototype running end to end:

- Upload or ingest source files.
- Parse them.
- Normalize metrics.
- Create dashboard outputs.
- Generate close outputs.
- Show reconciliation.

### Partner problem fit

Emphasize:

- Manual reporting pain.
- Management visibility.
- Business Central integration path.
- Auditability and control.

### Fits constraints

Respect:

- Existing workbook logic.
- Source-specific report timing.
- Source-specific business rules.
- Need for reconciliation evidence.
- Month-end close cannot break.

### Technical substance

Strong technical pieces:

- Source normalization.
- Rule engine or mapping layer.
- Reconciliation checks.
- Exception workflow.
- Export generation.
- Traceability from KPI to source file.

### Demo clarity

Keep the demo focused on one storyline:

"We transformed scattered portal reports and spreadsheet controls into a daily operating dashboard plus a controlled month-end close workflow."

## 21. Open Discovery Questions

These should be asked of Goodwill mentors or judges if possible.

- Which reports are available as CSV or Excel today?
- Which source should be automated first?
- Which source creates the most manual effort?
- Which current workbook tabs are most critical?
- Are workbook formulas stable month to month?
- Which Business Central fields are required for journal import?
- Is Business Central API access available, or is CSV import the realistic first step?
- What are the exact definitions of revenue, customer, buyer, and order by marketplace?
- How should refunds be represented?
- How should shipping charges and refunds be netted?
- How is supplier assigned for Jewelry today?
- Which report is the system of record for each KPI?
- How are labor hours tracked?
- What counts as an item identified for e-commerce?
- What counts as an item sent to e-commerce?
- How is sell-through rate defined?
- What target values exist for the 2027 anchor KPIs?
- Who owns each exception during close?

## 22. Recommended Build Stack

### Build guidance

For a weekend build:

- Frontend: React, Next.js, or a simple Vite app.
- Backend: Node/Express, Python/FastAPI, or local serverless routes.
- Data storage: SQLite, Postgres, Supabase, or even structured JSON for demo speed.
- File parsing: CSV parser, XLSX parser, and mocked PDF/email intake if necessary.
- Charts: Recharts, ECharts, Plotly, or similar.
- Export: CSV/XLSX export for Business Central-ready outputs.

Architecture:

1. Source intake module
2. Parser/normalizer module
3. Rule/mapping module
4. KPI calculation module
5. Reconciliation module
6. Dashboard UI
7. Export module

## 23. Success Criteria

### Minimum success

- A user can load source data.
- The app displays daily revenue and customers by marketplace.
- The app calculates total e-commerce revenue and customers.
- The app shows at least one monthly KPI view.
- The app identifies missing or invalid reports.

### Strong success

- The app includes the 15-KPI COO scorecard.
- The app tracks all nine month-end sources.
- The app generates journal-line-like output.
- The app generates AR-invoice-like output.
- The app reconciles output totals back to sources.
- The app includes an exception queue.

### Excellent success

- Source-to-KPI traceability is visible.
- Business Central export is credible.
- Workbook-equivalent validation is demonstrated.
- The cutover path protects the month-end close.
- The demo clearly shows before/after operational improvement.

