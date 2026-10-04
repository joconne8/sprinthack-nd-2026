# PRD 01: Report Acquisition and Upright Replica

## Status

Proposed P0 workstream PRD. This is the demo differentiator from the Drive plan.

## Primary source basis — Drive-led
- [Goodwill — Three-Phase Solution and Overnight Agent Plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk)
- [Amanda Baumer Goodwill Meeting.md](https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view?usp=drivesdk)
- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk)
- [Jack explanation.md](https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view?usp=drivesdk)
- [Amanda2.0](https://docs.google.com/document/d/1yveSPTDJ4PUVi1MjMvCP6ovVtyVy-M7UGOeDdDngz7g/edit?usp=drivesdk)

Relevant plan sections: §4 Reliable report acquisition; §7 Weekend P0/P1/P2.

Amanda reports restricted Upright API access, repeated same-report/date-only work, a 30–45-minute estimate and a preference for automated delivery. Wicks recommends grouping acquisition classes and a real-DOM screenshot-based replica. The plan separates authorized replay, optional Jev and deferred recorder.

## Source precedence
Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.


## Problem

Amanda's operational pain starts upstream of the dashboard: someone repeatedly retrieves reports from separate systems. A dashboard alone does not solve this if the data still arrives manually, late, inconsistently, or without evidence.

## Goal

Build a safe, synthetic, Upright-style report journey that proves the team's acquisition pattern: select a report and date range, generate/download a synthetic CSV, verify the file, and hand it into the import pipeline with lineage and failure handling.

## Users

- Operator or manager who currently pulls reports
- Demo presenter showing the end-to-end story
- Data pipeline owner receiving source packages
- Reviewer verifying this is a replica and not a live vendor integration

## In scope

- Inspect supplied screenshots or slides before building the replica
- Functional HTML/DOM report page, not a static image
- Clear simulated/synthetic labels
- Paid-orders report path with start date, end date, generate, ready/loading, and download states
- Synthetic CSV generation based on selected dates
- Deterministic Playwright or equivalent replay against the replica
- Failure modes: delayed generation, expired session, missing report, changed label, unsupported date
- File verification: headers, date coverage, row count, checksum/fingerprint, synthetic flag
- Handoff to data pipeline import path

## Out of scope

- Real Upright login or credentials
- Production browser automation
- API claims for Upright
- Vendor restriction bypass
- A universal macro recorder
- Jev production integration
- Nine source integrations

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| ACQ-01 | Replica uses actual supplied screenshots/slides as reference. | Notes identify the inspected source material and visible controls used. |
| ACQ-02 | User can choose paid-orders report and date range. | Test chooses two different date ranges and sees different synthetic file coverage. |
| ACQ-03 | Generate flow has observable pending and ready states. | Test waits for ready state and fails on timeout. |
| ACQ-04 | Downloaded file is a real CSV artifact. | File exists, parses, and contains expected synthetic headers and rows. |
| ACQ-05 | Replay is deterministic by default. | Script uses known DOM selectors/labels and assertions, not model-only guesswork. |
| ACQ-06 | Wrong page, missing label, expired session, or unsupported report stops visibly. | Negative tests return human-actionable errors and do not produce fake success. |
| ACQ-07 | Successful acquisition creates a source package for import. | Package includes source, report type, requested period, capture time, checksum, and synthetic flag. |
| ACQ-08 | Repeating the same acquisition does not double imported totals. | Same generated file or same logical file fingerprints as duplicate downstream. |

## Suggested user flow

1. Open the clearly labeled Upright-style simulated portal.
2. Select Reports.
3. Select Paid orders.
4. Enter start and end dates.
5. Generate the report.
6. Wait until ready.
7. Download the CSV.
8. Verify it through the acquisition script.
9. Import through the normal data pipeline.
10. Show the dashboard update and evidence trail.

## Data contract output

Each successful run should produce:

```text
source_package_id
source_name = upright_replica
report_type = paid_orders
requested_start_date
requested_end_date
generated_at
file_name
file_checksum
row_count
coverage_start_date
coverage_end_date
synthetic = true
replay_version
status = success | failed
error_category, if failed
```

## Dependencies

- PRD 00 accepted scope and contracts
- Synthetic sales fixture convention
- Data pipeline import endpoint or local intake folder
- One owner for browser tests and one reviewer for truthfulness/disclosures

## Risks

| Risk | Mitigation |
| --- | --- |
| Replica gets mistaken for a live integration. | Persistent simulated labels in UI, file, README, and demo script. |
| Screenshot-driven UI invents controls that were not in source material. | Inspect and record reference material before implementation. |
| Replay clicks Download but file is wrong. | Validate file content, headers, dates, row count, and checksum. |
| Browser flow breaks under small DOM changes. | Include changed-label or missing-element negative tests. |
| Jev becomes a distraction. | Deterministic replay is P0; model-assisted decisioning is P2 unless access and time are confirmed. |

## Evidence required for Done

- Screenshot or recording of the simulated portal
- Downloaded synthetic CSV artifact
- Test result for successful acquisition
- Test result for at least one failure mode
- Import evidence showing the file entered the normal pipeline
- Disclosure text used in the demo

## Demo talking point

"This is not live Upright. It is a faithful synthetic replica that lets us prove the operating pattern safely: a report is requested, verified, imported, reconciled, and shown with source evidence."
