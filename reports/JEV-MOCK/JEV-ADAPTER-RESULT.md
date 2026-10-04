# Jev adapter — ready for review

Branch: peyton/jev-mockup. Base: 3a8c734c91a9c86494eb646ec5c9356e220f563e.
Changes remain uncommitted; no merge, deployment, or issue acceptance is asserted.
Authorization: user's explicit Jev-assisted reporting implementation plan.

Changed files: experiments/jev/mockup.cjs, README.md, provider.cjs, dom.cjs,
run.cjs, verify.cjs, provider.test.cjs, browser.test.cjs; reports/JEV-MOCK/CLAIM.md
and this report. Shared acquisition runner, portal and contracts unchanged.

Implemented: explicit Jev mode, official pinned API/model, bounded DOM candidates,
0.90 confidence/probability gates, stale-target checks, deterministic parameter and
report invariants, real CSV/checksum/content verification, manifest handoff,
redacted transport logging, token usage and timing. No automatic API retries or
silent fallback. Provider caps: 20 calls/60 seconds; browser retains 40-second cap.

Actual verification used existing Node 22.14.0 and Playwright in
/private/tmp/goodwill-completion-tools plus installed Google Chrome:

- `node --test experiments/jev/provider.test.cjs`: 7 passed.
- `node experiments/jev/browser.test.cjs` with local portal on 4187:
  10 scenario groups passed; injected responses only, no external API calls.
  Independent expected row counts: September 30 = 128;
  October 1–2 = 256. Python CSV reader checked actual downloaded rows.
- Browser scenarios: normal, alternate dates/changed label, delayed generation,
  deterministic changed-label stop, expired session, missing report, reversed
  dates, low confidence, hidden/disabled candidates and stale target rejection.
  Wrong CSV dates and checksum mismatch were rejected.
- Missing-key CLI: emitted missing_credentials and no model call.
- Default model-free CLI regression: exit 0, 128-row CSV verified with
  checksum, date and synthetic-row checks; log /private/tmp/jev-default-cli.log.
- `node --check` for mockup.cjs and run.cjs: pass.
- `git diff --check`: pass (new files are untracked).

Evidence: /private/tmp/jev-provider-tests.log, /private/tmp/jev-adapter-browser.log,
/private/tmp/jev-browser-tests/results.json, /private/tmp/jev-missing-key.log.
CLI artifacts: .runtime/jev-mockup/. Synthetic browser CSVs:
/private/tmp/jev-browser-tests/.

Sources: dev/JEV JEV PLAN and development guide read during research;
https://docs.typesafe.ai/api, /models, /model-jaggedness/jev-1.13.

Outstanding: actual Jev API evaluation awaits secure key and explicit testing
budget. Injected fixtures do not prove Jev accuracy, calibration or adaptation.
Headed mode was not tested. Real Upright, recorder UI, automatic importer/dashboard
integration and production access remain outside this patch. Human review and
issue coordination remain outstanding; remote GitHub reads previously returned 404.
