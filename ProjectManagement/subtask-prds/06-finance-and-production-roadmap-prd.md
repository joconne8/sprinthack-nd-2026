# PRD 06: Finance and Production Roadmap

## Status

Proposed roadmap PRD. This is not a weekend implementation commitment.

## Problem

The weekend demo can show a trustworthy reporting workflow, but production use at Goodwill requires authorized access, Microsoft environment fit, validated accounting rules, data ownership, support processes, and security approval. Finance and Business Central work is high value but high control risk.

## Goal

Define the post-hackathon path from synthetic prototype to a controlled production pilot, especially around existing Microsoft workflows, Power BI/Excel compatibility, Copilot constraints, and Business Central/accounting gates.

## Users

- Goodwill process owner
- Goodwill IT/security owner
- Finance/accounting owner
- Amanda and operational users
- Sprint Lab continuation team
- Implementation/support partner

## In scope

- Production decision gates
- Microsoft/Excel/Power BI reuse assessment
- Source owner and access validation
- Metric dictionary approval
- Data handling and privacy review
- Browser automation approval and fallback policy
- Finance workbook and Business Central mapping validation
- Runbooks, monitoring, support, and incident ownership
- Three-month continuation plan

## Out of scope

- Production deployment during the hackathon
- Live vendor credentials
- Accounting posting without validation
- Autonomous financial decisions
- Universal recorder requirement
- Guaranteed ROI or measured savings before baseline collection

## Production requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| PROD-01 | Confirm authorized acquisition path per source. | Each source has owner, method, terms/permission, and fallback. |
| PROD-02 | Assess existing Microsoft workflow first. | Decision record compares Excel/Power Query/Power BI path against custom storage/app need. |
| PROD-03 | Approve metric definitions. | Metric dictionary signed off by operations/finance owners. |
| PROD-04 | Validate source overlap and system of record. | Revenue, settlement, fee, refund, and inventory sources are not double counted. |
| PROD-05 | Define data/security boundaries. | Data residency, retention, access, PII, credentials, and AI provider rules documented. |
| PROD-06 | Keep acquisition observable. | Run logs capture source, period, checksum, result, failure category, and recovery path. |
| PROD-07 | Validate Business Central path before posting. | Test environment, mapping, dimensions, accounts, periods, duplicate controls, and approvals exist. |
| PROD-08 | Assign maintenance ownership. | Named process, IT, metric/accounting, and support owners exist before unattended operation. |

## Finance and Business Central gates

1. Inventory current allocation workbook inputs, formulas, named ranges, and outputs.
2. Collect example month-end close files and reconciliation expectations.
3. Translate approved rules into versioned code or SQL.
4. Reconcile source reports to workbook-equivalent outputs.
5. Validate account, dimension, vendor/customer, period, and amount mappings.
6. Test import/posting only in an approved test environment.
7. Require human approval before any production posting.
8. Retain posted response and reconciliation evidence.

## Three-month roadmap

| Period | Outcome |
| --- | --- |
| Weeks 1-2 | Validate source inventory, metrics, Microsoft capabilities, policy, owners, and baseline effort. |
| Weeks 3-4 | Implement one approved source in parallel with current process. |
| Weeks 5-6 | Add prioritized source classes with source-specific parsing and reconciliation. |
| Weeks 7-8 | Stabilize daily reporting and compare Excel/Power BI path against custom storage. |
| Weeks 9-10 | Add approved dashboard/metric tools and Copilot proof of concept if tenant permissions allow. |
| Weeks 11-12 | Operational acceptance, runbooks, handover, and close-automation pilot decision. |

## Success metrics to collect

- Active operator minutes per report package
- On-time report arrival rate
- Successful acquisition rate
- Duplicate/reconciliation error rate
- Time to recover from source drift or missing report
- Reporting delay from source availability to useful dashboard
- Support effort and recurring cost
- Operator and leadership acceptance

Do not calculate guaranteed ROI before a measured baseline exists.

## Risks

| Risk | Mitigation |
| --- | --- |
| Browser automation violates provider or Goodwill policy. | Obtain explicit authorization; keep manual/API/email fallback. |
| Custom app duplicates existing Power BI capability. | Assess Microsoft stack before replacing it. |
| Accounting preview is mistaken for validated posting. | Label preview as proposal only; remove post/upload actions until approved. |
| AI conflicts with Copilot-only policy. | Use approved Copilot path or keep AI synthetic/read-only. |
| No owner for failures. | Do not deploy unattended production process until ownership exists. |

## Evidence required for roadmap acceptance

- Source/access inventory
- Approved metric dictionary
- Microsoft workflow assessment
- Data/security review notes
- Finance mapping validation plan
- Runbook outline
- Named owner list
- Pilot go/no-go decision record

## Weekend demo language

"The production path is not to replace Goodwill's current tools blindly. It is to prove the control pattern safely, then validate the real sources, Microsoft environment, metric definitions, and accounting rules with the right Goodwill owners."
