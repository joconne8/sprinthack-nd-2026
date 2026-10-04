# Technology Foundations: A Practical Guide for Nontechnical Readers

**Audience:** Anyone who wants to understand modern software, data, automation, dashboards, and AI without assuming a programming background.

**Purpose:** Explain what the tools are, how they work, how they differ, and when they are useful. This is a standalone guide, not a design for a particular project.

**How to read it:** Follow the sections in order if these ideas are new. Otherwise, use the contents and glossary as a reference. You do not need to memorize code or learn every product. Aim to understand the role each component plays and the questions to ask before relying on it.

The diagrams are plain text so they remain readable in a Markdown viewer, a text editor, or a printed copy. Examples are invented and deliberately small. Statements about products describe their broad purpose, not a guarantee that every feature is included in every edition.

## Contents

1. The basic picture: what software actually does
2. Programs, languages, and tools for building software
3. Websites, browsers, and the internet
4. APIs, SDKs, and ways systems connect
5. Files, formats, and structured data
6. Spreadsheet tools and automation
7. Browser automation, recorders, and Jev
8. Databases: tables, keys, relationships, and SQL
9. Data warehouses and reporting models
10. Data pipelines, quality, and trustworthy calculations
11. Dashboards and business intelligence
12. Power BI, Tableau, and open-source alternatives
13. AI models: generation, decisions, and uncertainty
14. Chatbots, agents, tools, skills, RAG, and MCP
15. Cloud services, hosting, and maintenance
16. Security, permissions, and privacy
17. Testing, logs, and failure handling
18. Choosing tools without getting lost in names
19. Acronym reference
20. Sources and further reading

---

## 1. The basic picture: what software actually does

### Data, instructions, and results

**Data** is recorded information: a date, a price, a name, a temperature, or a document.

**Software** is a set of instructions that tells a computer what to do with information. A **program** is a particular set of those instructions. An **application**, or app, is software designed for a person or another system to use.

Most useful software can be understood as inputs, processing, and outputs.

```text
          INPUT                   PROCESSING                OUTPUT
   Information supplied       Instructions carried out    Information produced

   Five expense amounts  ───► Add the amounts together ───► Monthly total
   A search phrase       ───► Find matching records     ───► Search results
   Temperature readings  ───► Compare with a limit      ───► Warning
```

The computer does not automatically understand the business meaning of a number. Someone must decide whether an amount is a price, a fee, a refund, or a total—and what to do with it.

### A tool is not the whole system

A finished application usually combines several components:

```text
Person
  │ uses
  ▼
Interface ───► Application logic ───► Data storage
  ▲                    │                    │
  └────── results ──────┴────── records ─────┘
```

- The **interface** is where a person enters information or sees results.
- The **application logic** contains the rules and calculations.
- The **data storage** keeps information for later use.

A database stores records; it does not automatically decide which chart is useful. A dashboard displays information; it does not automatically make the underlying data correct. An AI model can interpret a request; it does not automatically have access to the right records.

### Rule-based versus model-based behavior

A rule-based program follows explicit instructions:

```text
If the payment date is before today and the invoice is unpaid:
    mark the invoice as overdue.
```

An AI model may help with a less clear-cut judgment:

```text
Does this email appear to be an invoice, a receipt, or a general message?
```

The first task has a clear rule. The second involves interpretation and may be wrong. Reliable systems often use both: a model interprets something, while ordinary code enforces boundaries and performs exact calculations.

**Key distinction:** “Automated” does not necessarily mean “AI-powered.” Many reliable automations use no AI at all.

## 2. Programs, languages, and tools for building software

### What is code?

**Code** is instructions written in a programming language. The language defines how instructions are expressed so a computer can execute them.

A human-readable instruction such as “add all the amounts” might be represented in a program by a function that takes a list of numbers and returns their sum.

A **function** is a reusable operation. It accepts inputs, does a defined job, and may return an output.

```text
Input: [10, 20, 30] ───► sum function ───► Output: 60
```

You do not need to know the implementation to understand what the function promises to do. This idea appears throughout software: clearly defined inputs and outputs make components easier to combine.

### Languages you will encounter

- **Python:** widely used for scripts, data processing, analysis, backend services, and automation.
- **JavaScript:** widely used for browser behavior and also for server-side programs.
- **TypeScript:** builds on JavaScript with a system for describing and checking types. Types help catch certain mistakes; they do not prove the program's business logic is correct.
- **SQL:** a language for working with relational data. It is primarily about describing the data you want to retrieve or change.
- **VBA:** a language often used to automate desktop Microsoft Office applications.
- **DAX:** a formula language used for analytical calculations in products such as Power BI.

Different languages can be used in the same system. A website may use JavaScript in the browser, Python on the server, and SQL to query a database.

### Libraries, frameworks, and runtimes

A **library** is reusable code that performs a particular kind of work. A browser-control library, for example, can provide functions for opening pages and clicking controls.

A **framework** provides a broader structure for building an application. It supplies conventions and components so developers do not start from nothing.

A **runtime** is the software environment that executes a program. Python programs need a Python runtime. JavaScript runs in browsers and in environments such as Node.js.

```text
Your application
      │ uses
      ▼
Libraries / framework
      │ execute within
      ▼
Runtime
      │ runs on
      ▼
Computer or server
```

### Coding assistants are not finished applications

**Cursor** is an AI-assisted coding environment. **Claude Code** is an AI coding tool. Developers use tools like these to create, modify, and understand software.

**Claude** is an AI assistant/model family. **Copilot** is a name used for several Microsoft AI assistant products; the exact product matters when discussing features or integrations.

An AI coding tool can produce code quickly, but someone still needs to verify requirements, inspect changes, run tests, and protect data. Generating a program is not the same as proving it works.

### Git and GitHub

**Git** tracks changes to files, especially code. A **commit** records a set of changes. A **branch** lets someone work on a separate line of changes before combining it with another branch.

**GitHub** is a service for storing and collaborating on repositories that use Git. A **repository** is a managed collection of files and their change history.

A **pull request** proposes combining changes and gives people a place to review them.

