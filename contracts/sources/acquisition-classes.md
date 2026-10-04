# Acquisition classes and intake manifest (ING-05 DRAFT — must be reconciled by the GOV-03 contract owner)

This directory is a proposal. Contracts have one owner (GOV-03); nothing here is frozen.

## Classes
| Class | Meaning | Implemented? |
|---|---|---|
| C1 api | Documented, authorized API pull | No |
| C2 portal_export | Operator-permitted browser report generation + download | Synthetic replica only (ING-01/02) |
| C3 scheduled_file | Email attachment or controlled folder feed | No |
| C4 manual_upload | Human uploads a file; always the fallback | Not built |
| C5 statement_lookup | Monthly statement or accounting lookup | No |

Decision order follows PLAN §4: supported export, API, email/folder, authorized browser automation, manual upload.

## Common intake manifest (all classes)
Fields every class must supply with the exact bytes: `run_id`, `acquisition_class`, `source_name`, `report_type`, `requested_start_date`, `requested_end_date`, `reporting_timezone`, `file_name`, `file_checksum` (SHA-256), `byte_size`, `downloaded_at`, `artifact_ref`, `synthetic` (true/false), `skill_or_adapter_version`, `status` (+ `failure_type` if failed). Matches what `acquisition/intake.py` verifies, plus fields it does not yet require (`acquisition_class`, `byte_size`, `downloaded_at`).

## Stays source-specific (not shared)
Parsing, column mapping, date/timezone logic, identity keys (never merge buyers across platforms), accounting role, and system-of-record rules.

## Per-class interface (draft)
`acquire(params) -> {ok, manifest, file}` or typed failure `{ok:false, type, detail}`. Failure types: expired_session, access_denied, mfa, captcha, wrong_page, label_changed, timeout, download_failed, host_not_allowed, bad_params. Types requiring a human are never retried.
