# ENG-05 human integration checklist

Current baseline: shared foundation merged into main at `610035e` (PR #52).
Follow-up branch: `peyton/jackoc-data-completion`. Current evidence and task status:
`reports/integration/completion-verification.json` and `completion-status.md`.
The historical branch handoff below is superseded by these current checkpoints.

- [x] Reconcile old GOV-03/GOV-04 proposals with the running `goodwill-v1` API;
  preserve source timezones, explicit corrections and exact original bytes.
- [x] Run fresh backend/acquisition/fixture, strict client and actual browser-
  file→intake→import→API/archive regression; retain logs/hashes/limits.
- [x] Document the prototype stack, production bridge/options and approval gaps;
  verify required task documents and preserve other owners' lanes.
- [ ] Human accepts scope/contracts/architecture and claims for a reviewed commit.
- [ ] Landon delivers and integrates APP-01/02/03 using real API responses.
- [ ] Jack mc supplies independent ENG-04 expected results and acceptance evidence.
- [ ] Human reruns the complete product UI demo on the integrated commit, confirms
  the event requirements and records the release freeze/backup handoff.

ENG-05 final acceptance is pending those unchecked dependencies. This checklist
does not make developer regression an independent review. Export is P1/deferred;
assistant/Jev/live/production work remains outside this P0 freeze.

This branch delivers the combined shared setup and trusted-data foundation for
review. It is not an independently accepted full product or a deployment.

- [ ] Human reviews authorized scope, Python/SQLite prototype exception, source
  authority and versioned contracts.
- [ ] Landon wires operations/leadership/source drilldown to the actual v1 API,
  preserving nulls, coverage, rejected rows and stale warnings.
- [ ] Jack mc derives independent expected results and reviews exact-file
  continuity, alternate dates, malformed files, replay/overlap/corrections,
  controls, source-row sums and missing inputs.
- [ ] Human confirms issue claims/ownership and records actual acceptance
  commits/evidence; current connector access could not verify comments.
- [ ] Human integrates reviewed branches in dependency order and reruns the
  complete UI demo on the integrated commit.
- [ ] Confirm event deadline and record honest backup demo evidence.

P0 export is explicitly deferred (P1); it does not block the first slice.
Assistant/Jev/production Copilot, nine live sources, Business Central posting
and autonomous operations remain deferred/unapproved. Missing strategic inputs
show unavailable. No source CSV field named net_sales is rendered directly.

The branch may be pushed for review after local checks pass. A push makes the
branch fetchable; only human review/merge makes it available through ordinary
main pulls. Do not use an automatic merge-after-push workflow for this handoff.