```text
Main version:    A ─── B ───────────── E
                       \             /
Feature branch:         C ─── D ────┘
                             review
```

Version history helps explain what changed and recover earlier code. It is not a replacement for database backups or careful handling of confidential information.

## 3. Websites, browsers, and the internet

### What a browser does

A **browser** is an application such as Chrome, Safari, or Firefox. It requests information from web services and displays interactive pages.

A **server** is a computer or program that responds to requests from other computers. A **client** is the program making the request. A browser is often the client.

```text
Your browser                Network                 Web server
     │                                                │
     ├──────── Request: "show this page" ──────────────►│
     │◄──────── Response: page content ────────────────┤
     │                                                │
     └── Displays the page and runs allowed page code  │
```

### URL, DNS, HTTP, and HTTPS

A **URL** is an address for a resource, such as a webpage or API endpoint.

**DNS** helps translate a domain name such as `example.com` into the network address needed to reach the service.

**HTTP** is a protocol—a set of communication rules—for requests and responses. **HTTPS** uses HTTP over an encrypted connection.

HTTPS helps protect traffic between endpoints. It does not prove that a website's claims are true or that the organization receiving data is trustworthy.

### Frontend and backend

The **frontend** is the part users interact with: buttons, forms, charts, and page behavior.

The **backend** is server-side software that processes requests, checks access, applies rules, and communicates with databases or other services.

```text
FRONTEND                     BACKEND                       DATABASE
Chart and filters ───────► Check access and query ───────► Stored records
Chart updates     ◄─────── Return approved results ◄────── Query results
```

Private credentials should not be placed in frontend code that is delivered to a user's browser.

### HTML, CSS, JavaScript, and the DOM

- **HTML** describes page content and structure.
- **CSS** describes presentation, such as spacing, colors, and layout.
- **JavaScript** adds behavior, such as responding when a button is pressed.
- The **DOM** is the browser's live structured representation of the page.

```text
Document
 └── Page body
      ├── Heading: "Account"
      ├── Input: "Start date"
      └── Button: "Download"
```

This diagram represents structure, not a picture of pixels. Browser automation can locate the “Download” button through its label or other properties.

A page may change after loading. A button appearing in a screenshot does not prove it is currently available, enabled, or connected to the expected action.

### Iframes, extensions, and sessions

An **iframe** displays one page inside another. Some websites prohibit embedding, and browsers restrict how different sites can interact.

A **browser extension** adds capabilities to a browser. A recorder extension might observe selected interactions, but permissions must be narrowly controlled.

A **session** is the continuing state of an interaction with a service, including a signed-in state. Session cookies or tokens may grant access and must be protected like credentials.

## 4. APIs, SDKs, and ways systems connect

### An API is a defined software interface

An **Application Programming Interface (API)** describes how software can request an operation or exchange information.

Compare the two routes:

```text
HUMAN ROUTE
Person ──► Website ──► Click report ──► Download file

SOFTWARE ROUTE
Program ──► API request ──► Structured response
```

An API does not mean “all the data is freely available.” Access may depend on permissions, subscriptions, rate limits, and what the vendor exposes.

### Request, response, and endpoint

An **endpoint** is a specific API address for an operation or resource.

A **request** asks the service to do something. A **response** reports the result.

```text
Request: GET /invoices?status=unpaid
                  │
                  ▼
Response: a list of permitted unpaid invoice records
```

This is an invented example, not an actual vendor endpoint.

Common HTTP methods include:

- **GET:** retrieve information.
- **POST:** commonly submit information or create something.
- **PATCH:** commonly change selected fields.
- **DELETE:** commonly remove a resource.

The exact effect is defined by the service. Never assume a method is safe without checking the documented operation.

### REST, pagination, and rate limits

**REST** is an architectural style used by many web APIs. In practice, people often use “REST API” to describe an HTTP interface organized around resources and operations.

**Pagination** divides a large result into smaller pages. Fetching the first page of records is not the same as fetching every record.

A **rate limit** restricts how often requests can be made. A collector may need to slow down or retry later.

### SDKs are convenience tools

A **Software Development Kit (SDK)** supplies code and helpers for using a service. An SDK may handle request formatting, response parsing, or authentication details.

```text
Application ──► SDK helper ──► Service API ──► Response
```

The API is the interface. The SDK is a tool that helps use it. An SDK does not grant permissions or make invalid requests correct.

### Other connection methods

A **webhook** sends a notification when an event happens. Instead of repeatedly asking “is there a new payment?”, a receiving system may be notified that one occurred. It must still verify the notification and handle repeats.

A **connector** is an integration component that helps a tool communicate with another service.

An **adapter** translates a particular format or workflow into the form the rest of an application expects.

A manual export can also be a legitimate connection method. It may be less automatic, but easier to control initially.

### Business applications: marketplaces, operations, and accounting

It is useful to distinguish the software people work in from the infrastructure that connects it.

An **e-commerce platform** supports selling online. A **marketplace**, such as Amazon or eBay, brings multiple sellers and buyers together. A seller's own storefront is another kind of sales channel.

An **operations system** may manage listings, stock, fulfillment, or orders. An **ERP (Enterprise Resource Planning)** system coordinates functions such as finance and operations. Microsoft Business Central is an ERP product.

A **CRM (Customer Relationship Management)** system organizes customer relationships and interactions. A **CMS (Content Management System)** organizes website or other published content. Neither is the same thing as a general reporting database.

```text
Customer purchase
       │
       ▼
Sales channel ──► Order/fulfillment operations ──► Accounting
       │                    │                         │
       └────────────────────┴─────────────────────────┘
                            │
                            ▼
                      Reporting views
```

One event can appear in several systems for different reasons. An order record, a shipment record, and an accounting entry are not three separate sales. Connecting systems requires understanding which records represent the same activity.

## 5. Files, formats, and structured data

### A file format determines how information is represented

The same information can be stored in different formats. A format determines what structure can be preserved and which software can read it.

