# DAT-09 synthetic operations and backfill design

```text
Acquire → verify → archive → parse/validate → stage → reconcile → curate → publish
                                     ↘ rejected rows and human exceptions
```

The local importer executes dependent stages in one supervised command. No
scheduler, unattended job, paid orchestrator or production pilot is started.
Hugh owns retrieval retries/session handling; repeated delivery is safe at the
data identity layer. Authentication/provider restrictions require human action.

Raw bytes are immutable; parser/rule/metric versions are recorded. Replays and
overlap imports preserve published values. Corrections require an explicit
`--allow-corrections` operator choice and create superseding source-key versions.
Late refunds revise their original sale's as-of value, not an invented cash-flow
date. Backfill a declared source period; inspect reconciliation and old/new run
evidence. New keys outside the source period are rejected. Missing records do
not imply deletion; tombstone/full-replacement semantics need a new contract.

Publication is one transaction. Validation/control failure preserves last-good
rows, exposes rejected originals and marks the metric response stale/partial.
An unexpected process failure rolls back database mutations. An orphan raw
archive file can remain; an operator should investigate it before cleanup.
Recovery means retaining evidence, correcting the source/manifest, re-verifying
the exact bytes and rerunning under explicit rules, never disabling checks.

Prototype ownership: Peyton maintains parsing/mapping/metric rules, Hugh owns
synthetic acquisition, Landon renders warnings, Jack OC integrates, Jack mc
independently checks. Goodwill's production on-call/retention/session owners are
unconfirmed and cannot depend on the departed e-commerce manager.

Benchmark command: `python3 scripts/benchmark_data.py`. It measures imports,
scoped queries and duplicate replay for 650/1,800/900 declared synthetic rows in
one local process with temporary SQLite. Results and actual machine/runtime are
in `reports/integration/logs/benchmark.json`. They are not a production forecast.
Pilot validation must establish latency/volume budgets, alert routing, backup
restore, concurrency and retention with the client. No guaranteed runtime/ROI
or new database purchase is inferred.
