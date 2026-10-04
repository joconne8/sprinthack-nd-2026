# Goodwill reporting portal replicas

Working, screenshot-informed **Upright** and **Cash Monkey** reporting portals for the SprintHack@ND ingestion demo. Both use real HTML controls and generate actual CSV downloads. Every record is synthetic. Neither portal connects to Goodwill or a vendor.

## Start the website

From the repository root, run:

```sh
python3 "data ingestion/server.py"
```

Open **http://localhost:4173**. Python 3.9+ with timezone data is required; no Python packages, database, API keys, or model subscription are needed. Keep the terminal running. Stop it with Ctrl+C.

If port 4173 is already in use:

```sh
python3 "data ingestion/server.py" --port 4174
```

In an already approved Replit workspace, the equivalent command is `python3 "data ingestion/server.py" --host 0.0.0.0 --port 4173`; select that port in its web preview. This is a demo server, not a production deployment.

## Try the two flows

### Upright

1. Open **Upright**.
2. Click **Reports** in the top navigation.
3. Click **Paid orders** under Downloads in the left sidebar.
4. Set **Start date** and **End date** (default: September 30, 2026).
5. Optionally change timezone, channel, or payment status.
6. Click **Generate report**. The history displays Generating, then Complete.
7. Click **Download** on the new report. **Manifest** downloads verification metadata; **Preview** displays the first 20 rows and control totals.

**Paid order items** also generates a synthetic report. In this simplified fixture each Upright order has one item, so the two views have the same records but different declared grain/report type. No exact vendor export format is asserted.

### Cash Monkey / books

1. Open **Cash Monkey**.
2. Click **Reports** in the left sidebar.
3. Click **Orders** beneath Orders Reports.
4. Select **Order Date From** and **Order Date To**.
5. Optionally select accounts/channels or enter exact order IDs/SKUs. No account/channel selection means all.
6. Click **Submit** and wait for the CSV file link to appear.
7. Click the filename to download. The verification manifest and preview are separate controls.

Dates are inclusive. The replica supports all 2026 dates with a maximum of 31 days per request. Cash Monkey uses UTC. Upright applies the chosen reporting timezone to payment timestamps; the generated fixture timestamps are in afternoon/evening UTC, so supported US zones do not shift this fixture's date boundaries.

## Where the screenshots were used

Reference: screenshots supplied by Jack from the Goodwill presentation, October 3, 2026, captures at 20:55:37 through 20:56:26. These correspond to presentation pages 21–30 (Upright 1–6 and Cash Monkey 1–4).

| Reference | Replica behavior |
| --- | --- |
| Upright 1: Open Reports | Light header, operation cards, Reports navigation |
| Upright 2: Click Paid orders | Productivity overview, report sidebar and Downloads group |
| Upright 3: Set date range | Paid Order Report, dates, timezone, channel, payment-status controls |
| Upright 4: Generate report | Generation button, observable pending state and past-report table |
| Upright 5: Download | Completed report with an actual file download |
| Upright 6: Row count and daily summary | CSV rows and a preview that distinguishes orders from unique buyers |
| Cash Monkey 1: Open Reports | Black header, left navigation, illustrative console layout |
| Cash Monkey 2: Orders Report | Orders link beneath the report console |
| Cash Monkey 3: Select dates | UTC dates, account/channel multi-selects, order IDs, SKUs, CSV format and Submit |
| Cash Monkey 4: Download link | Generated CSV filename link after submission |

The presentation's margins, circled annotations, zoom buttons, and slide chrome are not part of the vendor UI. Exact fonts, hidden controls, authentication, network behavior, email delivery and production export schemas cannot be inferred from screenshots. Overview charts are labeled illustrative and are not calculated from the downloaded reports. Unimplemented menu items are non-interactive text; scheduling/debug/tax-export controls are omitted. This replica starts as a synthetic signed-in operator and never asks for credentials.

## Team integration and file contract

This is an isolated acquisition test target, not the downstream database/dashboard. Pass the actual downloaded CSV plus its manifest to your parser. No existing shared contracts, migrations, or fixtures have been modified. Existing `goodwill/synthetic-data/` files remain a separate dataset; do not combine these generated transactions with them without an explicit mapping.

