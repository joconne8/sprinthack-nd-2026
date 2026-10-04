# Environment and smoke evidence

Completion session: Python 3.9.6/macOS arm64, temporary official Node 22.14.0,
TypeScript 5.6.3, Playwright 1.62.1 and installed Chrome. Strict client build,
client boundary tests and real browser download/intake/import/API/archive/replay
checks passed. See `../integration/completion-verification.json` for commands,
timings, file hashes and logs. Node was downloaded to `/private/tmp` and checked
against the [official release checksums](https://nodejs.org/dist/v22.14.0/SHASUMS256.txt):
`e9404633bc02a5162c5c573b1e2490f5fb44648345d64a958b17e325729a5e42`.
The separate verification tools have a reproducible package manifest/lockfile.
The API still requires no npm dependency or production secret. CI now includes
strict client and browser-handoff jobs; remote results are not claimed.

The browser skill returned 128 and 256 rows for separate requested periods.
Downloaded CSV → unchanged verified intake → importer → metric/evidence API →
raw-file download preserved the checksum/bytes. Its filtered source scope does
not claim complete-source coverage. Expired sessions fail explicitly. Browser
runtime verification does not prove Landon's product UI or live source fidelity.

Original foundation environment observation follows.

Python 3.9.6 is installed; Node is absent. Python standard-library SQLite/zoneinfo/
HTTP code runs without dependency installation. CLI init, example import and
metrics commands passed; see `../integration/logs/cli-*.json` and verification.
HTTP tests bind temporary loopback servers and passed with sandbox escalation.
Their earlier sandbox-only bind failures were not treated as code defects or
passing tests. CI is configured, but remote CI has not run.

`planning/development.md` is the actual runtime guide. No invented npm/build
command, browser availability, React compilation or production hosting claim.
