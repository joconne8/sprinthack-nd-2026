# P0 source drilldown reconciliation

The actual browser flow opens M-DEMO-NET-SALES from the leadership card and retains its metric_run_id plus source/date/platform/store scope. The evidence API scope total and displayed value both equal 7127.78 for Upright replica on 2026-09-30. Evidence paginates 128 rows, including asserted rows 51–100, and opens an original paid_order_id source row.

[Evidence screenshot](../takeover/browser/source-evidence.png), [browser log](../takeover/logs/dashboard-browser.log) and [checksum chain](../ING-03/checksum-chain.json) capture the path to the same acquired CSV. The browser hashes the downloaded original file and checks equality with acquisition run, imported raw-file checksum and stored source manifest; acquisition_run_id and All payment-status metadata survive delivery.

The drawer identifies original file, batch/source row, parser/rule versions and rejection/reconciliation links. Evidence queries are pinned to the displayed metric run; an obsolete request cannot replace a new selection. Backend source-row sums/immutability/failed publication are covered by developer regression and the unchanged independent backend QA on the baseline.

P1 workbook export is deferred; no export artifact or malicious-cell test is claimed. Raw CSV/manifest downloads are source evidence, not a transformed financial workbook or Business Central import. Jack mc must supply independent browser/financial acceptance on the reviewed UI commit.
