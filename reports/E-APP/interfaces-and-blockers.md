# E-APP interfaces and blockers

Base commit `15fa25ad31f1720320dbb4b9fe073796436e2dce`, refreshed against `b329c0f` plus the unmerged
GOV-01/GOV-02 branch `jackoc/GOV-01-requirements-map`. Everything marked **proposal** is input for
Jack OC to accept, change or reject through GOV-02/GOV-03. None of it is a frozen contract, and APP work must
not code against it until GOV-03 freezes the real version.

## 1. Blockers and hazards found

### B1 — `net_sales` means two different things in the two Upright datasets (financial hazard)

Checked with `reports/E-APP/netcheck.awk` (gawk, exact integer-cent comparison):

| File | Rows | `net_sales` = gross − refund | `net_sales` = gross + shipping − refund |
|---|---|---|---|
| `goodwill/synthetic-data/02_upright_paid_order_items_aug2026.csv` (PR #1 fixture) | 650 | 55 (only where shipping = 0) | **650** |
| `data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv` (PR #45 replica) | 128 | **128** | 0 |

The approved demo convention (AGENTS.md, PLAN §5) is **item sales − refunds, excluding shipping, tax
and fees**. Only the replica's column matches it. The fixture column includes shipping, matching the older
README convention that PLAN §5 explicitly superseded.

- **UI rule (applies to all APP tasks):** never render a source CSV's `net_sales` column. Demo net
  sales are displayed only from Peyton's DAT-06 API.
- **Decision request → Jack OC / Peyton (GOV-03, DAT-03):** record in the contract that the fixture's
  `net_sales` column is ignored or renamed (e.g. `source_net_incl_shipping`). Otherwise a parser could pick it up by name.
- **Independent check for Jack mc (ENG-04):** expected demo net sales should be derived from
  `gross_sales − refund_amount`, never from the `net_sales` column.
- **Refresh:** the GOV-02 draft (`planning/metric-dictionary.md`, `M-DEMO-NET-SALES`, in review) adopts the
  same convention. A search of it and `planning/scope.md` found no mention of the fixture's
  `net_sales` column, so this request still stands for GOV-03.

### B2 — two candidate P0 datasets with different grain, dates and timezone

| Property | PR #1 fixture (02) | PR #45 replica output |
|---|---|---|
| Grain | Named "paid order items"; has `item_id` | Explicit `grain` column: "one row per paid order" |
| Dates | 650 rows, all 2026-08 | 2026-09-30 sample; replay accepts any requested range |
| Timezone | `paid_at` carries −04:00; all 24 stores in `10_stores.csv` are `America/Indiana/Indianapolis` | Manifest `reporting_timezone: America/Los_Angeles` |
| Manifest | `goodwill/synthetic-data/manifest.json` | `schema_version: replica-v1`, per-file manifest with checksum |

APP-02's acceptance test requires tracing a displayed metric **to the acquired file**. That only works if
the P0 slice imports the replica's output, not the August fixture. **Decision request → Jack OC (GOV-03):**
(a) which dataset feeds the P0 vertical slice, (b) the single reporting timezone. Day-boundary filters
in the UI depend on (b). The Los Angeles value looks like a placeholder for a South Bend–area organization.
That is my inference, so confirm it with Hugh before changing anything.

**Refresh:** GOV-02 (in review) proposes **America/New_York** "until Goodwill confirms another convention"
(`planning/scope.md`; GOV-01 OQ-05). The fixture's `America/Indiana/Indianapolis` matches that offset.
The replica's `America/Los_Angeles` does **not**. If GOV-02 is accepted as written, Hugh's replica manifest
needs to change, or GOV-03 needs to record the conversion. GOV-02's scope makes the P0 slice
replica → acquired file, with DAT-01 validating the fixtures separately. That answers (a) in principle,
pending acceptance.

### B3 — no scaffold, runtime or contracts exist

No `apps/`, frontend manifest or runtime guide is on any branch. The only `contracts/` content is Hugh's
ING-05 draft. The only Node manifest on main is `data ingestion/package.json`, which belongs to the replica. **Decision request → Jack OC (ENG-01):**
choose one baseline (PLAN §3 default: TypeScript React/Vite + Node API; or the separate Replit foundation)
and map the proposed APP lanes (`apps/dashboard/src/{operations,metrics,provenance}/`) onto it.

### B4 — ENG-04's demo sequence includes export, but APP-03 export is P1

This is already flagged in TEAM_ASSIGNMENTS. **Decision request → Jack OC:** record whether export is deferred
or required before QA acceptance. Until then, APP-03 treats export as P1 and does not let it block P0.

### B5 — APP-05/APP-06 reviewer independence

See `workstream-readiness.md`. **Decision request → Jack OC:** designate a different APP-06 evaluator.

### B6 — GitHub issue comments were not readable from this session

The repo is private, `gh` is not installed and the unauthenticated API returned 404. Any claims or acceptance posted only as
GitHub comments were not seen. Someone with access must recheck #6, #15, #32, #33, #34 and #38 before APP work starts.

## 2. What each P0 child needs from upstream, and what exists today

### APP-01 operations intake/status ← ING (Hugh), DAT-02/DAT-08 (Peyton), ING-05 (Hugh)

| UI needs | Exists today? | Source |
|---|---|---|
| Report/source identity, requested start/end dates, timezone | Yes, in the replica manifest (`source_name`, `report_type`, `requested_*_date`, `reporting_timezone`) | PR #45 |
| Acquisition state and failure reason | Partly. Replica job states are `pending` / `ready` / `failed` with `error_category` (e.g. `missing_report`). Session-expired is a test mode. | PR #45 `server.py` |
| File ready + checksum + row count + synthetic flag + replay version | Yes (`file_checksum`, `row_count`, `synthetic`, `replay_version`, `verification`) | PR #45 |
| Coverage of the file | Yes (`coverage_start_date`, `coverage_end_date`) | PR #45 |
| **Expected arrival** per report/period | No. Needs a report schedule/expectation contract. | GOV-03 |
| **Latest successful run** / run history | Replica jobs are in-memory, with no persisted run log. **Refresh:** `acquisition/run_state.py` (draft, ING-04 BLOCKED) records per-run attempts; persistence not checked. | ING-03 / DAT-02 |
| **Retriable vs needs-human** classification | **Refresh: draft exists.** `run_state.py` statuses are `pending · running · succeeded · failed_retriable_exhausted · needs_human · failed_permanent`, plus `owner_role`. Not frozen. | GOV-03 (+ ING-04 P1) |
| **Import status** (imported / duplicate no-op / rejected rows / failed) | No | DAT-02–DAT-05 |
| **Publication / stale last-good** | No | DAT-08 |
| **Sources not connected** (the other sources) | **Refresh: draft exists.** `planning/source-register.md` (nine sources) and `contracts/sources/acquisition-classes.md` (classes C1–C5 with an "Implemented?" column). Both ING-05 drafts, not accepted. | ING-05 nine-source map |
| Approved folder / manual-upload handoff target | No decision | GOV-03 / GOV-04 |

The replica's `note` field says "No downstream import has occurred". The UI must keep acquisition success
and import/publication state visibly separate. A download is not publication.

### APP-02 leadership pulse + KPI availability ← DAT-06 / DAT-08 (Peyton), GOV-02 (Jack OC)

Required per metric response, **proposal** for the GOV-03 metric API shape:

```text
metric_id, metric_version, definition (formula, grain, exclusions), value (decimal string) | null,
unit/currency, filters_applied {date range, store, platform}, availability (available|partial|unavailable),
availability_reason, coverage {sources expected/received, period}, freshness {published_at, run_id,
is_last_good}, reconciliation_state, synthetic: true, evidence_ref (→ APP-03 drilldown)
```

Rules the UI enforces: `null` renders as "Unavailable — <reason>", never `0` or `$0.00`. There is no red/green
status without an approved target. Values are rendered exactly as returned, with no client-side arithmetic.

### APP-03 source-row drilldown ← DAT-06, DAT-08, APP-02

Needs `metric_run → accepted rows + rejected rows → source_file / source_row / import_batch`. It also needs
reconciliation totals (accepted + quarantined = source total). Nothing exists yet. The PRD 02 lineage
requirements PIPE-01 and PIPE-08 define what Peyton has to expose.

## 3. Proposal — UI state vocabulary (for GOV-03)

APP-01's acceptance test requires distinguishing these states. Proposed values, kept separate per layer so one never masks another:

| Layer | States | Owner of the data |
|---|---|---|
| Source connection | `connected_synthetic` (replica) · `not_connected` | ING-05 |
| Acquisition run | **Refresh:** adopt Hugh's draft `run_state.py` set: `pending` · `running` · `succeeded` · `failed_retriable_exhausted` · `needs_human` · `failed_permanent` (+ `owner_role`). GOV-03 must map the replica job API's `pending/ready/failed` onto it. | ING |
| Import | `not_imported` · `imported` · `duplicate_noop` · `imported_with_rejections` · `failed` | DAT |
| Publication | `published` · `stale_last_good` · `unpublished` | DAT-08 |
| Metric | `available` · `partial` · `unavailable` (+ reason) | DAT-06 |

Every layer also carries `synthetic: true` for the weekend. "Simulated acquisition" is shown as a persistent label, not as a state.

## 4. Proposal — strategic KPI availability matrix (for GOV-02/GOV-03, used by APP-02)

These rows are from BRIEF/PLAN §5. "Available" means available **as a synthetic demo value**, never as approved Goodwill reporting.

| KPI requested | Proposed status | Reason / evidence |
|---|---|---|
| Demo net sales | Available (P0) | Acquired replica file → DAT-06. Convention per PLAN §5; see B1. |
| Customers (distinct buyers) | Partial, P1 | Platform-local only; no cross-platform total (PRD 03 DASH-08). `14_quality_exceptions.csv` lists 8 `missing_buyer` rows. |
| Listings created | P1 if scoped | Inputs exist (`11_listing_events_aug2026.csv`); not in P0 slice |
| Unlisted backlog | P1 if scoped | Needs a complete snapshot (`12_inventory_snapshots_aug2026.csv`); not derivable from sales |
| Revenue / profit per labor hour | **Unavailable** | No labor input in any fixture. The fixture README states no labor productivity is implied. |
| Net margin | **Unavailable** | No approved cost/allocation definition. Shipping and fees are separate ledgers. |
| Sell-through | **Unavailable** | No approved online target. The 50–55% figure is an in-store reference. No cohort/relist policy. |
| Year-over-year growth | **Unavailable** | No prior-year period in fixtures (Aug 2026 plus a Sep 1 increment only) |
| Customer survey measures | **Unavailable** | No survey input. PLAN §5 forbids inventing survey records. |

None of the unavailable rows may show a number, an estimate or a red/green status.
