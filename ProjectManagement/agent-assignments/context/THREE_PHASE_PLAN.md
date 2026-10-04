> Source snapshot fetched from the primary [Google Drive plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk). Read DRIVE_SOURCE_REGISTER.md for authority and later corrections. Legacy PRD references inside this historical synthesis are background; its §7 P0/P1/P2 governs the revised backlog. Statements about unpublished work describe original preparation, not current repository state.

# Goodwill Michiana: Three-Phase Solution and Overnight AI Engineering Plan

Prepared for the ESTEEM team — October 3, 2026.

## Executive recommendation

Build and demonstrate a controlled reporting workflow, not a dashboard disconnected from how Goodwill actually gets its data:

**Acquire the reports → make the data trustworthy → make it useful to people and approved agents.**

Michael Wicks’s three layers are the organizing structure:

1. Data ingestion.
2. Centralized data and repeatable calculations.
3. Application/dashboard with AI-native interaction.

Treat these as three phases of the solution, but not three isolated development projects. Build one narrow end-to-end path first, then deepen each layer. Amanda’s operational need and Debie’s management need are connected: leadership cannot get reliable visibility until the repetitive report retrieval and consolidation process works.

**Weekend recommendation:** one working Upright-style report acquisition flow against a clearly labeled HTML replica, a deterministic import/reconciliation pipeline, and a focused dashboard. Add bounded AI interaction only after that path passes its tests. Use synthetic data. Show other sources as explicitly not connected.

**Production recommendation:** retain Goodwill’s existing Microsoft workflow where it meets the requirements. Use authorized report retrieval; adopt managed storage only where needed; preserve Excel exports; assess Power BI before replacing it; require Goodwill approval for any AI, including Jev. Do not make a new commercial model, database, or custom dashboard a prerequisite for receiving reports.

This document is a proposed plan, not evidence that integrations, agents, benchmarks, deployments, accounting outputs, or production access already work.

## 1. Evidence, chronology, and corrections

### Sources reviewed

- Jack explanation.md: the internal walkthrough of ingestion, warehouse, dashboard, and AI.
- michael-wicks-plan.md: the actual three-layer advice and screenshot-to-HTML demo idea.
- Amanda Baumer Goodwill Meeting.md: detailed operational interview.
- Amanda2.0: follow-up noting that the e-commerce manager left and Amanda now has an assistant.
- goodwill-track-brief-v2.md: corrected problem brief and operating constraints.
- TECHNICAL_UPSKILLING.md: existing team guide, including Jev identification and technical corrections.
- GitHub: README, active goodwill/PRD.md, deck.md, goodwill/synthetic-data/README.md, notes/goodwill-problem-discussion.md, planning/agentic-build-plan.md, and planning/recommendation.md.
- Granola: the kickoff and Horatio discussion.
- TypeSafe’s Jev announcement and two public Jev browser implementations, to verify model/replay distinctions.

Earlier Replit conversations and delivered files were discovered through search, but their complete message histories were not returned. This plan does not claim to have exhaustively reread every past conversation. It uses the substantive source documents above and their latest clarifications.

Amanda’s PowerPoint and the Goodwill screenshot folder were located. This planning pass did not visually inspect every slide or screenshot. The replica implementation must inspect the actual supplied slides rather than inventing its UI from this document.

### What later evidence changes

| Earlier interpretation | Better-supported interpretation | Planning consequence |
|---|---|---|
| The dashboard is the immediate problem. | Amanda prioritizes getting reports automatically; Debie prioritizes management visibility. | Start with retrieval and show the dashboard as its downstream benefit. |
| API access merely costs extra. | Amanda reports restricted/revoked Upright API access. The commercial or contractual reason is not confirmed. | Do not design around an API key that Goodwill does not currently have. |
| Weekend data cannot be fetched until Monday. | Amanda says she can pull reports whenever she wants. | Distinguish report availability from staff/report-distribution timing. |
| Cash Monkey is as difficult as Upright. | Amanda says Cash Monkey is comparatively easy. | Prioritize Upright, not equal effort across sources. |
| The e-commerce manager will maintain the process. | Amanda2.0 says that manager left; Amanda now has an assistant. | Minimize upkeep and avoid depending on a departed role. |
| Jev is deterministic and has no token costs. | Jev is a probabilistic structured-decision AI model. Some browser implementations support model-free replay. | Separate model-assisted discovery from deterministic execution; account for usage and approval. |
| Excel becomes unsuitable at 10,000 rows. | No universal 10,000-row threshold establishes that. | Justify a data layer by controls, history, concurrency, and maintenance—not a false row limit. |
| 50–55% is the online sell-through target. | The corrected brief/PRD identifies that as an in-store reference; online target remains unresolved. | No invented online target or red/green status. |
| A data engineer costs $100k, therefore that is required. | Jack’s document identifies it as a rough guess. | Budget roles and actual support work rather than asserting a mandatory salary. |
| There is no reporting infrastructure at all. | Amanda describes Power BI downstream of manual consolidation. | Investigate and reuse existing reporting infrastructure. |

The current PRD has a conservative weekend scope. Wicks/Amanda evidence supports proposing one acquisition demonstration as the new differentiator, not silently promising nine live integrations. Update the spec through a deliberate scope decision before agents code.

The original recommendation to choose Beacon is superseded by the team’s Goodwill selection. Older setup language about not having a team is also stale.

## 2. ESTEEM approach: requirements before implementation

The team’s advantage is that it has examined both the executive request and the operator’s actual work. The credible story is not “we used AI to make charts.” It is:

