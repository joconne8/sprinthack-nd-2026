# ADR-001: Weekend prototype architecture and production path

Task: GOV-04 / issue #9
Status: **Proposed**. Waiting for Jack OC to accept. ENG-01 builds D1 and D2 only after acceptance.
Inputs:
- PLAN §3–§6, §8, §11, §13; WICKS; AMANDA; BRIEF; FOLLOWUP; JACK (as corrected by PLAN).
- GOV-01 register and process map; GOV-02 scope.
- The repository as it is at `f36684c`.

## Decisions

| # | Decision | Why |
| --- | --- | --- |
| D1 | **Weekend prototype stack:** reuse the repo's existing stack. Python 3.10+ standard library, a SQLite file, a static HTML/JS dashboard, and Node + Playwright for browser replay only. | Reuses working code; one pinned dependency; no paid service or credentials; fastest path to the P0 slice. |
| D2 | **Prototype data layer:** one local SQLite file with raw → staging → curated → metric tables and deterministic SQL. | Gives lineage, constraints and transactions with no server to run. Demo only. |
| D3 | **Production, first step:** authorized retrieval into an approved Microsoft folder, then Excel/Power Query, then the existing Power BI. | Delivers reports into tools Goodwill already pays for. No new paid database, model or dashboard is required. |
| D4 | **Managed relational layer:** only when a trigger in §4 is observed in a pilot **and** named owners accept it. The vendor is chosen then, against Goodwill IT standards. | Controls and ownership justify a database, not row counts or guessed salaries. Supabase is not assumed. |
| D5 | **Acquisition automation:** deterministic replay is the baseline. Jev is an optional, separately measured decision provider on synthetic data only. The recorder is deferred. | Jev is a probabilistic model. A financial flow must not drift silently. |
| D6 | **AI:** read-only tools over deterministic results. Production AI goes only through an approved Copilot route. | Amanda: AI must go through Copilot. Numbers come from SQL, not a model. |
| D7 | **Dashboards:** the custom app is the weekend demo and an operations console. Production leadership reporting stays in Power BI until assessed. | Avoids building and supporting a second reporting product. |

## Context

- Amanda's bottleneck is report retrieval, and Upright's API key is restricted. Debie needs visibility (BRIEF, AMANDA).
- Power BI already sits downstream of manual Excel consolidation and Sonia's weekly summary (GOV-01 process map).
- Amanda now works with an assistant; the e-commerce manager has left (FOLLOWUP). Any maintenance burden lands on a small team.
- Wicks advised keeping the data layer low-maintenance and treating a database as a constraint question, not a default.
- Event rules: synthetic data, no pre-built code, disclose what was borrowed, code freeze Sunday 4:00 pm (BRIEF).

## D1. Weekend prototype stack

| Option | Reuses existing code | Setup before freeze | Dependencies / lockfiles | Paid service or credentials | Risk |
| --- | --- | --- | --- | --- | --- |
| **A.** PLAN §3 default: TypeScript React/Vite, Node API, managed PostgreSQL | None (no TS in repo) | New scaffold, npm install, database account | Large npm tree | A managed Postgres account | Highest: second stack, new credentials |
| **B.** Repo-native: Python stdlib, SQLite, static JS, Playwright for replay | Replica, intake, run state, fixtures, contracts | Minimal; most pieces run today | Playwright 1.62.1 only (already pinned) | None | Plainer UI; Python's HTTP server is demo-grade |
| **C.** The separate Replit foundation | Unknown; not in this repo | Import plus review | Unknown | Unknown | Provenance and "built vs borrowed" disclosure; unseen code |

**Recommendation: B.** PLAN §3 says to reuse an existing implemented stack and never to build two. B is the stack already in the repo.

Use C instead only if Jack OC confirms all of the following:
- The Replit app exists and was built this weekend.
- Its provenance can be disclosed.
- It can be imported with passing tests before ENG-01 starts.

Never both. React/Vite polish becomes P1 after P0 passes, against the same contracts.

| Component | Option B technology | Lane |
| --- | --- | --- |
| Replica portal | Python `http.server` + static JS (exists) | Hugh |
| Browser replay | Node + Playwright 1.62.1 (exists) | Hugh |
| Intake / archive | Python, `acquisition/intake.py` (draft exists) | Hugh |
| Importer, reconciliation, metrics | Python `csv`, `decimal`, `sqlite3` plus SQL | Peyton |
| API | Python `http.server`, JSON per GOV-03 `planning/contracts.md` §8 (on branch `jackoc/GOV-03-contracts`); routes and entrypoint owned by ENG-01 | Peyton + Jack OC |
| Dashboard | Static HTML/JS served by the API process; no build step | Landon |
| Contracts | JSON Schema + `contracts/tests/validate-contracts.cjs` (GOV-03 branch) | Jack OC |
| Tests | Python `unittest`, Node test scripts, Playwright browser tests; ENG-04 acceptance | All lanes / Jack mc |

**Runtime prerequisites** (ENG-01 verifies on each teammate machine):
- Python ≥ 3.10.
- On Windows, the `tzdata` package. `zoneinfo` has no system timezone database there, and the replica calls `ZoneInfo`.
- Node ≥ 18 and `npx playwright install chromium`, needed only for replay and browser tests.

At least one teammate machine currently has neither Python nor Node. It can still run the contract checker through VS Code's bundled runtime.

## D2. Prototype data layer

