Task / issue / source requirement IDs: ING-05 (see ProjectManagement/agent-assignments/tasks/ING-05.md); PLAN §4, §7
State: BLOCKED (draft produced for review)
Branch / base commit / head commit: hugh/ING-acquisition / 15fa25a / uncommitted working tree
Changed files and diff summary: planning/source-register.md, contracts/sources/acquisition-classes.md, reports/ING-05/source-authority-and-overlap.md
Commands actually run, results, logs: No commands beyond reading sources; document check was manual against THREE_PHASE_PLAN §4 table (nine sources, classes, hypotheses labeled). Links not machine-validated. No verification.json created because no checker ran.
Independent expected-result comparison: expected values taken from the ING-01 example manifests (128 Upright rows, 32 Cash Monkey rows, SHA-256 from manifest), not recomputed by the code under test where applicable.
Measured elapsed time / usage: not measured; no model, paid service or live access used.
Tests NOT run and unsupported behavior: Owner/cadence/access for all nine sources unconfirmed. Not an owner-reviewed matrix.
Remaining blockers / exact missing evidence or human decision: GOV-01 and GOV-03 accepted commits; source-owner review. GOV-01/GOV-03 acceptance evidence and ENG-01 scaffold not found in repo; claims not posted to GitHub issues (no GitHub action taken); lane (acquisition/, contracts/sources/) not yet mapped by orchestrator.
Synthetic/production distinctions: synthetic replica only; nothing here is validated against real Upright or any live Goodwill source.
Recommended human review: Jack OC to confirm GOV-03 field names and file lane; confirm coordination with PR #45 contributor.

Not accepted, not merged, not DONE.
