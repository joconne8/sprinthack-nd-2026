# Acquisition classes and intake manifest (ING-05 / goodwill-v1 handoff)

Acquisition-class design is reconciled with the merged goodwill-v1 importer. Original manifest metadata/filters are retained with exact bytes. Source-specific live formats, access and ownership remain unconfirmed. Shared contract changes are additive and owned by Peyton under the combined takeover.

## Classes
| Class | Meaning | Implemented? |
|---|---|---|
| C1 api | Documented, authorized API pull | No |
| C2 portal_export | Operator-permitted browser report generation + download | Synthetic replica only (ING-01/02) |
| C3 scheduled_file | Email attachment or controlled folder feed | No |
| C4 manual_upload | Human uploads original CSV + manifest; fallback | Implemented synthetic UI/API |
| C5 statement_lookup | Monthly statement or accounting lookup | No |

Decision order follows PLAN §4: supported export, API, email/folder, authorized browser automation, manual upload.

## Common intake handoff
Proposed production metadata for each class; the implemented synthetic path uses the original replica-v1 manifest normalized by manifest_metadata() and adds acquisition run identity: `run_id`, `acquisition_class`, `source_name`, `report_type`, `requested_start_date`, `requested_end_date`, `reporting_timezone`, `file_name`, `file_checksum` (SHA-256), `byte_size`, `downloaded_at`, `artifact_ref`, `synthetic` (true/false), `skill_or_adapter_version`, `status` (+ `failure_type` if failed). Matches what `acquisition/intake.py` verifies, plus fields it does not yet require (`acquisition_class`, `byte_size`, `downloaded_at`).

## Stays source-specific (not shared)
Parsing, column mapping, date/timezone logic, identity keys (never merge buyers across platforms), accounting role, and system-of-record rules.

## Per-class interface
`acquire(params) -> {ok, manifest, file}` or typed failure `{ok:false, type, detail}`. Failure types: expired_session, access_denied, mfa, captcha, wrong_page, label_changed, timeout, download_failed, host_not_allowed, bad_params, report_unavailable, runtime_unavailable. Types requiring a human are never retried.

Actual routes: POST /api/v1/acquisition-runs starts one supervised synthetic run; GET /api/v1/acquisition-runs exposes persistent collection/import/publication states. intake.submit() now invokes the real importer, retaining full manifest filters, checksums and run→file→batch identity. Original source manifests are downloadable at /api/v1/imports/{id}/manifest. No live schedule, email delivery or new model service is active.
