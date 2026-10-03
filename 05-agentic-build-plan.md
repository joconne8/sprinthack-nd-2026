AGENTIC ENGINEERING PLAN FOR SPRINTHACK (28 hours, you lead)

PRINCIPLES
- You are the product owner and integrator. Agents write code. Humans decide scope, review, and demo.
- One repo, one spec file, small tasks, merge often.
- A working end-to-end skeleton by hour 6, then deepen. Never a big-bang merge.
- The demo is the spec. Work backward from the demo script.

SETUP (first 60-90 min, before any code)
1. Kickoff: ask the sponsor the scoping questions (see 01 PRD for Beacon).
2. Commit to the problem by end of hour 2.
3. Create repo with: SPEC.md (PRD pasted in), DEMO.md (demo script), TASKS.md (checklist), AGENTS.md (rules for all agents: stack, style, how to run tests, do not touch files outside their lane).
4. Pick stack. Keep it boring. Make one agent scaffold app, DB, CI, and a deploy to a public URL.

ROLES (each is a coding-agent session with its own instructions and file lane)
1. Orchestrator (you, plus one planning agent): turns SPEC into small tasks, assigns them, tracks TASKS.md. You approve plans.
2. Backend agent: API, data models, job queue.
3. Source-integration agents (one per data source): each builds one connector with tests and a fixture fallback. Parallel work, no shared files.
4. Frontend agent: dashboard and demo screens, against a mocked API from hour 1 so it never waits for backend.
5. Data agent: builds synthetic data and seeded edge cases for the demo.
6. QA agent: writes end-to-end test that runs the demo script, runs it after each merge, reports failures.
7. Review agent: reads each diff against SPEC and AGENTS.md before merge. Catches scope creep and invented claims.
8. Pitch agent (later): slides, speaker notes, one-pager, from DEMO.md and what actually works.

COORDINATION
- Contracts first: the Orchestrator writes API schemas (OpenAPI or typed interfaces) before parallel work, so agents integrate without talking.
- Branch per task, small PRs, QA and Review agents gate merges.
- A shared STATUS.md updated by every agent at task end: done, blocked, next.
- Max 2 retries per agent on a task, then escalate to you.

HUMAN CHECKPOINTS (you must look)
H2: problem chosen. H6: skeleton runs end to end. H12: a first demo run-through, cut scope now. H20: feature freeze, only polish and bugs. H24 (Sunday ~noon): full rehearsal, record backup demo video. H27 (3pm Sunday): final deploy, no new features. 4pm: code freeze.
Schedule: Sat 11am start puts H24 around Sunday 11am-noon, so plan backward from the 4pm freeze.

TIMELINE (adjust to clock)
Sat 11am-1pm: scoping, decisions, repo, contracts.
Sat 1pm-5pm: skeleton end to end, connectors in parallel, fixtures. Office hours from 3pm: use a slot for the sponsor.
Sat 5pm-11pm: core features, first demo run.
Sat night: sleep. Let the QA and Review agents grind on tests if you want overnight progress, but do not merge unattended features.
Sun 9am-1pm: nice-to-haves only if the core demo is solid. Office hours from 1pm.
Sun 1pm-3pm: rehearsal, backup video, pitch materials.
Sun 3pm-4pm: final deploy and freeze.

FAILURE RULES
- If a data source fights you for more than 90 minutes, switch to fixtures and label it.
- If end to end is not working by H12, cut features, not quality.
- Never show an unlabeled fake. Synthetic data labeled synthetic. Illustrative numbers labeled illustrative.

TEAM
Recruit the rest of the team early: one who can talk to sponsor, one strong frontend or design, one who can debug when agents get stuck. You are not on a team yet, so grab rows in the sign-up sheet at kickoff.

TOOLS
Use what you have: a coding agent (Claude Code or Codex style) per lane, git worktrees so lanes do not collide. Replit and ClickUp mentors are at office hours, ask for help with deploy and task tracking.