| Format | Useful for | Important limitation |
|---|---|---|
| CSV | Simple rows and columns | No workbook formulas, formatting, or multiple sheets |
| XLSX | Excel workbooks | May contain multiple sheets, formulas, hidden rows, and inconsistent layouts |
| JSON | Named fields, nested objects, lists | Needs an agreed structure and interpretation |
| PDF | Fixed-layout documents | Often harder to extract as reliable structured data |
| PNG/JPEG | Images and screenshots | The picture is not directly a table of verified values |

### CSV versus JSON

CSV is shaped like a table:

```csv
invoice_id,amount,currency
I-001,120.00,USD
I-002,75.00,USD
```

JSON can represent named fields and lists:

```json
{
  "invoice_id": "I-001",
  "amount": 120.00,
  "currency": "USD",
  "tags": ["subscription", "monthly"]
}
```

The data might look simple, but interpretation matters. Is the amount before tax? Is a date in day/month or month/day order? Is an empty field unknown, not applicable, or zero?

### Structured versus unstructured data

**Structured data** follows a defined organization, such as rows with known fields.

**Unstructured data** includes free-form text, images, or documents without a ready-made table of consistent fields.

```text
Email: "Please reimburse my train ticket..."
                    │ extraction and review
                    ▼
{ category: travel, amount: 28.50, currency: GBP }
```

Extraction can introduce mistakes. A structured result is easier to process, but its values still need verification.

**OCR (Optical Character Recognition)** extracts text from images. It can misread a decimal point, a date, or a heading. If precise numbers matter, prefer the original data export where possible.

## 6. Spreadsheet tools and automation

### What a spreadsheet is good at

Excel and Google Sheets organize information into cells, rows, and columns. They are useful for exploration, small models, inspection, and familiar manual workflows.

A **formula** calculates a value from other cells. A **pivot table** groups and summarizes data without requiring a custom program.

Spreadsheets can become difficult to maintain when there are many versions, repeated imports, hidden formulas, or unclear ownership. That does not make them useless; it means the workflow needs controls.

### Formulas, macros, and scripts are different

```text
Formula       ──► Calculates a value
Macro/script  ──► Performs a sequence of operations
Data query    ──► Retrieves or transforms a dataset
```

A **macro** automates steps such as formatting a report, deleting blank rows, or exporting a worksheet.

**VBA (Visual Basic for Applications)** is commonly used for desktop Excel macros. A recorder can generate a starting macro from a person's actions, but recorded code may depend on specific sheet names or cell positions.

**Office Scripts** provide another automation approach in supported Excel environments. They use TypeScript and a different execution model from VBA. Availability depends on the actual Microsoft setup.

### Google Apps Script

**Google Apps Script** is a JavaScript-based automation platform for Google Workspace products such as Sheets, Drive, Gmail, and Docs.

For example:

```text
Scheduled trigger
        │
        ▼
Apps Script ──► Read approved Sheet ──► Check rows ──► Create summary
```

A **trigger** is an event that starts a script, such as a scheduled time or an edit. Script permissions, execution limits, and failure handling still matter.

Apps Script is not a general replacement for controlling any website. It is particularly useful when a workflow lives in Google Workspace or a service has an API the script can use.

### Power Query

**Power Query** is a data connection and transformation tool used in environments including Excel and Power BI.

It can repeat steps such as:

1. Read a source.
2. Select the relevant worksheet or table.
3. Rename columns.
4. Set date and number types.
5. Filter rows.
6. Combine compatible tables.
7. Refresh the resulting dataset.

Its formula language is **M**. M is a language name, not an acronym.

Power Query is different from a cell formula: it prepares datasets. It is different from browser automation: it is not primarily a tool for clicking through a website.

## 7. Browser automation, recorders, and Jev

### Browser automation repeats web interactions

Browser automation code can open a page, locate a control, fill a field, wait for a result, or download a file.

**Playwright** and **Selenium** are examples of browser automation tools/libraries. They are not AI models.

```text
Program
  │ instructions
  ▼
Browser-control library
  │ interacts with
  ▼
Web page ──► Result or downloaded file
```

An approved API or export is often preferable when available because the interface is designed for data exchange. Browser automation can be useful when an API is unavailable, but its reliability depends on page changes, authentication, permissions, and timing.

### DOM-based versus image-based control

DOM-based control examines page elements and their properties. Image-based control uses screenshots and computer vision to identify what is on the screen.

```text
DOM approach                    Image approach
------------                    --------------
Button                          Pixels
  label: Download                 │
  enabled: true                   ▼
  element identity              Image interpretation
        │                         │
        ▼                         ▼
Target the element              Estimate a target on screen
```

Some workflows use both. Neither approach automatically proves that the page is correct or the action succeeded.

### What a macro recorder does

A recorder observes a sequence of actions and stores a representation that can be replayed.

```text
Record once:
Open report ──► Choose date ──► Download
       │
       ▼
Stored procedure + expected page checks
       │
       ▼
Replay with a different date
```

Changing values should become parameters rather than fixed recorded text. A good replay checks each important outcome and stops on unexpected states.

Recording passwords, unrestricted session tokens, or sensitive page content is unsafe. Recording what happened also does not prove that the original procedure was correct.

### Jev is a decision model, not a browser tool

**Jev** is TypeSafe AI's System One model. Its announcement describes a model designed to return type-safe structured decisions with probabilities, rather than generate free-form strings. It is named after William Stanley Jevons; Jev is not an acronym. [TypeSafe source](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

A developer defines the permitted output structure. Jev can then help choose, classify, route, or score within that structure.

For a browser task, the components might fit together like this:

```text
Browser state
    │
    ▼
Code prepares relevant state + permitted choices
    │
    ▼
Jev: structured decision and probability information
    │
    ▼
Application checks policy and uncertainty
    │
    ├── uncertain / unsafe ──► Ask a person
    │
    └── allowed ──► Browser code performs action
                             │
                             ▼
                     Verify actual outcome
```

Jev does not itself supply the entire login process, browser controller, file importer, or database. Those are separate responsibilities.

### Type safety versus correctness

Suppose software permits only these decisions:

```text
download_report
wait
ask_human
```

A type-safe output stays within the allowed structure. It cannot put an arbitrary paragraph in a field that only accepts those options.

