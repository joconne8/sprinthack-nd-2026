# Human review before main integration

Current review target is `peyton/jackoc-data-completion`, based on main `610035e`.
Check `completion-status.md`, exact command/log/hash evidence in
`completion-verification.json`, and the GOV-03/GOV-04 reconciliation decisions.
Review the request schemas/generated client and the separate pinned browser
runtime. Confirm original source bytes, unavailable inputs and filtered coverage
warnings are preserved. Human acceptance remains unrecorded.

Before final ENG-05 freeze, integrate Landon's actual UI and Jack mc's independent
ENG-04 evidence, run the complete demo on that reviewed commit, then record the
acceptance/commit and event/backup decisions. The user authorized implementation
of these two lanes; this is not acceptance of a missing UI or a live pilot.

Review source/scope/runtime exception, versioned contracts and exact-file tests;
confirm ownership claims with current issue access; have Jack mc independently
derive expected controls; wire and test Landon's actual UI; review synthetic
labels/null/coverage/failure behavior; integrate only the reviewed branch; run
the complete demo on the integrated commit. See `planning/release-checklist.md`.
No auto-merge or production deployment is authorized by this report.
