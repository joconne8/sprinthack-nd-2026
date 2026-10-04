# Hosted synthetic Jev demo

A password-protected date-driven runner. It starts the synthetic Python portal
on an internal loopback port and Chromium headlessly, then exposes one public
web page. Jev makes actual DOM decisions when selected. Replay is explicitly
model-free. No recorder, embedded video, real Upright connection or automatic
import is exposed. Downloaded CSV, manifest and trace remain available only after
verification; damaged artifacts are rejected again when downloaded.

## Replit setup

Use the generated `.runtime/jev-replit-demo.zip` to upload/extract the current
files into a Replit Node/Python project, or copy these files with their repository
paths. These changes are local and uncommitted: importing the current GitHub
branch alone will not include them. The ZIP contains no credentials, runtime
artifacts or node_modules and includes root `.replit`/`replit.nix` examples.

When using the full repository, copy `replit.example.toml` to root `.replit` and
`replit.example.nix` to root `replit.nix`. Preserve any existing Replit configuration
by applying the equivalent run/build/port changes manually. Use Node 22+, Python
3.11+ and Linux Chromium. The Nix example includes Chromium and its libraries;
start.sh detects system Chromium. Otherwise setup.sh installs Playwright Chromium;
missing Linux libraries must be installed with Playwright's `install-deps chromium`
or your Replit environment's dependency configuration. No Mac CHROME_PATH on Replit.

In **Replit Secrets**, set:

| Secret | Value |
| --- | --- |
| TYPESAFE_API_KEY | Your private Jev API key |
| DEMO_PASSWORD | A unique random password of at least 16 characters |
| HOSTED_MAX_RUNS | Optional; defaults to 5 admitted run attempts per server process |

Run once in the Replit shell:

```sh
bash experiments/jev/hosted/setup.sh
```

Press Run, or execute:

```sh
bash experiments/jev/hosted/start.sh
```

Open Preview in a separate browser tab if the embedded preview cannot show the
browser's HTTP Basic login prompt. Sign in with username **demo** and DEMO_PASSWORD.
Select dates, mode **Jev**, scenario **Normal**, and Run report. The page shows
actual screenshots, model calls/tokens, decisions and verification. Download both
CSV and manifest for the existing import workflow. Do not submit a live run before
configuring a key and accepting the displayed 20-call/60-second per-run budget.

For adaptation: run Replay with changed-label to show its stop; run Jev on the same
scenario and approve Build export within 15 seconds if confidence passes. Jev may
stop on confidence/API failure; no hidden replay substitution. The API chooses
controls, never the dates, report identity, financial rules or allowed browser host.

## Publishing and rehearsal

Prepared for one Reserved VM instance so a browser job and the in-memory evidence
stay with one process. Do not use static hosting or multiple instances. The code
binds the public server to `0.0.0.0:${PORT:-3000}`; expose only that port (3000 → 80
in the example). Both internal services remain loopback-only; never expose them
through Replit port forwarding. Replit Secrets must also be configured for the
published app. Browser authentication belongs behind Replit HTTPS.

Publishing has not been performed or validated from this workspace. Test Chromium,
Python timezone data, the model API, the screenshot stream and downloads inside
Replit before presenting. Actual Replit resource compatibility and live Jev speed
remain unverified. Configuration examples are reviewable templates, not a claim
that Replit publishing succeeded. No purchases or deployment are performed here.

Artifacts under `.runtime/jev-hosted/` are temporary; download evidence before a
restart. Only the latest completed run is offered. A new/failed run removes access
to the previous file. Run cap counts admitted attempts, including invalid inputs,
and resets on restart; it is a rehearsal limit, not an account-wide billing limit.
One active run per instance, at most 20 model requests/60 seconds, no automatic
API retries. Missing credentials fail visibly. The UI never receives the provider
key or password. Source/DOM content remains untrusted. Authenticated operators
share one demo state: use one presenter, not a multi-user pilot.

## Verification

```sh
# Synthetic portal in a separate test terminal:
python3 "data ingestion/server.py" --host 127.0.0.1 --port 4187
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/hosted/server.test.cjs
# Starts/stops its own internal portal and public test server on port 3195:
NODE_PATH="$PWD/tools/verification/node_modules" node experiments/jev/hosted/smoke.test.cjs
```

Server tests use labeled injected Jev responses, not external API calls. They
verify authentication, CSRF, route restrictions, simultaneous-run rejection,
128/256 row counts, hashes, CSV/manifest/trace downloads, checksum rejection,
approved drift repair, expired sessions and the process run cap. Smoke test uses
replay and checks full startup, missing-key UI, screenshots, browser download,
mobile layout and shutdown. Neither test proves live Jev quality or Linux hosting.

References: [Replit ports](https://docs.replit.com/features/project-setup/ports),
[Replit Secrets](https://docs.replit.com/core-concepts/project-editor/app-setup/secrets),
[Playwright browser dependencies](https://playwright.dev/docs/browsers#install-system-dependencies).
