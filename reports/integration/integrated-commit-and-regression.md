# Local regression state

Tested base commit: b329c0fece37c1694b4d84c0c55e609dc931f854 plus the recorded
working-tree code/schema/test hashes in verification.json. Final local handoff
commit is visible with `git log -1` on peyton/jackoc-data-foundation.

36 foundation, 23 acquisition and 10 fixture tests pass; 354 review checks pass;
schema regeneration, CLI smoke and other-lane preservation pass. This is local
combined foundation regression, not a merged-main or independent UI acceptance
claim. Main integration is still a human action after branch push/review.
