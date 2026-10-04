# Replica verification

Run October 3, 2026 on macOS with Python 3.12, Node and Playwright 1.62.1, using installed Google Chrome. These results verify the replica, not the real vendor portals or the downstream importer.

## Commands actually run

```sh
node --check "data ingestion/static/app.js"
PYTHONDONTWRITEBYTECODE=1 /Users/jack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s "data ingestion/tests" -p "test_*.py" -v
```

With the replica server running, from `data ingestion`:

```sh
NODE_PATH=/Users/jack/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" node tests/browser.test.cjs
```

The absolute runtime paths above describe the actual verification environment, not requirements for teammates. Portable commands are in README.md.

## Results

- JavaScript syntax check: pass.
- Nine Python artifact/API tests: pass.
- Ten browser verification groups: pass.
- Actual Upright CSV: 128 rows / 128 orders for September 30.
- Alternate Upright October 1–2 request: 256 rows, matching inclusive date coverage and a different checksum.
- Repeated identical acquisition: byte-identical CSV.
- Cash Monkey CSV: 32 unit rows / 30 orders; unit IDs unique.
- Downloaded CSV checksum, manifest, every row's synthetic flag and reporting date: pass.
- Delayed generation, missing report, expired session, changed label stopping replay and reversed dates: pass.
- Mobile horizontal overflow checks at 390px: pass.
- Browser JavaScript error list: empty.
- Desktop Upright, desktop Cash Monkey and mobile form screenshots visually inspected: readable, no clipped controls or overlapping content.

## Review artifacts

- `examples/`: actual CSVs and verified manifests acquired by browser replay.
- `docs/upright-report.png`: generated report, history/downloads and preview.
- `docs/cash-monkey-report.png`: orders form, generated link and preview.
- `docs/portal-chooser.png`: website entry screen.
- Complete per-run browser artifacts remain local under ignored `artifacts/browser-tests/` and can be regenerated.

## Material limits

No vendor session/API, inbox/email, Jev, universal recorder or business-system integration was tested. No dashboard or database import exists in this patch, so no downstream duplicate/reconciliation claim is made. Shared source/metric contracts and task predecessor acceptance remain for the human integrator. Sample fixture timezones are applied, but their afternoon/evening UTC timestamps do not exercise cross-midnight changes. Overview charts are illustrative. This is ready for replica review, not production acceptance.
