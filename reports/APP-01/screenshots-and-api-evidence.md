# Operations UI and API evidence

[Operations screenshot](../takeover/browser/operations.png) shows requested dates, expired-session owner, last success, separate collection/import/publication, bounded attempts, imports and nine-source map. [Mobile screenshot](../takeover/browser/mobile.png) demonstrates the responsive leadership state after a failed import.

Actual API: POST/GET /api/v1/acquisition-runs, GET run by ID; POST /api/v1/imports; GET imports/batch/staging/source-row; POST batch resolutions; GET original file and stored source manifest. The existing API server serves the UI at /.

[Browser regression](../takeover/logs/dashboard-browser.log) exercises successful collection, alternate dates, repeat no-op, expired session, manual upload, malformed-checksum import, last-good warning and API outage. [Checksum chain](../ING-03/checksum-chain.json) records run→batch→manifest→original archive identity. Backend reconciliation/audit negatives are in [developer regression](../takeover/logs/developer-regression.log).

Collection, verification, import and publication are distinct. A downloaded file does not imply publication. Bad imports preserve last-good metrics; review links expose controls and rejected original rows. There is no mock fallback on API failure. Human/Jack mc independent acceptance remains pending.