> We spoke with leadership, the person pulling the reports, and technical mentors. We learned that restricted API access and repeated manual retrieval are upstream of the dashboard problem. We designed the system around those constraints.

Do not say every stakeholder has approved the design. Interviews with finance, IT/security, Sonia, and every source owner are not established by the reviewed record.

### Stakeholder-to-requirement map

| Stakeholder | Documented or proposed need | Product response | Evidence still needed |
|---|---|---|---|
| Amanda, district manager | Reports should arrive without repeated portal work; Upright is the main pain. | Authorized retrieval into an approved folder, eventually approved delivery. | Exact reports, timing, machine/session ownership, measurable baseline. |
| Debie, president and CEO | Clear e-commerce visibility and strategic KPIs. | Executive view with coverage, definitions, trends, and drilldown. | Ranked initial metrics, approved targets, reporting cadence. |
| Amanda’s assistant | Role exists in follow-up; detailed needs not yet interviewed. | Proposed simple run status and recoverable exceptions. | Actual responsibility and usability feedback. |
| Sonia, administrative assistant | Interview describes combining summaries with store sales. | Compatible exports and explicit reconciliation. | Her workbook, definitions, and approval of output. |
| Finance/accounting | Deck describes allocation workbook and Business Central close. | Preserve rules; later validated journal/invoice previews and controlled imports. | Workbook, mappings, example close, accounting sign-off. |
| IT/security | Production owner and approval authority, not fully documented. | Approved storage, identity, browser runtime, data flows, least privilege. | Access policy, AI policy, provider terms, retention, hosting approval. |
| Michael Wicks | Three layers; generic acquisition; low-maintenance data; AI-native app. | Modular architecture and a faithful acquisition demo. | Advice is not production approval. |
| Horatio | Fast synthetic-data prototype and hosted application path. | Practical weekend build and clearly labeled demo. | Do not convert mentorship into client security certification. |

### Required planning artifacts before unattended work

1. A ranked requirement register: ID, stakeholder, source, acceptance test, priority, approval state.
2. Current-state process map with report names, clicks, date parameters, timing, handoffs, and failure points.
3. Source register distinguishing report source, underlying marketplace, acquisition method, and accounting role.
4. Metric dictionary with formulas, grain, required inputs, exclusions, freshness, and owner.
5. Data/API contracts shared by every coding agent.
6. Architecture decision record identifying demo choices versus production choices.
7. Explicit non-goals and permission boundaries.

Examples:

- **REQ-ING-01:** for a selected date range, collect the expected report and retain file/run evidence.
- **REQ-CTL-01:** uploading the same report twice leaves totals unchanged.
- **REQ-DAT-01:** a missing or late source is visible and cannot silently become a zero.
- **REQ-KPI-01:** every displayed metric identifies its definition, period, coverage, and supporting records.
- **REQ-AI-01:** an unsupported question receives an honest unavailable/uncertain answer.
- **REQ-FIN-01:** no production accounting posting without finance validation and explicit authorization.

## 3. End-to-end target architecture

```text
Authorized portals    Approved APIs    Approved email/folder intake
        \                   |                   /
         └──────── Acquisition adapters ────────┘
                            |
            Immutable raw reports + manifest
                            |
          Parse → validate → quarantine errors
                            |
         Normalize → reconcile → version rules
                            |
          Managed analytical data + SQL marts
                  /                  \
       Excel / Power BI          Metric API
                                      |
                       Dashboard + approved AI tools
                                      |
                        Proposed actions / review queue
```

Controls run throughout: credentials, source lineage, duplicate protection, freshness, reconciliation, role permissions, audit trail, and recovery.

**Default prototype stack:** TypeScript React/Vite interface; Node API; managed PostgreSQL; SQL transformations; Playwright-based isolated browser runner; CSV/XLSX adapters; deterministic fixtures; Vitest-style unit/contract tests and Playwright end-to-end tests.

Reuse an existing implemented stack if one exists; the inspected repository tree mainly contains requirements, planning, and small synthetic files, not proof of a running application. Do not ask overnight agents to build multiple alternative stacks.

The browser runner needs a runtime capable of running Chromium and an appropriate session policy. Do not assume the web application’s hosting automatically provides a suitable scheduled browser runtime.

## 4. Phase 1 — Reliable report acquisition

### Objective

Replace repetitive report retrieval with an authorized, parameterized, observable workflow. Deliver a usable source package before requiring Goodwill to change its analysis tools.

### Acquisition decision order

1. Use an existing supported scheduled report/export feature if available.
2. Use a documented API if access is available, affordable, authorized, and sufficient.
3. Use approved email attachments or a controlled folder feed.
4. Use authorized browser automation for the existing permitted user workflow.
5. Keep a manual-upload fallback.

API ingestion is still a good engineering option when supported. “API was last year’s answer” is pitch rhetoric, not a general architecture rule. Browser automation can reduce dependency on missing API access, but must not bypass a provider restriction or Goodwill policy.

### Nine sources are not nine complete integrations

Generic acquisition can be shared across source types, while parsing, date logic, identities, and accounting rules remain source-specific.

| Source workflow | Likely acquisition class | Special care |
|---|---|---|
| Upright paid-order reports | Portal initiation; possibly generated email delivery | Restricted API; report generation delay; paid orders versus paid order items. |
| Cash Monkey orders | Portal CSV export | Easier operator workflow; books reporting and overlap. |
| Jewelry report | Requested/provided report | Supplier enrichment and unconfirmed mappings. |
| OSM/PB/EasyPost | Approved export or lookup | Expense and bank-linked data, not another revenue feed. |
| FedEx charges/refunds | Export or authorized accounting lookup | Refund netting, period and mapping controls. |
| ShopGoodwill reports | Portal exports | Periodic report types and overlapping sales. |
| Goodwill Books statement | Monthly email attachment | Payout statement versus transaction revenue. |
| eBay report | Portal download or supported API | Listing/sales grain, refunds and relists. |
| Amazon summary | Asynchronous generated report | Payment summary versus sales revenue and settlements. |