However, selecting `download_report` at the wrong time can still be a mistake. TypeSafe's claims about hallucination and schema matching should not be interpreted as proof that all decisions or surrounding workflows are correct.

The announcement reports speed and benchmark results, with caveats. Model response time is only part of total workflow time; page loads, downloads, and checks add latency. Access and current product terms need checking before use.

## 8. Databases: tables, keys, relationships, and SQL

### What is a database?

A **database** stores and organizes information so software can retrieve and update it consistently.

A **DBMS (Database Management System)** is software that manages databases. PostgreSQL is an example.

A **relational database** organizes data into tables and supports relationships among them.

```text
CUSTOMERS                       INVOICES
customer_id                     invoice_id
name                            customer_id
                                amount

One customer ─────────────────► Many invoices
```

The relationship lets the system find a customer's invoices without copying all customer details into every invoice record.

### Rows, columns, types, and schemas

A **row** is one record. A **column** is an attribute of that record.

A **data type** defines the kind of value: text, integer, date, true/false, or a suitable numeric type.

A **schema** describes the database's structure and rules.

```text
Table: invoices
---------------------------------------------------
invoice_id       customer_id      amount      status
I-001            C-010            120.00      unpaid
I-002            C-010             75.00      paid
```

A financial application should use suitable exact numeric representations for money rather than casually relying on approximate floating-point arithmetic.

### Primary keys and foreign keys

A **primary key (PK)** uniquely identifies a row.

A **foreign key (FK)** refers to a related row in another table.

```text
CUSTOMERS
C-010 ──┐
C-011   │
        │ matching customer_id
        ▼
INVOICES
I-001 → C-010
I-002 → C-010
I-003 → C-011
```

An identifier may only be unique within one source. Two services can both issue an invoice numbered `100`. The system must preserve source context or use a suitable internal identifier.

### Constraints and missing values

A **constraint** enforces a rule, such as uniqueness or a required relationship.

**NULL** generally represents an absent or unknown value in SQL systems. It is not automatically zero or an empty string.

If hours worked are unknown, treating them as zero could make a productivity calculation misleading or impossible.

### SQL retrieves or changes data

**SQL (Structured Query Language)** lets software describe operations on relational data.

```sql
SELECT customer_id, SUM(amount) AS unpaid_total
FROM invoices
WHERE status = 'unpaid'
GROUP BY customer_id;
```

Read it step by step:

1. Start with the `invoices` table.
2. Keep records marked unpaid.
3. Group them by customer.
4. Add the amounts in each group.
5. Return a total for each customer.

This is an illustrative query. It assumes the field meanings, currency treatment, and dataset scope have been agreed.

### Joins and grain

A **join** combines related tables using matching values.

The **grain** is what one row represents: one invoice, one invoice line, one payment, or one day.

Grain matters because joining tables can repeat values:

```text
Invoice total: $100
        │ has
        ▼
Two invoice lines
        │ careless join repeats total
        ▼
Line 1: invoice total $100
Line 2: invoice total $100
        │ careless sum
        ▼
Wrong answer: $200
```

This is a data modeling error, not something a prettier dashboard fixes.

### Transactions and indexes

A **transaction** groups changes so they complete together or do not take effect together. For example, an operation should not update one side of a financial transfer but leave the other unchanged.

An **index** helps the database find certain records more efficiently. It can speed reads, but it takes storage and can add work when records are written.

### PostgreSQL and Supabase

**PostgreSQL**, often called **Postgres**, is open-source relational database software.

**Supabase** is a service/platform built around PostgreSQL, with related application capabilities such as authentication and storage.

```text
Application
    │
    ▼
Supabase services
    │
    ▼
PostgreSQL database
```

These names are not interchangeable. PostgreSQL is the database engine; Supabase provides a service environment around it. Managed infrastructure does not remove responsibility for schema design, permissions, data quality, and application maintenance.

## 9. Data warehouses and reporting models

### Database and warehouse are not opposites

A **data warehouse** is a data store organized especially for analysis across sources and time. It is often powered by database technology itself.

An operational database may focus on handling individual records and updates. A warehouse may focus on large historical queries.

```text
Operational systems
  ├── Billing
  ├── Support
  └── Subscriptions
          │ collection and transformation
          ▼
     Reporting store / warehouse
          │
          ▼
     Historical analysis and dashboards
```

**OLTP** describes online transaction processing: day-to-day record operations.

**OLAP** describes online analytical processing: analyzing collections of records.

These are workload styles. A small system can use one relational database for both operational and reporting needs; a separate warehouse is not mandatory for every dashboard.

### Fact tables and dimensions

A **fact table** contains events or measurements, such as a payment.

A **dimension table** contains descriptive context, such as customer, date, or plan type.

```text
                  Date
                   │
                   ▼
Customer ──────► Payments ◄────── Plan
                   ▲
                   │
                 Region
```

This is a simplified **star schema**: the fact table is connected to descriptive dimensions.

It can make analysis more consistent, but the table grain and relationships must still be right.

### A data lake is another concept

A **data lake** is a store that can hold a wide range of data in less-curated forms, including files and raw records.

A warehouse emphasizes organized analytical use. A lake emphasizes storing varied inputs. The terms overlap in modern products; neither removes the need for metadata, access rules, and quality checks.

**Practical question:** Do we actually need more infrastructure, or do we need better definitions and a cleaner dataset?

## 10. Data pipelines, quality, and trustworthy calculations

### A pipeline is a repeatable sequence

A **data pipeline** collects, checks, transforms, and delivers data.

```text
Sources ──► Collect ──► Validate ──► Standardize ──► Store ──► Use
                         │
                         └── invalid input ──► Review queue
```

**Ingestion** is bringing information into the system.

**Transformation** changes its representation or organization—for example, standardizing dates or mapping source headings to common fields.

### ETL and ELT

```text
ETL: Extract ──► Transform ──► Load
ELT: Extract ──► Load ──► Transform
```

ETL transforms before loading into the target store. ELT loads first and transforms there. Both can preserve raw inputs for later audit or reprocessing.

