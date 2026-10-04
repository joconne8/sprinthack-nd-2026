"""Capture reproducible local handoff evidence; never fabricate acceptance records."""
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "reports/integration"
    logs = output / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    runs = []

    def run(command, name, cwd=ROOT):
        started = time.perf_counter()
        process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=60)
        (logs / name).write_text(process.stdout+process.stderr)
        runs.append({"command": command, "cwd": str(cwd), "exit_code": process.returncode,
                     "elapsed_seconds": round(time.perf_counter()-started, 6), "log": "logs/"+name})
        print(name, "PASS" if process.returncode == 0 else "FAIL", flush=True)
        return process

    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], "foundation-tests.log")
    run([sys.executable, "-m", "unittest", "discover", "-s", "acquisition/tests", "-p", "test_*.py", "-v"], "acquisition-tests.log")
    run([sys.executable, "reports/DAT-01/review_fixtures.py"], "fixture-review.json")
    run([sys.executable, "scripts/benchmark_data.py"], "benchmark.json")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with tempfile.TemporaryDirectory(prefix="goodwill-fixture-verify-") as temporary:
        data = subprocess.check_output(["git", "archive", commit, "goodwill/synthetic-data"], cwd=ROOT)
        subprocess.run(["tar", "-xf", "-", "-C", temporary], input=data, check=True)
        run([sys.executable, "-m", "unittest", "discover", "-s", "goodwill/synthetic-data", "-p", "test_*.py", "-v"], "fixture-suite.log", Path(temporary))
    with tempfile.TemporaryDirectory(prefix="goodwill-cli-verify-") as temporary:
        command = [sys.executable, "-m", "goodwill_app", "--state-root", temporary]
        run(command+["init"], "cli-init.json")
        run(command+["import", "--csv", "data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.csv",
                     "--manifest", "data ingestion/examples/upright_paid_orders_2026-09-30_2026-09-30_synthetic.manifest.json"], "cli-import.json")
        run(command+["metrics", "--start-date", "2026-09-30", "--end-date", "2026-09-30", "--source", "upright_replica"], "cli-metrics.json")
    before = {p.name: p.read_bytes() for p in (ROOT/"contracts/v1").glob("*.schema.json")}
    run([sys.executable, "contracts/build_schemas.py"], "schema-generation.log")
    same = before == {p.name: p.read_bytes() for p in (ROOT/"contracts/v1").glob("*.schema.json")}
    run(["git", "diff", "--check"], "diff-check.log")
    run(["git", "diff", "--exit-code", "--", "goodwill/synthetic-data", "acquisition", "data ingestion"], "other-lanes-unchanged.log")
    files = {}
    for directory in ("services", "apps/api", "goodwill_app", "db", "contracts", "tests"):
        for path in sorted((ROOT/directory).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                files[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    verification = {"state": "READY_FOR_REVIEW", "accepted": False,
                    "base_commit": commit, "tested_state": "working tree before local handoff commit",
                    "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
                    "python": sys.version, "commands": runs, "schema_regeneration_identical": same,
                    "implementation_file_sha256": files,
                    "not_run": ["React/TypeScript compile or browser UI checks (Node absent)", "independent ENG-04 acceptance", "remote GitHub CI", "live Goodwill/provider/Microsoft integration"],
                    "authorization": "Peyton reported Jack OC approval and explicitly requested combined setup/data work; no stakeholder acceptance invented"}
    verification["passed"] = all(r["exit_code"] == 0 for r in runs) and same
    (output/"verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    return 0 if verification["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
