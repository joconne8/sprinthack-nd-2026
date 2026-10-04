# Approved Aimsigh showcase implementation

Peyton explicitly approved the complete presentation plan on October 4, 2026 and
confirmed that supplied sample inputs must produce the actual dashboard metrics.
Operator: Codex/Peyton. Branch: peyton/aimsigh-showcase. Worktree:
/private/tmp/aimsigh-showcase. Base: 3a8c734. Deadline: October 5, 10am Eastern;
target freeze 8am. Spend: local runtime only, zero paid/model calls.

Root owns services/showcase/, contracts/showcase-v1/, database migrations,
acquisition runner extensions, API/CLI entrypoints, requirements and CI wiring.
UI lane owns apps/showcase/. Presentation lane owns presentation/,
planning/pitch/, scripts/release/showcase* and DEMO.md. QA lane owns
tests/test_showcase*.py, tests/showcase*.cjs and scripts/verify_showcase.py.
Existing untracked experiments/jev and reports/JEV-MOCK are a separate session;
they are preserved in the original checkout and are not overwritten here.

User decisions supersede the previous P0-only freeze. This is the new GOV-02
scope acceptance: two synthetic sources, reviewed local recorder, matched sample
labor/cost inputs, Excel, charts, and model-free local conversation. Production
access/Teams/Copilot/Jev and accounting posting remain outside scope.
GOV-03 interfaces are frozen in CONTRACT.md. Human acceptance/merge remains
separate. At most two repairs per failing verification before reporting its cause.

Verification: original regression/handwritten financial ledger; independently
specified sample productivity/cost controls; real browser record/replay/export/
conversation flow; workbook cached-value reconciliation; deck/video/package checks.
