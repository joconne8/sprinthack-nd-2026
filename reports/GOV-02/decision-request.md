# Local scope decisions and review request

Peyton reported Jack OC approval and explicitly authorized the combined setup
and data implementation. The existing P0/P1/P2 scope and item-sales-minus-refunds
convention were selected for local work. Reporting is America/New_York, USD only,
without identity merging or invented labor/cost/cohort inputs. Python/SQLite is
the documented local runtime exception to the suggested Node/Postgres stack.

Human reviewers should confirm these artifacts for integration:

- `planning/scope.md`, `planning/metric-dictionary.md`.
- `planning/contracts.md`, including source dates versus reporting dates,
  source net/payout exclusions and source authority.
- `planning/decisions/architecture.md` and ownership/runtime handoff.

The user's delegation is not production/finance/provider acceptance or an
independent test review. All later production decisions remain open.
