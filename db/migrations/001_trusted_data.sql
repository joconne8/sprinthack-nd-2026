PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS schema_versions(version INTEGER PRIMARY KEY);
INSERT OR IGNORE INTO schema_versions VALUES (1);
CREATE TABLE IF NOT EXISTS source_files (
 id TEXT PRIMARY KEY, checksum TEXT NOT NULL UNIQUE, artifact_ref TEXT NOT NULL,
 byte_size INTEGER NOT NULL, archived_at TEXT NOT NULL, synthetic INTEGER NOT NULL CHECK(synthetic=1)
);
CREATE TABLE IF NOT EXISTS import_batches (
 id TEXT PRIMARY KEY, file_id TEXT REFERENCES source_files(id), source TEXT NOT NULL,
 report_type TEXT NOT NULL, request_start TEXT, request_end TEXT, source_timezone TEXT,
 manifest_json TEXT NOT NULL, parser_version TEXT NOT NULL, rule_version TEXT NOT NULL,
 status TEXT NOT NULL, recorded_at TEXT NOT NULL, error_code TEXT, error_detail TEXT,
 row_count INTEGER NOT NULL DEFAULT 0, accepted_rows INTEGER NOT NULL DEFAULT 0,
 rejected_rows INTEGER NOT NULL DEFAULT 0, duplicate_rows INTEGER NOT NULL DEFAULT 0,
 corrected_rows INTEGER NOT NULL DEFAULT 0, reconciliation_json TEXT
);
CREATE TABLE IF NOT EXISTS staging_rows (
 batch_id TEXT NOT NULL REFERENCES import_batches(id), row_number INTEGER NOT NULL,
 original_json TEXT NOT NULL, normalized_json TEXT, status TEXT NOT NULL,
 reason TEXT, PRIMARY KEY(batch_id,row_number)
);
CREATE TABLE IF NOT EXISTS exceptions (
 id TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES import_batches(id), row_number INTEGER,
 code TEXT NOT NULL, detail TEXT NOT NULL, owner_role TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('open','resolved')), resolution TEXT, resolved_at TEXT
);
CREATE TABLE IF NOT EXISTS sale_versions (
 id TEXT PRIMARY KEY, source TEXT NOT NULL, record_key TEXT NOT NULL,
 batch_id TEXT NOT NULL REFERENCES import_batches(id), row_number INTEGER NOT NULL,
 reporting_date TEXT NOT NULL, source_date TEXT NOT NULL, source_timestamp TEXT,
 platform TEXT NOT NULL, store_id TEXT, buyer_id TEXT, currency TEXT NOT NULL CHECK(currency='USD'),
 item_id TEXT, gross_cents INTEGER NOT NULL, refund_cents INTEGER NOT NULL,
 fingerprint TEXT NOT NULL, normalized_json TEXT NOT NULL,
 supersedes TEXT REFERENCES sale_versions(id),
 FOREIGN KEY(batch_id,row_number) REFERENCES staging_rows(batch_id,row_number)
);
CREATE TABLE IF NOT EXISTS active_sales (
 source TEXT NOT NULL, record_key TEXT NOT NULL, version_id TEXT NOT NULL REFERENCES sale_versions(id),
 PRIMARY KEY(source,record_key)
);
CREATE TABLE IF NOT EXISTS metric_runs (
 id TEXT PRIMARY KEY, source TEXT NOT NULL, batch_id TEXT NOT NULL REFERENCES import_batches(id),
 metric_version TEXT NOT NULL, published_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metric_run_rows (
 run_id TEXT NOT NULL REFERENCES metric_runs(id), version_id TEXT NOT NULL REFERENCES sale_versions(id),
 PRIMARY KEY(run_id,version_id)
);
CREATE TABLE IF NOT EXISTS source_publications (
 source TEXT PRIMARY KEY, run_id TEXT REFERENCES metric_runs(id),
 latest_batch_id TEXT NOT NULL REFERENCES import_batches(id)
);
CREATE TABLE IF NOT EXISTS coverage_windows (
 source TEXT NOT NULL, batch_id TEXT NOT NULL REFERENCES import_batches(id),
 starts_at TEXT NOT NULL, ends_at TEXT NOT NULL, scope_json TEXT NOT NULL,
 PRIMARY KEY(source,batch_id)
);
CREATE TABLE IF NOT EXISTS inventory_inputs (
 id TEXT PRIMARY KEY, file_id TEXT NOT NULL REFERENCES source_files(id), kind TEXT NOT NULL,
 loaded_at TEXT NOT NULL, manifest_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS listing_events (
 input_id TEXT NOT NULL REFERENCES inventory_inputs(id), row_number INTEGER NOT NULL,
 listing_id TEXT NOT NULL, platform TEXT NOT NULL, item_id TEXT NOT NULL, store_id TEXT,
 listed_at TEXT NOT NULL, original_json TEXT NOT NULL,
 PRIMARY KEY(input_id,listing_id)
);
CREATE TABLE IF NOT EXISTS inventory_snapshots (
 input_id TEXT NOT NULL REFERENCES inventory_inputs(id), row_number INTEGER NOT NULL,
 snapshot_at TEXT NOT NULL, item_id TEXT NOT NULL, store_id TEXT, workflow_state TEXT NOT NULL,
 original_json TEXT NOT NULL, PRIMARY KEY(input_id,snapshot_at,item_id)
);
CREATE TABLE IF NOT EXISTS audit_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT, recorded_at TEXT NOT NULL, action TEXT NOT NULL,
 reference TEXT NOT NULL, detail_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS sale_scope ON sale_versions(source,reporting_date,platform,store_id);
CREATE INDEX IF NOT EXISTS batch_source ON import_batches(source,recorded_at);