- One SQLite file in a gitignored local folder, next to the content-addressed raw archive from `acquisition/intake.py`.
- Tables follow PLAN §5 and the GOV-03 contracts:
  - `source_files`, `acquisition_runs`, `import_batches`, `rejected_rows`
  - versioned fact rows keyed by natural key
  - `metric_runs`, `reconciliation_results`, `exceptions`
- Idempotency is enforced by unique constraints.
- Imports run in transactions, and metrics are SQL views or recomputed tables.
- **Reset** = delete the file and re-import from the immutable archive. No server, no credentials.
- This is a demo choice, not a production recommendation. Peyton is the sole migration owner.

## D3 and D4. Production data path

| Need | Approved folder → Excel/Power Query → existing Power BI | Managed relational layer |
| --- | --- | --- |
| Raw file retention | SharePoint/OneDrive versioning and retention labels | Object storage plus file/batch tables |
| Repeatable ingestion | Power Query folder refresh | Scheduled jobs with run tables |
| Row-level lineage | Possible with file and row columns; harder to audit | Natural (file → row → batch → metric run) |
| Duplicates and corrections | Query rules; corrections need discipline | Unique keys plus versioned upserts |
| Reconciliation and exceptions | Workbook checks | SQL checks and exception tables |
| Concurrency and access | Workbook and workspace permissions | Roles and row-level security |
| Agent or tool access | Power BI semantic model / Copilot, subject to licensing | Narrow permissioned API |
| Owners needed | Query/workbook owner and Power BI owner (both roles exist today) | Platform owner, data/rule steward, support (new roles) |
| Cost | Existing licenses | Service cost plus support time |

**D3: start with the bridge.** It meets the first production need, reports arriving without portal clicking, using existing tools. A pilot runs it in parallel with today's manual path (PLAN §11, weeks 3–4).

**D4: add a managed layer only when both conditions hold:**
1. **At least one trigger is observed during the pilot:**
   - **T1:** auditors or finance need row-level lineage that Power Query cannot show reliably.
   - **T2:** several people must edit or approve the same data at once.
   - **T3:** corrections and backfills need versioned history.
   - **T4:** an approved agent or tool needs permissioned query access.
   - **T5:** the number of sources or the refresh frequency makes folder refresh unreliable.
2. **Named people accept the roles:** platform owner, data/rule steward and support escalation.

The vendor (for example Azure SQL inside the existing Microsoft tenant, or PostgreSQL) is chosen at that point against Goodwill IT standards.

**Explicitly rejected as reasons:**
- A supposed 10,000-row Excel limit (PLAN §1 correction).
- A guessed $100k data-engineer salary (JACK; PLAN §1 correction).
- An automatic Supabase commitment.

**Production ownership is not yet assigned** (GOV-01 OQ-07). The roles needed:

| Role | Responsibility | Today |
| --- | --- | --- |
| Process owner | Report list, timing, exceptions | Amanda (operations), working with an assistant whose role is not yet defined |
| Platform / IT owner | Runner host, identities, storage, approvals | Unassigned |
| Data / rule steward | Metric definitions, mappings, corrections | Finance; unassigned |
| Support escalation | Incidents, portal drift, repairs | Unassigned |
| Partner implementation owner | Sprint Lab delivery | Team, if continued |

## D5. Acquisition automation

The decision order follows PLAN §4: supported export, then authorized API, then email/folder, then authorized browser automation, then manual upload. Upright's API is restricted, so it starts at browser automation with a manual fallback.

| Approach | What it is | Weekend | Production |
| --- | --- | --- | --- |
| Deterministic replay | Tested Playwright code runs versioned skill steps with assertions. No model call. Stops on drift. | P0 on the replica | Only after provider and Goodwill approval |
| Jev | TypeSafe's probabilistic decision model choosing among observed controls | Optional, synthetic replica only, measured separately, if access exists | Needs Goodwill IT approval (Copilot-only policy) and provider terms |
| LLM planner | A separate model proposing goals or skills | Not planned | Same gate as Jev |
| Scripted demo | A fixed sequence presented to an audience | Must be labelled scripted | Not applicable |
| Recorder | Captures a human's clicks to make a skill | Deferred (P2) | Needs consent, redaction and review |

Live sessions are signed in by a Goodwill person (WICKS). Automation reuses that session only on an approved runner. Skills never hold credentials, as `acquisition/skills/upright-paid-orders.skill.json` already states.

## D6. AI

- Tools are read-only and typed (`ToolRequest` in the GOV-03 contracts).
- A report rerun is only a proposal awaiting human approval. No posting, email or browser-write tool exists.
- Production AI requires Goodwill IT approval of a Copilot route. APP-07 validates the tenant, licensing, identity and scopes.
- A Teams-styled interface is not a Teams integration.

## D7. Custom dashboard versus Power BI

The weekend app tells the end-to-end story and serves as an operations console. In production, leadership visibility stays in Power BI, fed by the D3 bridge, until it is assessed. A custom console survives only where it meets a need Power BI cannot (PLAN §6).

## Consequences

- **D1 is reversible.** The contracts are language-neutral, so a React UI can replace the static UI later against the same API.
- **D2 does not constrain production.** D3 does not depend on SQLite or Python.
- **ENG-01 follow-ups:**
  - Record the real commands.
  - Gitignore the SQLite file and the archive.
  - Add `tzdata` for Windows.
  - Wire the contract check and unit tests into CI. Today CI runs only the synthetic-data workflow.
- Security gates for every live route are in `planning/security-and-access.md`.
