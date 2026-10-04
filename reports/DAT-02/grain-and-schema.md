# Raw, staging, curated and metric schema

`db/migrations/001_trusted_data.sql` records immutable files (checksum/bytes),
imports (source/report/request period/timezone/parser/rules), original staging
rows (1-based data row), rejected reasons/exceptions, sale versions, active source
keys, immutable metric run memberships, coverage intervals and audit events.
Optional inventory inputs point to archived listing/catalog/snapshot bytes.

Source grains are explicit in `planning/contracts.md`. Sales/refunds are as-of
source-row amounts; fee/shipping/payout fields remain original evidence and
cannot be summed as sales. Expenses/settlements are separate future fact grains,
rejected by the revenue adapter. No invented refund event timestamp or labor fact.

Money is USD integer cents; date-only versus offset timestamp fields are distinct.
Missing/unmapped stores stay visible, and missing buyers cannot support a
customer estimate. A single transaction governs curated versions/publication.
Peyton is the only migration owner. No production warehouse approval is implied.
