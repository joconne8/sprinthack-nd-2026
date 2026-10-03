# PRD 02: Data Pipeline, Validation, and Reconciliation

## Status

Proposed P0 workstream PRD. This is the trust layer between acquisition and dashboard.

## Problem

Goodwill's reporting challenge is not only collecting files. The system must prevent duplicate imports, reject malformed rows, preserve source evidence, distinguish unknown from zero, and compute repeatable metrics from agreed definitions.

## Goal

Create a deterministic import and reconciliation pipeline that turns synthetic source files into validated normalized records, exceptions, import batches, and metric-ready facts.

## Users

- Dashboard users who need trustworthy numbers
- Operators who need to know whether a report was accepted or rejected
- Reviewers who need source-row evidence
- Future finance/accounting owners who need traceability

## In scope

- Raw source archive or equivalent source package preservation
- Import batch tracking
- Fingerprinting and repeat-import protection
- Validation for required fields, types, dates, amounts, currencies, platform, store, buyer, synthetic flag
- Row-level accepted and rejected outputs
- Unknown-store handling
- Missing buyer handling for customer metrics
- Normalized sale records
- Listing event and inventory snapshot imports if used by the dashboard
- Reconciliation from source rows to metric totals
- Expected-results ledger for fixtures

## Out of scope

- Production data warehouse procurement
- Real Goodwill data
- Real Business Central posting
- Nine complete source parsers
- Generated SQL or unrestricted agent database access
- Guessing missing stores, buyers, costs, or accounting classifications

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| PIPE-01 | Preserve file/run lineage. | Every normalized row links to source file, source row, import batch, and synthetic flag. |
| PIPE-02 | Detect duplicate imports. | Re-uploading the same file leaves totals unchanged and records a duplicate/no-op result. |
| PIPE-03 | Reject malformed rows without hiding them. | Seeded bad rows appear in rejected rows with clear reasons. |
| PIPE-04 | Keep unknown stores visible. | Missing store rows remain in an unknown-store bucket and can be inspected. |
| PIPE-05 | Treat missing buyer IDs as metric-impacting. | Customer metric reports unavailable/partial for affected input, not buyer count by order. |
| PIPE-06 | Normalize money safely. | Amounts parse as decimal or minor-unit values; currency is retained. |
| PIPE-07 | Preserve reporting dates and timestamps. | Date coverage is stored separately from import time. |
| PIPE-08 | Reconcile metric totals to source rows. | Revenue totals exactly match accepted source rows under the metric definition. |
| PIPE-09 | Support repeatable test fixtures. | Expected-results file can be checked independently of dashboard code. |

## Proposed entities

```text
sources
report_definitions
acquisition_runs
source_files
import_batches
rejected_rows
fact_sales
fact_listing_events
fact_inventory_snapshots
metric_definitions
metric_runs
reconciliation_results
exceptions
audit_events
```

A smaller prototype may collapse tables or use in-memory/local storage, but it must preserve the same information.

## Validation rules

- Required headers are present.
- Required IDs are non-empty unless explicitly allowed.
- Dates parse with timezone/period rules from PRD 00.
- Money values are numeric and have currency.
- Synthetic flag is present and true for demo files.
- Source row IDs are unique within a file unless the duplicate policy accepts them as harmless repeats.
- Malformed rows are quarantined with reasons.
- Missing source files are visible as missing coverage.

## Dependencies

- PRD 00 contracts
- PRD 01 source package if the acquisition demo is selected
- Synthetic fixture files and expected totals
- Shared app shell or import command

## Risks

| Risk | Mitigation |
| --- | --- |
| Wrong fixture math passes because code generated both inputs and expected values. | Keep an independently computed expected-results ledger. |
| Duplicate protection accidentally drops corrected files. | Distinguish identical file fingerprints from overlapping or corrected exports. |
| Missing data is treated as zero. | Explicit unavailable/partial states in import and metric outputs. |
| Different metrics use different row filters. | Metric definitions are versioned and referenced in outputs. |

## Evidence required for Done

- Fixture import pass/fail output
- Duplicate import test output
- Malformed row rejection evidence
- Unknown-store evidence
- Expected-results ledger
- Reconciliation output linking at least one displayed metric to source rows

## Handoff to dashboard

The pipeline must expose, directly or through fixtures, these outputs:

```text
import_batches
accepted row counts
rejected row counts and reasons
source coverage by source and period
metric-ready rows
exceptions
source-row drilldown lookup
freshness timestamp
synthetic flag
```
