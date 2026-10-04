# GOV-01 Stakeholder Requirement Register

Task: GOV-01 / issue #13
State: draft for human scope review
Evidence authority: current user decisions, then Drive source material and the three-phase plan. Older repo PRDs are background only.

## Source IDs

| ID | Source |
| --- | --- |
| PLAN | Goodwill - Three-Phase Solution and Overnight AI Engineering Plan |
| AMANDA | Amanda Baumer Goodwill Meeting.md |
| FOLLOWUP | Amanda2.0 |
| WICKS | michael-wicks-plan.md |
| BRIEF | goodwill-track-brief-v2.md |
| JACK | Jack explanation.md |

## Requirement Register

| Requirement ID | Stakeholder / owner | Requirement | Source basis | Type | Priority | Acceptance test | Approval state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-ING-01 | Amanda / operations | Reduce repeated Upright report retrieval by supporting an authorized, parameterized report request for the same report with changed dates. | AMANDA, PLAN, WICKS | Evidence-backed need | P0 | A user can request the selected report for date range A and B, and the resulting source package records requested dates, actual coverage and source identity. | Needs human scope review |
| REQ-ING-02 | Amanda / operations | Treat Upright as the main acquisition pain; Cash Monkey remains in the source register but should not receive equal P0 effort unless a later decision changes this. | AMANDA, PLAN | Evidence-backed prioritization | P0 | P0 task plan names Upright-style acquisition first and does not imply Cash Monkey is equally hard. | Needs human scope review |
| REQ-ING-03 | Amanda / operations, IT/security | Do not assume an Upright API key is available or design around bypassing a provider restriction. | AMANDA, PLAN, BRIEF | Evidence-backed constraint | P0 | Acquisition design lists API as optional only when authorized and available; restricted API access is recorded as an unresolved production dependency. | Needs human scope review |
| REQ-ING-04 | Amanda / operations | Distinguish report availability from report distribution timing: Amanda can pull reports whenever needed, while weekend e-commerce visibility can still be delayed by manual workflow. | AMANDA, PLAN, BRIEF | Evidence-backed correction | P0 | Scope notes do not claim the portal only provides reports Monday; they identify manual retrieval/consolidation as the delay source. | Needs human scope review |
| REQ-ING-05 | Operators / future support owner | Keep a manual upload or human fallback for unavailable reports, login/MFA/CAPTCHA, portal drift and unsupported sources. | PLAN, BRIEF | Proposal from synthesis | P0 | Failure states produce visible "needs human action" outputs and do not fabricate successful files. | Needs contract in GOV-03 |
| REQ-DAT-01 | Amanda, Sonia, leadership | Preserve source lineage from acquired file to accepted row, rejected row, metric and drilldown evidence. | AMANDA, PLAN, JACK | Evidence-backed need plus technical synthesis | P0 | A displayed metric can be traced to source file ID, source row IDs, import batch and metric definition version. | Needs contract in GOV-03 |
| REQ-DAT-02 | Leadership, finance | Use deterministic code/SQL for financial calculations; do not ask an LLM to calculate financial numbers. | AMANDA, JACK, PLAN | Evidence-backed constraint | P0 | Financial metric definitions are implemented outside model prompts, and assistant text can only cite computed values. | Needs implementation tests |
| REQ-DAT-03 | Leadership, finance | Missing inputs must remain unknown, unavailable or partial; never substitute zero or an invented estimate. | PLAN, BRIEF | Evidence-backed rule | P0 | Missing buyer, labor, source, cost or snapshot data produces an unavailable/partial state in metrics and UI. | Needs contract in GOV-03 |
| REQ-DAT-04 | Data owners | Separate revenue, refunds, fees, shipping, settlements and expenses before combining source reports. | PLAN, BRIEF | Evidence-backed control | P0 | Metric definitions specify source-of-record, grain and exclusions; nine source amounts are not summed as revenue. | Needs GOV-02/GOV-03 |
| REQ-DAT-05 | Demo finance reviewer | For the weekend demo, define demo net sales as item sales minus refunds, excluding shipping, tax and fees. | PLAN, AGENTS.md | Current operating rule | P0 | Fixture, SQL/API labels, dashboard text and exports all use the same demo net sales definition. | Needs GOV-02 freeze |
| REQ-KPI-01 | Debie / leadership | Provide clear e-commerce visibility with definitions, period, coverage, freshness and drilldown, not just decorative charts. | BRIEF, PLAN, WICKS | Evidence-backed need | P0 | At least one P0 dashboard metric shows formula, period, freshness, source coverage and supporting rows. | Needs downstream implementation |
| REQ-KPI-02 | Debie / leadership | Track strategic KPI needs as available, unavailable or deferred instead of manufacturing unsupported metrics. | BRIEF, PLAN | Evidence-backed need | P0 | KPI scorecard/open-question log marks labor productivity, margins, sell-through, category and customer measures with required missing inputs. | Needs GOV-02 |
| REQ-KPI-03 | Leadership / operations | Do not use the physical-store 50-55 percent sell-through reference as an approved e-commerce target. | BRIEF, PLAN | Evidence-backed correction | P0 | Any sell-through artifact labels e-commerce target as unresolved and omits red/green status against 50-55 percent. | Needs GOV-02 |
| REQ-OPS-01 | Amanda / assistant | Account for current staffing: the e-commerce manager assumption is stale; Amanda is now on her own with an assistant whose responsibilities are not yet validated. | FOLLOWUP, PLAN | Evidence-backed correction | P0 | Process map and run-state design do not depend on the former manager and list assistant role details as open questions. | Needs human validation |
| REQ-OPS-02 | Sonia / admin summary | Preserve the current handoff to Sonia's weekly summary and existing store-sales/Power BI flow until those owners validate a replacement. | AMANDA, PLAN | Evidence-backed handoff | P0 | Process map includes Amanda/master Excel -> Sonia weekly summary -> store sales/Power BI, with validation pending. | Needs Sonia review |
| REQ-OPS-03 | Operators / support | Report acquisition should produce a usable source package even if later dashboard/data stages are unavailable. | PLAN, AMANDA | Proposal from synthesis | P0 | Acquired output is stored with manifest/checksum/period and can be opened/exported independently. | Needs GOV-03 |
| REQ-AI-01 | Amanda, IT/security | Any production AI must go through an approved Goodwill path, likely Microsoft Copilot; demo AI must be synthetic/read-only and labeled. | AMANDA, BRIEF, PLAN | Evidence-backed constraint | P0 | App/pitch do not claim production Copilot/Jev approval; assistant, if any, is read-only and source-grounded. | Needs IT approval |
| REQ-AI-02 | Reviewers / users | Treat Jev or browser-decision tooling as probabilistic/model-assisted unless separately verified; deterministic replay is a separate baseline. | PLAN, JACK, WICKS | Evidence-backed correction | P1 | Architecture notes distinguish deterministic replay, model-assisted decisions and scripted demos. | Needs GOV-04 |
| REQ-FIN-01 | Finance/accounting | No Business Central posting in the weekend prototype; any output is a proposed mapping/export until finance validates accounts, periods, dimensions and duplicate controls. | BRIEF, PLAN | Evidence-backed boundary | P0 | UI and demo script have no production "post" action and label finance output as unvalidated preview if shown. | Needs finance review |
| REQ-FIN-02 | Finance/accounting | Measure baseline effort and ROI before claiming savings or mission impact; Amanda's 30-45 minute estimate is not a measured baseline. | AMANDA, BRIEF, PLAN | Evidence-backed limitation | P0 | Pitch/report distinguishes estimates from measured baseline and does not compute guaranteed ROI. | Needs production follow-up |
| REQ-SEC-01 | Goodwill/provider owners | Live vendor access, production data, credentials, provider restriction bypass and unattended production deployment are out of bounds without explicit approval. | BRIEF, PLAN, AGENTS.md | Evidence-backed boundary | P0 | Task packets and demo disclaimers state synthetic/local/replica only unless a live pilot is explicitly approved. | Current rule |

