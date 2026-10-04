"""P1 fixture inventory: completeness is verified against the declared catalog."""
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from services.data.contracts import (CONTRACT_VERSION, REPORTING_ZONE, DataError,
                                    canonical, day, digest, now, validate)
from services.data.raw.archive import archive

FILES = {"catalog": "13_item_catalog.csv", "listings": "11_listing_events_aug2026.csv",
         "snapshots": "12_inventory_snapshots_aug2026.csv"}
UNLISTED = {"received", "awaiting_inspection", "awaiting_photography", "ready_to_list"}


def load_pack(pipeline, fixture_root):
    root = Path(fixture_root)
    manifest = json.loads((root / "manifest.json").read_text())
    if manifest.get("synthetic") is not True:
        raise DataError("synthetic_required", "Inventory accepts labeled fixture packs only")
    tables, payloads = {}, {}
    for kind, name in FILES.items():
        payloads[kind] = (root / name).read_bytes()
        tables[kind] = list(csv.DictReader(payloads[kind].decode().splitlines()))
        control = manifest["files"][name]
        if digest(payloads[kind]) != control["sha256"] or len(tables[kind]) != control["rows"]:
            raise DataError("inventory_control_mismatch", name)
    catalog = {row["item_id"]: row for row in tables["catalog"]}
    if len(catalog) != len(tables["catalog"]) or any(row["synthetic"] != "true" for row in catalog.values()):
        raise DataError("catalog_invalid", "Catalog requires unique synthetic items")
    snapshots = tables["snapshots"]
    if len({(r["snapshot_at"], r["item_id"]) for r in snapshots}) != len(snapshots):
        raise DataError("snapshot_duplicate", "Duplicate item/cutoff")
    if {r["snapshot_at"] for r in snapshots} != set(manifest["inventory_controls"]):
        raise DataError("snapshot_controls_missing", "Cutoff controls must match input")
    for cutoff, control in manifest["inventory_controls"].items():
        selected = [r for r in snapshots if r["snapshot_at"] == cutoff]
        expected = {key for key, row in catalog.items() if row["received_at"] <= cutoff and
                    (not row["sold_at"] or row["sold_at"] > cutoff or
                     (row["canceled_at"] and row["canceled_at"] <= cutoff))}
        if {r["item_id"] for r in selected} != expected or len(selected) != control["total_inventory"]:
            raise DataError("incomplete_snapshot", cutoff)
        if dict(Counter(r["workflow_state"] for r in selected)) != control["workflow_states"]:
            raise DataError("snapshot_states_mismatch", cutoff)
        for row in selected:
            if row["workflow_state"] not in UNLISTED | {"listed"} or row["store_id"] != catalog[row["item_id"]]["store_id"]:
                raise DataError("snapshot_item_mismatch", row["item_id"])
    listings = tables["listings"]
    if len({r["listing_id"] for r in listings}) != len(listings):
        raise DataError("listing_duplicate", "Listing event ID is not unique")
    for row in listings:
        item = catalog.get(row["item_id"])
        if not item or any(row[k] != item[k] for k in ("store_id", "listed_at", "listing_id", "platform")):
            raise DataError("listing_item_mismatch", row["listing_id"])
    input_ids = {}
    with pipeline.db() as db:
        for kind, data in payloads.items():
            checksum, artifact = archive(data, pipeline.archive_root)
            db.execute("INSERT OR IGNORE INTO source_files VALUES(?,?,?,?,?,1)", (checksum, checksum, artifact, len(data), now()))
            input_id = kind + "-" + checksum
            input_ids[kind] = input_id
            already = db.execute("SELECT 1 FROM inventory_inputs WHERE id=?", (input_id,)).fetchone()
            if already:
                continue
            db.execute("INSERT INTO inventory_inputs VALUES(?,?,?,?,?)", (input_id, checksum, kind, now(), canonical(manifest)))
            for number, row in enumerate(tables[kind], 1):
                if kind == "listings":
                    db.execute("INSERT INTO listing_events VALUES(?,?,?,?,?,?,?,?)", (input_id, number, row["listing_id"], row["platform"], row["item_id"], row["store_id"] or None, row["listed_at"], canonical(row)))
                elif kind == "snapshots":
                    db.execute("INSERT INTO inventory_snapshots VALUES(?,?,?,?,?,?,?)", (input_id, number, row["snapshot_at"], row["item_id"], row["store_id"] or None, row["workflow_state"], canonical(row)))
        db.execute("INSERT INTO audit_events(recorded_at,action,reference,detail_json) VALUES(?,?,?,?)", (now(), "inventory_pack_verified", input_ids["catalog"], canonical(input_ids)))
    return {"synthetic": True, "input_ids": input_ids, "complete_for": "declared fixture catalog only"}