These are acquisition hypotheses based on the brief. Confirm actual paths with owners. A common mailbox fetcher does not mean all attached formats can use one parser.

### Michael’s screenshot/slides-to-HTML demonstration

Implement one scoped replica of the Upright report journey using the supplied PowerPoint/screenshots:

1. Inspect the slides and record visible controls, labels, states, and report sequence.
2. Build a functioning HTML interface, not a static picture.
3. Include Reports, Paid orders, start/end dates, Generate, a loading/ready state, and Download as supported by the actual material.
4. Generate a synthetic CSV whose date coverage follows the selected dates.
5. Add delayed generation, expired-session, unavailable-report, and changed-label test modes.
6. Point browser automation at the replica and verify the downloaded file.
7. Pass that exact file into Phase 2 and show the dashboard change.
8. Label the replica and every resulting figure as simulated/synthetic.

A screenshot documents appearance; it does not reveal the real portal’s DOM, network behavior, authorization, or download mechanics. Replica success verifies our demonstration harness, not compatibility with real Upright.

The browser skill should be parameterized by report type and dates, with explicit allowed hosts, expected page states, download validation, timeouts, and stop conditions. Never store passwords or session cookies in the shareable skill.

### Jev: use the right technical description

TypeSafe describes Jev as a System One AI model producing typed probabilistic decisions. It is not a macro recorder and not guaranteed to pick the right control. No type errors does not mean no semantic errors.

Distinguish:

- **Deterministic browser replay:** tested browser code executes a known sequence and assertions, without a model call.
- **Jev-assisted decisions:** model selects among observed allowed controls; surrounding code validates and acts.
- **Language-model planning:** an LLM proposes goals or builds a candidate skill; this is another model-based component.

Public implementations differ. One uses an LLM planner plus Jev per-step decisions. Another can generate cases and replay them without the decision model. Do not describe all implementations as one product.

Recommended prototype: deterministic Playwright flow as the reliable baseline; Jev behind an optional decision-provider interface. If actual Jev access exists, measure it separately. Without access, label a scripted provider as scripted—not Jev.

Recommended production operating pattern: human-approved capture/discovery → verified replay → pause on drift → reviewed repair. Do not let a model silently “heal” a financial acquisition flow into a different report.

Jev is an AI service and needs the same Goodwill review as other AI. Amanda’s Copilot-only condition means external Jev is not automatically production-compatible. Consider it a synthetic-data experiment until IT approves the data and model path.

### Recorder scope

For the weekend, prefer a saved, parameterized skill over a universal macro-recorder product. A limited capture mechanism against the replica is a stretch feature.

A production recorder would need consent, redaction, role/name locators, event and state capture, review/versioning, secret handling, and policy enforcement. An iframe is not a general portal-integration solution: cross-origin restrictions and frame-blocking policies can prevent it. A browser extension or approved local runner is later work.

### Phase 1 acceptance and handoff

- Report for date range A contains the expected A records; changing to B changes coverage correctly.
- A downloaded file is checked for source, format, headers, period, and actual content.
- Download completion is verified; clicking Download is not sufficient.
- Delayed generation waits safely and stops within a configured timeout.
- Login/MFA/CAPTCHA/access denial triggers human intervention, not bypass.
- Wrong dates, missing files, or wrong report types fail visibly.
- Run evidence includes skill version, source, period, timing, checksum, result, and error.
- A retry does not duplicate delivery or imports.
- A source package can be used with Excel even if later phases are unavailable.

For production, add approved scheduling, service identity/session ownership, a delivery location, incident ownership, and monitored reliability. “Ready Monday” requires those prerequisites; a replica alone does not establish it.

## 5. Phase 2 — Trusted centralized data and deterministic metrics

### Objective

Create a reconciled, explainable reporting foundation without forcing Goodwill to maintain unnecessary custom infrastructure.

Centralization is a requirement to investigate, not proof that a new warehouse is mandatory. Goodwill already has Microsoft reporting infrastructure. Start with the controls required; select the simplest approved tool that meets them.

### Excel versus an analytical store

| Need | Excel / Power Query | Managed relational analytical store |
|---|---|---|
| Familiar review and exports | Strong fit | Export/connected workbook preserves familiarity. |
| Repeatable ingestion | Possible with governed queries and refresh | Explicit job and batch model. |
| Concurrent updates | Requires careful design | Transactions and access controls. |
| Source history and lineage | Possible but needs discipline | Natural tables for files, rows, batches, versions. |
| Constraints and duplicates | Often conventions/custom logic | Unique keys, checks, foreign keys. |
| Dashboard and agent access | Possible through supported connectors/models | Narrow query/API interfaces. |
| Maintenance | Workbook ownership still required | Managed service still needs data/rule ownership. |

Do not argue that Excel cannot power dashboards or AI. The case for an analytical database is stronger control over history, repeatability, reconciliation, growing source diversity, and access.

A sensible bridge is automated reports in an approved folder → Power Query/validated master workbook → existing Power BI. A managed SQL layer is justified if that approach cannot meet the confirmed needs. The prototype can use PostgreSQL without implying that the client must buy it.

### Warehouse fundamentals

An operational database stores application records; a warehouse organizes data for consistent historical analysis. PostgreSQL can support a modest analytical prototype without pretending to be an enterprise warehouse platform.

