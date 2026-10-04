# ENG-05 human integration checklist

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