def inventory_response(pipeline, start, end, snapshot_at=None, store=None):
    if day(start) > day(end):
        raise DataError("invalid_period", "Start must precede end")
    if snapshot_at:
        try:
            stamp = datetime.fromisoformat(snapshot_at)
            if stamp.tzinfo is None:
                raise ValueError("missing zone")
        except ValueError:
            raise DataError("invalid_snapshot", "Use an offset-bearing snapshot cutoff")
        if not day(start) <= stamp.astimezone(ZoneInfo(REPORTING_ZONE)).date() <= day(end):
            raise DataError("snapshot_outside_period", snapshot_at)
    with pipeline.db() as db:
        listing_input = db.execute("SELECT * FROM inventory_inputs WHERE kind='listings' ORDER BY loaded_at DESC LIMIT 1").fetchone()
        snapshot_input = db.execute("SELECT * FROM inventory_inputs WHERE kind='snapshots' ORDER BY loaded_at DESC LIMIT 1").fetchone()
        listing_count = None
        backlog = None
        listing_available = False
        if listing_input:
            # History has June/July records, but only August's completeness is declared.
            pack = json.loads(listing_input["manifest_json"])
            listing_available = start >= "2026-08-01" and end <= "2026-08-31"
            if listing_available:
                selected = db.execute("SELECT * FROM listing_events WHERE input_id=?", (listing_input["id"],)).fetchall()
                listing_count = sum(start <= str(datetime.fromisoformat(r["listed_at"]).astimezone(ZoneInfo(REPORTING_ZONE)).date()) <= end and
                                    (store is None or (r["store_id"] is None if store == "unknown" else r["store_id"] == store)) for r in selected)
        snapshot_available = False
        if snapshot_input and snapshot_at:
            controls = json.loads(snapshot_input["manifest_json"])["inventory_controls"]
            snapshot_available = snapshot_at in controls
            if snapshot_available:
                selected = db.execute("SELECT * FROM inventory_snapshots WHERE input_id=? AND snapshot_at=?", (snapshot_input["id"], snapshot_at)).fetchall()
                backlog = sum(r["workflow_state"] in UNLISTED and
                              (store is None or (r["store_id"] is None if store == "unknown" else r["store_id"] == store)) for r in selected)
        def metric(key, version, value, definition, reason):
            return {"metric_id": key, "metric_version": version, "value": str(value) if value is not None else None,
                    "unit": "items", "availability": "available" if value is not None else "unavailable",
                    "availability_reason": None if value is not None else reason, "definition": definition}
        response = {"contract_version": CONTRACT_VERSION, "synthetic": True, "start_date": start, "end_date": end,
                    "snapshot_at": snapshot_at, "store": store,
                    "metrics": [metric("M-LISTINGS-CREATED", "listing-events-v1", listing_count, "Distinct events filtered by listed-at reporting date", "Complete listing-event input is unavailable for selected period"),
                                metric("M-UNLISTED-BACKLOG", "inventory-backlog-v1", backlog, "Unique unlisted items at one verified complete snapshot", "Choose an available complete snapshot; never infer from sales")],
                    "input_ids": [r["id"] for r in (listing_input, snapshot_input) if r],
                    "coverage_state": "complete" if listing_available and snapshot_available else "partial" if listing_available or snapshot_available else "unavailable"}
        return validate("inventory.schema.json", response)
