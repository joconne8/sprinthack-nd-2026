# Sample data that produces the Aimsigh dashboard

All records are fictional. These September 2026 source files use the same stable
IDs and amounts as the local Upright/Cash Monkey report portals. The original
August synthetic pack is unchanged. MANIFEST.json pins these sample bytes.

| Input | Grain | Rows | Classification |
|---|---|---:|---|
| upright_september.csv | One paid order | 3,840 | Synthetic portal sales |
| cash_monkey_september.csv | One unit (900 distinct orders) | 960 | Synthetic portal sales |
| labor.csv | Source/store/day | 1,440 | Invented matched labor allocations |
| shipping.csv | Source/sales record | 4,800 | Invented $3.50 expense per record |

Source fee columns are synthetic report values. Labor is 2 hours per Upright
store/day through September 23 and 3 hours afterwards; Cash Monkey is 0.5 hours
per store/day. Labor costs use an invented $20/hour. There is no platform labor
allocation. Contribution excludes overhead, payroll burden and tax, so it is
not production net margin. Upright uses Eastern payment dates; Cash Monkey uses
UTC order dates, without invented intraday timestamps.

Full-month expected controls: net sales **254059.40**, fees **26240.14**,
shipping expense **16800.00**, labor **1968.00 hours**, modeled labor cost
**39360.00**, demo contribution **171659.26**.
September 17–23: **60727.56 / 420.00 hours = 144.59 USD/hour**.
September 24–30: **61706.64 / 588.00 hours = 104.94 USD/hour**.

`demo prepare` imports September 1–29 into an isolated SQLite state and loads
these auxiliary CSVs. Teaching September 29 and replaying September 30 completes
the month using actual browser downloads. `demo prepare --checkpoint` imports
the pinned full-month sample source files for verified recovery. The dashboard,
workbook, and model-free answers all query published snapshots of that state.

Financial values are computed from the files, not embedded in the UI. Independent
controls live in tests/test_showcase.py. Sample expenses/settlements and overlapping
sales feeds are excluded from combined revenue. Any changed sample byte requires
an explicit new fixture manifest/version; silently altered inputs are rejected.
