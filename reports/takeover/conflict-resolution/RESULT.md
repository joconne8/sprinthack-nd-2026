# PR #58 conflict resolution

Merged main 0dd1b02 into peyton/acquisition-dashboard (feature parent ac59816). All seven reported conflicts are resolved without dropping Hugh's contributions or the dashboard's direct importer integration.

Intake now exposes two explicit paths: write_import_request(record, outbox) preserves the exact-byte/original-manifest file handoff; submit(record, pipeline) performs the real import and records its batch/publication result. Both recheck the archived checksum/byte size. Hugh's five E2E assertions remain intact, with their helper calling the explicit request writer. Direct-submit idempotency and file-request state separation/replay/tamper checks all run.

The source map retains REQ-ING-01–05, nine rows and working relative links. The acquisition design distinguishes stored original metadata, strict normalized import manifest and acquisition run record. Incoming Hugh reports/verification are preserved as main-handoff-result.md and main-handoff-verification.json; original ac59816 test counts/hashes remain historical. The new merge evidence is verification.json here. The incoming merge-after-push skill is retained with only an EOF whitespace fix; it was not invoked to merge/deploy the PR.

Actual verification: 30 acquisition tests and 48 developer backend/controller tests passed; actual Chrome dashboard flow, source checker, required-artifact checker, Python syntax and staged/working diff checks passed. Independent QA/source fixtures match main unchanged. The full Python suite ran 73 tests: one deliberate dashboard acceptance placeholder failure and one deferred-export skip. No new failing check was found. Logs, commands, measured elapsed times and implementation hashes are recorded alongside this report.

State: READY_FOR_REVIEW; accepted: false. No final PR merge/deployment or issue closure. Jack mc independent UI acceptance, human review/integration/freeze and remote CI remain pending.
