# ENG-04 — independent QA preflight

Historical preflight at b329c0f. Superseded by RESULT.md (610035e).

Operator: Codex assisting Jack mc. Branch: `jack-mc/eng-04-preflight`.
Base: `b329c0f` (main). Scope: this report only; no claim posted externally.
Source basis: repository ENG-04 packet, team assignments, PLAN §§5/7/8/9.
The actual Drive document and current issue comments have not been verified.
No unattended runner or paid services were started.

## Dependency evidence

- Latest `git pull --ff-only`: already up to date.
- GOV-03 (#15): user reports completion; accepted commit/contracts are not present
  in main. GitHub connector lookup returned 404. Completion remains unverified.
- DAT-01 (#25): no accepted result/verification artifact found in main's reports.
- ENG-01 (#33): no accepted scaffold result or integrated application manifest found.
- GOV-01/GOV-02 documents exist on fetched remote task branches; those branches
  are not proof of GOV-03 acceptance and were not merged into this checkout.
- Only `contracts/sources/acquisition-classes.md` is present under contracts.
- QA tests/fixture lane mapping and required-versus-deferred export decision
  must be recorded before implementation.

## Acceptance scenarios to implement once dependencies are accepted

| Scenario | Independent expectation and evidence |
|---|---|
| Exact artifact continuity | Download checksum equals immutable imported raw bytes; preserve file/run/batch IDs. |
| Inclusive and alternate dates | Source rows and published period match requested dates and agreed timezone. |
| Financial arithmetic | Item sales minus refunds, excluding shipping/tax/fees; use separately derived cent-exact controls. |
| Same-file replay | Second import adds no transactions and changes no totals. |
| Overlapping files | Existing business keys remain unique; only new eligible rows affect totals. |
| Corrections | Apply frozen correction policy; retain original and correction lineage. |
| Missing coverage | Missing input is unavailable/partial, never a fabricated zero. |
| Buyer/store keys | Marketplace buyer namespaces remain separate; store mappings follow frozen contract. |
| Malformed/wrong-period input | Fail explicitly without publishing corrupt data; keep last-good results with warning. |
| Reconciliation | Independent source-row sums agree with curated and API totals; exceptions remain visible. |
| Dashboard | Selected period, values, freshness, coverage and drilldown agree with verified API/source evidence. |
| Seeded defects | Wrong refund formula, false coverage and duplicate-count defects cause test failures. |
| Export | Test only according to the recorded P0/P1 decision; no silent waiver of issue criteria. |

## Existing checks, distinguished from ENG-04 completion

Earlier in this session, at this same base commit, actual commands passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s acquisition/tests -p 'test_*.py'`: 23 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s goodwill/synthetic-data -p 'test_*.py'`: 10 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s 'data ingestion/tests' -p 'test_*.py'`: 9 tests with localhost permission.

These existing author-written component/fixture tests are not an independent
ENG-04 ledger, importer acceptance, browser demo or dashboard verification.
They were not rerun during this preflight because the base code has not changed.

## Exact next handoff

Provide the GOV-03 accepted commit/PR and contract version, DAT-01 acceptance
evidence and ENG-01 scaffold commit/development commands. Confirm QA lane mapping
and export scope. Recheck issue claims/comments before implementing. Full ENG-04
and REL-01 are not complete; no push, merge, deployment or external claim occurred.
