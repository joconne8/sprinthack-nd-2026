# E-APP evidence review checklist

For the human reviewer (proposed: Jack mc for independent acceptance, Jack OC for integration).
A child is reviewable only when every applicable box can be checked from artifacts in
`reports/<TASK-ID>/` plus the commit. Agent summaries, closed issues or screenshots alone are not enough.

## Every APP child

- [ ] `reports/<TASK-ID>/RESULT.md` states READY_FOR_REVIEW or BLOCKED (never DONE). It also lists branch, base and head commits.
- [ ] Each hard dependency's accepted commit is an ancestor of the task's head commit (`git merge-base --is-ancestor <sha> <head>`).
- [ ] The diff touches only the mapped lane plus `reports/<TASK-ID>/`. No contracts, migrations, lockfiles, app shell or routes unless Jack OC approved it.
- [ ] `verification.json` lists commands that actually ran, with logs. Tests not run are listed as not run.
- [ ] Expected values come from QA or an independent derivation, not from the formula under test.
- [ ] A synthetic label is visible on every view and export.
- [ ] No CSV `net_sales` column is read or displayed (see interfaces-and-blockers B1).
- [ ] No client-side financial arithmetic. Displayed numbers are the API's values, unchanged.
- [ ] A failing API shows an error state. There is no silent mock fallback in the demo build.
- [ ] Requirement IDs are mapped (PLAN §6/§7, DASH-xx, AI-xx).

## APP-01 — operations intake/status (P0)

- [ ] Readiness, report name, period and next action are visible without opening logs.
- [ ] Simulated acquisition, failed import, stale publication and source-not-connected are visibly distinct (screenshot each).
- [ ] Acquisition success and import/publication state are shown separately. A downloaded file is not shown as published.
- [ ] Email delivery appears as a gated capability; no message is sent.
- [ ] Owner/assignee wording fits Amanda or her assistant. There is no reference to the departed e-commerce manager.
- [ ] Contract tests run against the frozen fixtures, plus one walkthrough against the real local endpoint.
- [ ] Loading, empty, error and keyboard/accessibility cases are tested.

## APP-02 — leadership pulse + KPI availability (P0)

- [ ] For at least one filter set, API value = card value, recorded in `api-to-card-comparisons.md` with the request and response.
- [ ] Changing date/store/platform filters changes every applicable card consistently.
- [ ] Each card shows definition, period, coverage, freshness and reconciliation state.
- [ ] Unavailable KPIs (labor productivity, margin, sell-through, YoY, survey) show the reason. No number, estimate or red/green.
- [ ] One displayed value traces to the acquired replica file (checksum matches its manifest).
- [ ] Responsive layout (≈390px) and negative states are tested.

## APP-03 — source-row drilldown (P0) / export (P1)

- [ ] For one P0 metric, the sum of drilled accepted rows equals the displayed value exactly. The arithmetic is shown in `drilldown-reconciliation.md`.
- [ ] Accepted + quarantined rows reconcile to the source file total. The file checksum matches the acquisition manifest.
- [ ] Each row links to source file, source row number and import batch.
- [ ] If export is built: values, period, currency, definitions and coverage match the UI. Cells starting with `= + - @` (or tab/CR) are neutralized, with a test.
- [ ] No Business Central import or posting claim. Export does not block P0.

## APP-04 to APP-07 (P1 stretch / P2 pilot), only after P0 is green and approved

- [ ] APP-04: tool outputs equal the deterministic API. Cross-scope access is rejected server-side (test proves the prompt is not the control). Errors return no fallback value.
- [ ] APP-05: an approved model route exists, or the interaction is labeled scripted. Every number in an answer matches a tool result. Missing labor returns unavailable. Observations are not presented as causes.
- [ ] APP-06: the evaluator is not APP-05's author. Injected instructions in report fields cause no writes or network calls. A numerical mismatch fails the evaluation.
- [ ] APP-07: design documents only. Teams styling is not called a Teams integration. "Copilot-ready" is not called "connected". A named Goodwill IT approver is required.
