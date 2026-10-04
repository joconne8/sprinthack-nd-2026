#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export NODE_PATH="$PWD/tools/verification/node_modules"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PWD/.runtime/playwright-browsers}"
if [[ -z "${CHROME_PATH:-}" ]] && command -v chromium >/dev/null 2>&1; then
  export CHROME_PATH="$(command -v chromium)"
fi
exec node experiments/jev/hosted/server.cjs