## Open Questions And Decisions For GOV-02/GOV-03

| Open ID | Question / decision | Why it matters | Source basis | Owner to confirm |
| --- | --- | --- | --- | --- |
| OQ-01 | Which exact Upright report names, filters and date parameters are in the accepted P0 flow? | GOV-03 contracts and ING-01 replica need exact report identity and fields. | AMANDA, PLAN | Amanda / Hugh lane |
| OQ-02 | Which source files/exports are actually available for each platform, and which overlap? | Prevents double counting and wrong system-of-record choices. | AMANDA, BRIEF, PLAN | Operations / data owner |
| OQ-03 | What is Sonia's weekly-summary workbook shape and acceptance criteria? | Current handoff cannot be safely replaced without Sonia validation. | AMANDA, PLAN | Sonia / operations |
| OQ-04 | What are Goodwill's approved revenue, refund, fee, shipping, tax and settlement definitions? | Demo net sales is a convention, not approved accounting revenue. | PLAN, BRIEF | Finance/accounting |
| OQ-05 | What reporting timezone and close cutoffs should be used? | Date-range imports and daily metrics depend on a period convention. | BRIEF, PLAN | Operations/finance |
| OQ-06 | What format does Business Central require, and what test environment exists? | Prevents false accounting-compatibility claims. | BRIEF, PLAN | Finance/accounting/IT |
| OQ-07 | Who owns production support, credentials/session ownership and incident recovery? | Unattended acquisition cannot run safely without named owners. | FOLLOWUP, PLAN | Goodwill leadership/IT |
| OQ-08 | Which AI provider/surface is approved for production, if any? | Amanda requires Copilot; external or separate model paths need approval. | AMANDA, BRIEF, PLAN | IT/security |

## Notes For Downstream Lanes

- GOV-01 does not freeze scope or contracts. GOV-02 must make the P0/P1/P2 scope decision, and GOV-03 must publish data/API/tool contracts.
- The old four-view/two-platform PRD is background. Current main says P0 is the acquisition-led vertical slice, with richer views and a second source only after P0 works.
- Every downstream artifact should retain source IDs or requirement IDs so human reviewers can verify what is evidence-backed, proposed, deferred or unresolved.
