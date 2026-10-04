# Contracts v1 (GOV-03)

Task: GOV-03 / issue #15
State: READY_FOR_REVIEW
Version: contracts `1.0.0`. Built on `GOV-02-scope-v0.1` and `GOV-02-metrics-v0.1`, which the user acting as Jack OC accepted in session on 2026-10-04.
Owner: Jack OC owns `contracts/` and any types or clients generated from it (ENG-01).

Every lane builds against these shapes instead of inventing fields. The schemas are in
[`contracts/v1/goodwill-contracts.schema.json`](../contracts/v1/goodwill-contracts.schema.json).
Validate an instance against `#/definitions/<Name>`.

## 1. What is frozen

| File | Purpose |
| --- | --- |
| `contracts/v1/goodwill-contracts.schema.json` | JSON Schema draft-07 bundle: every contract below plus shared types |
| `contracts/v1/expected-reports.json` | Which reports are expected per reporting date (drives coverage) |
| `contracts/v1/examples/valid/` | Shared fixtures: frontend mocks, tool tests and backend contract tests all use these |
| `contracts/v1/examples/invalid/` | Shapes that must be rejected |
| `contracts/tests/validate-contracts.cjs` | Contract checks: `node contracts/tests/validate-contracts.cjs` |

## 2. Who produces what

| Contract | Producer | Consumers | When |
| --- | --- | --- | --- |
| `AcquisitionRun` | ING-02/ING-04 (Hugh) | APP-01, coverage | Every request, success or failure |
| `SourcePackageManifest` | ING-02 runner | ING-03 intake | Only together with delivered bytes |
| `IntakeResult` = `VerifiedSourceFile` or `IntakeRejection` | ING-03 | DAT-02 | After verification; acquisition success is not publication |
| `ImportBatch` | DAT-02..05 (Peyton) | DAT-08, APP-01, tools | Every import attempt |
| `MetricResult`, `MetricComparison` | DAT-06 | APP-02, APP-04/05 | Displayed and returned unchanged |
| `SupportingRows` | DAT-06 | APP-03 | Drilldown for one metric run |
| `SourceCoverage` | DAT-08 using ING run data | APP-01, `M-SOURCE-COVERAGE` | Per selected period |
| `ExpectedReports` | Jack OC (config) | DAT-08 | Changes by PR only |
| `ErrorResponse` | Every API and tool | All clients | Every non-2xx response |
| `ToolRequest`, `RerunProposal` | APP-04 (P1) | APP-05 | Read-only tools; reruns are proposals only |

## 3. State layers: never collapse them

| Layer | States |
| --- | --- |
| Source connection | `connected_synthetic`, `not_connected` |
| Acquisition run | `pending`, `running`, `succeeded`, `failed_retriable_exhausted`, `needs_human`, `failed_permanent` |
| Intake | `acquired_verified`, `rejected` |
| Import | `not_submitted`, `submitted`, `imported`, `duplicate_noop`, `imported_with_rejections`, `failed` |
| Publication | `published`, `stale_last_good`, `unpublished` |
| Metric availability | `available`, `partial`, `unavailable`, each non-available state with a reason |

A downloaded file is not a published metric. The operations view shows each layer separately.

Acquisition failure types come in three classes:
- **Retriable** (`timeout`, `download_failed`, `report_unavailable`): bounded retries, then `failed_retriable_exhausted`.
- **Needs a human** (`expired_session`, `mfa`, `captcha`, `access_denied`, `label_changed`, `wrong_page`): never retried.
- **Permanent** (`host_not_allowed`, `bad_params`).

Every failed run names an `owner_role`, which is a role and never a person. The former e-commerce manager has left (REQ-OPS-01).

## 4. Frozen conventions

- **Synthetic only.** Every record carries `synthetic: true` as a constant. Real data needs contracts v2 plus Goodwill approval (REQ-SEC-01).
- **Timezone.** Every report is requested and labelled in `America/New_York`, and `reporting_date` is the local date in that zone. Intake rejects any other zone with `timezone_mismatch`. Nothing converts silently.
- **Money.**
  - Amounts are decimal strings with exactly two fraction digits, such as `"74.50"`, and never JSON numbers.
  - v1 supports USD only, and currencies are never mixed.
  - All arithmetic is done in integer cents.
- **Missing is never zero.**
  - `unavailable` means `value: null` plus a reason.
  - `partial` means a value plus a reason and a detail.
  - v1 has no target or red/green field, so no client can invent one.
