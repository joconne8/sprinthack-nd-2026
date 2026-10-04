Task / issue / source requirement IDs: ING-05 (issue #12); REQ-ING-01 to REQ-ING-05; PLAN §4, §7
State: READY_FOR_REVIEW for the source map and class design. Not an owner-reviewed matrix.
Branch / base commit: hugh/ING-05-reconcile / 63a2b6c
Changed files: planning/source-register.md (requirement IDs added; drafts labels removed), contracts/sources/acquisition-classes.md (now separates the frozen goodwill-v1 import manifest from the acquisition record; adds no fields to the contract), reports/ING-05/check_source_register.py, verification.json, RESULT.md
Commands actually run: python3 reports/ING-05/check_source_register.py → exit 0: 5 requirement IDs cited, all in the GOV-01 register; no broken relative links; 9 source rows. See verification.json.
Dependencies: GOV-01 (#13) is state:review on GitHub. GOV-03 acceptance was reported to me by Hugh; GitHub issue #15 still showed state:blocked and I could not verify it.
Tests NOT run / unsupported: no source facts re-verified; Drive documents not re-read in this session; external links not machine-checked; owner, cadence and access for all nine sources remain unconfirmed.
Blockers: owner review of the source matrix; confirmation of channels with Goodwill.
Synthetic/production: only the Upright replica path is implemented; nothing connects to real sources.
Not accepted, not merged, not DONE.