Define grain before joins:

- One sales fact per source-specific sale/item event.
- One refund fact per refund event.
- One cost fact per fee/shipping/expense event.
- One listing fact per listing event.
- One inventory fact per item/snapshot.
- One labor fact per store/team/work period, with explicit allocation policy.
- One settlement fact per payment/settlement event, separate from revenue.

Dimensions include date, source, marketplace, store, category, item, and platform-local buyer. Conformed IDs and mappings enable joins; unmatched IDs remain exceptions.

Never total all nine report values as revenue. Upright and ShopGoodwill may describe the same transactions; a Books payment statement may be a settlement; FedEx is an expense. Create a metric-specific system-of-record matrix before combining them.

### Raw → staging → curated → metrics

1. **Raw archive:** unchanged source files, checksums, coverage, capture time, synthetic flag.
2. **Staging:** parsed rows with original row identity and typed values; quarantined invalid rows.
3. **Curated facts/dimensions:** normalized records with source-specific keys, mappings, and rule versions.
4. **Metric marts:** approved calculations at daily/platform/store/category/month grain.
5. **Consumption:** dashboard, controlled Excel exports, approved Power BI model, narrow agent tools.

Use decimal arithmetic or integer minor units for money. Record currency and explicit conversion policy. Store transaction timestamps separately from reporting dates and timezone. Keep missing values distinct from zero.

### ETL versus ELT

- **ETL:** extract, transform in code, then load curated records.
- **ELT:** extract, load raw/staging records, then transform inside SQL.

Recommended practical hybrid: acquire/archive files; parse and validate types in code; load staging; normalize/reconcile/aggregate in SQL. Both labels are legitimate depending on the step. Do not distort the architecture to satisfy an acronym.

A DAG is a directed acyclic graph of dependencies, not necessarily a heavy orchestration product. Initially:

```text
Acquire → verify file → archive → parse → validate → stage
                                                |
                         map + deduplicate + reconcile
                                                |
                       publish approved metric version
```

Jobs must be idempotent, dependency-aware, observable, and recoverable. Start with a small job runner and control tables. Add an enterprise orchestrator only if scale and support justify it.

### Views, materialized views, and freshness

A normal SQL view stores a query, not its results. A materialized view stores results and needs refresh. Aggregate tables can be recomputed transactionally. Use the simplest approach that meets measured performance.

Do not promise “10-second calculations” without a benchmark. Publish metrics only after required validation succeeds. Retain the last good version with a conspicuous freshness warning if the new batch fails.

Store source coverage separately from last ingestion time: an import today may contain last month’s data. Late-arriving refunds and corrected exports need controlled reprocessing and revised metrics.

### Proposed core tables

- `sources`, `report_definitions`, `acquisition_runs`
- `source_files`, `import_batches`, `rejected_rows`
- `fact_sales`, `fact_refunds`, `fact_costs`, `fact_settlements`
- `fact_listing_events`, `fact_inventory_snapshots`, `fact_labor_hours`
- `dim_store`, `dim_marketplace`, `dim_category`, `item_source_mapping`
- `metric_definitions`, `metric_runs`, `daily_metrics`
- `reconciliation_results`, `exceptions`, `audit_events`

Minimum row lineage: source file → row → curated record → metric version. Include parser, transformation, mapping, and metric-definition versions.

### Resolve the existing revenue conflict

The active PRD proposes sales less refunds, excluding shipping/tax. The synthetic README proposes including shipping credits/collected shipping. Both are proposals; they conflict.

For the weekend, use the narrower active-PRD convention:

**Demo net sales = item sales − refunds, excluding shipping, tax, and fees.**

Keep shipping and fees separate. Call the metric “demo net sales” rather than implying approved Goodwill net revenue. Align fixtures, expected totals, SQL, API, chart labels, exports, and assistant wording before parallel work.

Production definitions must come from finance. Distinguish net sales, gross profit, net profit, marketplace payout, and cash received.

### KPI contracts

| KPI | Deterministic calculation | Required inputs / caveat |
|---|---|---|
| Demo net sales | Item sales minus refunds | Approved synthetic convention; matching scope/currency. |
| Customers | Distinct non-empty buyer IDs within platform and period | Do not use rows as unique people or sum identities across platforms. |
| Operational row-count proxy | Rows counted under the existing process | May be useful for reconciliation; label separately from unique buyers. |
| Listings created | Count distinct listing events | Relists separated; source-store key. |
| Unlisted backlog | Items in approved unlisted states at a complete snapshot | Not derivable from sales alone. |
| Revenue per labor hour | Agreed revenue / matched labor hours | Employee count is not labor hours; missing/zero denominator means unavailable. |
| Net margin | Approved net profit / approved revenue | Cost coverage and allocation rules required. |
| Sell-through | Sold eligible cohort items / eligible cohort items | Explicit cohort/window and relist policy. |
| Year-over-year growth | Comparable current/prior period change | Prior data; zero/unknown baseline policy. |

Never invent labor, inventory, customer survey, or cost records to make an unavailable real metric look available. Synthetic demo inputs can illustrate these measures only with explicit labeling.

### Phase 2 acceptance

- Same file twice leaves totals unchanged.
- Distinct files with overlapping records do not duplicate transactions.
- Revised exports follow a declared replacement/upsert policy; file checksum alone is insufficient.
- Malformed rows are quarantined with recoverable errors.
- Source totals reconcile to accepted/quarantined rows.
- Revenue, settlement, and expense records are not double-counted.
- Missing store/buyer/labor/cost data appears as unknown, partial, or unavailable.
- Dashboard totals and source-row drilldown agree.
- Reprocessing yields the same result under the same rule versions.
- Failed batches cannot publish an apparently complete new reporting day.
- Corrections and backfills are auditable.