### Raw, staging, and curated layers

```text
RAW                    STAGING                   CURATED
Original input ─────► Checked and standardized ─────► Approved for reporting
```

These are logical roles, not necessarily three separate products.

Keep the original report and enough metadata to understand where records came from. **Metadata** is information about data: source, collection time, format, or field definition.

**Lineage** is the trace of how data moved and changed from source to result.

### Duplicates, retries, and idempotency

If an import runs twice, it should not automatically count the same records twice.

**Idempotency** means repeating an operation has the same intended effect as running it once.

```text
File A imported once  ──► 100 records
File A imported again ──► Still 100 intended records, not 200
```

This may involve file identifiers, transaction keys, or controlled updates. It must be designed; it is not automatic.

### Quality checks

Useful checks include:

- Expected columns are present.
- Dates fit the requested period.
- Currency and units are explicit.
- Required IDs exist.
- Duplicate records are detected.
- Totals reconcile with a trusted source.
- Missing data remains distinguishable from zero.

**Reconciliation** compares two representations of the same activity and explains differences.

A perfectly formatted file can still contain wrong or incomplete information.

### Metrics need definitions before formulas

A **metric** is a defined measure. A **KPI** is a metric selected to assess performance.

Consider an invented calculation:

```text
Collected payments       $1,000
Refunds                    $100
Net collections            $900
```

The calculation is easy. The definition is harder:

- Does the measure include tax?
- Which date counts: invoice date or payment date?
- Have all refunds arrived?
- Are amounts in the same currency?
- Which customers or products are included?

Exact arithmetic on misunderstood data still gives an unreliable answer.

### Freshness, completeness, and timeliness

**Freshness** says when data was last updated.

**Completeness** says whether the expected records or sources arrived.

**Timeliness** says whether the information arrived soon enough for its purpose.

A freshly refreshed dashboard can still be incomplete. A “real-time” chart cannot make a source that exports daily become real-time.

## 11. Dashboards and business intelligence

### What a dashboard is

A dashboard collects important views in one place: figures, trends, comparisons, filters, and detail.

**Business Intelligence (BI)** is the practice of using data to understand business activity and support decisions.

```text
Data ──► Shared metric definitions ──► Visuals ──► Human interpretation
```

A dashboard should not just answer “what is the number?” It should also reveal the period, filters, definition, source, and limitations.

### Common visuals

- A **card** shows one headline value.
- A **line chart** shows change over time.
- A **bar chart** compares categories.
- A **table** shows detailed values.
- A **filter** limits the records being considered.
- A **slicer** is an on-screen filter control.
- **Drill-through** opens a more detailed view behind a summary.

Chart choice matters. A misleading axis, mixed units, or incompatible periods can distort understanding even when individual values are correct.

### Semantic models and filter context

A **semantic model** defines the meaning used by reports: relationships, measures, names, and business rules.

**Filter context** is the selection of records used for a calculation.

```text
All records
    │ filter: January
    ▼
January records
    │ filter: Product A
    ▼
January, Product A records
    │ calculate
    ▼
Displayed total
```

Two tools should return the same total if they use the same definition and scope. If they do not, investigate the context and data—not just the chart styling.

### Reports, dashboards, and embedding

Products use “report” and “dashboard” differently. A report may include several detailed pages; a dashboard may emphasize a compact overview.

**Embedding** displays a report or chart inside another application. It requires supported interfaces, authentication, permissions, and applicable licensing. It is not simply pasting an image into a page.

## 12. Power BI, Tableau, and open-source alternatives

### Power BI

Microsoft Power BI supports connecting to data, modeling it, calculating measures, and creating interactive reports.

Typical concepts:

- **Power Query:** prepares data.
- **DAX:** defines analytical calculations.
- **Semantic model:** defines relationships and reusable measures.
- **Desktop authoring:** a development environment for creating reports.
- **Service:** a hosted environment for sharing and operating supported reports.
- **Gateway:** a component that can bridge the service to certain data sources it cannot directly reach.

The practical sequence is: connect, prepare, model, calculate, visualize, validate, share, and refresh. Licensing and supported deployment features must be checked.

### Tableau

Tableau is a commercial visual analytics platform. Its product family includes Desktop for authoring/analysis, Cloud as a hosted service, and Server for organization-managed deployment.

An analyst may build worksheets, combine them into dashboards, and add interactions. The same data-modeling and validation concerns still apply.

Tableau can be a sensible choice where skills, licenses, and support already exist. Its presence does not automatically provide a custom chatbot or a complete data pipeline.

### Metabase

Metabase offers a graphical query builder and a SQL editor. A saved **question** contains a query, results, and a visualization. Questions can be assembled into dashboards.

It has an open-source edition and commercial offerings. Exact access-control, embedding, AI, and governance features vary by edition and should be checked rather than assumed.

Metabase is a useful candidate when business users want approachable exploration over an existing database.

### Apache Superset

Apache Superset is an open-source data exploration and visualization platform with visual chart building, SQL tools, datasets, and dashboard filters.

It is useful for database-centered analytics with technical administration. It does not replace ingestion or make a database's definitions correct.

### Grafana

Grafana is a visualization and monitoring platform with an open-source edition and other offerings.

It is especially associated with time trends, operational monitoring, and alerts: service health, sensor readings, processing delays, and failures.

It can display business data with appropriate connections, but monitoring a process and doing finance-style self-service analysis are different needs.

### Comparing the roles

| Tool | Common reason to evaluate it | Responsibility that remains |
|---|---|---|
| Power BI | Business reporting in a Microsoft-oriented environment | Definitions, refresh, permissions, licenses, support |
| Tableau | Visual exploration and established enterprise reporting | Definitions, access, licenses, operations |
| Metabase | Accessible questions and dashboards over a database | Database quality, edition choices, administration |
| Apache Superset | Flexible visual and SQL-driven analytics | Technical setup, security, maintenance |
| Grafana | Monitoring, trends, and operational alerts | Data connections, alert quality, response procedures |
| Custom web app | A tailored interface and integrated workflow | Building and maintaining the entire experience |

