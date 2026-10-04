# ING-07 constrained capture and drift repair (design only, P2/pilot; no live execution authorized)

## Capture (human-approved, bounded flow)
Record DOM role/name, labels, URL path (not query strings), and state transitions for one supported flow. Capture excludes: passwords, cookies, tokens, form values other than declared parameters (dates), and page text beyond control names. Redact before write; reject a capture containing patterns like secrets or personal data. A human reviews the generated skill JSON (same shape as `acquisition/skills/*.skill.json`) before it is saved or shared.

## Drift
Replay asserts expected role/name and page state at each step. On mismatch it stops with `label_changed`/`wrong_page` and does not guess. A repair is a proposed new skill version produced offline, shown as a diff to a human, and run against the replica or a validated environment before activation. A model may propose a repair but never auto-applies one to a financial flow.

## Options
Local runner with approved Chromium profile, or an approved browser extension; both need Goodwill security approval. Claims are limited to the bounded flow tested, not "record once, works everywhere".

## Test plan (not executed)
Secret-exclusion test on captures; replica label-change mode must pause execution (ING-01 already provides this mode); revalidation required after version bump.
