# ING-04 manual fallback and production prerequisites (draft, P1)

Code: `acquisition/run_state.py` (bounded retries, 3 attempts / 600s default, human-required failures never retried, unknown failures fail closed, no double delivery). It is pure logic tested in isolation; it is **not wired to the runner or any UI**, so last-success/coverage visibility is not built.

## Manual fallback
An approved folder or manual upload: operator drops the report plus a manifest (or the intake tool computes one) and `acquisition/intake.py` verifies it identically. No live email is sent. The folder location needs Goodwill approval.

## Production prerequisites (NOT claimed to exist)
A runtime that can run Chromium on a schedule, a session/credential policy approved by Goodwill, provider permission for automation, an owner for MFA/CAPTCHA prompts, monitoring of last success and coverage. Scheduled production capability is not delivered here.
