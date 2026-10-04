# Source authority and overlap review

Basis: PLAN §4/§7 and registered stakeholder repository snapshots. This is the synthetic implementation decision; Goodwill source owners have not approved a production matrix. See [nine-source register](../../planning/source-register.md) and [acquisition classes](../../contracts/sources/acquisition-classes.md).

| Source | Accounting role / authority boundary | Demo implementation |
|---|---|---|
| Cash Monkey | Sales/payout; select separately from Upright, never sum overlapping orders | Synthetic manual CSV + manifest |
| Upright | Selected authority for P0 demo item sales minus refunds; excludes shipping/tax/fees | Synthetic deterministic portal collection |
| Jewelry | Item enrichment, not revenue | Mapped, unconnected |
| OSM/PB/EasyPost | Expense; system of record unknown | Mapped, unconnected |
| FedEx | Charges/refunds; expense netting | Mapped, unconnected |
| ShopGoodwill | Potential transaction overlap with Upright | Mapped, unconnected |
| Goodwill Books statement | Settlement/payout, not additional transaction revenue | Mapped, unconnected |
| eBay listing sales | Listing/sales; potential platform coverage overlap | Mapped, unconnected |
| Amazon payments summary | Settlement/payment summary, not transaction revenue | Mapped, unconnected |

The API queries one selected source. Source-qualified transaction keys and platform-local buyer identities preserve boundaries. No buyer identity is merged across platforms. All nine live owners/access and operational cadence need confirmation; monthly statement delivery is a source hypothesis, not a running connection.

The P0 skill selects All statuses and Eastern source dates. Original filters/timezones survive intake→import; filtered manual reports retain partial coverage. Browser UI tests verify the visible map and unavailable unconnected source. No live formats/authentication or owner review was tested.
