# ENG-04 regression report

Tested commit: `610035e` (main after PR #52), branch `jack-mc/eng-04-preflight`, Python 3.9.6.
Date: 2026-10-04 03:47 UTC. Earlier b329c0f runs are in preflight.md (historical).

| Suite | Command | Result |
|---|---|---|
| Independent acceptance (new) | `python3 -m unittest discover -s tests/acceptance -p 'test_*.py' -v` | 25 run, OK, 2 skipped |
| Full CI discovery | `python3 -m unittest discover -s tests -v` | 61 run, OK, 2 skipped |
| Acquisition | `python3 -m unittest discover -s acquisition/tests -p 'test_*.py'` | 23 run, OK |

## Coverage map (issue checklist → test)

| Requirement | Test |
|---|---|
| Refunds, full refund, decoy shipping/tax/fees/net | `test_refunds_replay_overlap_and_correction` |
| Duplicates (replay, in-file, overlap) | same + `test_exact_duplicate_within_file_counts_once`, `test_replay_changes_nothing` |
| Corrections (refused unless approved) | `test_refunds_replay_overlap_and_correction` |
| Dates: inclusive first/last second, alternate ranges, outside period | `test_inclusive_edges_and_alternate_dates`, `test_row_outside_requested_period_blocks_file` |
| Missing days / other-timezone partial coverage | `test_missing_day_is_unknown_not_zero`, `test_other_timezone_report_only_partially_covers_day` |
| Missing sources | `test_missing_sources_are_unavailable` |
| Buyer namespaces / store keys | `test_buyer_namespaces_and_store_keys`, `test_missing_buyer_keeps_sales_but_hides_customers` |
| Malformed money / last-good | `test_invalid_rows_fail_without_publishing`, `test_invalid_money_keeps_last_good` |
| Acquire→import→reconcile→API→evidence | `test_demo_sequence.py` (actual replica portal over HTTP) |
| Dashboard | skipped: BLOCKED, no UI in main |
| Export | skipped: deferred from P0 |

## Seeded defects (mutation evidence)

Each defect is injected with `unittest.mock` for one test only. The control test shows the
same checks pass on the unmodified code.

| Defect | Caught by |
|---|---|
| Refunds ignored | core ledger |
| Shipping + tax + fees added to item sales | core ledger |
| Source `net_sales` field used as revenue | core ledger |
| Unstable business key (duplicates counted) | core ledger |
| Coverage forced to complete | coverage gap |
| Missing/unmapped store silently mapped | buyer/store keys |

Fixture integrity is not end-to-end success. The DAT-01 fixture tests prove fixtures only.
The demo sequence above proves importer/API behavior on real downloaded bytes. The UI is unproven.
