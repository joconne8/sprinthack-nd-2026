---
name: merge-after-push
description: Safely push the current branch and merge its GitHub PR only when the user asks for merge-after-push behavior and repository checks show it is ready.
---

# Merge After Push

Use this skill when the user asks to push a branch and merge it if it works, merge a just-pushed PR after checks pass, enable auto-merge for a PR, or otherwise wants the current GitHub branch merged only when validation succeeds.

The goal is a normal reviewed GitHub merge path: local changes committed, branch pushed, PR identified, checks passing, mergeability confirmed, then merge or GitHub auto-merge. Do not bypass branch protection, skip checks, force-push, use admin merge, deploy production, delete unrelated branches, or merge a different PR than the one tied to the current branch.

## Preconditions

Before mutating anything, establish the repository and PR context:

- Run `git status --short` and stop if the worktree has uncommitted changes that are not part of the requested push.
- Identify the current branch with `git branch --show-current`. Never merge directly from `main`, `master`, or the PR base branch.
- Read `git remote -v` and use the repo's normal `origin` unless the user named another remote.
- Fetch remote state before deciding whether the branch is current.
- Identify the PR for the current branch with GitHub CLI, usually `gh pr view --json number,url,title,headRefName,baseRefName,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup`.
- If no PR exists, create one only when the user asked for that or when their request clearly requires it. Otherwise report the branch is pushed but has no PR to merge.
- If more than one PR could match, stop and ask for the exact PR number.

## Push Flow

If the user asked to push local commits first:

1. Confirm there is at least one local commit to push or that the branch already tracks the expected remote branch.
2. Run `git push -u origin <current-branch>` for a new branch, or `git push` for an existing upstream branch.
3. After pushing, re-read the PR metadata and checks; do not assume push success means the PR is mergeable.

Never use `--force`, `--force-with-lease`, or branch deletion as part of this skill unless the user explicitly asks for that separate action.

## Merge Readiness

Treat "works properly" as all of the following unless the repository has a stricter documented rule:

- The PR is open and not draft.
- The PR head branch matches the current branch or the user-named branch.
- Required and visible status checks have succeeded. Pending checks mean wait, enable auto-merge, or report pending status depending on the user's request.
- GitHub reports the PR is mergeable or in a clean merge state. If GitHub says dirty, behind, blocked, unstable, unknown after retries, or otherwise not mergeable, stop and report the reason.
- Required review state, if present, is satisfied. Do not merge when review is explicitly required and missing, or when requested changes are unresolved.
- Local branch state has not changed since the push/check decision.

Useful commands:

```bash
gh pr checks <number> --watch
gh pr view <number> --json number,url,title,headRefName,baseRefName,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
```

If checks are pending and the user asked to merge whenever they pass, prefer GitHub auto-merge over a long local wait when branch protection supports it. If auto-merge is unavailable, wait only for a reasonable bounded interval and then report what remains pending.

## Merge Action

Use the repository's established merge strategy when it is obvious from prior PRs or repo settings. If not obvious, prefer squash merge for small feature/task branches because it keeps history tidy. Use one of:

```bash
gh pr merge <number> --squash --delete-branch
gh pr merge <number> --merge --delete-branch
gh pr merge <number> --rebase --delete-branch
gh pr merge <number> --auto --squash --delete-branch
```

Choose `--auto` only when checks are pending or branch protection will merge later after requirements pass. Do not use `--admin`, `--disable-auto`, or `--match-head-commit` unless the user or repo instructions specifically require it. If using `--match-head-commit`, get the exact head SHA from GitHub immediately before the merge.

After merge or auto-merge setup, verify and report:

- PR number and URL.
- Merge command used and whether it merged now or auto-merge is enabled.
- Final PR state if immediately merged.
- Any local untracked or unrelated files left untouched.
- Any checks or reviews that are still pending.

## Stop Conditions

Stop and report instead of merging when:

- The worktree is dirty in unrelated or unclear ways.
- The branch is not pushed or push failed.
- No matching PR exists and creating one was not requested.
- The PR is draft, closed, from an unexpected branch, or targets an unexpected base.
- Checks failed, are cancelled, or are missing where required.
- Merge state is dirty, blocked, behind, unknown after a retry, or conflicts exist.
- Required reviews are missing or changes are requested.
- Repo instructions require human review or say "move to review, not done." In that case, open/push the PR and report it for human review rather than merging.
- The action would merge production-impacting, credential, deployment, accounting, or external-system changes without explicit user authorization for that exact merge.

Do not describe an action as complete unless the command output confirms it.