**Open source** means source code is available under an applicable open-source license. It does not mean all commercial features are included, hosting is free, or no one needs to maintain the software.

## 13. AI models: generation, decisions, and uncertainty

### AI, machine learning, and models

**Artificial Intelligence (AI)** is a broad category of systems performing tasks associated with interpretation, reasoning, prediction, or decision-making.

**Machine learning** is an approach in which a system learns patterns from data rather than having every behavior hand-coded.

A **model** is the resulting system used to make predictions or produce outputs.

```text
Training data + training method
              │
              ▼
            Model
              │ receives new input
              ▼
        Prediction or generated output
```

Training a model and using a model are different activities. Most application teams use an existing model rather than train one from scratch.

### LLMs and tokens

A **Large Language Model (LLM)** generates and interprets language. A **token** is a unit the model processes; it may be a word fragment, word, punctuation, or another representation.

The **context window** is the amount of input/context a model can consider in a request. It is not unlimited memory, and supplying more information does not guarantee the model will use it correctly.

A **prompt** is the request and instructions supplied to a model.

A language model can write a plausible explanation without possessing reliable evidence. Fluent writing is not a truth test.

### Generative models versus structured decision models

```text
GENERATIVE MODEL
Input ──► Model ──► Free-form text, code, or another generated artifact

STRUCTURED DECISION MODEL
Input + allowed structure ──► Model ──► Defined choices/values
```

Jev emphasizes the second pattern. A language model can also be constrained to structured output in some setups, but output validity and decision correctness are still separate concerns.

### Hallucinations and grounding

A **hallucination** commonly means a model producing an unsupported or false claim as though it were factual.

**Grounding** connects a response to actual evidence, such as retrieved documents or query results.

Grounding helps but is not a guarantee: a model can misunderstand evidence or overstate what it proves.

### Probabilities and calibration

A probability estimate describes uncertainty. **Calibration** asks whether estimated probabilities correspond to observed accuracy across comparable examples.

```text
Many comparable decisions rated around 80% likely
                       │ evaluate against outcomes
                       ▼
About 80% correct would support calibration for that test setting
```

This is an illustrative explanation, not a benchmark for any product.

A confidence score is not necessarily a calibrated probability. A threshold that works in one setting may fail when inputs change.

### Training acronyms

- **RLHF:** reinforcement learning from human feedback.
- **RLVR:** reinforcement learning with verifiable rewards.
- **RLCD:** reinforcement learning for calibrated decisions, TypeSafe's named approach.

These describe training methods, not proof that an application cannot fail.

### What AI should not replace

Use explicit calculations for sums, ratios, accounting rules, and other exact measures.

Use models where interpretation is genuinely useful. If an ordinary rule is simpler, cheaper, and easier to verify, it may be the better solution.

## 14. Chatbots, agents, tools, skills, RAG, and MCP

### A chatbot is an interface; an agent describes behavior

A **chatbot** is software people interact with through messages.

An **agent** uses a model to interpret a request and choose actions through tools. A chatbot may be an agent, but it may also only answer from a document collection.

```text
User message
     │
     ▼
Assistant interprets request
     │
     ├── Needs clarification ──► Ask user
     │
     └── Needs permitted data/action
                    │
                    ▼
               Tool request
                    │
                    ▼
              Result and checks
                    │
                    ▼
               User response
```

“Agentic” does not mean unrestricted autonomy. The application should limit what the agent can access and do.

### What is a tool call?

A **tool** is a defined operation exposed to the assistant: retrieve invoices, search documents, or calculate a permitted comparison.

A **tool call** requests that operation with arguments.

```text
Assistant: "get unpaid total for permitted customer C-010"
                     │
                     ▼
Backend checks authorization and executes query
                     │
                     ▼
Structured result returned to assistant
```

The backend must enforce permissions even if the model requests something it should not.

### What is a skill?

A **skill** is reusable guidance, sometimes bundled with code/resources, for performing a task consistently.

It can describe:

- When to use the skill.
- Required inputs.
- Approved tools.
- The procedure.
- Output expectations.
- Conditions requiring a human.

```text
Skill: Explain an invoice total
    │
    ├── Confirm customer and period
    ├── Retrieve approved records
    ├── Calculate using tested code
    ├── Explain filters and exclusions
    └── Link to supporting records
```

A skill is not the same as training a new model, an SDK, or a security policy. Application code must enforce important restrictions.

### RAG: retrieve evidence before generating an answer

**Retrieval-Augmented Generation (RAG)** retrieves relevant information and includes it in the context used to generate a response.

```text
User question ──► Search relevant material ──► Selected evidence
      │                                             │
      └─────────────────────────────────────────────┤
                                                    ▼
                                           Model writes answer
                                                    │
                                                    ▼
                                           Answer + references
```

For documents, retrieval may use keyword search or **embeddings**—numeric representations used to find content with related meaning.

A **vector database** can store/search these representations. It is not the same thing as a relational financial ledger.

Use document retrieval to find a policy or definition. Use SQL or approved calculation tools for exact totals. Finding a paragraph about revenue is not the same as computing revenue from records.

### MCP: a standard for communicating with tools

**Model Context Protocol (MCP)** standardizes communication between compatible AI applications and tool/data providers.

```text
AI application / MCP client
              │ standardized communication
              ▼
          MCP server
              │ exposes permitted operations
              ▼
       Data service or application
```

MCP is not a model, database, or permission bypass. It is an interface protocol. A normal application API can also be enough for many assistants.

### Chat, charts, and screenshots

A dashboard chatbot should receive structured context—selected metric, date range, filters, and user permissions—not just an image of the chart.

```text
Chart filters + question
           │
           ▼
Approved query ──► Tested calculation ──► Explanation + evidence
```

A screenshot can document the view or highlight a result. If the assistant reads a screenshot, image interpretation may introduce errors. The source records remain the authoritative place to verify exact values.

### Explanation is not causation

An assistant might observe that refunds rose and a contribution measure fell. That does not automatically prove why refunds rose.

Good responses distinguish:

- What the records show.
- What was calculated.
- What is a plausible hypothesis.
- What remains unknown.

