# Acquisition classes and acquisition record (ING-05)

This is a design note, not a contract. The frozen contract is contracts/v1 (goodwill-v1, owned by GOV-03). Nothing here changes it.

## Classes
| Class | Meaning | Implemented? |
|---|---|---|
| C1 api | Documented, authorized API pull | No |
| C2 portal_export | Operator-permitted browser report generation + download | Synthetic replica only (ING-01/02) |
| C3 scheduled_file | Email attachment or controlled folder feed | No |
| C4 manual_upload | Human uploads a file; always the fallback | Not built |
| C5 statement_lookup | Monthly statement or accounting lookup | No |

Decision order follows PLAN §4: supported export, API, email/folder, authorized browser automation, manual upload.

## Two records, kept separate
1. **Import manifest (frozen, goodwill-v1 or replica-v1):** source_name, report_type, requested dates, reporting_timezone, file_name, file_checksum, row_count, currency, synthetic, filters. It rejects extra properties, so acquisition fields must not be added to it. The importer takes the CSV bytes plus this manifest.
2. **Acquisition record (outside the contract, written by acquisition/intake.py):** run_id, acquisition_class, skill or adapter version, artifact_ref, byte_size, recorded_at, acquisition_state, import_state, failure type. It links a run to the file but is not an importer input. acquisition_class is not written yet; adding it is a small change to intake.py if the team wants it.

## Stays source-specific (not shared)
Parsing, column mapping, date/timezone logic, identity keys (never merge buyers across platforms), accounting role, and system-of-record rules.

## Per-class interface (draft)
`acquire(params) -> {ok, manifest, file}` or typed failure `{ok:false, type, detail}`. Failure types: expired_session, access_denied, mfa, captcha, wrong_page, label_changed, timeout, download_failed, host_not_allowed, bad_params. Types requiring a human are never retried.
