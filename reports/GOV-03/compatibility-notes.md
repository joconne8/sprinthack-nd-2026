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

## GOV-03 proposal reconciliation

Compared `origin/jackoc/GOV-03-contracts` at `4464458` with main's merged
`goodwill-v1` foundation at `610035e`. The parallel proposal is reviewed input,
not an accepted second API. Keep the deployed local interface below.

| Concern | Parallel proposal | Combined implementation decision |
|---|---|---|
| Envelope/version | `1.0.0`, `MetricResult`, `SupportingRows` | Keep `goodwill-v1`, metrics/evidence/batch schemas and current routes. A future envelope rename requires a coordinated version change. |
| Source timezone | Require `America/New_York`; change Los Angeles manifests | Preserve declared source timezone and exact bytes. Convert offset timestamps to reporting New York days; source windows may have partial boundary days. |
| Corrections | Latest acquired row wins with history | Explicit `allow_corrections: true` is required. Default rejection prevents silent financial changes. Old versions/runs remain available. |
| Refund timing | Separate refund facts proposed | Current acquired exports contain as-of refund amounts on sales. Do not invent refund event dates. Separate event facts need a new adapter/version. |
| Acquisition/intake state | Rename Hugh's run/intake fields | Preserve existing files. Original manifest + CSV is preferred; full intake record has a documented conservative adapter. Reduced outbox remains invalid. |
| Money/customer inputs | Exact money; missing metrics unavailable | Adopted: integer cents internally, decimal strings externally, USD only, platform-local customers, unavailable strategic inputs. |
| Shared client | Add type generation and validator checks | Schemas and TypeScript types now derive from the same source; runtime validates the supported schema subset. |
| Tools | Permission-bearing read-only tools | Typed metrics/evidence design contracts supplied; execution/identity/assistant remain deferred. |
| Expected report registry | Nine report/source proposals | Hugh retains source-map authority. One explicitly selected source drives the P0 API; no sum across nine feeds or claim of live connections. |
| Export | Decision outstanding | P1 explicitly deferred by the combined scope decision. ENG-04 P0 sequence uses source drilldown/raw-file evidence. |

Use `planning/development.md` and `contracts/v1/client.ts` for the current
producer/consumer handoff. Do not cherry-pick the older proposal's shared
`planning/contracts.md` or monolithic schema over this baseline. No changes to
Hugh's report bytes or portal are needed for this compatibility decision.
Human review and issue status confirmation remain outstanding.
