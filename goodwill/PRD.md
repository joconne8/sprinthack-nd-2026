# PRD 2: Goodwill Michiana e-commerce reporting

**Status:** Recommended build for Jack.

**Evidence:** [`notes/kickoff-notes.md`](../notes/kickoff-notes.md), October 3 kickoff, Debbie's Goodwill pitch and Q&A plus organizer clarification. Sponsor facts are attributed below. Product scope, schema, formulas, tests, and demo pacing are proposed decisions. All weekend business records and results must be labeled **synthetic demo data**.

## Problem and users

Debbie wants "good, clear, easy-to-find data" to make decisions. She gets store-sales reporting at 10pm but says Friday through Sunday e-commerce sales do not arrive until Monday. Staff handle platforms individually each morning, consolidate reporting manually, and then manually feed accounting. She warns that re-entering numbers creates more chances for errors.

Primary users are Debbie and operations managers reviewing daily performance; managers and assistant managers assembling reports; and accounting staff preparing month-end close. Debbie's district manager is expected to answer detailed questions at office hours.

The goal is visibility and trustworthy reporting, not automated pricing, marketplace listing, or deciding which donations to sell online.

## Sponsor context from the transcript

- **Platforms:** Shop Goodwill handles the majority of marketplace sales; Debbie also names Amazon and eBay. She calls the book-reporting platform **Cash Monkey**. Preserve that transcript spelling until confirmed.
- **Store attribution:** there are **24 stores**. Debbie says the store supplying an item receives credit when it sells through e-commerce. Marketplace reporting is not described as 24 independent marketplace accounts.
- **Accounting:** she wants to upload into **Business Central** instead of manually entering everything. The transcript supplies no import schema or API contract.
- **Existing AI:** Debbie describes Thriftly and an "e-commerce eye" in two stores. That upstream item-selection work is context, not this reporting prototype's scope.
- **Mission:** better bottom-line efficiency supports Goodwill's education, job-training, and other mission work. Do not claim dollars saved without measurement.
- **Data:** organizers expect synthetic/artificial data for the weekend and allow public data for the proof of concept. Actual internal data is described as part of the later Innovation Sprint Lab work, not weekend access.
- **Continuation:** organizers describe a three-month Sprint Lab to develop the prototype and potentially integrate it with Goodwill. This is an opportunity, not an accepted pilot or contract.

Debbie guesses report preparation might take half an hour to an hour, then says she does not know for sure. Do not present that as a measured baseline or compute an ROI from it.

## Metrics Debbie actually asks for

| Priority topic in her pitch | Meaning to confirm before production |
| --- | --- |
| Total revenue and customers per day | Refunds, taxes, shipping, reporting timezone, and what counts as a customer |
| Revenue and profit per labor hour | Which revenue/profit basis, labor allocation, costs, and reporting window |
| Listings per store per day | Originating-store key and distinction between items identified, processed, and listed |
| Sell-through rate | Eligible inventory cohort, time window, relists, and unsold items |
| Unlisted inventory backlog | Which workflow states count as waiting to be listed and whether complete snapshots exist |

Her broader wishlist includes margins, growth, category performance, average/median selling prices, days to sell, repeat buyers, and customer satisfaction. The weekend is not a promise to deliver that entire list.

Debbie's **50-55%** sell-through reference is for physical stores. She explicitly says the e-commerce percentage still needs to be figured out. Do not use it as an online target.

## Weekend scope: four metric views, two platforms maximum

Proposed demo sources: **Shop Goodwill and eBay**, both represented by clearly marked synthetic exports. Amazon and Cash Monkey are roadmap sources, not secretly simulated live connections. A platform selector must never imply a working connector that does not exist.

The four views:

1. **Daily revenue:** sales by day, platform, and originating store, with a source-row drilldown.
2. **Daily customers:** distinct buyers within each platform/day. Show platform counts separately; do not claim a cross-platform unique customer total without an identity mapping.
3. **Listings per store per day:** new listing events attributed to the source store. Unknown-store rows remain visible and flagged, not dropped or distributed by guesswork.
4. **Unlisted backlog:** counts from a synthetic inventory snapshot, by store and snapshot time. Do not infer backlog from sales exports alone.

The synthetic store dimension can represent the 24 stores Debbie describes, using fictional IDs rather than fabricated real names. Use a focused subset on stage. All metric cards, charts, source files, and exports carry the synthetic label.

### Must work end to end

- Upload the two synthetic platform exports plus synthetic listing/inventory inputs.
- Validate and normalize to a common schema.
- Show the four views with date/platform/store filters and data freshness.
- Reconcile accepted source rows to dashboard totals; show rejected rows and discrepancies.
- Re-upload a file without doubling the result.
- Export a source-linked summary CSV. If time permits, show a **proposed Business Central mapping preview** explicitly marked unvalidated, with no upload button that claims to post accounting entries.

### Not in the weekend commitment

Live marketplace integrations; production credentials; real customer or employee data; live Business Central posting; all-platform coverage; scheduled delivery; autonomous listing/pricing; predictive demand; a general chatbot; or production-ready accounting statements.

## Proposed data contract

Keep ingestion and metric math deterministic. Use LLMs only for optional wording or explanations of already-computed facts.

