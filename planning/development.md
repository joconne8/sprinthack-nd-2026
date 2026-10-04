# ENG-01 runtime and team quick start

Runtime: Python 3.9+ with zoneinfo data. Locally verified on Python 3.9.6/macOS.
SQLite and HTTP libraries ship with Python; no install, production secrets or
paid service is needed. CI is configured for Python 3.9/3.12; remote CI has not
yet run. Node is absent locally, so TypeScript/client/browser builds were not
verified. This is the deliberate prototype exception documented in
`planning/decisions/architecture.md`.

From the repository root:

```sh
python3 -m goodwill_app init
python3 -m goodwill_app import \
  --csv 'data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv' \
  --manifest 'data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.manifest.json'
python3 -m goodwill_app metrics \
  --start-date 2026-09-30 --end-date 2026-09-30 --source upright_replica
python3 -m goodwill_app serve --port 8000
```

The checked-in example yields synthetic demo net sales `7127.78`. It is filtered
and uses Los Angeles source dates, so its coverage is partial. That warning is
intentional. `.runtime/` holds the ignored database/raw archive. Supply
`--state-root /your/local/directory` **before** the subcommand to isolate a run.

For the complete P0 source-period test, start Hugh's unchanged portal:

```sh
python3 'data ingestion/server.py' --port 4173
```

Select Upright, `paid_orders`, a 2026 period, **All** payment statuses, no filters,
and `America/Indiana/Indianapolis`. Download CSV and manifest; import those files
using the same command above. Keep the acquisition date controls separate from
the downstream reporting filter. The API converts timestamp reporting days to
America/New_York while retaining source dates/timezone. Tests cover a cross-zone
midnight. Cash Monkey's date-only/UTC source window can have partial edge days.

API locations for Landon:

```text
GET http://127.0.0.1:8000/api/v1/health
GET http://127.0.0.1:8000/api/v1/metrics?start_date=2026-09-30&end_date=2026-09-30&source=upright_replica
GET http://127.0.0.1:8000/api/v1/imports
GET http://127.0.0.1:8000/api/v1/evidence?start_date=2026-09-30&end_date=2026-09-30&source=upright_replica&run_id=ACTUAL_RUN_ID
```

Use the returned metric_run_id for drilldown. Preserve the response's filters,
definitions, partial/unavailable/null states and last-good warning. Financial
values are strings from this API; do not calculate different frontend totals or
fall back silently to mocks. Development CORS permits localhost/127.0.0.1:5173.
API errors and failed imports remain visible; inspect HTTP 422 batch bodies.

Hugh's full acquisition record can enter the same importer:

```sh
python3 -m goodwill_app import-intake --record /path/to/archive/runs/ACTUAL_RUN_ID.json
```

That record lacks original filter details, so its coverage remains conservatively
partial. Prefer the full portal manifest for full-source coverage. The partial
outbox stub is insufficient and rejected. No acquisition code was rewritten.

Optional DAT-07 inputs:

```sh
python3 -m goodwill_app load-inventory
python3 -m goodwill_app inventory --start-date 2026-08-01 --end-date 2026-08-31 \
  --snapshot-at 2026-08-31T23:59:59-04:00
```

That yields 1,443 August listing events and backlog 765 at the selected complete
snapshot. It does not supply September inventory or all-store physical coverage.

Verification:

```sh
python3 contracts/build_schemas.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s acquisition/tests -p 'test_*.py' -v
python3 reports/DAT-01/review_fixtures.py
python3 scripts/benchmark_data.py
```

The HTTP suite binds ephemeral loopback servers; sandbox permission may be
required. It drives actual portal HTTP generation/download and the data API,
but does not substitute for independent browser/UI acceptance. Existing fixture
regeneration tests overwrite fixtures; `scripts/verify_foundation.py` runs them
in a temporary git-archive extraction to preserve the working tree.

Handoff to Jack mc: derive an independent expected ledger, verify source-row sums,
alternate dates, repeat/overlap imports, corrections, malformed files, coverage,
and stale last-good warnings. P0 export is deferred. Landon's actual UI and
independent ENG-04/human integration remain the release checkpoints.