- **Dates.** `Date` is `YYYY-MM-DD` in the reporting zone. `DateTime` is ISO 8601 with `Z` or an explicit offset.
- **Identity.** `source_file_id` is the SHA-256 of the exact bytes.

## 5. Demo net sales (`M-DEMO-NET-SALES`) column mapping

| Source / report | Item sales | Refunds | Never use for this metric |
| --- | --- | --- | --- |
| `upright_replica` / `paid_orders` (P0) | `gross_sales` | `refund_amount` | `net_sales`, `shipping_collected`, `sales_tax`, `marketplace_fee` |
| `cash_monkey_replica` / `orders` (P1) | `item_revenue` | `refund_amount` | `payout_amount`, `shipping_revenue`, `payment_fee` |

Never read any source's `net_sales` column. In the replica it means gross minus refund. In the August fixture `02_upright_paid_order_items_aug2026.csv` it includes shipping for all 650 rows (`reports/E-APP/interfaces-and-blockers.md`, B1).

**Refund attribution** (a gap found in the GOV-02 review): a refund counts on the `reporting_date` of the row that carries it. P0 sources put refunds on the order row and have no separate refund date. A later revised export that changes a refund is a correction (§6). It revises the original date and creates a new metric run. Sources with separate refund events, such as the fixture `15_order_lifecycle.csv`, need a v1.x decision before use.

## 6. Idempotency, duplicates, corrections and lineage

- **Delivery key (ING):** file checksum plus requested period gives one handoff per key, matching `submit()` in `acquisition/intake.py`.
- **Import key:** `idempotency_key` = `source_file_id`. The same bytes imported twice produce `duplicate_noop`, and totals stay unchanged (PLAN §2 REQ-CTL-01).
- **Row natural keys:** `paid_order_id` for `upright_replica/paid_orders`, and `unit_id` for `cash_monkey_replica/orders`. If a key repeats inside one file, the later row is rejected as `duplicate_key_in_file`.
- **Corrections** follow `upsert_policy: latest_acquired_wins_with_history`:
  - Identical rows keep their existing version and lineage.
  - Changed rows get a new version from the later file, and previous versions are kept.
  - `counts.replaced_by_correction` reports how many rows were replaced.
- **Lineage** uses `SourceRowRef`: `source_file_id`, `source_row_index`, `source_record_key` and `import_batch_id`.
  - `source_row_index` is the 1-based position of the data record after CSV parsing, with the header not counted.
  - In files without quoted newlines, the "line n" in intake errors equals `source_row_index + 1`.
- **Reconciliation:**
  - `reconciled` means `source_reported = accepted + rejected` for each amount, compared in cents.
  - Unparseable money becomes `null`, which makes the batch `unreconciled`.
  - DAT-08 then blocks publication and keeps the last good version with `stale_last_good`.

## 7. Semantic rules beyond the schema

`validate-contracts.cjs` enforces these rules on every example. Producing lanes should enforce the same rules in their own tests.

- `start_date <= end_date`. Manifest coverage lies inside the requested period, and an empty file has `null` coverage.
- **AcquisitionRun:**
  - A `succeeded` run ends with exactly one `delivered` attempt.
  - A failed run has no delivered attempt, and its `failure_type` equals the last attempt's outcome.
- **ImportBatch:**
  - `accepted + rejected = rows_in_file`.
  - The exception is `duplicate_noop`, which accepts and rejects nothing and counts every row as unchanged.
  - `rejected_rows` has `counts.rejected` entries.
- **MetricResult:**
  - `available` requires complete coverage.
  - `partial` or `missing` coverage lists the missing reports.
  - `stale_last_good` requires a `stale_reason`.
  - Evidence and freshness name the same metric run.
- **SupportingRows:**
  - Each row's `contribution` equals `item_sales - refunds`.
  - The row sums equal the totals.
  - `matches_displayed_value` is true only when they really match.
- **MetricComparison:** `change` is `null` when either side is unavailable.

## 8. API surface

The payload shapes are frozen. The paths are proposals for DAT-06 and ENG-01 to confirm.

