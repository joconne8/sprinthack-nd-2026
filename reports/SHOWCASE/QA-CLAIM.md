# Independent showcase QA claim

Operator/session: showcase_qa under Codex/Peyton's approved showcase implementation.
Branch/worktree: peyton/aimsigh-showcase, /private/tmp/aimsigh-showcase; base 3a8c734.
Lane: tests/test_showcase*.py, tests/showcase*.cjs, scripts/verify_showcase.py,
reports/SHOWCASE/QA*. No backend, contracts, migrations, UI or presentation edits.
Contract: reports/SHOWCASE/CONTRACT.md, showcase-v1. Deadline: October 5, 10am
Eastern; local tools only, zero paid/model calls. Maximum two repairs per failing
verification before reporting to the root integrator. Existing ledgers preserved.

Independent expected controls:

* Handwritten two-sale ledger: item sales 30 less refunds 3 = net 27; fees 3;
  shipping 7; one store-hour 1 at $20 = labor 20; contribution -3, margin -11.11%.
  Shipping, tax and supplied `net_sales` columns are deliberate decoys.
* September 17–23: 60727.56 sales, 420 modeled hours, 144.59 per hour.
* September 24–30: 61706.64 sales, 588 modeled hours, 104.94 per hour.
* September month independently inspected from downloaded-format portal CSV:
  Upright 3840 orders, 210273.10 net, 21681.06 fees; Cash Monkey 960 units,
  900 orders, 43786.30 net, 4559.08 fees. Combined net 254059.40.
* September 30: Upright 128 orders, net 7127.78; Cash Monkey 32 units and
  30 orders, net 1654.59.

Tests cover input/publication immutability, grain fanout, missing/zero inputs,
platform allocation unknown, coverage, non-sales source exclusion, read-only
supported questions, actual workbook cached formula values, and the real browser
record/review/approve/replay/export/question flow. Outcomes belong in QA-RESULT.
