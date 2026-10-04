# Technical Upskilling Guide: Goodwill E-commerce Reporting

**Audience:** Teammates with operations, mechanical engineering, finance, math, or other non-software backgrounds  
**Purpose:** Explain the proposed system in everyday language so everyone can help make sound product and data decisions—without needing to become a software engineer.

**How to use this guide:** Read the overview first, then work through the three stages in order. Each stage explains the vocabulary, shows how the parts fit together, and gives a step-by-step exercise. Code examples are illustrations, not production integrations. The acronym reference at the end expands the technical shorthand.

**What everyone can contribute:** Mechanical engineering and operations teammates can map processes and failure points. Finance teammates can define costs, reconciliation rules, and accounting controls. Math teammates can challenge denominators, probability claims, and comparisons. Technical teammates can implement these requirements. You do not need to write code to identify whether the system is solving the right problem.

## The idea in one picture

```text
E-commerce sites, shipping reports, email, and spreadsheets
                         │
             1. Collect and check the data
                         │
           2. Keep it in a consistent data store
                         │
           3. Show it in dashboards and answers
                         │
        People make decisions; the system shows its work
```

The goal is not “add AI” for its own sake. It is to reduce repetitive report gathering, make calculations repeatable, and help Goodwill staff see trustworthy results across their sales channels.

## Read this first: what is confirmed, and what is still a proposal?

Michael Wicks’s notes describe three layers: **data ingestion**, **centralized data**, and an **application/dashboard layer**. They recommend grouping sources by how data is obtained, keeping the data layer simple to maintain, and building an AI-friendly dashboard. They do **not** settle every product choice.

In particular:

- **Jev is the TypeSafe AI model identified by the team.** The office-hours notes transcribed it inconsistently, but the supplied [TypeSafe announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev) identifies the actual product. Jev makes structured decisions; it is not, by itself, a browser, a macro recorder, or an end-to-end integration. The model and the code that operates the browser are separate components.
- **Power BI is not named in Wicks’s notes.** It is one possible dashboard product, not a confirmed part of his recommendation.
- **Google Apps Script is not named in Wicks’s notes.** It is a useful Google Workspace automation option, explained below so the team can compare approaches.
- A **macro recorder** is described as a possible way to record a person’s steps once. The notes call this an idea to evaluate, not a finished design.

Keep these distinctions visible when discussing scope. A good demo can use a mock site or synthetic data; that does not prove that a live integration, vendor permission, or production workflow is ready.

### One example to follow throughout the guide

Imagine Goodwill wants a daily report answering: **“How much did each online channel sell, what were the associated costs, and which store should receive credit?”**

The collector obtains reports. The data layer reconciles records and calculates agreed measures. The dashboard shows the results. The chatbot explains the results using those same calculations. None of these steps can supply missing labor hours or missing store attribution by guessing.

# Stage 1 — Data ingestion: getting information out of the source systems

## What “data ingestion” means

**Data ingestion** is the process of collecting information from another system and bringing it into your solution. Think of it as receiving, labeling, and checking deliveries before putting them in storage.

Goodwill’s sources may include e-commerce platforms, a shipping carrier, emailed reports, and files such as CSV exports. Wicks’s notes suggest mapping the sources into a few **types**—for example, downloaded files, email attachments, or reports collected from a website—rather than building a completely different process for every vendor.

## E-commerce software: the storefronts and sales channels

An **e-commerce platform** is a system where items are listed, orders are managed, or sales happen. Each platform may label fields differently or provide reports in a different format.

- **Upright:** described in the notes as a major pain point and specific to Goodwill Michiana. The current report workflow is a person signing in, selecting paid orders and a date, generating a report, and downloading it. The notes say API access was unavailable at that time.
- **CashMonkey:** described as a shared Goodwill system used for books.
- **ShopGoodwill, eBay, and Amazon:** other sales channels named in the Goodwill track brief.
- **FedEx:** a shipping carrier, not an online marketplace. Shipping information can help calculate delivery costs or understand fulfillment.
- **Business Central:** an accounting/enterprise system. The Goodwill brief says information is re-entered there for accounting and month-end close; whether or how a new system can upload data must be confirmed with the partner.

The exact mix of systems and report formats should be verified with Goodwill. Platform names alone do not tell us which data fields are available.

Also distinguish a **marketplace** (where buyers purchase items), an **operations tool** (which may manage listings, inventory, and orders), and an **accounting system** (which records financial activity). The same sale may appear in more than one system. Adding every report together without checking overlap could count a sale twice.

**ERP** means **Enterprise Resource Planning**: software that coordinates business functions such as finance and operations. Business Central is an ERP product. A reporting database is not automatically a replacement for the accounting system or its controls.

## API, export, and browser automation

There are several ways to collect data:

- **API:** a supported, structured connection between software systems. An API can let one system request data directly from another. Access may require vendor approval, a subscription tier, and credentials such as an API key.
- **Export:** a person or system downloads a report, often as a CSV or Excel file. This can be a practical first version even when an API is unavailable.
- **Browser automation:** software controls a browser to repeat actions a person would otherwise do on a website, such as opening a report and downloading it. It may be used when there is no usable API, but it can break if the website changes or sign-in/security rules change.

Wicks discussed browser automation that uses the page’s **DOM**. The DOM (Document Object Model) is the browser’s structured representation of a web page: its buttons, labels, fields, tables, and their relationships. It is more like using a page’s labeled controls than guessing where to click in a photograph of the screen. Browser-control code can prepare this page state for a decision model such as Jev. That is why the notes distinguish DOM-driven automation from screenshot-based computer vision.

**HTML**, or **HyperText Markup Language**, is a common language used to describe web-page content. The browser turns that content into the live DOM, which may change as someone interacts with the page. A **UI** is a **User Interface**: the controls a person sees and uses.

The notes’ suggested demo was to build a **fake Upright-like web page from screenshots** and test automation against that replica. A replica is a safe practice target; it is not the real Upright website, and a screenshot by itself is not a working integration.

