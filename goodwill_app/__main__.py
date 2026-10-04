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
    serve.add_argument('--node', help='Node executable for synthetic collection')
    serve.add_argument('--node-modules', help='Directory containing pinned Playwright')
    serve.add_argument('--chrome-path', help='Installed Chrome executable (optional)')
    serve.add_argument('--replica-url', help='Existing loopback replica; otherwise start a local replica')
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
            from acquisition.controller import AcquisitionManager
            import importlib.util
            import threading
            from http.server import ThreadingHTTPServer
            replica = None
            if not args.replica_url:
                path = Path(__file__).resolve().parents[1] / 'data ingestion/server.py'
                spec = importlib.util.spec_from_file_location('dashboard_replica', path)
                portal = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(portal)
                replica = ThreadingHTTPServer(('127.0.0.1', 0), portal.Handler)
                threading.Thread(target=replica.serve_forever, daemon=True).start()
            chrome = args.chrome_path
            installed_chrome = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
            if not chrome and installed_chrome.is_file():
                chrome = str(installed_chrome)
            manager = AcquisitionManager(pipeline, args.replica_url or f'http://127.0.0.1:{replica.server_port}',
                                         args.node, args.node_modules, chrome)
            server = make_server(pipeline, args.port, acquisition=manager)
            print(f"Synthetic Goodwill dashboard: http://127.0.0.1:{server.server_port}/", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
                manager.close()
                if replica:
                    replica.shutdown()
                    replica.server_close()
            return 0
        print(json.dumps(result, indent=2))
        return 1 if isinstance(result, dict) and result.get("status") == "failed" else 0
    except (DataError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"synthetic": True, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
