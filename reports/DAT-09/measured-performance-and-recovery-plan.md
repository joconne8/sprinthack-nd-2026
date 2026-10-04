# Synthetic measurement and recovery

Fresh merged-foundation/completion benchmarks are in
`../integration/completion-logs/benchmark.json`; backfill/reprocessing regressions
are in `completion-logs/foundation-tests.log`. All declared source sizes imported
successfully and replayed as duplicate no-ops. Earlier benchmark logs below are
historical; neither measurement implies production throughput or pilot approval.

Actual benchmark results: `../integration/logs/benchmark.json`; conditions are
Python 3.9.6, macOS arm64, one process, temporary local SQLite, 650/1800/900
synthetic source rows. Imports, query and duplicate replay timings are measured
separately; no production latency/throughput guarantee follows.

Late-refund backfill changes only the intended source key/period and preserves
old runs. Reprocessing the corrected bytes is a duplicate no-op with identical
values. Atomic rollback and rejected-row/last-good recovery are tested.
`planning/data-operations.md` defines DAG, operator recovery and ownership gaps.
No scheduler, live pilot, credentials, alert service or unattended job is started.
