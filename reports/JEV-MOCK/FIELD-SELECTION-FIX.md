# Field selection repair

User authorized repairing the observed low-confidence run and calling Jev again.
Evidence: .runtime/jev-mockup/2026-10-04T17-01-17-466Z-23439/result.json
and trace.jsonl. Actual Jev selected End date correctly but confidence 0.86
failed the 0.90 gate after four calls.

Change: provider receives explicit action and requested_field_label for fills and
selects. Instructions distinguish field identification from value/date reasoning,
require literal label matching, and explain that equal current dates do not make
Start date and End date interchangeable. Thresholds remain 0.90; no retry added.

Checks: Node provider suite 8/8 passed, including request construction for two
fields with identical dates. Browser regression log:
/private/tmp/jev-field-fix-browser.log (injected responses; not Jev accuracy).

Live retry blocked: TYPESAFE_API_KEY is absent from the agent tool environment.
The user's terminal export is not inherited. No secret files/history were read,
no credential copied, and no actual API call made by this repair session.
User can rerun the same command in their already configured terminal; confidence
improvement remains unverified until that real run's evidence is inspected.
