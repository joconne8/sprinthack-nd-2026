# E-APP workstream readiness

Checked 2026-10-04T01:51Z (2026-10-03 evening, US Eastern) against `origin/main` at
`15fa25ad31f1720320dbb4b9fe073796436e2dce`. This is a dated observation, not live status.

## Refresh against `origin/main` `b329c0f` (fetched ~02:30Z)

New since the first check. **Readiness is unchanged: every APP child is still BLOCKED.**

- **GOV-01** is in review on PR #48 (branch `jackoc/GOV-01-requirements-map`). **GOV-02** was merged into that
  branch via PR #50, **not into main**. Both `RESULT.md` files say READY_FOR_REVIEW. Neither is accepted.
  GOV-03 and ENG-01, the APP-01/02 gates, have not started.
- **Hugh's PR #49 is merged to main.** It contains ING-02–05 drafts: `acquisition/run_state.py`,
  `acquisition/intake.py`, `contracts/sources/acquisition-classes.md` and `planning/source-register.md`.
  Every ING `RESULT.md` says BLOCKED, and the contract file calls itself an ING-05 draft that "must be
  reconciled by the GOV-03 contract owner". These are useful APP-01 inputs but **not frozen contracts**
  (see interfaces-and-blockers §2).
- The statement below that no `contracts/` existed on any branch was true at `15fa25a`. It is now outdated
  only because of that draft file.

## How this was checked

- Read every APP packet's hard dependencies, scope, acceptance tests and file lane.
- Searched `main` and **all five remote branches** for accepted-task evidence. Searched for `reports/GOV-0*`,
  `reports/ENG-0*`, `apps/`, `contracts/` and any acceptance JSON. The only acceptance file found is
  the empty `templates/acceptance.example.json`.
- GitHub issue comments could **not** be read. The repo is private, `gh` is not installed, and the
  unauthenticated API returned 404 for #6, #15, #32, #33, #34 and #38. Someone with access must check for
  claims or acceptance comments posted on GitHub but not committed.

## Result: no APP implementation packet is eligible

Every child is blocked on predecessors that have no accepted commit on any branch.

| Child | Priority | Hard dependencies | Dependency evidence found | Readiness | Proposed lane (unmapped) | Proposed reviewer |
|---|---|---|---|---|---|---|
| [APP-01](https://github.com/joconne8/sprinthack-nd-2026/issues/38) operations intake/status | P0 | GOV-03, ENG-01 | None. No contracts, no app scaffold, no runtime manifest. | **BLOCKED** | `apps/dashboard/src/operations/`, `tests/ui/operations/` | Jack mc (independent acceptance); Jack OC (integration) |
| [APP-02](https://github.com/joconne8/sprinthack-nd-2026/issues/32) leadership pulse + KPI availability | P0 | GOV-03, ENG-01 | None | **BLOCKED** | `apps/dashboard/src/metrics/`, `tests/ui/metrics/` | Jack mc, with independently derived expected values |
| [APP-03](https://github.com/joconne8/sprinthack-nd-2026/issues/34) source-row drilldown (+P1 export) | P0 drilldown / P1 export | DAT-06, DAT-08, APP-02 | None. DAT chain has not started. | **BLOCKED** (two layers deep) | `apps/dashboard/src/provenance/`; `services/exports/`, `tests/exports/` only if export is approved | Jack mc; Peyton confirms lineage semantics |
| [APP-04](https://github.com/joconne8/sprinthack-nd-2026/issues/35) read-only tools | P1 stretch | DAT-06, DAT-08, GOV-04 | None | **BLOCKED**; also needs P0 green | `services/agent-tools/`, `contracts/tools/` (contracts are Jack OC's) | Jack OC (GOV-04 security) + Jack mc |
| [APP-05](https://github.com/joconne8/sprinthack-nd-2026/issues/29) grounded assistant | P1 stretch | APP-04, GOV-04 | None | **BLOCKED**; needs approved model route | `services/assistant/`, `apps/dashboard/src/assistant/` | Jack mc |
| [APP-06](https://github.com/joconne8/sprinthack-nd-2026/issues/31) adversarial evaluation | P1 stretch | APP-04, APP-05, ENG-04 | None | **BLOCKED**; **reviewer-independence conflict** (below) | `tests/assistant-adversarial/` | Must not be APP-05's author |
| [APP-07](https://github.com/joconne8/sprinthack-nd-2026/issues/36) Microsoft Copilot / Power BI | P2 pilot | GOV-04, APP-04 | None | **BLOCKED**; design-only even when unblocked | `planning/microsoft-integration.md`, `contracts/microsoft/` | Jack OC + named Goodwill IT approver |

## Critical path into this lane

Hard dependencies from the TEAM_ASSIGNMENTS register (`A ← B` means A waits for B):

```text
APP-01, APP-02 ← GOV-03 + ENG-01
APP-03         ← APP-02 + DAT-06 + DAT-08
GOV-03 ← GOV-02 ← GOV-01            ENG-01 ← GOV-02 + GOV-04     GOV-04 ← GOV-01 + GOV-02
DAT-08 ← DAT-05 + DAT-06            DAT-06 ← DAT-05 + GOV-03     DAT-05 ← DAT-03 + DAT-04
DAT-04 ← DAT-03                     DAT-03 ← DAT-01 + DAT-02
DAT-02 ← GOV-03 + ENG-01            DAT-01 ← GOV-02
```

APP-01 and APP-02 unblock as soon as GOV-03 and ENG-01 are accepted. They can use approved contract
fixtures until Peyton's API exists. APP-03 is the latest P0 item in the lane: it waits for
the full DAT-02→DAT-08 chain. That makes it the main schedule risk for the P0 demo.

## Changes since TEAM_ASSIGNMENTS.md was written

- **PR #45 is merged** (`15fa25a`). The guide describes it as open and unmerged. The replica
  (`data ingestion/`) is now on main. It is still **not** an accepted ING-01 handoff, because
  GOV-03/ENG-01 acceptance is explicitly not asserted in `reports/ING-01/CLAIM.md`.
- `data ingestion/package.json` is now the only Node manifest on main. It belongs to the replica,
  not to an app scaffold. APP work must not adopt it as the dashboard runtime.

## Reviewer-independence conflict: APP-05 / APP-06

TEAM_ASSIGNMENTS puts both APP-05 (build the assistant) and APP-06 (evaluate that assistant's safety)
under Landon. The guide's own rule is: "If you contributed a feature under review, disclose that and have
Jack OC designate a different independent checker." **Decision request:** Jack OC designates a
different APP-06 evaluator (suggest Jack mc, who owns ENG-04, an APP-06 dependency). The other option
is for Landon to write the attack set and Jack mc to run and judge it. Both tasks are P1 stretch, so
this is not urgent. It should be settled before either one starts.

## What Landon can do before the gates clear

These are allowed before implementation eligibility ("reading packets/preparing questions"):

1. Send the decision requests in `interfaces-and-blockers.md` to Jack OC as GOV-02/GOV-03 input.
2. Ask Jack OC which baseline/scaffold ENG-01 will select. If it is the Replit foundation,
   get read access to see its component conventions before APP-01 starts.
3. Review the draft UI state inventory and KPI availability matrix in `interfaces-and-blockers.md`.
   They become APP-01/APP-02 inputs only once GOV-03 freezes them.
4. Install Python 3.10+ (and Node, if ENG-01 picks a Node stack) on this machine. That makes the
   selector and fixture tests runnable here. Neither is currently installed.
