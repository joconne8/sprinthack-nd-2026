# Hosted Jev demo result

Implemented in experiments/jev/hosted/: server.cjs, index.html, app.js, setup.sh,
start.sh, replit.example.toml, replit.example.nix, README.md, server.test.cjs,
smoke.test.cjs and package.cjs; experiments/jev/README.md links setup. Shared portal,
runner, contracts, lockfiles and dashboard unchanged. Branch observed
peyton/aimsigh-showcase; all experiment/report files remain uncommitted.

Hosted proxy exposes one public server, password auth, same-origin/session checks,
one active predefined replay/Jev run, five admitted run attempts per process by
default, screenshots, approved drift repair and verified CSV/manifest/trace.
Python portal/internal lab listen only on loopback. Keys remain server-side.
Missing credentials are visible; no model fallback. Per-run provider cap remains
20 requests/60 seconds/no retries. Download revalidates content/checksum.

Commands actually run: node --check server.cjs/app.js/smoke.test.cjs;
bash -n start.sh/setup.sh; server.test.cjs against isolated port 4187 (exit 0);
full-startup browser smoke script against public test port 3195 (exit 0 after
one mobile-layout repair); package.cjs; git diff --check. Mac test runtime used
Node 22.14, existing Playwright and installed Google Chrome. No live API calls.

Evidence: /private/tmp/jev-hosted-tests.log (four PASS scenario groups);
/var/folders/1t/r8vbq2ns31z3ld8d_36zw3s40000gn/T/jev-hosted-tests-PizRQ3;
/private/tmp/jev-hosted-smoke.log; .runtime/jev-hosted-preview.png;
/private/tmp/jev-hosted-smoke.csv. Independently expected128/256 rows and checksums
passed; API tests are explicitly injected-test-only. Full UI replay produced
verified256-row download, screenshots and mobile layout. Startup/shutdown passed.
Temporary test processes stopped; user's original lab/portal not stopped.

Upload bundle .runtime/jev-replit-demo.zip contains explicit source allowlist,
root Replit examples and no .env/key/runtime artifacts/node_modules. Rebuild with
node experiments/jev/hosted/package.cjs. Source setup includes Replit ports/Secrets
and official Playwright dependency references.

Limitations: not deployed; no Replit account access used; Linux/Nix/Replit browser
libraries and live API reliability/speed require target-host rehearsal. Runtime
files temporary, run cap resets on restart, one shared presenter state, latest
artifact only. Basic auth requires HTTPS on public hosting. No real Upright
integration, dashboard publication, production readiness, purchase, merge or
external message claimed.