## 6. Phase 3 — Dashboard and bounded agentic interaction

### Objective

Give leaders useful visibility and operators a clear explanation of reporting status. Provide approved AI access to the same trusted metrics—not a separate model-generated version of the truth.

### Three user views

**Operations / Amanda:** expected reports, arrival status, coverage, latest run, retries requiring review, files ready for use, exception owner.

**Leadership / Debie:** daily/monthly performance, available strategic KPIs, comparisons, store/category/platform drilldown, definitions, freshness and missing-source warnings.

**Finance:** source readiness, reconciliation, source-linked exports, later workbook-equivalent output preview. No production posting in the weekend scope.

Prototype screens: source intake; daily pulse; executive scorecard; exceptions/provenance; optional Ask the data panel. Keep the four committed metric views unless the team deliberately replaces one with a verified strategic KPI.

### Existing Power BI versus custom demo

Use the custom app for a clear weekend story and combined intake/metrics demonstration. Production may be better as improved data acquisition plus Power BI, with a small operations console only if needed.

Avoid rebuilding a reporting product solely because an agent can generate frontend code quickly. Custom ownership, user administration, accessibility, refresh, monitoring, and support remain real costs.

### What “agentic” should mean

An agent should select among permitted tools, retrieve evidence, compare results, and propose a next step under policy. A chatbot that invents numbers is not the goal.

Proposed progression:

1. **Read-only grounded assistant:** answer metric questions with source coverage and supporting results.
2. **Proactive analyst:** scheduled checks on published data; draft summaries and anomaly explanations for review.
3. **Controlled workflow assistant:** propose a re-run or exception assignment; require explicit approval for consequential actions.
4. **Later automation:** execute only narrowly preauthorized actions after reliability and security validation.

### Narrow tool interface

Illustrative tools:

- `get_metric(metric_id, period, filters)`
- `compare_metric(metric_id, periods, filters)`
- `get_source_coverage(period)`
- `get_reconciliation(import_id)`
- `get_metric_definition(metric_id, version)`
- `get_supporting_rows(metric_run_id, limit)`
- `propose_report_rerun(report_id, period)`

Responses include metric ID/version, value/unit, scope, coverage, freshness, warnings, and evidence references. Enforce permissions in the service/database, not just the prompt.

Default to approved metric queries, not unrestricted SQL. If later adding generated SQL, use a restricted read-only role, allowlisted datasets, validated queries, limits, timeouts, and audited execution. MCP is an interface protocol, not a security guarantee.

RAG can retrieve operating procedures and definitions. Exact numbers must come from deterministic queries, not embeddings or snippets of spreadsheets.

### Example: “Why is revenue per labor hour down?”

1. Confirm reporting window and store/platform scope.
2. Check that revenue and labor datasets cover the same scope.
3. Retrieve current and prior calculated values.
4. Decompose the ratio into revenue and labor-hour changes.
5. Inspect categories/marketplaces with sufficient coverage.
6. Explain observed contributors and cite the results.
7. Identify missing data and distinguish possible causes from established causes.
8. Propose investigation rather than autonomously changing staffing or prices.

It can say that revenue fell and hours rose. It cannot infer that staff were less productive without supporting evidence. If labor data is absent, say the metric is unavailable.

### Copilot and Teams

Amanda explicitly says AI must go through Copilot. Plan an approved Copilot surface rather than silently deploying a separate commercial chatbot with real Goodwill data.

Confirm tenant licensing, Copilot extension/tool options, identity, approved service endpoints, permissions, data residency/retention, and the owner who will support the integration. A Teams-styled interface is not an actual Teams integration. A “Copilot-ready” backend is not a working Copilot connection.

For the demo, a synthetic-data assistant can be an optional illustration. If the approved model path is unavailable, use direct typed queries or clearly labeled scripted example interactions. Never misrepresent them as live Copilot.

### Agent safety and evaluation

- Treat source text, DOM labels, reports, and retrieved procedures as untrusted data, not instructions.
- Restrict network hosts and tool capabilities; block arbitrary code and writes.
- Test fabricated instructions in report fields and portal content.
- Test cross-store access, unavailable metrics, missing sources, changed definitions, and unsupported causal questions.
- Validate that every financial number in a response matches a returned deterministic result.
- Fail closed on tool errors; never substitute a plausible figure.
- Audit prompts/tool calls/results while respecting privacy and retention.
- Do not send real buyer, employee, or accounting data to unapproved providers.

### Phase 3 acceptance

- Metric cards, exports, and assistant responses agree for identical scopes.
- User filters and permission scope are honored.
- Missing coverage is displayed and mentioned in assistant answers.
- Definition and source evidence are accessible.
- Read-only questions cannot trigger postings, emails, or browser writes.
- Unsupported questions stay unsupported.
- Scripted interactions and model-assisted interactions are distinguishable.
- Observed drivers are not presented as proven causation.

## 7. Weekend MVP versus production roadmap

### P0: working evidence

- One functional Upright-style HTML replica derived from supplied material.
- One parameterized browser flow producing a real downloadable synthetic CSV.
- One import adapter with validation, lineage, duplicate/overlap protection, and reconciliation.
- A dashboard updated from that exact acquired file.
- Source coverage/freshness plus an exception view.
- One alternate date range and one failure demonstration.

### P1: deepen only after P0 passes

- A second source represented by an explicitly synthetic file, using the same intake contract.
- Focused four-view dashboard consistent with the current PRD.
- Excel-compatible summary export.
- Small grounded assistant using the approved demo model path.
- Side-by-side Jev versus deterministic replay measurements if access is actually available.

