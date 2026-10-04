# GOV-03 compatibility notes

How existing work maps onto contracts `1.0.0`, and what each producer must change.

## 1. Replica output (`replica-v1`) → `SourcePackageManifest`

The ING-02 runner performs this translation. `validate-contracts.cjs` replays it on the committed example file
`data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.*`.

| v1 field | Comes from | Note |
| --- | --- | --- |
| `contract_version` | constant `1.0.0` | |
| `run_id` | runner | not in replica-v1 |
| `acquisition_class` | constant `portal_export` | |
| `source_name`, `report_type`, `requested_start_date`, `requested_end_date` | same names | |
| `reporting_timezone` | same name | **Must be `America/New_York`. The replica sends `America/Los_Angeles`, so this is the only failing field.** |
| `file_name`, `file_checksum`, `checksum_algorithm`, `row_count`, `coverage_start_date`, `coverage_end_date`, `synthetic`, `currency`, `source_package_id` | same names | |
| `byte_size` | runner: length of the exact downloaded bytes | not in replica-v1 |
| `downloaded_at` | runner's download timestamp | Not the replica's `generated_at`, which is when the report was generated |
| `skill_or_adapter_version` | `skill_id@skill_version` from `acquisition/skills/*.skill.json` | the replica's `replay_version` stays in `source_metadata` |
| `source_reported_totals` | replica `item_sales`, `refunds`, `demo_net_sales` | informational; the importer recomputes |
| `source_metadata` | every other replica field | never used for metrics |

**Result from the run (`contract-run.log`):**
- The CSV's SHA-256 `ecea8818…d2f166b` equals the manifest.
- The translated manifest fails **only** on `reporting_timezone`.

Independent check: gawk recomputed the 128 rows in integer cents as item sales 7353.00, refunds 225.22 and demo net 7127.78. That matches the replica's printed totals exactly.

## 2. Hugh's PR #49 drafts → v1

| Draft | v1 | Change |
| --- | --- | --- |
| `acquisition-classes.md` classes C1–C5 | `AcquisitionClass` | Same five, named `api`, `portal_export`, `scheduled_file`, `manual_upload`, `statement_lookup` |
| `acquisition-classes.md` common manifest `status` + `failure_type` | Moved to `AcquisitionRun` | A manifest exists only with delivered bytes |
| `acquisition-classes.md` common manifest, other fields | `SourcePackageManifest` | All kept. Adds `checksum_algorithm`, `row_count` and coverage dates as required |
| Ten failure types | `AcquisitionFailureType` | Same ten plus `report_unavailable` |
| `run_state.py` statuses | `RunStatus` | Identical |
| `run_state.py` `RETRIABLE` / `HUMAN_REQUIRED` / `PERMANENT` | Failure classes in `planning/contracts.md` §3 | Identical sets, plus `report_unavailable` as retriable |
| `run_state.py` `owner_role` strings | `AcquisitionRun.owner_role` | Kept as roles, never people |
| `intake.py` record (`intake-draft-v1`) | `VerifiedSourceFile` | `intake_version` → `contract_version`; `acquisition_state` → `intake_state`; `checksum` → `source_file_id`; `coverage_start`/`coverage_end` → `coverage_start_date`/`coverage_end_date`; embeds the manifest |
| `intake.py` `IntakeRejected` codes (15) | `IntakeRejectionCode` | All 15 kept, plus `timezone_mismatch` |
| `intake.py` `REQUIRED_MANIFEST` (9 fields) | `SourcePackageManifest.required` | All nine are required in v1 |
| `intake.py` `submit()` key `checksum_start_end` | Delivery key | Unchanged. The importer's own key is the checksum (`ImportBatch.idempotency_key`) |
| Replica job API `error_category: session_expired` | `expired_session` | The runner maps it |
| Replica job API `error_category: missing_report` | `report_unavailable` | The runner maps it |
| Replica job states `pending`/`ready`/`failed` | `AcquisitionRun.status` | `pending` → `running`. `ready` plus a verified download → `succeeded`. `failed` → the failure type above |

## 3. Landon's E-APP proposals → v1

| Proposal (`reports/E-APP/interfaces-and-blockers.md`) | Outcome |
| --- | --- |
| §3 state vocabulary | Adopted, with Hugh's run states for the acquisition layer |
| §2 metric response shape | `MetricResult`. `null` value when unavailable; no target field; evidence link |
| §4 KPI availability matrix | Roadmap metric IDs are in `MetricId` and reported `unavailable` with reasons |
| B1 `net_sales` column conflict | Closed. `planning/contracts.md` §5 says never read `net_sales` |
| B2 timezone | Closed for the contract (`America/New_York`). The replica change is still open |
| B4 export for ENG-04 | **Still open.** v1 has no export schema; export stays P1 until Jack OC decides |
| B5 APP-06 reviewer independence | **Still open.** Not a contract matter |

## 4. Changes that would break v1

Each of these requires `contracts/v2/`:
- Changing the timezone, the synthetic constant or the money format
- Removing or renaming a field or an enum value
- Making an optional field required

## 5. Required producer changes

| Owner | Change |
| --- | --- |
| Hugh | Add `America/New_York` to the replica's `ZONES` and request it for Upright. Cash Monkey is currently forced to UTC (P1). |
| Hugh | Have the ING-02 runner emit `SourcePackageManifest` per table 1. |
| Hugh | Map `session_expired` and `missing_report` to the v1 names. |
| Hugh | Rename the intake record fields per table 2, and add a `timezone_mismatch` check. |
| Peyton | Implement `ImportBatch` (natural keys, upsert policy, reconciliation in cents), plus `MetricResult`, `SupportingRows` and `SourceCoverage`. |
| ENG-01 | Add a standard validator (for example ajv) and type generation, and run `validate-contracts.cjs` in CI. |
