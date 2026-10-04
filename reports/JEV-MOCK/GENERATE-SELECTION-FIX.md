# Generate button refinement — second repair

Evidence: actual Jev run .runtime/jev-mockup/2026-10-04T17-09-54-312Z-24801/.
Date-field repair succeeded at 0.98 confidence. Generate selection stopped at
0.82 confidence, despite selecting the intended button with probability 0.91.

Refinement distinguishes next-control identification from report completion.
The runner supplies reportParametersVerified only after deterministic date,
timezone and payment-status checks pass. The provider explicitly identifies the
enabled report submit control, with Generate report/Build export semantics.
Report completion and file verification remain separate deterministic checks.
No confidence thresholds lowered, retry added, or success implied.

Provider tests: 9/9 passed using Node 22.14.0. Browser regression evidence:
/private/tmp/jev-generate-fix-browser.log (injected decisions only).
Actual API validation remains pending because the key is not inherited by the
agent tool process. The user may rerun in their configured terminal.

This is repair two following the real API failures. If another semantic
confidence failure occurs, stop prompt repairs and review the workflow design
with the human orchestrator, per AGENTS.md. Do not tune until one lucky run passes.
