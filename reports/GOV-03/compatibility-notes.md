# Compatibility decisions

Portal replica-v1 enters through the documented legacy-manifest adapter, with
original bytes/manifest retained. August fixture-v1 uses distinct source names
and grains, never a silent substitution for the acquired portal file.
Hugh's complete run record is supported; its reduced outbox stub is insufficient.

Source `net_sales`/payout columns are ignored for demo net sales. Timezones are
preserved; offset timestamps are converted to reporting dates and partial source
edge-day coverage remains visible. Filtered/intake-unknown report scopes cannot
assert full-source completeness. Unsupported currency/version/grain is rejected.
No acquisition or portal file was rewritten.

No claim of live Upright/Cash Monkey schema compatibility. Future breaking
semantics require a versioned migration and coordinated frontend handoff.
