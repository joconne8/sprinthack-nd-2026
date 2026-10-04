# ENG-04 pre-merge check: peyton/jackoc-data-completion

Date: 2026-10-04 (UTC). Operator: Claude Code assisting Jack mc. Read-only QA; no edits to Peyton's branch.

Tested: detached worktree of `origin/peyton/jackoc-data-completion` (`4396a9c`) with `origin/main`
(`d5c4413`, includes ENG-04 PR #53) merged in without committing. The merge applied cleanly.

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/acceptance -p 'test_*.py'` | 25 run, OK, 2 skipped |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` | 68 run, OK, 2 skipped |

The independent ledger, seeded-defect and portal→API demo-sequence checks still hold after the
branch's contract/API changes. The same two skips remain: there is no dashboard UI on this branch
(`apps/` contains only `api/`), and export is deferred. This does not accept Peyton's branch. It shows
only that ENG-04 found no regression. The worktree was removed after the run.
