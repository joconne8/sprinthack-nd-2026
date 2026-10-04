# Coverage and last-good demonstration

Source coverage is the requested source-local interval, distinct from upload
time. Full reporting days are computed by unioning UTC intervals. Filtered or
unknown-scope reports and timezone edge days remain partial.

Fixed demonstration in `../DAT-04/before-after-controls.json`: publish 27.00;
replay remains 27.00; unapproved correction fails and exposes 27.00 with
stale_last_good; explicit corrected refund publishes 23.00 with audit/version
lineage. Malformed new rows cannot add half-published facts. Historical run
evidence retains its old amounts. Missing source yields null; a verified complete
empty source can yield zero. API and CLI share the same warning contract.
