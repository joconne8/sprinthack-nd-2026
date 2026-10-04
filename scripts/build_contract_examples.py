"""Produce explicitly synthetic API examples from the actual service, not a UI seed."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services.data.contracts import validate
from services.data.importer import Pipeline
from services.metrics.query import evidence_response, metric_response


def main():
    spec = importlib.util.spec_from_file_location("example_portal", ROOT/"data ingestion/server.py")
    portal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(portal)
    output = ROOT/"contracts/v1/examples"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        pipeline = Pipeline(temporary)
        request = portal.validate({"source": "upright", "start_date": "2026-09-30", "end_date": "2026-09-30",
                                   "timezone": "America/Indiana/Indianapolis", "payment_status": "All"})
        data, manifest = portal.create_artifact(request)
        imported = pipeline.import_bytes(data, manifest)
        available = metric_response(pipeline, "2026-09-30", "2026-09-30", "upright_replica")
        unavailable = metric_response(pipeline, "2026-09-30", "2026-09-30", "not_connected")
        evidence = evidence_response(pipeline, available["metric_run_id"], "2026-09-30", "2026-09-30", "upright_replica", limit=2)
        changed = dict(manifest, file_checksum="0"*64)
        failed = pipeline.import_bytes(data, changed)
        last_good = metric_response(pipeline, "2026-09-30", "2026-09-30", "upright_replica")
        partial = metric_response(pipeline, "2026-09-29", "2026-09-30", "upright_replica")
        for name, schema, body in [("batch-imported", "batch", imported), ("batch-failed", "batch", failed),
                                   ("metrics-available", "metrics", available), ("metrics-unavailable", "metrics", unavailable),
                                   ("metrics-partial", "metrics", partial), ("metrics-last-good", "metrics", last_good),
                                   ("evidence", "evidence", evidence)]:
            validate(schema+".schema.json", body)
            (output/(name+".json")).write_text(json.dumps(body, indent=2)+"\n")
    print("Generated seven synthetic contract examples; references are example-run IDs, not current runtime state.")


if __name__ == "__main__":
    main()
