# GOV-04 access, retention and rollback

Weekend implementation is synthetic/local only. The API binds 127.0.0.1, checks
loopback Host values, accepts bounded JSON uploads without server file paths,
and allows development origins on localhost/127.0.0.1 port 5173. It has no
production identity or role enforcement; UI role views do not constitute access
control. CSVs/manifests are data, never executable instructions.

Raw files are created exclusively by content hash and filesystem read-only
permissions; reuse and download verify bytes. This detects corruption but does
not claim tamper-proof storage against a machine owner. `.runtime/` and local
databases are gitignored. Keep no production data or credentials there.

SQLite transactions keep curated facts and publication pointers atomic. A bad
batch preserves raw/rejected evidence and last-good metrics. Explicit corrections
create versions with superseded lineage; old runs remain queryable. Exception
resolution appends audit evidence and does not change missing source values.
Back up SQLite and its raw archive together before supervised prototype changes.

Production retention, deletion rights, credential/session ownership, MFA/CAPTCHA
fallback, approved folder destination and incident response remain decisions for
Goodwill/provider/IT. Do not bypass restrictions or use live sessions/data.
Production Copilot/tenant/identity, Jev data flows and Business Central mapping
are unapproved. No model is called by this pipeline. No accounting posting,
autonomous operational action or production deployment is included.