- Upright: one row per paid order; IDs start `UP-YYYYMMDD-`. Key columns include `paid_order_id`, `paid_at`, `store_id`, `channel`, `buyer_id`, `gross_sales`, `refund_amount`, `net_sales`.
- Cash Monkey: one row per unit; IDs start `CM-YYYYMMDD-`. Deduplicate using `unit_id`, **not order_id alone**. Key columns include `order_id`, `unit_id`, `order_date`, `sku`, `quantity`, `item_revenue`, `refund_amount`, `payment_fee`, `payout_amount`.
- Each row includes `source_name`, `synthetic=true`, `grain`, `reporting_date`, `reporting_timezone`, and `currency=USD`.
- Demo net sales = item sales minus refunds, excluding shipping, tax and fees. The Cash Monkey `payout_amount` is a different figure that includes shipping and deducts fees.
- Paid means originally paid, including partially refunded orders. Refunded selects the partial-refund records. This is a declared demo rule, not a verified vendor rule.
- The manifest includes requested period, actual coverage, source/report, SHA-256, row/order counts, synthetic flag, monetary control totals and capture metadata. Row count is **not** a cross-platform unique-customer count.
- CSV bytes and their checksum are identical for the same filters. Manifest capture time changes between requests. A stable source-package ID derives from the CSV hash. The downstream importer still must implement duplicate and overlap protection; replay evidence does not prove it.
- A valid zero-row filter produces a header-only CSV, row count 0 and null actual coverage. This means no matches in the selected synthetic dataset, not a missing source.
- Reports remain in server memory, up to the latest 200 jobs; restarting clears report history. Downloads already saved to disk remain.

### Useful page routes and DOM controls

| Route | Purpose |
| --- | --- |
| `/` | Portal chooser |
| `/upright` | Upright home |
| `/upright/reports` | Reports landing/productivity |
| `/upright/reports/paid-orders` | Paid-order form |
| `/upright/reports/paid-order-items` | Paid-order-item form |
| `/cash-monkey` | Cash Monkey home |
| `/cash-monkey/reports` | Reports and Orders link |
| `/cash-monkey/reports/orders` | Orders form |

Use accessible names such as `Reports`, `Paid orders`, `Start date`, `End date`, `Generate report`, `Order Date From:`, `Order Date To:`, `Submit`, and `Download`. Both forms use `#start-date`, `#end-date`, `#report-form`, and `#generate-report`. Read `#messages` for pending/success/error state. Use the individual report row's download link, rather than a stale historical download. `replay.cjs` demonstrates this.

### Local helper API

These are **our replica's** endpoints, not vendor APIs. Browser automation should exercise the UI to prove acquisition.

- `GET /api/health`
- `POST /api/reports`: source (`upright` or `cash_monkey`), report_type, start_date, end_date, timezone, optional channels/accounts/order_ids/skus/payment_status, format `CSV`, mode. Returns 202 and a pending job ID.
- `GET /api/reports/{id}`: pending, ready or failed.
- `GET /api/reports/{id}/download`: CSV only after ready; 409 otherwise.
- `GET /api/reports/{id}/manifest`: manifest only after ready.
- `GET /api/reports`: in-memory job history.

## Deterministic browser replay (optional)

The website itself does not need Node. The included automation uses Playwright without Jev or model calls.

Install the optional browser-test dependencies from this folder:

```sh
cd "data ingestion"
npm install
npx playwright install chromium
```

Leave the Python server running in another terminal, then run:

```sh
node replay.cjs upright 2026-09-30 2026-09-30
node replay.cjs cash_monkey 2026-10-01 2026-10-01
npm run test:browser
```

Replay saves verified CSVs and manifests under ignored `artifacts/`. It checks the actual downloaded bytes, required headers, dates in every row, row count, requested period and SHA-256. It stops on DOM drift or failed requests. Replay is limited to loopback URLs to keep it targeted at the local synthetic site.

To use installed Chrome instead of downloading Chromium, set `CHROME_PATH` to its executable. `BASE_URL` selects another localhost port and `OUTPUT_DIR` changes the artifact directory.

## Failure demonstrations

Click **Test controls** in the top banner. Scenario persists in this browser tab until changed:

- Normal: brief pending state, then ready.
- Delayed generation: six-second pending state.
- Missing report: failed state with no download.
- Expired demo session: request rejected with a visible message. Select Normal to resume; this does not imitate real authentication.
- Changed Generate label: button changes to Build export. The baseline replay deliberately stops rather than guessing at a changed workflow.

Reversed dates, unsupported years, ranges over 31 days and unsupported API parameters are rejected. These are demo behaviors, not claims about the real portals.

## Tests

From the repo root:

```sh
python3 -m unittest discover -s "data ingestion/tests" -p "test_*.py" -v
```

There are nine Python tests covering fixed control totals, file fingerprints, dates, filters, unit grain, invalid input, asynchronous availability, missing reports, expired sessions and page routes. The browser suite exercises both journeys and verifies actual files, delayed readiness, drift, negative states and mobile layouts. See `VERIFICATION.md` for the run performed for this change.

## Limits and next handoff

The replica does not implement a recorder, Jev, live login, email, vendor APIs, database ingestion, reconciliation against Goodwill's workbook, accounting posting, or a management dashboard. No paid services are added. The next team task is to connect the verified CSV to the approved parser/importer and show the dashboard using that exact file. ING-01's replica portion is reviewable; this does not complete ING-02/03 or the full acquisition-to-dashboard PRD.