| Method and path | Response |
| --- | --- |
| `GET /api/v1/acquisition-runs?start_date&end_date` | `AcquisitionRun[]` |
| `GET /api/v1/coverage?start_date&end_date` | `SourceCoverage` |
| `POST /api/v1/imports` with `{ "source_file_id": ... }` | `ImportBatch` (idempotent) |
| `GET /api/v1/imports/{import_batch_id}` | `ImportBatch` |
| `GET /api/v1/metrics/{metric_id}?start_date&end_date&store_id&platform&source_name` | `MetricResult` |
| `GET /api/v1/metric-runs/{metric_run_id}/rows?limit&offset` | `SupportingRows` |

Errors return `ErrorResponse` with these HTTP statuses:

| HTTP status | Error codes |
| --- | --- |
| 400 | `invalid_request` |
| 404 | `not_found`, `unsupported_metric` |
| 409 | `conflict` |
| 403 | `permission_denied` |
| 503 | `upstream_unavailable` |
| 504 | `timeout` |
| 500 | `internal_error` |

A metric that exists but lacks inputs is not an error. It returns `MetricResult` with `availability: unavailable`.

Clients never substitute example data when the API fails. The examples are for development and tests only.

## 9. Ownership and change policy

- Jack OC owns `contracts/`. Other lanes propose changes through a PR that touches `contracts/`, updates the examples and includes a passing validator run.
- Versioning is semantic. A 1.x release may only add (for example a new optional field). Anything breaking goes in `contracts/v2/`. Producers send `contract_version`, and consumers reject an unknown major version.
- ENG-01 chooses the validator dependency (for example ajv) and the type generator. It also runs `validate-contracts.cjs` in CI. The current runner is a dependency-free subset validator: it refuses unsupported keywords and has self-tests, but it is not a full draft-07 implementation.

## 10. What each lane changes

| Lane | Required change |
| --- | --- |
| Hugh (ING-02/03) | Request reports in `America/New_York`: the replica's `ZONES` list lacks it, and Cash Monkey is forced to UTC. Emit `SourcePackageManifest` from the runner using the translation in `reports/GOV-03/compatibility-notes.md`. Map replica errors `session_expired` → `expired_session` and `missing_report` → `report_unavailable`. Align the intake record to `VerifiedSourceFile`/`IntakeRejection`, and add the `timezone_mismatch` check. |
| Peyton (DAT-01..08) | Produce `ImportBatch`, `MetricResult`, `SupportingRows` and `SourceCoverage`. Use the natural keys, upsert policy and cent arithmetic above. Ignore `net_sales` columns. |
| Landon (APP-01..03) | Use `examples/valid` as development mocks. Show state layers separately. Render unavailable/partial values with their reasons. Do no client-side arithmetic. Show an `ErrorResponse` as an error, never as mock data. |
| Jack mc (ENG-04) | Validate API responses against the schema. Derive expected totals independently from source CSVs (`gross_sales - refund_amount`), not from the examples. |

## 11. Requirement trace

| Requirement | Where the contract enforces it |
| --- | --- |
| REQ-ING-01 | Requested dates, coverage and source identity in `SourcePackageManifest` |
| REQ-ING-03 | `api` is one class among five; nothing assumes a key |
| REQ-ING-05 | `needs_human` states with `owner_role`; `manual_upload` class |
| REQ-DAT-01 | `SourceRowRef` lineage; `SupportingRows` |
| REQ-DAT-02 | Values come from deterministic runs; no model arithmetic |
| REQ-DAT-03 | `null` value plus availability reason; never zero |
| REQ-DAT-04 | Item sales and refunds kept separate; fees, shipping and settlements excluded |
| REQ-DAT-05 | §5 column mapping |
| REQ-KPI-01 | Definition, coverage, freshness and evidence in every `MetricResult` |
| REQ-KPI-02 / REQ-KPI-03 | Roadmap IDs are reported as unavailable; no targets exist |
| REQ-OPS-01 | `owner_role` names a role, never a person |
| REQ-OPS-03 | Source package stands alone with manifest and checksum |
| REQ-SEC-01 | `synthetic: true` constant |
| REQ-AI-01 | Tools are read-only; a rerun is only a proposal awaiting approval |
| REQ-FIN-01 | No posting tool or field exists |

## 12. Known gaps

- The replica's real output fails v1 only on `reporting_timezone` until ING-02 requests `America/New_York`. The check is automated in `validate-contracts.cjs`.
- The API paths are proposals.
- `expected-reports.json` cadences for sources that are not connected are `none`. Their real cadence is unconfirmed (`planning/source-register.md`).
- Separate refund-event attribution is deferred (§5).
