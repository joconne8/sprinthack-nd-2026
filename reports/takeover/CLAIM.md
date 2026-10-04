# Authorized acquisition/application takeover

Peyton explicitly requested taking over Hugh and Landon's remaining work while
Jack mc continues independent QA. Branch `peyton/acquisition-dashboard`, base
main `7f94806`; remote branches fetched before work. Hugh's acquisition and
Landon's coordination proposals are reused. Existing shared/data contracts and
independent QA artifacts are the baseline; do not edit Jack mc's tests/reports.

Sequential scope: ING-02/03/04/05 and APP-01/02/03 P0 drilldown. Optional exports,
assistant/Jev and production integrations stay deferred under frozen scope.
Allowed files: acquisition/, apps/dashboard/, apps/api/, goodwill_app/, additive
contracts and their generator, owned developer tests, runtime/CI/planning and
per-task reports. Peyton retains shared setup/data ownership from the earlier
combined authorization. No source fixture rewrites or independent QA edits.

Plan: bounded replay and full-manifest intake→real importer; persisted actionable
run state and manual upload fallback; operations/leadership/drilldown UI served
by the existing Python app. Actual API values only, visible synthetic/unavailable/
coverage/error states, pinned evidence run IDs, safe text rendering. One supervised
request starts acquisition; no production schedule/model/agent is launched.

Checks: Python intake/controller/API tests; existing data and Jack mc QA suites
unchanged; actual headless Chrome/Playwright UI/date/download/failure/filters/
evidence/mobile tests; screenshot inspection; exact commands, outputs and hashes.
Per-command bounds and at most two repairs. No paid service/model calls; usage
totals unavailable. Human review/acceptance and Jack mc's final independent UI
evaluation stay separate. This local claim is not a posted GitHub issue comment;
connector access was unavailable in earlier sessions. Primary source basis is
the registered repo Drive snapshots/three-phase plan, not a new interview.