### P2: defer

- Universal macro recorder/browser extension.
- Nine live integrations.
- Fully automated month-end close.
- Live Business Central journal/invoice posting.
- Production Copilot deployment.
- Autonomous pricing, staffing, or marketplace listing.
- Predictive inventory models.

The nine-source synthetic package is useful for mapping/testing, not a commitment to finish nine integrations overnight.

## 8. AI engineering practices for overnight work

### Separate build agents from operating agents

**Build agents** write code/tests/documentation in isolated development environments. **Operating agents** interact with business systems and data.

Authorize overnight build tasks against fixtures and the replica. Do not give those agents production marketplace sessions, real reports, broad database access, or permission to post accounting entries.

An overnight agent is not a substitute for an agreed requirement. Humans own stakeholder interpretation, security policy, financial definitions, scope, and final acceptance.

### Prerequisites before anyone sleeps

1. Commit one authoritative scope/requirements document.
2. Freeze the metric, file, API, and error contracts for the night.
3. Build a minimal passing vertical slice and establish its smoke test.
4. Assign mutually exclusive file lanes and separate git worktrees/branches.
5. Install dependencies and verify each runner can execute the required tests.
6. Prepare deterministic fixtures and an independently computed expected-results ledger.
7. Set time, retry, cost, permissions, and network limits.
8. Configure output collection, failure reporting, and the morning review process.

If a vertical slice is not working at handoff, overnight work should focus on fixing that skeleton and writing tests, not adding a chatbot, recorder, or more sources.

### Recommended agent lanes

Start with three or four simultaneous workers, not nine. Parallelism helps only when contracts and lanes are independent.

| Lane | Bounded task | Permitted area | Required return |
|---|---|---|---|
| Replica/browser | Functional report replica and one acquisition flow | Replica/browser modules and their tests | Download evidence; date, delay, drift and session tests. |
| Data pipeline | Parse fixture, normalize, reconcile, deduplicate | Ingestion/data modules; approved migrations | Expected totals and unit/integration tests. |
| Dashboard | Screens against frozen API fixtures | Frontend only | Filter/freshness/source-drilldown tests and screenshots. |
| QA | Independent end-to-end and adversarial tests | Test/fixture areas only | Failure list with reproduction and evidence. |
| Assistant, later wave | Read-only tools and grounded responses | Assistant/tool modules | Evaluation cases; numerical agreement and permission tests. |

Migrations, lockfiles, generated client types, shared API contracts, and entrypoints each need a single owner. Other agents propose changes rather than concurrently editing those files.

Do not assume an unattended Replit session automatically orchestrates all of this. Choose and verify an actual runner: bounded project tasks, coding-agent sessions, or a managed job/CI mechanism. Scheduled execution needs its own persistent runtime, credentials and permissions, timeouts, budget enforcement, and cancellation. This plan does not schedule any jobs.

### Agent task packet

```text
Task ID and title:
Business requirement IDs:
Goal:
Allowed files:
Forbidden files/actions:
Frozen interfaces:
Fixtures and expected results:
Acceptance tests:
Commands to run:
Runtime/cost/retry limits:
Stop and escalation rules:
Output location:
```

Task example:

```text
ING-01: build the paid-orders browser replay against the local replica.
Use report start/end dates from inputs, not hard-coded values.
Do not access real Goodwill portals or credentials.
Verify the downloaded CSV’s headers and date coverage.
Test delayed generation and expired-session handling.
Edit only browser-flow/ and its tests.
Do not change the shared ingestion contract.
Stop after two failed repair attempts or the configured deadline.
Return branch, commit, tests actually run, evidence files, and blockers.
```

### Repository instruction files

- `SPEC.md`: authoritative requirements and non-goals.
- `DEMO.md`: behavior the demo must prove and truthful labels.
- `AGENTS.md`: stack, commands, file ownership, permission limits, source-data handling.
- `contracts/`: data/API/tool schemas and frozen examples.
- `TASKS.md`: IDs, dependencies, acceptance criteria and assigned owners.
- `decisions/`: metric and architecture decisions.
- `fixtures/expected-results.*`: independent expected values.
- `reports/<task-id>/`: each agent’s results, logs, diff summary and evidence.

Use one orchestrator to update shared task status, or separate per-task reports. The older plan’s “every agent edits STATUS.md” creates avoidable collisions.

### Test-driven and evidence-driven development

Require agents to read contracts and write/confirm tests before implementation. Test execution is part of the deliverable:

- Static checks/types.
- Unit tests for parsers and formulas.
- Contract tests for frontend/backend/tool results.
- Integration tests for database imports and reconciliation.
- Browser tests for actual download artifacts.
- End-to-end test matching the demo sequence.
- Negative tests for wrong dates, expired sessions, duplicates, missing sources and injected instructions.

Independent expected totals matter. An agent that writes both the formula and an expected value using the same wrong assumptions can pass its own tests.

Judge model-based components with a fixed evaluation set. Do not keep changing prompts until only favorable examples remain.

### Bounded autonomy

Proposed defaults, to be chosen within the team’s actual credit/time budget:

- One task per worker and a small patch.
- At most two repair attempts, then stop with a reproducible blocker.
- Explicit per-task deadline and total nightly spend cap.
- No purchasing/upgrading plans, adding unapproved providers, external messages, credential changes, production access, posting, or deletion.
- No unattended feature merges or deployment.
- No disabling/skipping tests to make a build appear successful.
- No hiding unsupported inputs or removing synthetic labels.

