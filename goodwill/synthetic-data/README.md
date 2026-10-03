# Goodwill Synthetic Source Data

All files in this folder are synthetic demo data. They do not contain real Goodwill, marketplace, customer, employee, vendor, or accounting records.

Reporting period: August 2026

The files model the nine source workflows named in the SprintHack deck:

1. Cash Monkey orders
2. Upright paid order items
3. Jewelry report
4. OSM / Pitney Bowes / EasyPost shipping activity
5. FedEx charges and refunds
6. ShopGoodwill periodic reports
7. Goodwill Books payment statement
8. eBay listing sales report
9. Amazon payments summary

## Suggested Uses

- Build upload adapters by source.
- Normalize sales, refunds, fees, shipping, and payout fields.
- Produce daily revenue and customer counts by marketplace.
- Track source readiness for month-end close.
- Generate a proposed Business Central journal export.
- Test exception handling and reconciliation logic.

## Seeded Test Conditions

- `01_cash_monkey_orders_aug2026.csv` includes a refunded order.
- `02_upright_paid_order_items_aug2026.csv` includes one missing `buyer_id`.
- `03_jewelry_report_aug2026.csv` includes one unconfirmed supplier row.
- `04_shipping_osm_pb_easypost_aug2026.csv` includes one postage adjustment.
- `05_fedex_charges_refunds_aug2026.csv` includes refunds netted against charges.
- `06_shopgoodwill_periodic_reports_aug2026.csv` includes one row with missing `store_id`.
- `07_goodwill_books_payment_statement_aug2026.csv` includes one partial refund.
- `08_ebay_listing_sales_aug2026.csv` includes one relisted item.
- `09_amazon_payments_summary_aug2026.csv` includes one returned order.

## Demo Metric Conventions

For a weekend prototype, use these synthetic conventions unless a mentor gives better definitions:

- Net revenue = gross/item/product sales plus shipping credits or collected shipping, less refunds.
- Customer count = distinct non-empty buyer IDs by platform and day.
- Fees are tracked separately from net revenue unless building a profitability view.
- Shipping expense files should reconcile to source/provider totals, not directly to marketplace revenue.
- Missing store IDs should remain visible as exceptions, not allocated by guesswork.