Other terms in that discussion:

- **Computer vision:** software interpreting an image or screenshot. It may identify a button visually, whereas DOM-based automation can inspect the button as a structured page element. Neither approach is guaranteed to survive every website change.
- **Browser session:** the active state of a browser, including whether a person is signed in. Wicks’s proposed approach has a person sign in first, then lets automation use that session. It still requires authorized access and must not expose passwords or session information in recordings or logs.
- **Chrome extension:** a small add-on to the Chrome browser. A recorder extension could observe authorized page interactions, but it needs carefully limited permissions.
- **Iframe:** a web page embedded inside another web page. Wicks mentioned this as another possible recorder interface. Not every vendor allows its pages to be embedded, so this needs testing rather than assuming it will work.

## Jev: what it is, what it outputs, and where it fits

TypeSafe calls Jev a **System One model**, inspired by fast “System 1” thinking. The name Jev comes from William Stanley Jevons; **Jev is a product name, not an acronym**. The September 14, 2026 announcement describes it as an early-access model designed for fast, structured decisions rather than free-form text generation. [Source: TypeSafe announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

Here is the practical distinction:

- A typical **LLM (Large Language Model)** can write an explanation, a paragraph, or code.
- **Jev** returns values within a structure defined by the developer, along with probabilities/confidence information. It can help classify, route, score, or choose among permitted options.
- **Ordinary application code** decides what to do with that output, executes permitted actions, and checks whether they worked.

**Type-safe** means the output matches its declared shape and allowed value types. For example, a decision field might allow only `download`, `wait`, or `ask_human`; the model cannot return an arbitrary essay in that field.

**Correct shape is not the same as correct judgment.** Choosing an allowed button can still mean choosing the wrong button. TypeSafe's “can't hallucinate” language should not be interpreted as “the complete workflow cannot fail.” A wrong classification, stale page, incomplete input, or bad metric definition can still produce a bad result.

### A conceptual Jev-assisted report workflow

1. **A person signs in** through the normal authorized process. Multi-factor authentication (**MFA**) may still require human involvement.
2. **Browser-control code inspects the page.** A browser automation library such as Playwright or Selenium could do this; these are illustrative implementation options, not products chosen in Wicks’s notes.
3. **The code prepares the model’s input.** It supplies relevant labels and page state, the task, and a limited set of possible decisions. Do not send every page field or customer detail unnecessarily.
4. **Jev evaluates the permitted choices.** For example: which available control appears to open the paid-orders report?
5. **The application applies a policy.** If the decision is uncertain, the page is unexpected, or the action is disallowed, stop and ask a person. A confidence threshold must be tested on realistic examples, not picked because it sounds safe.
6. **Browser code performs the action.** Jev’s decision does not itself download a file. The browser-control program clicks, waits, or fills the approved field.
7. **The application checks the outcome.** Did the correct report open? Is the requested date range correct? Did a valid file arrive?
8. **The collector logs the result and passes the file onward.** If a check fails, flag it rather than treating “the model returned an answer” as success.

Conceptually, the application might define the following decision fields:

```text
next_action: one of [open_report, wait, ask_human]
target_control: one of the controls actually found on this page
confidence: model confidence information used by the application's policy
```

This is an illustration of constrained decisions, **not Jev’s SDK syntax or a claim about its exact API response fields**.

### Probabilities, speed, and training jargon

A **calibrated probability** means that predictions assigned a given probability should be correct at roughly that frequency across suitable test cases. It is not a guarantee for a single decision, and calibration on one task may not transfer unchanged to another.

TypeSafe reports fast model calls and benchmark advantages in its announcement, with caveats about comparisons and workflows. Do not promise Goodwill the same speed for an entire reporting process: browser navigation, authentication, downloads, vendor delays, and validation all add time.

The article names **RLCD (Reinforcement Learning for Calibrated Decisions)** as its training method. It contrasts this with **RLHF (Reinforcement Learning from Human Feedback)** and **RLVR (Reinforcement Learning with Verifiable Rewards)**. For our project, the important distinction is what comes out of the model and how we verify it—not learning to train a model ourselves.

Jev availability, pricing, access permissions, and the actual integration interface need checking before implementation. The article establishes the product’s identity and intended role, not that the team already has access.

## What is a “generic adapter”?

An **adapter** is a small connector that translates one source’s format into the common format used by the rest of the system. For example, one adapter might read CSV exports and another might collect a report from a browser. If several vendors provide similar CSV files, one reusable CSV adapter may be enough; each vendor does not necessarily need a brand-new program.

The point of first mapping sources is to find the real number of collection methods. Nine sources might turn out to need only a few kinds of adapters.

## Macro, macro recorder, and Apps Script

These words sound similar but refer to different things:

- **Macro:** an automated sequence of steps. In Excel, a macro might format a report, remove blank rows, or calculate totals. Excel macros are often written in VBA. A macro can save time, but it usually works best inside the application where it was created.
- **Macro recorder (Wicks’s idea):** a proposed small tool that watches a person work through a website once, then helps repeat those steps. The notes suggest capturing page structure at each step rather than making a video of the screen. This is a concept to scope and test, not a confirmed component.
- **Google Apps Script:** Google’s scripting tool for automating Google Workspace products such as Sheets, Drive, Gmail, and Docs. For example, it can process a spreadsheet or move files in Drive. It is useful when the workflow lives in Google Workspace, but it is not the same thing as a browser agent for third-party e-commerce sites.

**Practical distinction:** use a spreadsheet macro for repetitive spreadsheet work, Apps Script for Google Workspace tasks, and browser automation for a website workflow when there is no suitable API or export. They are not interchangeable, and automation still needs failure checks and a human fallback.

**VBA (Visual Basic for Applications)** is the programming language commonly used for desktop Excel macros. **Office Scripts** are another Microsoft automation option for supported Excel environments, using a different language and execution model; they are not VBA macros. Check the partner’s actual environment before selecting either.

Google Apps Script uses JavaScript-based code and can run from triggers, such as a schedule or a spreadsheet event. A possible workflow is: locate an approved report file in Drive, read rows, check headings, and update a Sheet. Permissions, execution limits, duplicate processing, and failed runs still need handling.

### How a browser macro recorder could work

1. Record the authorized user's approved report-gathering actions.
2. Store which controls were used and the expected page state—not passwords or unrestricted session tokens.
3. Identify values that change, such as the report date, and make those inputs.
4. Replay the steps against a safe test site.
5. Check each expected outcome rather than blindly replaying clicks.
6. Stop when the website no longer matches the expected process.

A recorder reduces repeated setup; it does not prove the recorded steps are correct or that they will work forever.

## Formats and pipeline vocabulary

- **CSV (Comma-Separated Values):** a text file representing rows and columns. CSV does not carry Excel formulas or formatting, and date/currency interpretation needs care.
- **XLSX:** the common modern Excel workbook file format. A workbook may contain several worksheets, formulas, and formatting; the importer must know which sheet and columns matter.
- **JSON (JavaScript Object Notation):** a structured text format often used by APIs. It can represent named values and lists, rather than just a flat spreadsheet.
- **ETL (Extract, Transform, Load):** collect data, clean/reshape it, then put it into the reporting store.
- **ELT (Extract, Load, Transform):** store collected data first, then clean/reshape it there. Both approaches can retain the original source for audit and reprocessing.

For example, one export's `Sale Total` and another's `amount` might map to a common field. But do not assume they mean the same thing: one may include shipping or tax and the other may not.

## Stage 1: step-by-step team exercise

1. **Map the current process.** Ask an operator to demonstrate one actual report. Write down each click, input, report name, and destination.
2. **Classify the collection method.** Is this an approved API, CSV/XLSX export, emailed attachment, or browser-only workflow?
3. **Choose a narrow first case.** One source and one date range is easier to verify than all sources at once.
4. **Collect a sample safely.** For the hackathon, use synthetic/public data as the brief requires. Label a mock source clearly.
5. **Preserve the raw input.** Keep the original file, source name, collection time, requested date range, and an import/run ID.
6. **Validate the file.** Check headings, dates, record counts, amounts, and whether the file is empty or incomplete.
7. **Map fields explicitly.** Document how source fields translate into common fields, including any changes to units or date formats.
8. **Handle repeated runs.** Detect a previously processed file or repeated transaction so a retry cannot silently double revenue.
9. **Test failure paths.** Try an expired login, changed column name, missing report, and wrong date range.
10. **Show the handoff.** The collector should deliver a checked dataset or a visible error—not just a “completed” message.

**Team deliverable:** A source map, one sample export, a field-mapping sheet, and a record of successful and failed collection attempts.

## Stage 1 practice and success test

Make a source map with one row per report: source name, owner, how a person gets it today, file or fields provided, frequency, date range, and what happens when it is missing. Then test one source end to end.

**Stage 1 is working when** the team can collect a sample report, identify its source and date, spot missing or duplicate records, and explain what happens if the source changes or the automation fails.

# Stage 2 — Data storage: Excel versus a relational database

## Excel is useful—but it is not automatically the shared system of record

**Excel** is a spreadsheet: a grid of cells that is excellent for inspecting a small dataset, doing quick calculations, and sharing a prototype. A master workbook can be a reasonable starting point.

As the process grows, a spreadsheet can become difficult to operate reliably: people may overwrite formulas, create slightly different copies, enter duplicates, or use inconsistent names and dates. It can also be hard to trace exactly how a reported number was produced. Those are risks to check in the current workflow, not proof that Excel must be removed.

## What is a relational database?

A **relational database** stores information in tables with defined columns and links between related records. It is like a set of well-organized ledgers with consistent IDs.

For example:

- An **Orders** table could have one row per order, with an order ID, order date, platform, and status.
- An **Items** table could have one row per item, with a SKU, category, and store.
- A **Sales** table could connect an item to an order and record price, fees, and returns.
- A **Labor** table could record hours by store, date, or activity.

A shared ID connects the tables. This avoids typing the same store or platform details into every row and makes it possible to combine the right records for a report. **SQL** (Structured Query Language) is the common language used to ask questions of many relational databases, such as “total net sales by week and platform.”

### Tables, keys, relationships, and joins

- A **row** is one record, such as one order or one line within an order.
- A **column** is one attribute, such as amount, date, or source.
- A **schema** describes the tables, columns, data types, and rules. It is the agreed structure of the data.
- A **primary key (PK)** identifies a row uniquely. A platform's order number may be unique only within that platform; a robust design can use an internal ID and enforce uniqueness on the platform-plus-order combination.
- A **foreign key (FK)** refers to a related record. For example, a sales row's `store_id` refers to a store.
- A **join** combines related tables using matching keys. It is similar in purpose to using an Excel lookup, but works within the database's query and relationship rules.
- A **constraint** is an enforced rule, such as “this order cannot be imported twice under the same source ID.”

The **grain** means what one row represents. This is crucial: one row per order is different from one row per item. If an order contains three items, joining its full shipping cost onto all three rows and then adding it up can accidentally triple that cost.

### Small illustrative tables

These are invented records for learning, not Goodwill data.

| internal_order_id | source | source_order_id | store_id | gross_sales |
|---|---|---|---|---|
| 1 | ExampleChannelA | A-100 | S01 | $100 |
| 2 | ExampleChannelB | A-100 | S02 | $80 |

| store_id | store_name |
|---|---|
| S01 | Example North |
| S02 | Example South |

Both channels happen to have an order called `A-100`. That is why order number alone is not necessarily a safe unique key. The store relationship lets the report display the store name without copying and maintaining it on every sales row.

An illustrative SQL query:

```sql
SELECT source, SUM(gross_sales) AS total_gross_sales
FROM orders
GROUP BY source;
```

In plain English: read the `orders` table, group rows by channel, add gross sales in each group, and name that result `total_gross_sales`. This query assumes the field has already been defined and the table contains the intended records.

## Excel versus a relational database: choosing by need

| Question | Excel or a spreadsheet | Relational database |
|---|---|---|
| What is it especially good at? | Exploring data, small manual models, quick checks | Consistent shared records, linked tables, repeatable queries |
| How are calculations expressed? | Cell formulas, tables, pivots, queries, or scripts | Queries and application logic, often with shared definitions |
| How do you prevent bad records? | Validation rules and careful workflow | Enforced types, keys, constraints, and permissions |
| How do multiple people work together? | Depends on the workbook and collaboration setup | Designed for concurrent access, with access rules |
| What still needs maintenance? | Formulas, files, permissions, imports | Schema, imports, access policies, backups, application logic |

Neither option fixes poorly defined data. Excel can remain a familiar inspection/export tool even if the central store becomes a database.

## Database versus data warehouse

A **database** is a broad term for an organized store of information. A **relational database** is one kind of database, organized into related tables.

A **data warehouse** is designed especially for analyzing large amounts of historical data from multiple systems. It is often arranged to make reporting fast and consistent. A warehouse can be valuable when there are many years of data, many data sources, and heavy reporting needs—but it adds setup and maintenance.

Wicks’s notes recommend avoiding a custom database if Goodwill would have to maintain it, and suggest keeping a possible solution simple (with Supabase given as an example). They do not recommend building a data warehouse for the prototype. Start with the simplest store that meets the verified need; do not add a warehouse just because it sounds more advanced.

You may hear **OLTP (Online Transaction Processing)** for day-to-day record operations and **OLAP (Online Analytical Processing)** for analytical queries across many records. These describe workload styles, not an absolute rule that every dashboard requires a separate warehouse. A modest relational database can support reporting too.

A reporting design may use a **fact table** for events or measurements (sales, for example) and **dimension tables** for descriptive context (dates, stores, categories). A **star schema** connects these dimensions to a fact table. This can make reporting easier to understand, but the team still must agree on the grain and avoid double counting.

## What is Supabase?

**Supabase** is a managed software service that includes a PostgreSQL relational database and related application tools. “Managed” means the service provider handles some of the underlying infrastructure. The team still has to design tables, control access, back up data appropriately, and maintain the application logic. It is not an automatically correct data model.

**PostgreSQL** (often shortened to “Postgres”) is the database software underneath this option. Supabase is the service around it; PostgreSQL is the engine that stores tables and runs SQL queries.

## Calculation rules belong in the shared data process

Before making a dashboard, write down how each metric is calculated. For example, **revenue per labor hour** needs a clear definition of revenue, which labor hours count, and how dates and stores are matched. **Net margin** also needs agreed treatment of fees, refunds, shipping, and other costs.

For high-stakes numbers, the system should use explicit, testable formulas—not ask a chatbot to invent arithmetic. Finance and operations experts are essential reviewers of these definitions.

### Worked calculation: why business definitions come first

Suppose an invented example has $1,000 in item sales, $100 in refunds, $90 in marketplace fees, $60 in shipping costs, and $200 in allocated labor cost.

1. **Define net sales.** If our agreed definition is item sales minus refunds, this is `$1,000 - $100 = $900`.
2. **Define which costs belong in the measure.** Deducting the three listed costs gives `$900 - $90 - $60 - $200 = $550`.
3. **Name the result accurately.** This is contribution after those specified costs. Do not call it complete net profit if overhead or other required costs are absent.
4. **Define the denominator.** Contribution divided by net sales is `$550 / $900 ≈ 61.1%`. Dividing by gross sales gives 55%; those are different measures.
5. **State the scope.** Which dates, stores, channels, and accounting basis are included? Have fees and refunds actually arrived?

Other measures also need agreed rules:

- **Revenue growth:** compare like-for-like periods; specify what to do if the earlier period is zero.
- **Revenue per labor hour:** define the revenue basis and relevant labor hours. Missing labor data means the measure is unavailable, not zero.
- **Sell-through rate:** define the eligible inventory/listing cohort, time window, and sold count. “Items sold this month divided by items newly listed this month” can mix different cohorts and give a misleading answer.

### Raw, staging, and curated data

**Raw data** preserves what arrived. **Staging data** is where the system checks and standardizes it. **Curated data** is approved for reporting. These can be simple layers in one service; they do not necessarily require three different products.

Keep a trace from a dashboard total to curated records and back to the original report. This trace is called **data lineage**. A reconciliation compares the system's counts and totals with a trusted source. Explain differences; do not just adjust a total until it matches.

## Stage 2: step-by-step team exercise

1. **Choose the grain.** State exactly what one row represents.
2. **Write a data dictionary.** Define each field, meaning, type, source, and whether it can be missing.
3. **Choose safe keys.** Test whether IDs collide between sources.
4. **Design the relationships.** Draw how orders, items, stores, costs, and labor connect.
5. **Agree on transformations.** Standardize dates, currencies, statuses, and category mappings without erasing the original values.
6. **Import a tiny sample.** Make it small enough that a teammate can calculate totals by hand.
7. **Test repeated imports.** A second run should not double the same transactions. If the source changes a record, define how updates are handled.
8. **Reconcile.** Compare row counts and totals to the original reports; test joins for duplicated amounts.
9. **Approve metric definitions.** Finance/operations review the formulas, exclusions, missing-data behavior, and period rules.
10. **Assign ownership.** Specify who fixes a failed import, changes a mapping, manages access, and maintains backups.

**Team deliverable:** A table diagram, data dictionary, metric definition sheet, and reconciliation example.

## Stage 2 practice and success test

Take a small sample export and agree on a few fields and metric definitions. Load it into a consistent table (or tables), then compare totals with the original report and document any mismatches.

**Stage 2 is working when** the same input produces the same answer every time, the team can trace a total back to source rows, and someone can explain who is responsible for maintaining the data store.

# Stage 3 — Dashboard: charts, agents, skills, and chat

## What a dashboard does

A **dashboard** presents selected measures in a form people can scan and act on: totals, trends, comparisons, and filters such as date, store, platform, or category. A dashboard is only as trustworthy as its underlying data and metric definitions.

Possible measures in the Goodwill brief include revenue, growth, revenue per labor hour, margin, sell-through, days to sell, and listing backlog. These are examples of desired measures, not proof that every source currently supplies the data needed to calculate them.

## What is Power BI?

**Microsoft Power BI** is a business-intelligence product for connecting to data, defining measures, and building interactive reports and dashboards. Users can filter charts and view details. It is a reasonable option to evaluate if Goodwill already uses Microsoft tools and can support the necessary data refresh, access, and licensing.

Power BI is **not named in Michael Wicks’s plan**. His notes call for a fast, AI-friendly application/dashboard, but do not choose Power BI or prescribe a specific dashboard product. Compare Power BI with a custom web dashboard based on partner fit, maintenance, access controls, refresh needs, and the ability to explain the figures.

### How a Power BI report is assembled, step by step

1. **Connect to approved data.** This could be a database or a maintained file source. A connection alone does not make the data complete.
2. **Prepare it with Power Query.** Power Query can select columns, change types, and combine tables. Its formula language is **M**; M is a language name, not an acronym to expand.
3. **Build the semantic model.** This is the report's shared meaning: table relationships, named measures, and business definitions.
4. **Define measures.** **DAX (Data Analysis Expressions)** is used for many Power BI calculations. A measure such as total sales changes according to the selected dates, stores, or channels—its **filter context**.
5. **Add visuals.** Cards show headline figures; charts show trends and comparisons; tables show detail.
6. **Add slicers.** A slicer is an on-screen filter. Users might select a date, store, or platform.
7. **Validate independently.** A teammate should reproduce the displayed result from source data. Check that relationships do not duplicate amounts.
8. **Publish and control access.** The Power BI service supports sharing in the relevant setup, but licensing and permissions must be confirmed.
9. **Configure refresh.** Decide when updated data is loaded. Some environments require a gateway—a connector bridging the service to a data source it cannot directly reach.
10. **Show freshness and completeness.** A dashboard should show when its data was last updated and which sources are missing.

“Real-time” must be justified by the entire chain. A dashboard refreshing every minute cannot make an upstream daily export real-time.

### Power BI versus a custom dashboard

Power BI provides established reporting and modeling features. A custom web app can give more control over workflows, chat interactions, and interface design, but the team must implement and maintain those features. Either option needs trustworthy data.

## Tableau and open-source dashboard alternatives

Power BI is not the only choice. **Tableau** is another commercial BI platform. **Metabase**, **Apache Superset**, and **Grafana** have open-source editions. These are additional options for the team to evaluate, not products selected in Wicks’s notes.

### Tableau: visual exploration and shared business reporting

Tableau lets people explore data and build visual analyses and dashboards. Its product family includes **Tableau Desktop** for authoring and analysis, **Tableau Cloud** as a hosted service, and **Tableau Server** for an organization-managed deployment. [Source: Tableau products](https://www.tableau.com/products).

A beginner's Tableau workflow:

1. Connect to an approved database or dataset.
2. Check column meanings, types, and table relationships.
3. Create a worksheet—a single analytical view such as sales by platform.
4. Add dates, categories, and measures to the view.
5. Combine worksheets into a dashboard and add filters.
6. Verify totals and any calculated fields independently.
7. Publish through the organization's approved setup and test user access.
8. Confirm refresh behavior, source completeness, and maintenance ownership.

**Fit for this team:** Consider it if Goodwill already has Tableau access or someone who can maintain Tableau reports. Do not select it just because its charts look good; check licenses, author/viewer access, connections, and partner support first.

### Metabase: business questions without requiring everyone to write SQL

Metabase provides a graphical query builder as well as a SQL editor. Its central unit is a **question**: a query, its result, and a visualization. Saved questions can be organized into dashboards. It offers an open-source edition, while other editions and features have separate commercial terms. [Sources: Metabase questions](https://www.metabase.com/docs/latest/questions/introduction), [open-source edition](https://www.metabase.com/start/oss/).

A beginner's Metabase workflow:

1. Connect an appropriately restricted reporting account to the database.
2. Choose a table or approved dataset.
3. Use the graphical builder to select a measure, grouping, and filters—for example, total sales grouped by channel.
4. Display the result as a chart or table.
5. Save the question with a clear description of its scope and definition.
6. Add related questions to a dashboard and check filters.
7. Test sharing and permissions for the actual edition being evaluated.
8. Compare the result to the source report and assign an operator to maintain the deployment.

**Fit for this team:** A useful first open-source candidate for mixed-background users who want to ask straightforward business questions. Do not assume every security, embedding, governance, or AI feature mentioned in the overall product documentation is included in the open-source edition.

### Apache Superset: database-centered analytics with visual and SQL tools

Apache Superset is an open-source data exploration and visualization platform. It offers a no-code visualization builder, SQL tools, datasets, dashboard filters, and database connectivity. It uses the existing data infrastructure rather than replacing the ingestion process. [Source: Apache Superset](https://superset.apache.org/).

A beginner's Superset workflow:

1. Have a technical owner configure the deployment, database connection, and permissions.
2. Register a reporting table or query as a dataset.
3. Define shared metrics and labels.
4. Create a chart using the visual interface or an approved SQL query.
5. Add charts to a dashboard with clear filters.
6. Verify record grain, totals, and how filters affect each chart.
7. Test permissions, performance, and failure behavior.
8. Document ongoing updates, configuration, backups, and support.

**Fit for this team:** A candidate when the technical teammate can own administration and the team wants flexible database-driven analytics. Open-source flexibility is useful only if someone can keep the system operating reliably.

### Grafana: monitoring, time trends, and operational alerts

Grafana's open-source edition focuses on data visualization and monitoring across data sources. Its ecosystem includes dashboards, time-series views, and alerting. Grafana Cloud is a separate managed option. [Source: Grafana OSS](https://grafana.com/oss/grafana/).

For this project, a possible use is monitoring **whether reports arrived, how long imports took, and when a source failed**. Grafana can also show business data with suitable connections, but it should not be chosen by default for finance-style self-service analysis.

A beginner's Grafana workflow:

1. Choose the data source and the operational signals to monitor.
2. Query those signals—for example, last successful ingestion time by source.
3. Create panels for trends and current status.
4. Set alert rules for meaningful conditions, such as a missing expected report.
5. Test an actual failure and confirm the right person receives the alert.
6. Maintain access rules and a documented response procedure.

### Practical dashboard comparison

These are project-fit recommendations, not product benchmark results.

| Option | What to evaluate it for | Main decision for this team |
|---|---|---|
| Power BI | Business reporting in a Microsoft-oriented environment | Existing access, approved measures, refresh, sharing, and support |
| Tableau | Visual exploration and established business dashboards | Existing expertise, licensing, governance, and maintenance |
| Metabase open-source edition | Accessible database questions and dashboards | Edition-specific permissions/features and an operator for the service |
| Apache Superset | Flexible visual/SQL analytics over reporting data | Technical ownership of setup, security, and operations |
| Grafana open-source edition | Operational monitoring, time trends, and alerts | Whether the primary need is monitoring or financial analysis |
| Custom web dashboard | A tailored workflow and integrated chat experience | Who will build, test, secure, and maintain every feature |

**Recommended evaluation order:** First check tools and support Goodwill already has. If there is no established BI tool and open source is preferred, try Metabase on a small verified dataset. Compare Superset if more flexible SQL-driven analysis is needed. Evaluate Grafana separately for pipeline monitoring. Keep a custom dashboard in consideration when the integrated workflow/chat experience is a genuine requirement.

### What “open source” does—and does not—mean

**OSS (Open-Source Software)** makes source code available under an applicable license. It does not mean “no ongoing cost,” “no license obligations,” or “every commercial feature is included.”

Someone must still provide a hosting environment, security updates, backups, configuration, access management, and support. Managed services may reduce some operations work but have their own terms and costs. Review each edition's license and feature availability, especially before modifying or embedding it into another product.

**TCO (Total Cost of Ownership)** includes hosting, subscriptions, setup, maintenance labor, support, and future changes. A no-license-fee option can cost more overall than a tool the partner already knows.

### How these options connect to the chatbot

Do not assume that a dashboard's open-source status—or its marketing about AI—provides our exact chatbot workflow. Check the actual edition and supported integration interfaces.

For any option:

1. Keep metric definitions consistent between the charts and chatbot.
2. Use approved data/API access rather than reading numbers from chart screenshots.
3. Pass the selected filters and user identity through a supported mechanism.
4. Verify that the chatbot cannot reveal rows the user cannot see in the dashboard.
5. Check embedding and authentication requirements if placing reports inside a custom app.
6. Test a real answer against the underlying records.

**Embedding** means displaying a report or chart inside another application. It is not automatically permitted or secure, and it does not remove the original tool's licensing or access requirements.

The **frontend** is what the user sees. The **backend** is the server-side code that handles approved requests and data access. A custom chatbot normally needs a protected backend: do not put database secrets or model credentials in code sent to the user's browser.

**BI (Business Intelligence)** means using business data for reporting and decisions. A **KPI (Key Performance Indicator)** is a selected measure used to assess performance. **UX (User Experience)** is how easy and understandable the overall workflow feels; it is more than making the charts attractive.

## Tools used to build the dashboard versus tools used by staff

Wicks named **Cursor** and **Claude Code** as ways to build quickly. They are AI-assisted programming tools: developers use them to write, change, and understand code. They are not the dashboard itself, and Goodwill staff would not need to learn them just to use the finished dashboard.

**Claude** is an AI assistant/model family; the notes suggest using it to help build the mock Upright web app from screenshots. An AI-generated app still needs review and testing.

**Copilot** is Microsoft's branding for several AI assistant products. The notes say Goodwill uses Copilot and mention a possible Copilot or agent interaction with the data. That does not establish which Copilot product, license, or data connection is available. An assistant is only useful for this task if it has approved access to the relevant data and can show where its answers came from.

**LLM** means “large language model”—the kind of AI behind many chat and coding assistants. It generates and interprets language; it is not a replacement for an agreed accounting formula or a tested calculator.

## “Agentic” and AI-native: what those terms mean here

An **AI agent** is software that uses an AI model to interpret a request and take bounded actions using approved tools—for example, looking up a metric, applying a date filter, or explaining which categories changed. “Agentic” does not mean the AI should have unlimited access or make business decisions on its own.

An **AI-native dashboard** puts conversational help alongside the normal charts and filters. A user might ask, “Why did net margin fall last month?” The system should use the same approved metric definitions as the dashboard, show which data and filters it used, and link the answer back to relevant rows or reports. The chatbot should explain the result—not quietly change the definition of net margin.

For calculations such as totals and ratios, use database queries or tested application code. Let the AI help interpret the question, choose an approved query, and explain the result. If a required field is missing, it should say so rather than guess.

### Jev, a language model, and a calculator have different jobs

Jev could help choose among permitted tasks or classify a request. A language model could phrase an explanation or ask a clarifying question. SQL or tested code should calculate the financial figure. The team does not have to force one model to perform all three jobs.

An **API** is a software interface; an **SDK (Software Development Kit)** is a library/toolkit that helps developers use an interface. Neither is an agent skill by itself. A **tool call** is the agent requesting a specific operation from application code, such as “get weekly sales for these filters.”

**MCP (Model Context Protocol)** standardizes how compatible AI applications communicate with tools and data providers. It can be useful for an assistant that needs approved reporting tools, but it is not a database, a permission bypass, or a requirement for every chatbot. A normal application API may be sufficient.

**RAG (Retrieval-Augmented Generation)** means retrieving relevant information and supplying it to a language model as context. It can help find a metric definition or operating procedure. For exact totals, retrieve structured query results—not just snippets of reports—and calculate with deterministic code.

## What are “skills” for an AI agent?

A **skill** is a reusable set of instructions and, sometimes, tools or code that teaches an agent how to perform a particular task. Think of it as a procedure the agent can follow consistently.

For example, a “daily e-commerce report” skill could instruct an agent to:

1. Check that each expected source arrived.
2. Validate dates, columns, and duplicate order IDs.
3. Run the approved sales and margin calculations.
4. Show a summary with links to the underlying report.
5. Flag missing data for a person instead of filling it in.

Skills do not replace reliable data, testing, access controls, or a person’s judgment. A skill can be wrong too; someone who understands the business should review its steps and expected results.

### Example skill specification

```text
Skill name: Explain a weekly platform comparison
Use when: A user asks about sales or margin across channels.
Inputs: Approved metric, date range, permitted stores, comparison period.
Tools: Read-only metric query, metric-definition lookup, source-status lookup.
Procedure:
  - Confirm the metric and filters.
  - Check whether all expected sources are available.
  - Run the approved query.
  - Calculate differences using tested code.
  - Explain the result and list exclusions.
Output: Summary, figures, filters, definition, freshness, evidence links.
Stop when: Data is missing, access is denied, or the requested metric is undefined.
Never do: Change accounting entries or invent missing values.
```

This is a proposed procedure, not a feature already implemented in the project. A skill is reusable guidance; the surrounding software must still enforce authorization and safe tool access.

## Chatbot and screenshots

A chatbot can answer natural-language questions about the dashboard, such as “Which platform changed most this week?” A strong answer should include the time period, filters, metric definition, and a way to inspect the underlying evidence.

Screenshots can help people see what the system did, support a walkthrough, or document a demo. They are **not** a substitute for the underlying data or a calculation trace. The team should be able to reproduce the answer from the source records and metric logic. If browser automation uses screenshots to recreate a mock site, keep that demo separate from claims about a live vendor integration.

### How an integrated dashboard chatbot should work, step by step

1. **The user selects a chart or filters.** For example: a weekly channel comparison.
2. **The app supplies structured context.** Send the selected metric, period, stores, and chart identifier—not just a screenshot.
3. **The user asks a question.** “Why is this channel's contribution lower than last week?”
4. **The assistant checks ambiguity and access.** Does “contribution” have an agreed definition? Is the user permitted to see these stores?
5. **The backend runs approved queries.** Obtain comparable sales, refunds, and costs where available.
6. **Tested code calculates changes.** Compute differences and ratios from actual results.
7. **The assistant explains the observable drivers.** It can describe a higher refund amount; it should not claim a causal explanation like “staff performance worsened” without evidence.
8. **The app presents evidence.** Include filter settings, refresh time, source completeness, the metric definition, and a drill-through table.
9. **Offer a screenshot or annotated view.** Highlight the relevant chart or table for communication, subject to permissions and privacy.
10. **Allow a correction.** A user should be able to change the period, inspect records, or flag a mismatch.

If the user uploads an image of a report, **OCR (Optical Character Recognition)** can read text from the image. OCR may misread decimals, dates, or column labels. Treat image-derived numbers as unverified until checked against the actual export.

### Proposed interface outline

This is an explanatory text sketch, not a screenshot of a built application.

```text
Date: [This week]   Store: [Permitted stores]   Channel: [All]
Data status: last refreshed [time]; [sources received / expected]

[Net sales]  [Defined contribution]  [Labor productivity if available]
[Weekly channel chart]             [Detailed results table]

Ask about this view: _______________________________________

Answer:
  - Comparison and calculated difference
  - Observed changes in refunds/fees/etc.
  - Missing data and limitations
  - [Metric definition] [Underlying rows] [Source report]
```

Useful screenshots for training would show the whole view with filters, a selected chart with its chat explanation, and the underlying evidence table. Avoid sharing customer details or credentials in screenshots.

## Access, safety, and reliability

**RBAC (Role-Based Access Control)** grants access by job role. **RLS (Row-Level Security)** limits which database rows a user can access, such as the stores within their remit. The chatbot must respect the same access boundaries as the dashboard; an answer is another way of revealing data.

**PII (Personally Identifiable Information)** includes customer details that can identify a person. Collect and expose only what the reporting task needs. Credentials and session information belong in secure storage, not skill files, browser logs, exports, or screenshots.

A first reporting assistant should be read-only. Creating accounting entries, changing listings, or sending information outside the organization are different workflows requiring separate controls and approval. Text in source reports or web pages should be treated as data, not instructions granting the agent new permissions.

## Stage 3: step-by-step team exercise

1. **Pick one decision the user needs to make.** Avoid a page of attractive charts without a clear purpose.
2. **Select two or three approved measures.** Make missing data visible.
3. **Build the view in the selected dashboard tool.** Evaluate Power BI, Tableau, an open-source option, or a custom app based on partner requirements, not novelty.
4. **Add date/store/platform filters.** Verify the resulting totals change correctly.
5. **Expose definitions and source status.** A user should not have to ask the chatbot to discover whether data is stale.
6. **Add one bounded chat skill.** Begin with a read-only comparison, using the same measures as the dashboard.
7. **Check an answer manually.** Finance or math teammates reproduce the calculation and review the explanation.
8. **Test misleading questions.** Try missing labor hours, incomplete fee reports, zero denominators, and questions outside the user's permissions.
9. **Document the experience with safe screenshots.** Show the result, selected filters, and evidence.
10. **Have an operator try it without coaching.** Record confusion, extra steps, incorrect answers, and maintenance needs.

**Team deliverable:** A validated dashboard view, one evidence-backed chat interaction, and a short training walkthrough.

## Stage 3 practice and success test

Build one useful view first—such as weekly sales by platform—and test it with a finance or operations teammate. Then add one read-only chat question that uses the same metric as the chart. Ask a teammate to verify both against the source report.

**Stage 3 is working when** a user can find an important number quickly, understand how it was calculated, and check its source. The chatbot should admit uncertainty or missing data rather than present a confident guess.

## Full acronym reference

Use this as a lookup sheet. These terms describe concepts and options; their inclusion does not mean every technology is required for the prototype.

| Acronym | Expanded name | Meaning in this project |
|---|---|---|
| AI | Artificial Intelligence | Software models used for interpretation, decisions, or explanations |
| API | Application Programming Interface | A defined software-to-software interface |
| BI | Business Intelligence | Reporting and analysis for business decisions |
| CSV | Comma-Separated Values | A simple tabular text export |
| DAX | Data Analysis Expressions | A language for measures and calculations in Power BI |
| DOM | Document Object Model | The browser's structured representation of a page |
| ELT | Extract, Load, Transform | Collect and store data before transforming it |
| ERP | Enterprise Resource Planning | Enterprise software such as Business Central |
| ETL | Extract, Transform, Load | Collect and transform data before loading it |
| FK | Foreign Key | A reference from one table to a related record |
| HTML | HyperText Markup Language | Markup describing web-page content |
| JSON | JavaScript Object Notation | A format for structured values and lists |
| KPI | Key Performance Indicator | An agreed measure used to assess performance |
| LLM | Large Language Model | A language-generating/interpreting model |
| MCP | Model Context Protocol | A standard interface between compatible AI apps and tools/data |
| MFA | Multi-Factor Authentication | Sign-in using more than one verification factor |
| OCR | Optical Character Recognition | Reading text from an image, with possible errors |
| OLAP | Online Analytical Processing | Analytical querying across records |
| OLTP | Online Transaction Processing | Day-to-day record operations |
| OSS | Open-Source Software | Software whose source is available under an open-source license |
| PII | Personally Identifiable Information | Data that can identify a person |
| PK | Primary Key | A unique row identifier |
| RAG | Retrieval-Augmented Generation | Retrieving information to ground a model's response |
| RBAC | Role-Based Access Control | Access based on a user's role |
| RLCD | Reinforcement Learning for Calibrated Decisions | TypeSafe's named model-training approach |
| RLHF | Reinforcement Learning from Human Feedback | Model training using feedback/preferences from people |
| RLS | Row-Level Security | Rules restricting which rows a user can access |
| RLVR | Reinforcement Learning with Verifiable Rewards | Model training using automatically checkable rewards |
| SDK | Software Development Kit | Libraries/tools helping developers use a service |
| SKU | Stock Keeping Unit | An identifier for an inventory item or product |
| SQL | Structured Query Language | A language for querying and manipulating relational data |
| TCO | Total Cost of Ownership | Costs including hosting, setup, maintenance, support, and changes |
| UI | User Interface | The screens and controls a person uses |
| UX | User Experience | How understandable and usable the overall workflow is |
| VBA | Visual Basic for Applications | A language commonly used for desktop Excel automation |

**Names rather than acronyms:** Jev, Supabase, PostgreSQL/Postgres, Power BI (BI is the acronym), Power Query, M, Tableau, Metabase, Apache Superset, Grafana, Cursor, Claude Code, Copilot, and Google Apps Script. XLSX is an Excel file extension, not a business or architecture acronym.

## Shared glossary

| Term | Plain-language meaning |
|---|---|
| API | A supported way for software systems to exchange structured information. |
| Adapter | A connector that translates one source’s data or workflow into the format used by the rest of the system. |
| CSV | A simple text file representing a table, commonly used for data exports. |
| DOM | The browser’s structured map of the elements on a web page. |
| Data ingestion | Collecting information from source systems and bringing it into a solution. |
| Relational database | A structured store of connected tables with consistent fields and IDs. |
| Data warehouse | A store designed to combine and analyze large volumes of historical data. |
| Metric | A business measure with a defined calculation, such as sell-through rate. |
| Power BI | Microsoft’s tool for data modeling, interactive reports, and dashboards. |
| Agent | AI software that interprets a request and uses approved tools to carry out a bounded task. |
| Skill | A reusable procedure and toolset that guides an agent through a task. |

## Final team checklist: demonstrate the complete chain

1. **Collect:** Show one source and one date range being obtained through an approved or clearly labeled mock process.
2. **Validate:** Show checks that reject an incomplete or wrong report.
3. **Store:** Show that the same transactions do not double when re-imported.
4. **Calculate:** Reproduce one agreed measure independently.
5. **Display:** Show the figure with its filters and data freshness.
6. **Explain:** Ask the chatbot about it and inspect the query evidence.
7. **Fail safely:** Demonstrate missing data, a changed page, or denied access without fabricated results.
8. **Maintain:** Name the person/process responsible for failures and future changes.

The complete chain matters more than any single model or flashy chart. A simple, verified workflow is more useful than a sophisticated demo whose numbers cannot be checked.

## Source notes

This guide is based on Michael Wicks’s Goodwill office-hours plan, the Goodwill track brief, and the TypeSafe article supplied by the team to identify Jev. Step-by-step procedures, example records, formulas, interface sketches, and architecture details are explanatory proposals—not claims that they are already implemented or approved by Goodwill. Product access, data fields, and partner requirements should be confirmed before treating a prototype choice as a production commitment.

- [TypeSafe AI: Introducing System One Models and Jev — September 14, 2026](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Tableau: product overview](https://www.tableau.com/products)
- [Metabase: questions and query-building workflow](https://www.metabase.com/docs/latest/questions/introduction)
- [Metabase: open-source edition](https://www.metabase.com/start/oss/)
- [Apache Superset: overview and documentation](https://superset.apache.org/)
- [Grafana: open-source edition](https://grafana.com/oss/grafana/)
- [Michael Wicks Office Hours: Goodwill Plan](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view)
- [Goodwill Track: Problem Brief](https://drive.google.com/file/d/1HWd2Pi0Le4zU_iDVQK7a9y4bw42vTKRr/view)