Use less expensive model tiers for bounded fixture/test/documentation tasks and more capable tiers for difficult debugging when justified. Tier choice does not replace acceptance tests.

### Nightly dependency waves

**Wave 0, human-led:** frozen contracts, metric decisions, seed data, scaffolding, passing smoke test.

**Wave 1, parallel:** replica/acquisition; deterministic pipeline; dashboard against mocked contract; independent QA.

**Wave 2, only after integration checkpoint:** assistant; second adapter; usability polish. Dependent jobs wait for a known passing upstream artifact instead of assuming it exists.

**Morning integration:** review each patch, merge dependency order, run the complete demo, reject scope creep, inspect failure evidence, rehearse, and record backup.

Human review must inspect financial logic, permissions, date coverage, source authenticity, and reconciliation even if a reviewer agent gives a positive summary. A review agent is not independent accounting approval.

### Illustrative remaining schedule

Adapt to actual team readiness; do not treat earlier relative H2/H6 checkpoints as still upcoming.

| Checkpoint | Outcome |
|---|---|
| Before overnight handoff | Freeze scope/contracts; one vertical slice; agent limits and lanes. |
| First night wave | Three independent implementation lanes plus QA; no production actions. |
| Overnight | Bounded repairs and test completion; per-task evidence; stop on limits. |
| Sunday morning | Human merge/reconciliation review and full end-to-end run. |
| By midday | Cut unproven features; fix correctness and provenance first. |
| Early afternoon | Rehearse, capture fallback and final evidence, assemble submission. |
| Before 4pm planned freeze | Verify event deadline, submit required materials, no new features. |

The corrected brief states Sunday 4pm freeze and 4:30pm Pod B demos. Confirm any event updates with organizers. Recorded evidence is essential; a live-run capability is desirable but event format remains a logistics check.

### Morning report template

```text
Task:
Requirement covered:
Branch / commit:
Changed files:
Tests actually run:
Pass/fail and logs:
Evidence artifact:
Measured runtime / usage:
Remaining limitations:
Production/synthetic distinction:
Blockers:
Recommended review step:
```

Do not accept “done” without the artifacts needed to reproduce the result.

## 9. Synthetic data and realistic test coverage

The repository’s existing nine CSVs are small and useful, but not sufficient evidence of scale or full financial coverage.

Build deterministic test fixtures using a fixed seed, agreed schemas, fictional IDs, and independently computed control totals. Use generated code to create data after a human freezes the conventions.

Include:

- Multiple dates and a weekend.
- Several fictional stores and marketplace-local buyer IDs.
- Sales, partial/full refunds, costs, settlements and overlapping source reports.
- Missing buyer/store/supplier keys.
- Duplicated files, overlapping exports and corrected files.
- Month boundaries, report-date differences and late data.
- Relists and unsold inventory.
- Missing/partial labor and inventory coverage.
- Delayed report readiness and session failures.

Keep each input’s grain explicit. Synthetic labor/snapshots are additional invented demo inputs, not fields confirmed in current Goodwill exports.

Measure import/query/browser performance on declared fixture sizes, hardware/runtime and conditions. Report measurements as prototype measurements, not promised production savings.

## 10. Finance and Business Central roadmap

The three-phase story does not remove the close-control problem. Preserve it as later gated work:

1. Inventory allocation workbook inputs, formulas, named ranges and outputs.
2. Translate approved rules into versioned code/SQL.
3. Reconcile source → workbook-equivalent → proposed journal/invoice output.
4. Validate dimensions/accounts and interfaces in an approved test environment.
5. Obtain accounting and security approval.
6. Pilot human-approved import/posting with retained responses and reconciliation.

Balanced debits/credits are necessary, not sufficient. A balanced journal can still use the wrong period, account, dimension, duplicate source, or amount.

Use workbook parity and signed mapping/definition tests. No model should decide account mappings, silently invent missing suppliers, or autonomously post entries.

The weekend should show at most a clearly labeled unvalidated mapping/export preview. Remove any button or phrasing that implies production posting.

## 11. Production continuation: proposed three-month plan

The Sprint Lab is a possible continuation, not an approved contract. The following is a planning estimate, contingent on access and owners:

- **Weeks 1–2:** validate source/metric inventory, workbook, Microsoft capabilities, policy, authorized retrieval, support owner and baseline effort.
- **Weeks 3–4:** implement one approved source, run in parallel, verify coverage, recovery and operator usability.
- **Weeks 5–6:** add prioritized source classes; implement source-specific parsing/mapping and reconciliation.
- **Weeks 7–8:** stabilize daily reporting; compare existing Power BI/Excel path against added storage needs; validate strategic KPI inputs.
- **Weeks 9–10:** approved dashboard/metric tools; Copilot proof of concept if tenant/permissions allow.
- **Weeks 11–12:** operational acceptance, runbooks, handover, and decision on close-automation pilot.

Do not require a universal recorder, all-source coverage, fully automated accounting and enterprise Copilot rollout to fit that estimate.

Assign real owners before deployment: Goodwill process owner, IT/platform owner, metric/accounting owner, support escalation, and partner implementation owner. A managed database removes some infrastructure work but not data engineering or business-rule stewardship.

## 12. Success metrics and ROI

Collect a baseline rather than turning interview estimates into a guaranteed saving. Amanda estimates roughly 30–45 minutes for someone reasonably capable, with interruptions; other notes use 45+ or 30–60 minutes.

Measure:

- Active operator minutes per report package.
- Coverage by required report/period.
- On-time report arrival and successful acquisition rate.
- Duplicate and reconciliation error rate.
- Time to recover from a changed portal or missing source.
- Reporting delay from availability to useful dashboard publication.
- Support effort and total recurring cost.
- Operator and leadership acceptance.

