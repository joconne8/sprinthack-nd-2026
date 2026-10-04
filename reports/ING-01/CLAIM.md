# ING-01 replica implementation lane

Operator: Codex working with Jack in the hackathon setup chat.

User authorization: October 3 request to create the reporting decoy from supplied screenshots and push it under a new folder named `data ingestion`.

Branch: `codex/reporting-decoy`. Isolated checkout: `/private/tmp/sprinthack-nd-2026`. Base: `3b5060f`.

Allowed files: `data ingestion/**`, `reports/ING-01/**`. Root contracts, fixture package, migrations, lockfiles, existing application entrypoints and other teams' files remain outside this lane.

Task: standalone screenshot-informed Upright and Cash Monkey replicas with functional forms, synthetic CSV downloads and tests. The latest user explicitly selected this new folder and the two reference journeys; this supersedes the issue's suggested `apps/portal-replica/` location for this bounded patch. It does not change shared pipeline contracts or approve production access.

Context checked: root AGENTS.md; Drive primary three-phase plan fetched through the connected account; source register, repo plan, traceability and shared context; acquisition PRD; ING-01 issue #14 and comments (no claims/comments at read time). GOV-03/ENG-01 acceptance is not asserted. This is a self-contained review proposal based on the direct user request, not an unattended rollout dependent on those gates.

No GitHub issue claim comment was sent because the user authorized publishing the implementation, not messaging teammates. This local claim travels with the patch.

Planned verification: Python artifact/API tests; real browser journeys/downloads; independent control-total checks; alternate date, delayed, unavailable, expired-session and DOM-drift cases; visual and mobile review.

Boundaries: no external AI calls, paid services, production credentials, deployment or merge. No scheduled work or subagents started. Finish in this turn; no provider spending beyond this conversation. At most two repairs per observed failure.
