#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
npm ci --prefix tools/verification --ignore-scripts --no-audit --no-fund
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PWD/.runtime/playwright-browsers}"
if ! command -v chromium >/dev/null 2>&1 && [[ -z "${CHROME_PATH:-}" ]]; then
  node tools/verification/node_modules/playwright/cli.js install chromium
fi
printf '%s\n' 'Chromium installed. On Linux, run Playwright install-deps chromium if system libraries are missing.'
