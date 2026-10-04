# Security and access gates

Task: GOV-04 / issue #9
Status: **Proposed**. Waiting for Jack OC to accept.

This document separates what the team may do this weekend from what any live pilot needs first. **No live route is approved.** Approval comes from Goodwill and the providers, never from this document.
Sources: PLAN §4, §6, §8, §13; AMANDA; BRIEF; WICKS; FOLLOWUP; GOV-01 REQ-SEC-01, REQ-AI-01, REQ-ING-03, REQ-FIN-01, OQ-06..08.

## 1. Allowed this weekend

- Synthetic data only. Every contract record carries `synthetic: true`.
- Replica portals on loopback only. The skill's `allowed_hosts` are `127.0.0.1`, `localhost` and `[::1]`.
- Not allowed:
  - credentials, cookies or API keys in the repo, skills, logs or prompts
  - external AI on any Goodwill data
  - deployment, external messages or accounting posting

## 2. Credentials and sessions

- Never commit, store or log credentials, cookies or tokens. The Upright skill file already says it must never contain them.
- Amanda shared Upright access with another person so they could view reports, and offered access to teams (AMANDA). **That is permission to look. It is not approval to automate**, and no team artifact uses those credentials.
- A live session must be signed in by a person at Goodwill (WICKS). Automation may reuse that session only:
  - on an approved runner
  - for the duration of one run
  - with session data kept on that runner
- Login pages, MFA, CAPTCHA or access denial stop the run with `needs_human`. Nothing is bypassed (REQ-ING-03, REQ-ING-05).

## 3. Provider permission

- Upright restricted Goodwill's API key (AMANDA). Automating its web portal may also fall under its terms.
- Live browser automation of any provider needs **both** that provider's permission and Goodwill's.
- The nine-source register (`planning/source-register.md`) lists acquisition hypotheses only. None has a confirmed owner or permission.

## 4. Browser runtime

The browser runner is separate from any web hosting: it needs a machine that can run Chromium. A production runner requires:
- **Host:** a Goodwill-managed workstation or an approved VM, with a named owner.
- **Network:** allowlisted hosts only, per skill.
- **Limits:** per-step and total timeouts (the replica skill uses 12 s per step and 60 s total), plus a kill switch.
- **Verification:** downloads checked by checksum, period and headers before handoff (`acquisition/intake.py`).
- **Drift:** a changed page stops the run. Repairs are reviewed and versioned; a model never "heals" the flow silently.
- **Logs:** no secrets, and no customer data beyond what the retention policy (§7) allows.

## 5. Microsoft identity and tenant

Any SharePoint, Graph, Power BI or Copilot integration needs:
- tenant administrator approval
- an Entra ID app registration with least-privilege permissions
- compliance with conditional access
- a named owner and a support path

Role-based views in the demo are presentation only, not access control. Production access is enforced by Entra ID groups and by per-store or per-source scope checks in the service or database (APP-04), never by a prompt.

## 6. Where data would flow for each AI or automation path

| Path | Data it would see | Weekend | Production gate |
| --- | --- | --- | --- |
| Deterministic replay | Portal pages, locally; no model | P0, replica only | Provider and Goodwill approval; approved runner |
| Copilot (Goodwill tenant) | Tool results inside the tenant | Not used: no tenant access | Goodwill IT approval, licensing, APP-07 validation |
| Jev (TypeSafe, external) | Portal page structure, which may include order or customer data | Optional, synthetic replica only, only if access exists | Goodwill IT plus provider approval, and data-processing terms. Treat as not compatible with the Copilot-only policy until approved. |
| Other LLM (demo assistant) | Synthetic metric results only | Optional and labelled | Not permitted on real data (Copilot only) |
| Power BI / Excel | Published metrics and source files | Not connected | Reporting owner and IT approval |

## 7. Retention

| Data | Rule | Production decision needed |
| --- | --- | --- |
| Raw source files | Immutable, content-addressed archive; never edited | Retention period and location (finance/records owner) |
| Run, import and audit records | Kept with the archive; no secrets | Retention period |
| AI prompts and tool calls | Audited when an assistant exists | Retention under Goodwill policy; none on real data now |
| Synthetic weekend data | Disposable | None |

## 8. Rollback and safe failure

- **Acquisition:** skills are versioned. On drift, stop, then roll back to the previous skill version or fall back to manual upload.
- **Data:**
  - Only reconciled runs publish. A failed or unreconciled batch keeps the last good version with a visible warning.
  - Corrections are versioned upserts, and any run can be reprocessed from the immutable archive.
- **Reporting:** during a pilot, today's manual Excel → Sonia → Power BI path keeps running in parallel (PLAN §11). Rolling back means turning the automation off.
- **AI:** read-only. Removing tool access cannot affect reports.

## 9. Live-access gate register

Every live route is **not approved**.

| Route | Approvers needed | Evidence needed before a pilot |
| --- | --- | --- |
| Live Upright browser automation | Goodwill IT, Upright Labs, process owner | Provider permission or terms review; runner and session policy; named operator account; parallel-run plan |
| Live Cash Monkey export | Goodwill IT, Cash Monkey owner | Export method; access scope |
| Email or folder intake (for example the Books statement) | Goodwill IT | Mailbox or SharePoint scope; retention |
| Power BI or Excel connection | Goodwill reporting owner, IT | Dataset ownership; refresh path; Sonia's workbook validated (OQ-03) |
| Copilot integration | Goodwill IT/security | APP-07 tenant and permission validation plan (OQ-08) |
| Jev or any external model on real data | Goodwill IT/security; provider | Data-flow review; processing terms |
| Business Central import or posting | Finance/accounting, IT | Workbook parity, test environment and format (OQ-06, REL-02) |
| Real Goodwill data in this repository | Goodwill and the team lead | Data-handling agreement. Not allowed this weekend (BRIEF: real data only in the Sprint Lab phase). |
