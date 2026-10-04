# GOV-04 approval gaps

Nothing in this list is approved. Group A can be decided by the team this weekend. Group B needs Goodwill or a provider, and nobody on the team may treat it as granted.

## A. Team decisions (Jack OC)

| ID | Decision | Recommendation | Blocks |
| --- | --- | --- | --- |
| A1 | Accept ADR-001 D1: the repo-native prototype stack (Python stdlib, SQLite, static JS, Playwright for replay) | Accept. Choose the Replit foundation only if it exists, was built this weekend, can be disclosed and arrives with passing tests. | ENG-01 scaffold, and through it DAT-02, APP-01, APP-02 and ENG-04 |
| A2 | Accept D2: a local SQLite file as the demo data layer, with Peyton owning migrations | Accept | DAT-02 |
| A3 | Accept D3/D4: the production bridge first, and a managed database only on triggers with named owners | Accept for the pitch and the Sprint Lab plan | REL-01 narrative, REL-04 |
| A4 | Accept D5/D6: deterministic replay baseline, Jev optional on synthetic data only, AI read-only through an approved Copilot route | Accept (matches GOV-02) | ING-02, ING-06, APP-04/05 |
| A5 | Confirm whether Jev access exists for the replica comparison | Ask the team. If there is no access, ING-06 stays blocked and the pitch says so. | ING-06 |
| A6 | ENG-01 runtime prerequisites: Python ≥ 3.10, `tzdata` on Windows, Node ≥ 18 plus Playwright Chromium for replay | Verify on each teammate machine before dispatching build lanes | Every build lane |

## B. Goodwill and provider approvals

| ID | Approval or evidence | Owner to ask | Needed before | Requirement / open question |
| --- | --- | --- | --- | --- |
| B1 | Upright Labs permission (or terms review) for browser automation of its portal | Goodwill IT with Upright Labs | Any live Upright pilot | REQ-ING-03, GAP-06 |
| B2 | Approved runner host, session ownership and operator account | Goodwill IT, process owner | Any live acquisition | OQ-07 |
| B3 | Approved storage location (SharePoint/OneDrive folder) and retention period | Goodwill IT, records/finance owner | The D3 bridge pilot | REQ-OPS-03 |
| B4 | Power BI dataset owner and refresh path; Sonia's workbook validated | Reporting owner, Sonia | Connecting the bridge to Power BI | REQ-OPS-02, OQ-03, GAP-02 |
| B5 | Copilot route: tenant, licensing, identity, scopes, support owner | Goodwill IT/security | Any production AI | REQ-AI-01, OQ-08 (APP-07) |
| B6 | Any external model (including Jev) on Goodwill data | Goodwill IT/security, provider | Never during the weekend; only after review | REQ-AI-01, REQ-AI-02 |
| B7 | Approved finance definitions (revenue, refunds, fees, shipping, settlement) | Finance/accounting | Production metrics; any claim beyond "demo net sales" | REQ-DAT-05, OQ-04 |
| B8 | Business Central format and test environment | Finance/accounting, IT | Any import or posting (posting is out of scope) | REQ-FIN-01, OQ-06 |
| B9 | Named production owners: platform, data/rule steward, support escalation | Goodwill leadership | D4, and any unattended operation | REQ-OPS-01, OQ-07 |
| B10 | Assistant's role in run-state exceptions | Amanda | Assigning `needs_human` owners in production | REQ-OPS-01, GAP-05 |
| B11 | Exact Upright report names, fields and date semantics (Amanda's PowerPoint and screenshots) | Amanda / Hugh's lane | Claiming fidelity to the real portal | OQ-01, GAP-01 |

## How these get resolved

Group A: Jack OC accepts or amends ADR-001, for example in a reply on issue #9. Group B: the human team raises the items with Goodwill. This task sent no messages and contacted no provider.