## 15. Cloud services, hosting, and maintenance

### What “cloud” means

Cloud services provide computing resources or applications over a network. The physical computers still exist; another organization operates some of the infrastructure.

**Hosting** provides an environment where an application runs and can be reached.

```text
User device ──► Network ──► Hosted application ──► Data/services
```

A locally running prototype is not automatically a secure, maintained online service.

### SaaS and managed services

**Software as a Service (SaaS)** is software accessed as an ongoing service.

A **managed service** takes responsibility for some infrastructure operations. The exact division of responsibility varies.

The user still needs to understand who handles:

- Application updates.
- Data backups and restoration.
- Permissions.
- Security configuration.
- Failures.
- Billing and service limits.

### Deployment and environments

**Deployment** makes a version of software available in its intended runtime environment.

Common environments include:

```text
Development ──► Test / staging ──► Production
Experiment       Verify safely      Real users and data
```

Production changes can affect real users and records. A successful test with synthetic data does not establish that production credentials, performance, or source formats work.

### Containers and Docker

A **container** packages an application with parts of the environment it needs, helping it run consistently.

**Docker** is a widely used container tool.

Containers do not eliminate hosting, updates, security configuration, persistent storage, or backups. Restarting a container should not be assumed to preserve application data unless storage is configured correctly.

### Open source and total cost

**OSS** is open-source software. Each product has a license defining permitted use and obligations.

**Total Cost of Ownership (TCO)** includes more than a subscription:

```text
TCO = subscriptions/hosting
    + setup effort
    + maintenance
    + support
    + upgrades and future changes
```

A product with no software license fee can still require substantial staff time. A managed service may cost money but reduce certain operations tasks.

## 16. Security, permissions, and privacy

### Authentication versus authorization

**Authentication** asks: who are you?

**Authorization** asks: what are you allowed to do?

```text
Sign in ──► Identity established ──► Permission check ──► Allowed operation
                                         │
                                         └── not permitted ──► Deny
```

Being signed in does not mean a person or program should see every record.

### Keys, tokens, OAuth, and MFA

An **API key** is a credential used in certain service interfaces.

A **token** represents an authorization or session capability. It may expire, but it can still be sensitive.

**OAuth** is a framework for delegated authorization. It can allow an application to access approved parts of an account without handing the application the user's password.

**MFA** uses more than one verification factor during authentication.

Credentials belong in protected secret storage, not shared documents, screenshots, repository files, or browser-visible code.

### Least privilege, RBAC, and RLS

**Least privilege** means granting only the access needed for the task.

**Role-Based Access Control (RBAC)** assigns permissions by role.

**Row-Level Security (RLS)** restricts access to particular records.

```text
User: Regional analyst
          │
          ▼
May view: permitted region's rows
May not:  view all customer data or change accounting records
```

A chatbot must follow the same boundaries as other interfaces. Revealing a restricted value in a chat answer is still a data disclosure.

### Encryption, backups, and audit logs

**Encryption** protects information through cryptographic encoding. It does not replace access controls.

A **backup** is a recoverable copy of data. A backup is useful only if restoration works.

An **audit log** records important actions, such as who changed a mapping or accessed sensitive information.

Avoid logging secrets or unnecessary personal details. “Log everything” is not a safe default.

### PII and prompt injection

**Personally Identifiable Information (PII)** is information that can identify a person. Collect and expose only what the task requires.

**Prompt injection** occurs when untrusted content tries to influence an AI system's instructions or behavior—for example, a document telling an assistant to send private data elsewhere.

Documents, webpages, and tool outputs are data to interpret, not authority to grant new permissions. The application must enforce boundaries independently of what the model reads.

## 17. Testing, logs, and failure handling

### Different tests answer different questions

- A **unit test** checks a small component, such as a formula function.
- An **integration test** checks that components communicate correctly.
- An **end-to-end test** checks a complete user workflow.
- A **user acceptance test** checks that the result meets the user's real need.

```text
Calculation works?        ──► Unit test
Collector reaches store? ──► Integration test
User gets report?        ──► End-to-end test
Report is useful?        ──► User acceptance
```

Testing code does not automatically establish that the deployed system has the right permissions, configuration, or data.

### Logs and observability

A **log** records events or errors.

**Observability** is the ability to understand a system's state from signals such as logs, metrics, and traces.

Useful signals include:

- Last successful run.
- Number of records received.
- Sources still missing.
- Failure category.
- Processing time.
- A run ID linking related events.

A green “job started” message does not prove that the intended output was created.

### Retries and safe failure

A **retry** repeats an operation after failure. It is appropriate only when repeating is safe and there is reason to expect success.

```text
Temporary network failure ──► Safe delayed retry
Wrong permissions        ──► Fix access, not endless retry
Uncertain payment write  ──► Check whether it applied before repeating
```

Some failures happen after an operation already took effect. Repeating a payment or record creation can duplicate it.

A **human-in-the-loop** design asks a person to review uncertain or consequential situations.

### CI/CD

**Continuous Integration (CI)** automatically checks proposed changes.

**Continuous Delivery or Deployment (CD)** describes processes for preparing or releasing changes.

These processes help consistency, but the quality of the checks and the rules around production release still matter.

## 18. Choosing tools without getting lost in names

### Start with the job, not the product

Ask in this order:

1. What task must be done?
2. What input information is available?
3. How accurate and timely must the result be?
4. Who uses it and who maintains it?
5. Which permissions and constraints apply?
6. What is the smallest solution that meets those requirements?
7. How will we verify it and handle failure?

### Match the tool category to the task

