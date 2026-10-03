# PRD 04: Read-Only AI Interaction and Metric Explanation

## Status

Proposed P1/P2 workstream PRD. Start only after the deterministic acquisition, pipeline, and dashboard path passes.

## Problem

A conversational layer can help users understand metrics, but AI can also overstate certainty, fabricate causes, ignore missing data, or conflict with Goodwill's Copilot-only policy. The prototype must treat AI as a bounded explanatory layer over deterministic results, not as the source of financial truth.

## Goal

If time allows, add one read-only, source-grounded explanation workflow that answers a narrow metric question using approved query results, metric definitions, coverage, and evidence references.

## Users

- Leadership or operations users asking what changed in a selected view
- Presenter showing the future AI-native interaction path
- Reviewer checking that numbers come from deterministic calculations

## In scope

- One or two fixed question patterns, such as "What changed in revenue for this selected date and store?"
- Use existing metric query results, filters, definitions, freshness, and exceptions
- Explain observed contributors from deterministic results
- Cite supporting metric run, source rows, and coverage state
- Admit unavailable data
- Keep all actions read-only
- Label scripted/model-assisted behavior honestly

## Out of scope

- General chatbot
- Generated SQL over unrestricted data
- Production Copilot deployment
- Jev production usage
- Autonomous pricing, staffing, listing, email, or accounting actions
- Causal claims without evidence
- LLM calculation of financial numbers

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| AI-01 | Use deterministic metric results as source of truth. | Numeric values in the answer match dashboard/API values exactly. |
| AI-02 | Include filters and metric definitions. | Answer states period, platform/store scope, formula/version, and unit. |
| AI-03 | Include freshness and coverage caveats. | Missing source or partial data is mentioned when present. |
| AI-04 | Distinguish observation from causation. | Answer says records show X changed; it does not infer unsupported reasons. |
| AI-05 | Fail closed for unsupported questions. | Unsupported metric or missing data returns an honest unavailable answer. |
| AI-06 | Remain read-only. | No writes, postings, emails, browser actions, or data changes are available. |
| AI-07 | Respect synthetic/prototype labels. | Answer explicitly labels synthetic demo data. |

## Example supported answer pattern

Question: "Why is revenue lower for Store S-003 this week?"

Required behavior:

1. Confirm selected period, comparison period, store, platform, and currency.
2. Retrieve current and comparison revenue from the deterministic metric result.
3. Decompose into sale amount and refund amount where available.
4. Check source coverage and rejected rows.
5. Explain observed movements and limitations.
6. Link to source rows or metric evidence.
7. Avoid saying staff performance, pricing, or customer satisfaction caused the change unless supporting data exists.

## Model/provider policy

- Goodwill production AI is subject to approval and may need to go through Microsoft Copilot.
- Demo AI may use synthetic data only and must not imply production approval.
- Jev is a probabilistic structured-decision model; it is not a macro recorder or financial calculator.
- Deterministic code and SQL remain responsible for exact math.

## Dependencies

- PRD 00 metric definitions and policy boundaries
- PRD 02 deterministic metric outputs
- PRD 03 dashboard/filter context
- QA evaluation examples

## Risks

| Risk | Mitigation |
| --- | --- |
| AI invents causes or missing numbers. | Restricted prompt/tool context and evaluation cases for missing data. |
| Users believe demo assistant is Copilot-approved. | Clear synthetic/demo labels and production gate language. |
| Model-generated math diverges from dashboard. | Assistant receives numbers from tested metric queries only. |
| Scope distracts from core demo. | AI remains P1/P2 and starts only after P0 passes. |

## Evidence required for Done

- Fixed evaluation set with supported and unsupported questions
- Output showing numeric agreement with metric results
- Missing-data answer example
- Unsupported-question answer example
- Reviewer confirmation that no write actions are exposed

## Demo talking point

"The assistant is not calculating the money. The system calculates the money deterministically; the assistant explains the selected result, its filters, its source coverage, and its limitations."
