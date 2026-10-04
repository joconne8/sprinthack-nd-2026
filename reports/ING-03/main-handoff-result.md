Task / issue / source requirement IDs: ING-03 (issue #17); PLAN §4, §5; contracts/v1 (GOV-03, READY_FOR_REVIEW, not accepted)
State: READY_FOR_REVIEW for the intake-to-importer hand-off. Human acceptance of GOV-03/DAT-02/ING-01/ING-02 still outstanding.
Branch / base commit: hugh/ING-03-importer-handoff / 7f94806
Changed files: acquisition/intake.py (submit() now writes a goodwill-v1 import-request with exact archived bytes and the original manifest, per planning/contracts.md; the earlier outbox stub was not a valid importer input), acquisition/tests/test_intake.py, acquisition/tests/test_e2e_import.py (new), reports/ING-03/RESULT.md
Commands actually run: python3 -m unittest discover -s acquisition/tests → 28 OK (14 intake, 5 end-to-end, 6 run-state, 3 skill config). python3 -m unittest discover -s "data ingestion/tests" → 9 OK (tail of output only).
End to end (acquisition/tests/test_e2e_import.py, real ING-01 CSVs through intake into services.data.importer.Pipeline in a temp dir): downloaded SHA-256 equals the imported raw file checksum (Upright 128 rows, reconciliation verified); Cash Monkey imports; resubmitting the same file gives duplicate_noop; a wrong date range is rejected at intake and nothing reaches the importer; tampered bytes that bypass intake are rejected by the importer with checksum_mismatch.
State separation: intake leaves import_state = not_submitted; the importer owns the import and publication states.
Independent expected results: row counts and checksums come from the ING-01 manifests; importer status values come from services/data, not my code.
Tests NOT run: full repo test suite; cross-midnight timezone cases; real Goodwill files; browser skill to importer in one process (the skill was run separately earlier).
Blockers: human acceptance of GOV-03, DAT-02, ING-01, ING-02. Field names still need Jack OC review.
Synthetic only. Not accepted, not merged, not DONE.
