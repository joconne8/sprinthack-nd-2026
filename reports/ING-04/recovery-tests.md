# Bounded acquisition recovery evidence

The actual commands and exit codes are in [verification](../takeover/verification.json). All owned checks passed; independent UI acceptance remains pending.

| Case | Observed/asserted behavior | Evidence |
|---|---|---|
| Transient delay | Bounded retry reaches one real import, two attempts maximum | developer-regression.log; test_acquisition_controller |
| Repeat submission/collection | Existing delivery batch reused; new replay is duplicate_noop | acquisition-tests.log; dashboard-browser.log |
| Expired session | One attempt, needs_human, not_submitted, actionable operator | dashboard-browser.log; operations.png |
| Password/MFA/CAPTCHA/access denial | Human-required typed failure, no bypass | browser-negatives.log; acquisition-tests.log |
| Missing report, wrong page, changed label | Dedicated typed failures, no publication | browser-negatives.log |
| Deadline | Actual delayed browser stops under one-second test deadline | browser-negatives.log |
| Invalid dates, off-host, busy run | Fail before unauthorized collection | browser-negatives.log; developer-regression.log |
| Tampered download/archive | Verification fails; no import/publication | developer-regression.log; acquisition-tests.log |
| Interrupted process | Pending run becomes needs_human on restart; completed batch retained | developer-regression.log |
| Failed manual import | Failed batch visible; last-good value retained with warning | dashboard-browser.log; mobile.png |

Paths above are relative to reports/takeover/logs or reports/takeover/browser. See [runbook](../../planning/operations/acquisition.md) for manual fallback and production prerequisites. There is no active production scheduler/email connection.
