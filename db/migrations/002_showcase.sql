CREATE TABLE IF NOT EXISTS showcase_inputs (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('labor','shipping')),
 checksum TEXT NOT NULL, definition_version TEXT NOT NULL, recorded_at TEXT NOT NULL,
 artifact_ref TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS showcase_input_rows (
 input_id TEXT NOT NULL REFERENCES showcase_inputs(id), row_number INTEGER NOT NULL,
 source TEXT NOT NULL, row_key TEXT NOT NULL, payload_json TEXT NOT NULL,
 PRIMARY KEY(input_id,row_number), UNIQUE(input_id,source,row_key)
);
CREATE TABLE IF NOT EXISTS showcase_active_inputs (
 kind TEXT PRIMARY KEY, input_id TEXT NOT NULL REFERENCES showcase_inputs(id)
);
CREATE TABLE IF NOT EXISTS showcase_snapshots (
 id TEXT PRIMARY KEY, published_at TEXT NOT NULL, manifest_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS showcase_recordings (
 id TEXT PRIMARY KEY, source TEXT NOT NULL, status TEXT NOT NULL,
 events_json TEXT NOT NULL, recipe_json TEXT, recipe_id TEXT
);
CREATE TABLE IF NOT EXISTS showcase_recipes (
 id TEXT PRIMARY KEY, source TEXT NOT NULL, version TEXT NOT NULL,
 approved_at TEXT NOT NULL, skill_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS showcase_runs (
 id TEXT PRIMARY KEY, record_json TEXT NOT NULL
);
