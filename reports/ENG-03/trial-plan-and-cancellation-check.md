# Overnight trial and cancellation

Implementation: scripts/release/overnight.py. Configuration mapping approved by Peyton's request
for overnight code execution; no second runner stack or coding agent is introduced.
Three executable tests cover explicit Eastern-to-UTC deadline conversion/naive rejection,
cancelled or expired jobs never starting, and killing a long-running child process group while
retaining its log. They are part of the full release suite. See ../release/verification.json.
Actual overnight status is local .runtime/overnight/status.json and is not fabricated here.
No future cycle is claimed as passed. Peyton reviews failures and the team reviews release acceptance.
