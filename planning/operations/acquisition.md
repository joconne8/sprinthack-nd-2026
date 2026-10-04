# Synthetic report operations

P0 uses one Upright paid-orders replica and versioned skill 0.2.0. An operator
chooses an ordered 2026 period of up to 31 days. The skill selects all payment
statuses and Eastern source dates, asserts the expected pages, downloads real
CSV bytes and checks their manifest. Source dates/timezone are retained; reporting
remains New York under goodwill-v1. Cash Monkey is a synthetic manual-upload
path; the other seven sources are mapped and unconnected.

POST `/api/v1/acquisition-runs` starts a supervised run. One active request is
allowed; concurrent requests fail visibly. At most two transient attempts fit
within 90 seconds; each child browser attempt has a bounded deadline. No schedule,
production email, model call or agent is started. Versioned skill/run logs are in
the ignored state directory. Collection/import/publication are separate states.

Verified intake retains the original manifest, filters, exact checksum/byte size,
run ID and raw reference. `intake.submit(record, pipeline)` invokes the real
importer and records its batch; repeated submission reuses that batch. Repeated
new collection runs retain their histories and import as duplicate no-ops.
Changed financial records require explicit correction approval at manual import.
Bad files and control differences never replace last-good verified metrics.

History persists under `.runtime/acquisition/`. On restart, interrupted requests
become human-review states; completed imports and their batch identity remain
visible. The UI displays last success, attempt limits, cause and next owner.
Authentication, MFA, CAPTCHA, access denial, wrong page, control drift and missing
reports stop for human review rather than retrying or bypassing restrictions.

Fallback: open the simulated portal, choose a report, download CSV and manifest,
then use Report intake → Upload a report. Review failed-batch controls/rejected
source rows and record nonfinancial resolution notes. Download the original CSV
and stored source manifest from the batch evidence. Real approved folder/email
delivery is a production design, not an active connection.

Before a production schedule: Goodwill/provider permission; real report formats;
approved runner/session account and human re-authentication/MFA ownership;
storage/retention/incident policy; source-of-record and cadence; named rule/support
owners; workbook/Power BI validation. Amanda's assistant role must be confirmed.
No credential, cookie or provider session is requested or stored by this demo.
