Task / issue / source requirement IDs: ING-03 (see ProjectManagement/agent-assignments/tasks/ING-03.md); PLAN §4, §7
State: BLOCKED
Branch / base commit / head commit: hugh/ING-acquisition / 15fa25a / uncommitted working tree
Changed files and diff summary: acquisition/intake.py, acquisition/tests/test_intake.py
Commands actually run, results, logs: python3 -m unittest discover -s acquisition/tests → 14 intake tests OK against the real ING-01 example CSVs and manifests; negatives: wrong period, wrong report, missing/empty file, tampered bytes, schema change, out-of-period row, truncated file, unlabeled synthetic, incomplete manifest, reused run id.
Independent expected-result comparison: expected values taken from the ING-01 example manifests (128 Upright rows, 32 Cash Monkey rows, SHA-256 from manifest), not recomputed by the code under test where applicable.
Measured elapsed time / usage: not measured; no model, paid service or live access used.
Tests NOT run and unsupported behavior: Skill download to intake verified end to end (256 rows, checksum matches, acquired_verified/not_submitted). No import: the frozen import contract and DAT-02 do not exist, so submit() writes to a local outbox placeholder. 'Checksum matches imported raw file' is unproven. Tests do not cover cross-midnight timezone cases.
Remaining blockers / exact missing evidence or human decision: DAT-02 immutable archive/batches and GOV-03 import contract. GOV-01/GOV-03 acceptance evidence and ENG-01 scaffold not found in repo; claims not posted to GitHub issues (no GitHub action taken); lane (acquisition/, contracts/sources/) not yet mapped by orchestrator.
Synthetic/production distinctions: synthetic replica only; nothing here is validated against real Upright or any live Goodwill source.
Recommended human review: Jack OC to confirm GOV-03 field names and file lane; confirm coordination with PR #45 contributor.

Not accepted, not merged, not DONE.
