# Contract examples

Every file here is **illustrative synthetic data**. Checksums such as `aaaa…` are placeholders and do not refer to real files.
The numbers are not an expected-results ledger. QA derives expected values independently from source CSVs.

The file name prefix is the definition the file must validate against. For example, `MetricResult.available.json` validates against `#/definitions/MetricResult`.

## valid/

Frontend mocks, tool tests and backend contract tests share these fixtures. They tell one story:

| Date | What happened |
| --- | --- |
| 2026-09-30 | Imported cleanly (`batch-20260930-0001`). A byte-identical re-import is a `duplicate_noop`. A revised export raised two refunds (`late-correction`). |
| 2026-10-01 | Imported with two rejected rows (a duplicate key and a missing `paid_at`). Still reconciled. |
| 2026-10-02 | Not acquired. The session expired, so the run `needs_human`. That makes the 09-30..10-02 metric `partial`. |
| 2026-10-03 | A newer file has an unparseable amount and is `unreconciled`, so the metric shows the last good version (`stale_last_good`). |
| 2026-10-04 | The report stayed unavailable after three attempts (`failed_retriable_exhausted`). |

Labor productivity is `unavailable` because no labor input exists. Seven of the nine sources are `not_connected` and are listed in the coverage example.

## invalid/

Each file is one valid example with exactly one thing broken:
- **Wrong values:** a Los Angeles timezone, `synthetic: false`, or money written as a JSON number.
- **Missing pieces:** a `needs_human` run without an owner, or a duplicate import without its reference.
- **Dishonest states:**
  - an "unavailable" metric showing `0.00`
  - an "available" metric with no value
  - an "available" metric with partial coverage
- **Inconsistent totals:**
  - a red/green target field
  - an unbalanced "reconciled" import
  - drilldown totals that contradict the displayed value
- **Misused records:** a run recorded for a source that isn't connected, or a write tool.
