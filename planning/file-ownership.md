# ENG-02 file ownership and handoff

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
