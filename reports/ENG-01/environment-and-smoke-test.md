# Environment and smoke evidence

Python 3.9.6 is installed; Node is absent. Python standard-library SQLite/zoneinfo/
HTTP code runs without dependency installation. CLI init, example import and
metrics commands passed; see `../integration/logs/cli-*.json` and verification.
HTTP tests bind temporary loopback servers and passed with sandbox escalation.
Their earlier sandbox-only bind failures were not treated as code defects or
passing tests. CI is configured, but remote CI has not run.

`planning/development.md` is the actual runtime guide. No invented npm/build
command, browser availability, React compilation or production hosting claim.
