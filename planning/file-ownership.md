# ENG-02 file ownership and handoff

## Current authorized takeover

Peyton explicitly took over Hugh/Landon's remaining core implementation on
`peyton/acquisition-dashboard`, base main `7f94806`. Ownership now also includes
`acquisition/`, `apps/dashboard/`, the integration entrypoints/additive contracts,
owned controller/browser regressions and ING-02/03/04/05 + APP-01/02/03 reports.
The existing synthetic replica in `data ingestion/` is reused without edits.
See `reports/takeover/CLAIM.md` and `RESULT.md` for scope and actual evidence.

Jack mc retains `tests/acceptance/`, `fixtures/expected-results/` and
`reports/ENG-04/`; these files and source CSV fixtures are unchanged. His
dashboard acceptance placeholder remains a reported failure. Shared generation
still runs through `contracts/build_schemas.py`. Human review/merge/freeze and
independent acceptance remain separate from developer implementation delivery.
The previous allocation and earlier completion branch below are historical.

Peyton reported Jack OC's approval to combine setup and data tasks in this session.
Peyton owns `services/data/`, `services/metrics/`, `db/migrations/` and data tests.
Delegated setup ownership covers `contracts/v1/`, `goodwill_app/`, `apps/api/`,
runtime/CI and the planning documents produced here. Jack OC remains human
integration/scope coordinator. Reports are per task; no shared task-board state
is automatically changed. No agents/schedules or GitHub claims are started.

Hugh retains `acquisition/` and `data ingestion/`; those files were read and tested
without feature edits. Landon retains UI screens/components (suggested future
lane `apps/dashboard/`); consume `contracts/v1/` and the documented API. Jack mc
retains independent expected-results and acceptance evidence. He should review
this implementation without copying its formulas for expectations.

Before edits, record operator, branch/base, exact paths, dependency decisions,
versions, actual test commands, deadline/reviewer/spend limits. Serialize tasks
within a lane. No shared schema/migration/entrypoint should be edited concurrently
without handoff. Repository issue access is currently unavailable (404), so
claims cannot be represented as verified or posted.

This implementation can be pushed for team review. Everyone can fetch the branch;
ordinary `git pull` on main will receive it only after a human reviews/merges it.
Independent ENG-04 and human ENG-05 acceptance remain outstanding. Do not invent
an `accepted_tasks` record or mark issues done to bypass those reviews.

## Current combined completion branch

PR #52 merged the shared foundation into main at `610035e`. Follow-up work lives
on `peyton/jackoc-data-completion`, with claim and exact verification in
`reports/integration/completion-claim.md` and `completion-verification.json`.
This supersedes the historical push instructions above, not other owners' lanes.
`contracts/build_schemas.py` owns schemas and generated `types.ts`; edit that
source instead of independently changing generated client interfaces.

Dispatch Landon against the documented API, Hugh against original manifest plus
exact bytes/full intake record, and Jack mc against independently derived expected
results. Jack OC's old GOV-03/GOV-04 branches are reconciled proposals; do not
overwrite the shared baseline with conflicting versions. Human integrator records
acceptance on a reviewed commit after the UI/QA checks. No issue comments were
posted because current connector access remains 404.
