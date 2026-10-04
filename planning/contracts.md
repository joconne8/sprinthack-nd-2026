# GOV-03 frozen local interface — goodwill-v1

This is the local implementation contract under Peyton's reported delegation
from Jack OC. Team review remains required before integration. Source requirements:
PLAN §5/7, REQ-DAT-01 through 05, PIPE-01 through 09. JSON schemas and TypeScript
consumer types are in `contracts/v1/`. Backend responses validate those schemas.

## Manifest and compatibility

`replica-v1` portal manifests enter the importer directly. `manifest_metadata()`
is the documented adapter to `goodwill-v1`; original metadata is retained.
`fixture-v1` is a separately labeled August fixture adapter. No real source format
is asserted. Required metadata: source/report identity, requested source dates,
source timezone, filename, SHA-256, row count, currency and synthetic=true.
Optional byte size and source financial controls must match if supplied.
Queries with channels/accounts/order IDs/SKUs/payment status retain their filter
scope; they never become full-source coverage. Unsupported schema/currency is
rejected. v1 supports USD only, without currency conversion.

Hugh can send the original portal manifest plus exact CSV bytes, or use
`import-intake --record <full acquisition runs/run_id.json>`. The latter checks
checksum/byte count and preserves acquisition run identity. Hugh's outbox stub
omits dates/timezone/counts/filters and is not a valid importer input. The full
intake record also omits filters, so that adapter marks coverage conservatively
partial. A full original manifest is preferred.

## Grains, authority and amounts

Upright replica paid orders: one order key. Its item report: order+item key.
Cash Monkey replica: one unit key. August fixtures use distinct source names,
source-specific keys and the documented fixture grain. A source cannot mix two
report grains as authoritative revenue. Separate source scopes are never summed
automatically; real Upright/ShopGoodwill overlap is unresolved.

Item amount and refund are exact integer cents. Demo net sales = gross item sales
minus item refunds; source `net_sales`, shipping, tax, premiums and payouts are
preserved in original rows and excluded from that calculation. Source amounts
are already row-level; quantity does not multiply them. Refunds are as-of amounts
on the original sale, not invented refund-date cash-flow events. Expenses and
settlements have separate proposed grains and are refused by the sales parser.

Source timestamps, source report dates, source timezone and reporting dates remain
distinct. Reporting timezone is America/New_York. Offset-bearing timestamps are
converted to it; date-only events retain their declared source date. Coverage
uses source-local midnight intervals converted to UTC: partial boundary days stay
partial, including timezone/DST changes. No silent change to Hugh's file bytes.

## Identity, corrections and reconciliation

Immutable file identity is SHA-256. Sale identity is source + a canonical JSON
array of adapter key fields, preventing separator collisions. Same-file/overlap
imports record duplicate no-ops. Changed keys are rejected unless
`allow_corrections: true`; approved corrections retain old versions. File absence
does not imply deletion. Full report replacement/tombstones are not implemented.

Counts are disjoint: accepted (including corrected), duplicate, rejected. Source
money reconciles to accepted+duplicate+rejected when numeric; unknown money is
null. Rejected rows or control differences block the entire new publication.
Staging can contain valid rows of a failed batch, but they never become metrics.
Unexpected failures roll back all database changes; a raw orphan can remain for
later operator investigation. No cleanup scheduler is started.

The existing fixture exception ledger counts **root** gaps. Related shipping
rows with missing stores retain explicit lineage to the corresponding missing-
store order, rather than inflating the root count or guessing attribution. The
DAT-01 review verifies seven such links. Sales parser exceptions are emitted
per actual imported row. Resolutions are auditable notes, not financial edits.

## Consumption

- `GET /api/v1/metrics`: one source, inclusive reporting period, optional canonical
  platform/store (`store=unknown` includes missing/unmapped attribution).
- `GET /api/v1/evidence`: same filters plus displayed `run_id`, offset, limit 1..200.
  Returns full-scope total and page rows; never present a page sum as the total.
- `GET /api/v1/imports`, `/imports/{id}`, `/imports/{id}/rows`: acquisition/import
  statuses, controls, rejected/accepted originals and exceptions.
- `GET /api/v1/files/{file_id}`: exact archived bytes by checksum identity.
- `POST /api/v1/imports`: `{csv_text, manifest, allow_corrections?}`. HTTP 201 for
  imported/no-op; HTTP 422 with batch contract for a rejected import.
- `POST /api/v1/exceptions/{id}/resolve`: nonempty human resolution note.
- `GET /api/v1/inventory`: optional accepted fixture events/one selected complete
  snapshot. Never infer backlog from sales or sum multiple snapshots.

Metric values are decimal/count strings or null, never floats. Missing buyer
IDs make customer counts unavailable; customers require one platform. Unsupported
labor, margin, cohort and prior-period inputs produce null strategic KPIs.
All responses retain synthetic labels, definitions/version, scope, coverage,
freshness and evidence. Acquisition, import and publication states stay separate.
Failed batches mark stale last-good outputs with an explicit warning. A complete
zero-row verified source can yield zero; an absent source cannot.

Schema changes are additive only within v1; semantic/grain changes require a new
version and migration. Frontend mock examples validate the same backend schemas.
No assistant, unrestricted SQL tool, export or live integration is activated.

## Completion and parallel-proposal reconciliation

The baseline is the foundation merged in PR #52 at `610035e`. The GOV-03
proposal at `4464458` predates that integration and defines different `1.0.0`
envelopes. Its useful controls are incorporated into this baseline; its schema
must not overwrite the running API. Detailed mapping is in
`reports/GOV-03/compatibility-notes.md`. This is the implementation choice under
Peyton's authorized combined lane, pending human review, not a claim that Jack
OC accepted the proposal or that GitHub issues were closed.

Request schemas now accompany responses: metrics-query, evidence-query,
import-request and resolution-request. Imports/staging, health and resolution
responses have schemas too. API requests reject unknown/ignored filters, invalid
calendar dates, unbounded evidence pages and non-boolean correction flags.
Backend imports still independently verify original manifest/date/hash/bytes.
`contracts/build_schemas.py` generates all schemas and `types.ts` from one
structural source. `client.ts` consumes those types, retains failed batch bodies
in `ApiError`, and has no mock fallback. Run schema regeneration and strict
TypeScript compilation before changing the shared interfaces.

The design-only tool-request/tool-response schemas allow `get_metrics` and
`get_evidence` with the same requests/responses. No tool execution endpoint,
assistant, identity integration or write action is implemented. Consumers must
validate external JSON at runtime; TypeScript types alone do not validate JSON.
