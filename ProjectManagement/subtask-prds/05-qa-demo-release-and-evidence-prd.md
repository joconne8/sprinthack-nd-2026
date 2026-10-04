# PRD 05: QA, Demo, Release, and Evidence

## Primary source basis — Drive-led
- [Goodwill — Three-Phase Solution and Overnight Agent Plan](https://drive.google.com/file/d/1RffkmafbqbMEs7o_lNaTvIRL3hW9paai/view?usp=drivesdk)
- [michael-wicks-plan.md](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view?usp=drivesdk)
- [goodwill-track-brief-v2.md](https://drive.google.com/file/d/1o0QBoew17f7IgEEHweBoe-VLQFGDEatg/view?usp=drivesdk)

Relevant plan sections: §8 AI engineering practices for overnight work; §9 Synthetic data and realistic coverage.

The three-phase plan §8 is the main engineering source: passing vertical slice before handoff, 3–4 isolated lanes, frozen contracts, independent expected totals, actual runner, two repair attempts, budgets/deadlines, per-task evidence and human morning integration. Mentor advice is not unattended production authority.

## Source precedence
Current user decisions govern. Primary evidence is the Google Drive stakeholder/mentor material; the Goodwill Three-Phase Solution and Overnight Agent Plan is the implementation synthesis. This card operationalizes those sources. Older goodwill/PRD.md and planning/agentic-build-plan.md are legacy implementation background, NOT governing requirements or automatic scope limits. Preserve corrections in the three-phase plan where earlier source notes contain unsupported technical claims. Freeze new scope/contracts through GOV-02/GOV-03.


## Status

Proposed P0 workstream PRD. This workstream protects the presentation from unverified claims and last-minute breakage.

## Problem

A hackathon demo can fail even when individual pieces work: data may not load from a clean state, screenshots may be stale, feature claims may exceed what runs, or a live presentation may hit an avoidable failure. The team needs a repeatable regression and evidence packet.

## Goal

Create and run the end-to-end demo regression, maintain the evidence trail, prepare truthful pitch language, verify deployment/access, record a fallback, and freeze/submission materials before the event deadline.

## Users

- Team lead and presenter
- Integrator
- Human reviewers
- Judges watching the final demo

## In scope

- Clean-start demo regression
- P0 acquisition path with actual downloaded artifact
- Manual upload fallback
- Accepted P0 dashboard view; richer/four-view dashboard only if P1 implemented
- Duplicate import test
- Malformed row/rejected row test
- Missing/partial data test
- Source drilldown/reconciliation test
- Export test if implemented
- Second-device access check
- Backup recording
- Pitch disclosures
- Submission checklist

## Out of scope

- Adding new features after freeze
- Unattended production deployment
- Purchasing/upgrading hosting or AI plans
- Claims of real integrations or ROI without evidence
- Hiding broken or incomplete features

## Functional requirements

| ID | Requirement | Acceptance test |
| --- | --- | --- |
| QA-01 | Clean-start workflow runs end to end. | From no local app state, user can complete the intended demo path. |
| QA-02 | Core data-quality tests are visible. | Duplicate import, malformed row, and unknown store are demonstrated or logged. |
| QA-03 | Metrics match expected results. | Displayed values reconcile to expected-results ledger and source rows. |
| QA-04 | Failure mode is safe. | Missing report, expired session, or unsupported source stops with a visible error. |
| QA-05 | Deployment or preview works on another device. | Second laptop/browser can access and run the demo path. |
| QA-06 | Backup recording exists. | Recording shows the known-good path and disclosures. |
| QA-07 | Pitch script matches working software. | Every claim in the script maps to a verified feature or is stated as roadmap. |
| QA-08 | Freeze is respected. | After feature stop, only verified bug fixes and submission tasks occur. |

## Regression script

1. Open the app from a clean state.
2. Show synthetic/prototype labeling.
3. Run simulated acquisition or use manual synthetic upload fallback.
4. Verify import batch accepted/rejected counts.
5. Show daily revenue and source drilldown.
6. Show daily customer counts and no cross-platform unique claim.
7. Show listings per store per day.
8. Show backlog snapshot and completeness state.
9. Re-import same file and confirm totals do not double.
10. Trigger one failure or malformed input and show safe handling.
11. Export or show source-linked summary, if implemented.
12. Close with production gates and roadmap.

## Evidence packet

```text
repo commit or version
preview/deploy URL
known-good demo data files
expected-results ledger
regression run notes
screenshots or recording
failed/partial feature list
pitch script
submission receipt or checklist
```

## Dependencies

- PRD 01 P0 acquisition path (manual upload is fallback, not equivalent proof)
- PRD 02 pipeline outputs
- PRD 03 dashboard
- PRD 04 only if AI explanation is included
- Confirmed event submission requirements

## Risks

| Risk | Mitigation |
| --- | --- |
| Live demo failure. | Backup recording and manual upload fallback. |
| Presenter overclaims. | Pitch script tied to evidence packet and reviewed against non-goals. |
| Last-minute feature additions destabilize app. | Feature stop and cut list. |
| Submission missed or wrong artifact submitted. | Submission checklist and receipt capture. |

## Evidence required for Done

- Regression pass/fail record
- Known-good recording
- Deployment/preview proof from another browser/device
- Final pitch script with disclosures
- Submission assets and receipt, when available

## Cut order if behind

1. Generic recorder
2. Chatbot or AI explanation
3. Second source beyond the minimum
4. Business Central mapping preview
5. Extra charts or polish
6. Keep validation, reconciliation, synthetic labels, and safe failure intact
