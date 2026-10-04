# PR #1 fixture review — preparatory evidence

Original preparatory state: BLOCKED. Updated state: READY_FOR_REVIEW under the
later user-authorized combined setup/data implementation.
This fixture review does not independently accept DAT-01 or establish UI
correctness. Importer evidence is separately available in the integration logs.

Tested repository commit: `b329c0fece37c1694b4d84c0c55e609dc931f854`.
Merged PR #1 fixture commit: `ee7291d515a10da51be0ee9e887dfa53b73b5650`.
Current branch: `peyton/jackoc-data-foundation` (renamed from the preparatory branch).

## Checks actually run

The supplied suite ran against a temporary extraction of the tested commit,
including deterministic regeneration there. All 10 tests passed. The user's
fixture files were not regenerated. See `integrity-and-regeneration-logs/fixture-suite.log`.

The separate read-only review does not import generator code. It compares CSV
values with the existing manifest, checks exception coverage across all nine
source files, filters listings by their actual timestamps, and treats inventory
as distinct snapshots. **353 of 354 checks passed.** The failing check is retained
as evidence, not waived. See `integrity-and-regeneration-logs/cross-check.json`.
The initial failing log remains preserved. The combined GOV-03 decision treats
the ledger as root exceptions and verifies explicit propagated shipping links;
`cross-check-final.json` now passes all 354 checks without changing fixtures.
Manifest expectations were generated with the pack; these checks do not replace
an independently approved expected-results ledger from QA.

## Finding: exception ledger excludes propagated shipping attribution gaps

The ledger contains 21 declared exceptions: 8 Upright buyer IDs, 8 ShopGoodwill
store IDs, and 5 jewelry suppliers. Seven additional missing `store_id` values
occur in `04_shipping_osm_pb_easypost_aug2026.csv` at 1-based data rows:

`1816`, `1825`, `2146`, `2367`, `2605`, `2996`, `3442`.

The README says missing store attribution propagates to related records. The
supplied exception test checks only the sales/statement filenames in generator
`FILES`; it excludes shipping files. Thus its passing result and this broader
failure describe different coverage. These shipping gaps may be intentional
propagated exceptions, but consumers need a declared policy for displaying them
without double-counting root exceptions. Preserve them visibly in the importer;
do not assign a guessed store. The fixture owner and contract owner should decide
whether to extend the ledger or document related-row exception lineage.

## Financial conventions

USD amounts recomputed with Decimal; each source is shown separately. No combined
revenue is approved while the source-authority/overlap matrix is unresolved.

| Synthetic source | Gross item sales | Refunds | Demo net sales | Existing source net/payout total |
| --- | ---: | ---: | ---: | ---: |
| ShopGoodwill | 114403.37 | 3141.19 | 111262.18 | 141865.59 (`net_sales`) |
| eBay | 56990.67 | 1475.41 | 55515.26 | 57046.74 (`payout_amount`) |
| Upright | 37021.26 | 864.16 | 36157.10 | 42895.51 (`net_sales`) |

Demo net sales is item sales minus refunds, excluding shipping, tax and fees.
Existing source net/payout columns follow their own formulas. They cannot be
used directly as the proposed `M-DEMO-NET-SALES` value. Missing store records stay
in source totals and an unresolved store bucket; Upright customer coverage is
incomplete because eight buyer IDs are missing. Do not substitute order count.

## Listing and snapshot interpretation

The listing CSV has 3,181 events: 69 in June, 1,669 in July, and 1,443 in August.
An August listing metric must select `listed_at`, not count every file row.
The eBay `relisted` flag does not imply an additional listing-event record.

| Snapshot cutoff | Inventory rows | Unlisted backlog |
| --- | ---: | ---: |
| 2026-08-01T23:59:59-04:00 | 2577 | 832 |
| 2026-08-15T23:59:59-04:00 | 2196 | 757 |
| 2026-08-31T23:59:59-04:00 | 1246 | 765 |

Select one complete snapshot; never sum snapshots as current inventory. These
controls cover the declared fixture universe, not all Goodwill inventory.

## Handoff limitations

- Original source CSVs do not uniformly contain row-level currency/synthetic
  fields. The manifest and sidecars carry pack metadata. GOV-03 must specify how
  the acquired-file contract carries those values; do not invent new headers.
- The portal examples use September 30 and a separate dataset/schema. August
  fixtures are not an approved drop-in adapter for those acquired bytes.
- Expenses, settlements, sales, refunds, listings and snapshots have distinct
  grains. Tests of synthetic joins do not establish real source exclusivity.
- Missing labor, approved cost allocations, cohort definitions and prior-year
  inputs cannot support productivity, margin, sell-through or growth claims.
- At the original preparatory check, GOV-02 scope/metric proposals were read from remote commit
  `38120523f60ff9cc0f888146b9450be5be74f674`; they remain ready for review,
  not accepted or merged prerequisites. GOV-03/ENG-01 handoffs were not found then.
  The later user-authorized combined session now supplies local contracts/runtime
  in `planning/contracts.md` and `planning/development.md`; team review remains.
- The primary Drive plan and current GitHub issue comments returned 404. Local
  source-register/plan/PRD snapshots were read; current remote authority and
  claims could not be verified.
