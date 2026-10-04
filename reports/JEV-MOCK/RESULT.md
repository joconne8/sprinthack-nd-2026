# JEV-MOCK — ready for review

Branch: peyton/jev-mockup; base 3a8c734. Uncommitted standalone diff.
Files: experiments/jev/mockup.cjs, experiments/jev/README.md,
reports/JEV-MOCK/CLAIM.md and this report. Existing acquisition code unchanged.

Verified with the prior project's Node 22.14.0/Playwright runtime in
/private/tmp/goodwill-completion-tools and installed Google Chrome.

Actual commands/results:
- `node --check experiments/jev/mockup.cjs` using that runtime: pass.
- Local `data ingestion/server.py --host 127.0.0.1 --port 4187`: started.
- Mockup `2026-09-30`: exit 0, downloaded CSV, checksum matched manifest,
  128 records. Trace reports 2108 ms total (mock prototype measurement only).
- Mockup `2026-09-30 --mode session-expired`: expected exit 1, expired_session,
  no downloaded CSV.
- Independent Python csv reader: 128 rows confirmed; failure artifact has no CSV.
- `git diff --check`: pass.

Logs: /private/tmp/jev-mock-success.log, /private/tmp/jev-mock-failure.log.
Durable local evidence: .runtime/jev-mockup/*/{trace.jsonl,result.json},
successful run's synthetic CSV. These artifacts are not committed.

Limits: no actual Jev model, model calls, live data, import or dashboard publication.
Headed presentation mode and other portal failures were not tested this session.
Plain node/npm were absent from PATH; default install attempt could not run.
Remote issue reads returned 404; no issue claim/update or acceptance is asserted.
User expressly authorized this standalone mockup after the earlier blocker report.