| Record | Proposed fields |
| --- | --- |
| Sale | platform, source_file_id, source_row_id, order_id, item_id, store_id, sold_at, currency, sale_amount, refund_amount, buyer_id |
| Listing event | platform, listing_id, item_id, store_id, listed_at, source_row_id |
| Inventory snapshot | snapshot_at, item_id, store_id, workflow_state, source_row_id |
| Import batch | file fingerprint, platform, import time, row counts, date coverage, validation results, synthetic flag |

For the demo, define revenue as synthetic sale amount less synthetic refunds, excluding shipping/tax. State that convention in the UI. It is a proposed convention, not Goodwill's confirmed accounting definition. Do not aggregate unlike currencies without an explicit conversion policy.

A platform-local buyer ID supports a daily platform customer count. If IDs are missing, show the metric as unavailable for that input rather than substituting order count.

Backlog is the count of items in the demo's declared unlisted states at the selected complete snapshot. It is a point-in-time measure, not a daily flow. Missing or partial snapshots must be labeled.

## Deferred formulas and why they are deferred

- **Revenue per labor hour:** revenue for a defined store/platform/window divided by matched labor hours. Missing labor data or a zero denominator gives unavailable, not zero productivity.
- **Profit per labor hour:** agreed profit for the same scope divided by labor hours. Confirm whether profit includes marketplace fees, shipping, processing costs, and labor cost; avoid double counting. Never invent those costs.
- **Sell-through:** items sold from a defined eligible cohort divided by eligible items in that same cohort, over a stated window. Confirm relisting and cross-platform item handling. Avoid dividing today's sales by today's new listings and calling that sell-through.

These are important next steps because Debbie explicitly asks for them. Only replace a committed metric with one of these if office hours resolves its definition and required inputs; do not expand the four-view limit.

## Validation and acceptance

- Every displayed number can be traced to accepted source rows and the declared metric definition.
- A duplicate import leaves totals unchanged; a row with a missing store remains flagged and recoverable.
- A deliberately malformed synthetic row is rejected with an explanation and does not silently change totals.
- Refunds change net revenue correctly under the stated demo convention.
- Customer counts do not silently merge identities across marketplaces.
- Revenue totals reconcile by platform, store, and day; discrepancies are visible.
- A new synthetic reporting day's import updates the dashboard without changing the template or code.
- Unknown/missing data stays unknown. Every synthetic-derived view and export remains labeled.

These are engineering acceptance tests, not claims that sponsor systems have passed them.

## Architecture and build order

Use the team's familiar web stack, a small relational database, explicit import adapters, and a shared metric library. A file-upload workflow is sufficient. Do not spend the weekend chasing marketplace APIs.

Build in this order: upload-to-revenue skeleton; reconciliation and repeat-import protection; the other three views; filters and source drilldown; export preview; then presentation polish. Optional narrative summaries must cite the computed figures and distinguish observed changes from possible causes.

## Risks and fallback

- **Unknown production exports:** make the synthetic adapter contract clear and document what would need remapping with real data.
- **Dashboard without trust:** prioritize row-level provenance and reconciliation over extra charts.
- **False accounting compatibility:** call the output a proposed mapping until accounting validates it.
- **No labor/cost/cohort data:** defer productivity and sell-through rather than manufacture them.
- **Scope creep:** stop at the selected metric views and two platforms. The organizers' instruction is to build less that works well.
- **Demo interruption:** keep a local, labeled synthetic replay and record a backup of the completed workflow. Do not claim the replay is live access.

## Seven-minute demo script

The pacing below is a proposed seven-minute presentation, not an official slot length.

| Time | Show and say |
| --- | --- |
| 0:00-0:45 | State Debbie's problem: physical-store reporting arrives nightly, but weekend e-commerce visibility waits until Monday. Name the two demo platforms and say every business record is synthetic. |
| 0:45-1:30 | Show separate synthetic exports, upload them, and display coverage/freshness. No live-connector claim. |
| 1:30-2:30 | Show daily revenue and platform-specific customer counts. Filter to a fictional store and trace a revenue total to its source rows. Explain why unique buyers are not summed across platforms. |
| 2:30-3:30 | Show listings per store and the unlisted snapshot backlog. Connect store attribution to Debbie's rule that originating stores get sale credit. |
| 3:30-4:30 | Re-upload the same file: totals do not double. Show a seeded malformed row and missing-store flag, then demonstrate the reconciliation report. |
| 4:30-5:30 | Import the next synthetic reporting day's file. The same views update without hand-rebuilding a report. Export the summary; call any Business Central mapping a proposal, not a posted transaction. |
| 5:30-6:30 | Explain what is deferred: confirmed labor/cost inputs for revenue and profit per labor hour, a cohort definition for sell-through, Amazon/Cash Monkey, and real export formats. |
| 6:30-7:00 | Close on the Sprint Lab path the organizers described: validate with real Goodwill data and accounting, then test a limited reporting workflow. Do not promise a pilot or quantified savings. |

## Office-hour questions and continuation gate

Ask the district manager to rank the first metric views and show representative export shapes when permitted. Confirm reporting timezone, revenue treatment, originating-store mapping, customer keys, labor/cost sources, and inventory states. Ask accounting for the Business Central import template and approval process.

A later real-data pilot requires approved access, verified source schemas, reconciled totals against Goodwill's current reporting, confirmed metric definitions, and accounting validation before any posting. Synthetic-demo success is evidence of the workflow, not production readiness.
