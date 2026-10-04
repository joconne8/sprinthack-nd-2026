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

## Separate source, import and acquisition records

The schemas in `contracts/v1/` define goodwill-v1. This acquisition-class document is a design note and does not change those schemas.

1. **Original source manifest:** replica-v1/fixture-v1 metadata, dates, timezone, filters, checksums and controls are retained with exact CSV bytes. Direct submission adds `acquisition_run_id` to stored original metadata for provenance; this is not a field in the strict normalized manifest.
2. **Normalized import manifest:** `manifest_metadata()` selects source/report, requested dates, timezone, filename, checksum, row count, currency, synthetic marker, source schema version and filters, then validates `manifest.schema.json`. Extra properties are rejected in this normalized shape. Original source metadata is stored separately, so run metadata and controls are not discarded.
3. **Acquisition record:** intake records contain run identity, artifact reference, checksum/byte size, row count, recorded time, original manifest and acquisition/import states. The controller exposes versioned skill logs, failure/owner, attempts and publication/batch state. `acquisition_class` is a design field, not currently a required/written intake field.

`intake.write_import_request(record, outbox)` retains Hugh's file-based handoff: exact archived UTF-8 CSV plus original source manifest, validated against `import-request.schema.json`. Creating this request leaves import state `not_submitted`. `intake.submit(record, pipeline)` performs the dashboard's real import and records the importer-returned batch/state; it does not infer publication from a download.

Production metadata such as delivery cadence, adapter class, download time and retention policy still require owner review. No additional live acquisition class is implemented by this design.

## Stays source-specific (not shared)
Parsing, column mapping, date/timezone logic, identity keys (never merge buyers across platforms), accounting role, and system-of-record rules.

## Per-class interface
`acquire(params) -> {ok, manifest, file}` or typed failure `{ok:false, type, detail}`. Failure types: expired_session, access_denied, mfa, captcha, wrong_page, label_changed, timeout, download_failed, host_not_allowed, bad_params, report_unavailable, runtime_unavailable. Types requiring a human are never retried.

Actual routes: POST /api/v1/acquisition-runs starts one supervised synthetic run; GET /api/v1/acquisition-runs exposes persistent collection/import/publication states. intake.submit() now invokes the real importer, retaining full manifest filters, checksums and run→file→batch identity. Original source manifests are downloadable at /api/v1/imports/{id}/manifest. No live schedule, email delivery or new model service is active.
