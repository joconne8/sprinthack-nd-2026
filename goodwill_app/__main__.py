import argparse
import json
from pathlib import Path

from services.data.adapters import fixture_manifest, import_intake
from services.data.contracts import DataError
from services.data.importer import Pipeline
from services.data.inventory.store import inventory_response, load_pack
from services.metrics.query import evidence_response, metric_response


def main():
    parser = argparse.ArgumentParser(description="Local synthetic Goodwill data foundation")
    parser.add_argument("--state-root", default=".runtime")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    imp = commands.add_parser("import")
    imp.add_argument("--csv", required=True)
    imp.add_argument("--manifest", required=True)
    imp.add_argument("--allow-corrections", action="store_true")
    intake = commands.add_parser("import-intake")
    intake.add_argument("--record", required=True)
    intake.add_argument("--allow-corrections", action="store_true")
    fm = commands.add_parser("fixture-manifest")
    for arg in ("csv", "start-date", "end-date", "source", "report-type"):
        fm.add_argument("--" + arg, required=True)
    for name in ("metrics", "evidence", "inventory"):
        query = commands.add_parser(name)
        query.add_argument("--start-date", required=True)
        query.add_argument("--end-date", required=True)
        query.add_argument("--store")
        if name != "inventory":
            query.add_argument("--source", required=True)
            query.add_argument("--platform")
            query.add_argument("--run-id", required=name == "evidence")
        else:
            query.add_argument("--snapshot-at")
        if name == "evidence":
            query.add_argument("--offset", type=int, default=0)
            query.add_argument("--limit", type=int, default=100)
    inv = commands.add_parser("load-inventory")
    inv.add_argument("--fixture-root", default="goodwill/synthetic-data")
    serve = commands.add_parser("serve")
    serve.add_argument("--port", type=int, default=8000)
    commands.add_parser("imports")
    resolve = commands.add_parser("resolve-exception")
    resolve.add_argument("--id", required=True)
    resolve.add_argument("--resolution", required=True)
    args = parser.parse_args()
    pipeline = Pipeline(args.state_root)
    try:
        if args.command == "init":
            pipeline.db().close()
            result = {"state_root": str(pipeline.root), "synthetic": True}
        elif args.command == "fixture-manifest":
            result = fixture_manifest(args.csv, args.start_date, args.end_date, args.source, args.report_type)
        elif args.command == "import":
            result = pipeline.import_file(args.csv, json.loads(Path(args.manifest).read_text()), args.allow_corrections)
        elif args.command == "import-intake":
            result = import_intake(pipeline, args.record, args.allow_corrections)
        elif args.command == "metrics":
            result = metric_response(pipeline, args.start_date, args.end_date, args.source, args.platform, args.store, args.run_id)
        elif args.command == "evidence":
            result = evidence_response(pipeline, args.run_id, args.start_date, args.end_date, args.source, args.platform, args.store, args.offset, args.limit)
        elif args.command == "inventory":
            result = inventory_response(pipeline, args.start_date, args.end_date, args.snapshot_at, args.store)
        elif args.command == "load-inventory":
            result = load_pack(pipeline, args.fixture_root)
        elif args.command == "imports":
            result = pipeline.batches()
        elif args.command == "resolve-exception":
            pipeline.resolve_exception(args.id, args.resolution)
            result = {"status": "resolved", "synthetic": True}
        elif args.command == "serve":
            from apps.api.server import make_server
            server = make_server(pipeline, args.port)
            print(f"Synthetic local API: http://127.0.0.1:{server.server_port}/api/v1/health", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return 0
        print(json.dumps(result, indent=2))
        return 1 if isinstance(result, dict) and result.get("status") == "failed" else 0
    except (DataError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"synthetic": True, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
