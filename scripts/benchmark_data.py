"""Isolated synthetic benchmarks, not a production performance prediction."""
import json
import platform
import sys
import tempfile
import time
from pathlib import Path

# Support the documented direct invocation from the repository root.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services.data.adapters import fixture_manifest
from services.data.importer import Pipeline
from services.metrics.query import metric_response


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix="goodwill-benchmark-") as temporary:
        pipeline = Pipeline(temporary)
        for name, source, report in [
            ("02_upright_paid_order_items_aug2026.csv", "upright_fixture", "paid_order_items"),
            ("06_shopgoodwill_periodic_reports_aug2026.csv", "shopgoodwill_fixture", "sales"),
            ("08_ebay_listing_sales_aug2026.csv", "ebay_fixture", "sales"),
        ]:
            path = ROOT / "goodwill/synthetic-data" / name
            manifest = fixture_manifest(path, "2026-08-01", "2026-08-31", source, report)
            started = time.perf_counter()
            batch = pipeline.import_file(path, manifest)
            import_seconds = time.perf_counter()-started
            started = time.perf_counter()
            metrics = metric_response(pipeline, "2026-08-01", "2026-08-31", source)
            query_seconds = time.perf_counter()-started
            started = time.perf_counter()
            replay = pipeline.import_file(path, manifest)
            replay_seconds = time.perf_counter()-started
            results.append({"source": source, "rows": batch["counts"]["row_count"], "status": batch["status"],
                            "import_seconds": round(import_seconds, 6), "query_seconds": round(query_seconds, 6),
                            "replay_seconds": round(replay_seconds, 6), "replay_status": replay["status"],
                            "demo_net_sales": metrics["metrics"][0]["value"]})
    print(json.dumps({"synthetic": True, "python": sys.version, "platform": platform.platform(),
                      "conditions": "one local process; temporary SQLite; standard library; no production data", "results": results}, indent=2))
    return 0 if all(r["status"] == "imported" and r["replay_status"] == "duplicate_noop" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