| Need | Category to consider | Examples |
|---|---|---|
| Inspect a small dataset | Spreadsheet | Excel, Google Sheets |
| Repeat supported spreadsheet operations | Spreadsheet automation | VBA, Office Scripts, Apps Script |
| Prepare and combine datasets | Transformation tool or script | Power Query, Python |
| Connect supported systems directly | API/connector | Vendor API, documented integration |
| Repeat a web workflow | Browser automation | Playwright, Selenium |
| Make constrained interpretive decisions | Decision model | Jev |
| Store linked records consistently | Relational database | PostgreSQL, a managed service around it |
| Analyze substantial historical data | Reporting store/warehouse | An appropriate analytical data platform |
| Share business analysis | BI platform | Power BI, Tableau, Metabase, Superset |
| Monitor operations and alerts | Monitoring dashboard | Grafana |
| Generate explanations or language | Language model | An appropriate LLM |
| Ground answers in documents | Retrieval system | Keyword/semantic retrieval with RAG |
| Expose bounded operations to assistants | Tool interface | Application API or MCP |
| Guide a repeatable agent procedure | Skill | Reviewed instructions and tools |

### Questions that reveal misleading claims

- “Is this AI?” → Which part requires interpretation rather than explicit rules?
- “Is it real-time?” → How quickly does the original source provide new data?
- “Is it accurate?” → Accurate for which cases, measured how?
- “Is it secure?” → Which users, records, credentials, and attack paths were considered?
- “Is it open source?” → Under which license, and which edition includes the needed features?
- “Is it automated?” → Which steps still require sign-in, approval, or repair?
- “Is it integrated?” → Through an API, files, browser control, or something else?
- “Can it explain the number?” → Can the result be reproduced from source records and agreed formulas?

The most valuable understanding is knowing where one component's responsibility ends and another's begins.

## 19. Acronym reference

| Acronym | Expanded name | Plain-language meaning |
|---|---|---|
| AI | Artificial Intelligence | Models/systems used for interpretation, prediction, or decisions |
| API | Application Programming Interface | A defined software interface |
| BI | Business Intelligence | Data analysis for business understanding and decisions |
| CD | Continuous Delivery / Continuous Deployment | Processes for preparing or releasing software changes |
| CI | Continuous Integration | Automated checks when changes are combined |
| CMS | Content Management System | Software for managing published content |
| CRM | Customer Relationship Management | Software for customer relationships and interactions |
| CSS | Cascading Style Sheets | Rules for web-page presentation |
| CSV | Comma-Separated Values | A simple tabular text format |
| DAX | Data Analysis Expressions | Analytical formula language used in Power BI |
| DBMS | Database Management System | Software that manages databases |
| DNS | Domain Name System | Resolves domain names to network addressing information |
| DOM | Document Object Model | A browser's structured representation of a page |
| ELT | Extract, Load, Transform | Collect/store first, transform afterward |
| ERP | Enterprise Resource Planning | Integrated software for functions such as finance and operations |
| ETL | Extract, Transform, Load | Collect/transform first, load afterward |
| FK | Foreign Key | Reference to a related record |
| HTML | HyperText Markup Language | Markup for web-page content |
| HTTP | Hypertext Transfer Protocol | Rules for web requests and responses |
| HTTPS | Hypertext Transfer Protocol Secure | HTTP communicated over an encrypted connection |
| JSON | JavaScript Object Notation | A structured text format |
| KPI | Key Performance Indicator | A chosen performance measure |
| LLM | Large Language Model | A model that generates/interprets language |
| MCP | Model Context Protocol | Standard communication between compatible AI apps and tools |
| MFA | Multi-Factor Authentication | Authentication using multiple factors |
| OCR | Optical Character Recognition | Reading text from images |
| OLAP | Online Analytical Processing | Analytical work across records |
| OLTP | Online Transaction Processing | Day-to-day record operations |
| OSS | Open-Source Software | Software available under an open-source license |
| PDF | Portable Document Format | A document format preserving fixed page layout |
| PII | Personally Identifiable Information | Information that can identify a person |
| PK | Primary Key | A unique row identifier |
| RAG | Retrieval-Augmented Generation | Retrieving evidence for a model-generated answer |
| RBAC | Role-Based Access Control | Permissions assigned by role |
| REST | Representational State Transfer | An architectural style often used for web APIs |
| RLCD | Reinforcement Learning for Calibrated Decisions | TypeSafe's named training approach |
| RLHF | Reinforcement Learning from Human Feedback | Training influenced by human feedback |
| RLS | Row-Level Security | Restrictions on which records a user can access |
| RLVR | Reinforcement Learning with Verifiable Rewards | Training using checkable rewards |
| SaaS | Software as a Service | Software provided as an ongoing service |
| SDK | Software Development Kit | Tools/libraries for using a service |
| SKU | Stock Keeping Unit | Inventory/product identifier |
| SQL | Structured Query Language | Language for relational data operations |
| TCO | Total Cost of Ownership | Full cost of setup, operation, support, and changes |
| UI | User Interface | Screens and controls users interact with |
| URL | Uniform Resource Locator | Address of a resource |
| UX | User Experience | Overall usability and clarity |
| VBA | Visual Basic for Applications | Language used for Office automation |

**Names, not acronyms:** Jev, Python, JavaScript, TypeScript, PostgreSQL/Postgres, Supabase, Tableau, Metabase, Apache Superset, Grafana, Docker, Git, GitHub, Cursor, Claude Code, Copilot, Power Query, and M.

**File extensions, not tool categories:** `.csv`, `.xlsx`, `.json`, `.pdf`, `.png`, and `.jpg`.

## 20. Sources and further reading

This guide combines general technical explanations with the following product references. Product editions, access, licensing, and interfaces can change; consult current official documentation before selecting or implementing a tool.

- [TypeSafe AI: Introducing System One Models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — product identity, structured outputs, probability/calibration claims, and benchmark caveats.
- [Tableau product overview](https://www.tableau.com/products) — product family and deployment roles.
- [Metabase: questions](https://www.metabase.com/docs/latest/questions/introduction) — graphical/SQL querying, saved questions, and dashboards.
- [Metabase open-source edition](https://www.metabase.com/start/oss/) — open-source offering.
- [Apache Superset](https://superset.apache.org/) — data exploration, visual/SQL tools, and administration documentation.
- [Grafana OSS](https://grafana.com/oss/grafana/) — visualization, monitoring, and edition distinctions.

The diagrams and examples in this guide are explanatory illustrations. They are not screenshots, vendor API specifications, implementation instructions, or evidence that a particular integration has been tested.