Formula:

**Annual net benefit = measured hours avoided × agreed loaded hourly cost − recurring service/support costs.**

Separate gross time saved from time redirected, and label extrapolations and assumptions. Do not multiply by 24 stores without evidence that each independently does this task; the sources may use shared platform accounts and centralized retrieval.

Financial uplift, improved sell-through, and mission impact are possible downstream outcomes, not established by faster report acquisition alone.

## 13. Risks and scope decisions

| Risk | Mitigation / stop rule |
|---|---|
| Unauthorized browser automation | Provider/Goodwill approval before live use; no restriction bypass. |
| External AI conflicts with Copilot-only policy | Synthetic-only Jev experiment unless approved; model-free production path. |
| Replica mistaken for live integration | Persistent simulated labels and explicit narration. |
| Wrong report/date downloaded | State checks plus file-content assertions. |
| Portal changes / MFA | Pause, manual fallback, versioned reviewed repair. |
| Conflicting metric rules | One signed/frozen metric dictionary before parallel build. |
| Overlapping source transactions | Metric-specific system-of-record and source key mappings. |
| Incomplete data looks complete | Coverage controls and last-good version warnings. |
| Agent patches conflict | Separate worktrees/lanes, one owner for shared contracts/migrations. |
| Overnight usage runs away | Deadline, budget, retries, cancellation and reporting. |
| Too much demo scope | Cut recorder, extra sources, chatbot, close posting—in that order. |
| No maintenance owner | Do not deploy unattended live operation until ownership exists. |

## 14. Demo narrative

Suggested sequence, to fit the event’s actual allotted time:

1. Explain the CEO’s goal and Amanda’s upstream bottleneck.
2. Show the supplied process material and clearly labeled Upright-style replica.
3. Run the report flow for a date range and verify the synthetic downloaded file.
4. Import it; show validation, reconciliation and source lineage.
5. Show dashboard updates and available metric definitions.
6. Change dates; rerun; demonstrate parameterization without editing code.
7. Reimport the file; totals stay unchanged.
8. Trigger a missing report or expired session; the system stops visibly.
9. If ready, ask a grounded metric question and show its supporting results.
10. Explain what remains for production: authorized live access, Goodwill policy, source mappings, Microsoft integration and named owners.

Recommended close:

> We did not start by coding a dashboard. We understood the report-retrieval work, the restricted access, the spreadsheet handoffs, and leadership’s need for trustworthy visibility. Our prototype connects those needs: collect a report, verify the data, calculate consistently, and make the result accessible—with a clear path to Goodwill’s existing tools.

Do not claim it works for every source, takes nine seconds in production, costs no tokens, has no errors, or can be installed Monday without prerequisites.

## 15. Immediate team decisions

1. Approve the acquisition-led weekend scope and update the authoritative spec.
2. Inspect Amanda’s actual PowerPoint/screenshots for the replica.
3. Resolve the demo net-sales convention everywhere.
4. Freeze the acquisition/file/metric/tool contracts.
5. Confirm actual Jev access and model policy; choose deterministic replay fallback.
6. Build one vertical slice before releasing overnight lanes.
7. Assign one human integrator and independent financial/test review.
8. Configure bounded runners and a morning evidence report.

No agents have been started, no jobs scheduled, no repository changes published, and no production systems modified as part of preparing this plan.

## Source register

### Internal documents

- Jack explanation.md: https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view?usp=drivesdk
- Michael Wicks plan: https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk
- Amanda interview: https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view?usp=drivesdk
- Amanda2.0: https://docs.google.com/document/d/1yveSPTDJ4PUVi1MjMvCP6ovVtyVy-M7UGOeDdDngz7g/edit?usp=drivesdk
- Corrected track brief: https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk
- Technical guide: https://drive.google.com/file/d/1F9aCkJTAbD2J58LxVtiKVH7prWXzJX2d/view?usp=drivesdk
- Amanda’s PowerPoint, located for implementation inspection: https://docs.google.com/presentation/d/1vkc_Mr8341bDyKkXOkxcKLMj-Du4rOYt/edit?usp=drivesdk
- Goodwill screenshot folder, located for implementation inspection: https://drive.google.com/drive/folders/1ZSaLN16iNElB123edptxJmjqCzyukcGx

### Repository material

- Repository: https://github.com/joconne8/sprinthack-nd-2026
- Active PRD: https://github.com/joconne8/sprinthack-nd-2026/blob/main/goodwill/PRD.md
- Deck extraction: https://github.com/joconne8/sprinthack-nd-2026/blob/main/deck.md
- Existing build plan: https://github.com/joconne8/sprinthack-nd-2026/blob/main/planning/agentic-build-plan.md
- Synthetic data conventions: https://github.com/joconne8/sprinthack-nd-2026/blob/main/goodwill/synthetic-data/README.md
- Team discussion: https://github.com/joconne8/sprinthack-nd-2026/blob/main/notes/goodwill-problem-discussion.md

### Meeting sources

- Kickoff: https://notes.granola.ai/d/645b31e5-53aa-495b-a338-1e5cd47db938
- Horatio: https://notes.granola.ai/d/bd4a35ce-e104-4029-8143-5aa47ba43995

### Jev verification

- TypeSafe announcement: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- Unofficial LLM-planner/Jev browser implementation: https://github.com/Ying-Kai-Liao/jev-browser
- Indexed browser implementation with generated replay cases: https://github.com/openqa-cn/jev-browser

Source statements, team interpretations, and proposed implementation decisions are intentionally distinguished throughout this document.