# Launch guide — package does not launch agents

## What exists
36 bounded task prompts and 7 coordination prompts, one per existing issue. All remain unclaimed unless current issue comments say otherwise. No acceptance is inferred from this package. Source snapshot at packaging: tree 8abf7b2f1ef57d53f5f5b5e3e71ae22ff683f06b. Native GitHub Projects access remains blocked; these packets use existing repository issue refs.

## Operator workflow
1. Start PM-00 coordination and GOV-01 source/requirements drafting; supervise workstream packets as needed. Human scope/contract/security decisions are not delegated away.
2. After accepted GOV-01, draft GOV-02 scope; then GOV-03 contracts and GOV-04 architecture/security. DAT-01 validates the now-merged PR #1 fixture contribution after GOV-02; do not duplicate or re-merge it.
3. Establish ENG-01 actual scaffold/test/runtime guide and ENG-02 ownership. Build one verified vertical slice before handing off an unattended feature wave. If absent, supervised skeleton work and tests only.
4. Reserve at most THREE concurrent build sessions with non-overlapping actual file lanes. Frontend uses frozen mocks; replica/data/QA interfaces follow accepted contracts.
5. After a verified integrated checkpoint, optionally dispatch P1/assistant/Jev/extra-source work if the existing runner and policy permit it. Do not force pilot work into the weekend.
6. Human morning review checks commit/artifacts/financial logic/source coverage/permissions, integrates separately authorized patches in dependency order, runs full demo and freezes verified work.

## How to hand off one task
From a current checkout, use the read-only selector. No credentials are requested, no agent is started, and no git changes occur:

```bash
python3 ProjectManagement/agent-assignments/select_assignment.py --list
python3 ProjectManagement/agent-assignments/select_assignment.py GOV-01
# Once a human has created real accepted-task evidence records:
python3 ProjectManagement/agent-assignments/select_assignment.py ING-02 --acceptance /path/to/acceptance.json
# Inspect a blocked prompt without clearing any gates:
python3 ProjectManagement/agent-assignments/select_assignment.py ING-02 --emit-blocked
```

Copy the resulting packet into ONE coding-agent session rooted in the repository. Review current issue comments and resolve lane claims. For an isolated checkout, a human/operator may prepare:

```bash
git fetch origin main
git worktree add -b agent/GOV-01 ../goodwill-GOV-01 origin/main
```

Use your task ID instead of GOV-01, and a unique branch/worktree if that name already exists. Verify every accepted dependency commit is included before work, for example `git merge-base --is-ancestor ACCEPTED_SHA HEAD`. Never auto-merge missing prerequisites. Worktree preparation commands were supplied, not executed by packaging.

## Evidence record format
`accepted_tasks` maps task IDs to records with `accepted: true`, actual reviewer, full accepted_commit SHA, a non-empty evidence array and a tests array. Each test has command/result/pass log. Example structure (illustrative; replace with real reviewed values):

```json
{"accepted_tasks":{"GOV-01":{"accepted":true,"reviewer":"ACTUAL_HUMAN_REVIEWER","accepted_commit":"ACTUAL_40_CHARACTER_SHA","evidence":["ACTUAL_REPORT_PATH"],"tests":[{"command":"ACTUAL_COMMAND_OR_REVIEW_CHECK","result":"pass","log":"ACTUAL_LOG_PATH"}]}}}
```

The selector checks record structure only; it does NOT verify reviewer identity/artifact truth, inspect git ancestry, run tests or enforce runner budgets. The human/real runner must perform those checks. Missing acceptance prints BLOCKED and exits 2. `--emit-blocked` remains review-only and exits 2; it is not a bypass.

## Limits and ownership
Default per task: 60 minutes, max 2 repair attempts; ENG-04 allows 90 minutes. These are proposed instruction limits, not automated enforcement. Before unattended launch the actual runner must support deadline/cancellation and a recorded per-task and total spend/token cap. No new paid services/credentials, production actions or unattended merges/deployments. Design/pilot packets may draft evidence requests/plans with synthetic experiments, never execute live client changes.

One owner for contracts (GOV-03), scaffold/lockfiles/entrypoints (ENG-01), migrations (designated DAT-02 owner) and shared status (PM-00 human orchestrator). Same-lane agents must serialize or get exact subdirectory reservations. Only write reports/<own-task-id>/; do not concurrently edit STATUS.md.

## Dependency layers — ordering aid, NOT a concurrency/approval guarantee
These are topological levels of the current 36-task graph; mixed levels include P1/pilot/human work and are NOT invitations to launch every row. Apply scope, accepted artifacts, exact file ownership and checkpoint first.

| Dependency level | Tasks |
|---|---|
| 0 | GOV-01 |
| 1 | GOV-02 |
| 2 | GOV-03, GOV-04, DAT-01 |
| 3 | ENG-01, ING-05, ENG-02 |
| 4 | ING-01, DAT-02, APP-01, APP-02, ENG-04 |
| 5 | ING-02, DAT-03 |
| 6 | ING-03, DAT-04, ING-06, ING-07 |
| 7 | DAT-05 |
| 8 | DAT-06, REL-02 |
| 9 | DAT-08, DAT-07, ENG-03 |
| 10 | ING-04, DAT-09, APP-03, APP-04, ENG-05 |
| 11 | APP-05, APP-07, REL-01, REL-03 |
| 12 | APP-06, REL-04 |

## Cut/stop rules
Keep acquisition, validation/reconciliation, source evidence, coverage and truthful failure states. Cut optional recorder/assistant/extra sources/finance preview/polish before weakening controls. Stop on missing approvals, test failures, source contradiction, time/spend, two repairs or overlapping edits. Return READY_FOR_REVIEW/BLOCKED with exact evidence; a generated prompt does not mark a task complete.

## Latest repository correction at packaging
PR #1 is now merged (GitHub reports 2026-10-04T00:13:02Z). Source summaries/issue snapshots that call it an open draft are historical. DAT-01 validates the merged fixture/generator contribution in current main; do not regenerate a competing dataset or attempt to merge it again. Fixture checks still do not establish application correctness.

