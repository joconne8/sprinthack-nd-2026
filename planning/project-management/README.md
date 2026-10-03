# GitHub Projects setup and shared backlog

[Hub](https://github.com/joconne8/sprinthack-nd-2026/issues/7) · [Backlog index](BACKLOG.md) · [Agent context](AGENT_CONTEXT.md) · [Full plan](THREE_PHASE_PLAN.md)

## What is already live
43 repository issues, six epic trackers, numbered dependency references, 21 labels and agent instructions. No agents, production actions or merges were started.

## What remains blocked
The connected GitHub App returns HTTP 403 Resource not accessible by integration for user Projects. Repository permissions do not prove Projects permissions. The connection diagnosis reported healthy and no reconnectable scope recommendation. The native board has NOT been created or populated.

## Bootstrap with authorized GitHub CLI access
Run from a checkout where gh is installed and authenticated to a user permitted to manage the destination project. The script never requests or stores credentials. For OAuth CLI login, project access may require gh auth refresh -s project; do not paste tokens into chat.

```bash
python3 planning/project-management/bootstrap_github_project.py --allow-create
# Or choose an existing PRIVATE project owned by joconne8:
python3 planning/project-management/bootstrap_github_project.py --project-number YOUR_PROJECT_NUMBER
```

The script creates/reuses a private project, links the repository, adds these exact issues and existing PR #1, creates Delivery phase/priority/scope, Agent workflow, Task ID, Agent lane, Dependencies and Human gate fields, initializes newly added cards, and verifies membership. It does not create duplicate issues and preserves current fields on already attached cards. Syntax/static checks were run during preparation; live execution was not possible with the current connection. If interrupted after adding an item but before setting all fields, inspect/complete that item manually; existing items are deliberately not overwritten on rerun.

## Recommended saved views (configure in GitHub UI)
- Delivery Board: group by Agent workflow; filter out epic/hub cards if desired.
- Weekend Critical Path: scope weekend, priority P0; show Dependencies and Human gate.
- Three Phases: group by Delivery phase.
- Overnight Work: lanes/claim status, blocked dependencies, evidence-ready review.
- Production Roadmap: scope pilot, with approval gates visible.

Custom fields and labels are not continuously synchronized by this one-time script. After attachment, agents/humans must update issue labels and project fields consistently or later implement approved synchronization. Built-in Status is left unchanged; group the board by Agent workflow. Named agent lanes are roles, not verified GitHub assignees.

## Safety
Do not publish private source context to a public board. Human approval gates, provider policies and AGENTS.md apply regardless of issue/project state.
