#!/usr/bin/env python3
"""Run independent controls and an actual isolated CLI/browser rehearsal.

This script creates disposable synthetic local state, never resets a user's state,
and records outputs for review. Optional --base-url uses an already prepared
rehearsal server and leaves its lifecycle to the caller.
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def run(command, log, env):
    with log.open("w") as output:
        result = subprocess.run(command, cwd=str(ROOT), env=env, stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError("Command failed (%s); inspect %s" % (result.returncode, log))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", default=shutil.which("node"))
    parser.add_argument("--node-modules", default=os.environ.get("NODE_PATH"))
    parser.add_argument("--chrome-path", default=os.environ.get("CHROME_PATH"))
    parser.add_argument("--base-url", help="Existing isolated Sep1–29 rehearsal server")
    parser.add_argument("--output", default=".runtime/showcase-qa")
    args = parser.parse_args()
    if not args.node:
        parser.error("Provide --node or install the documented Node runtime")
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if args.node_modules:
        env["NODE_PATH"] = args.node_modules
    if args.chrome_path:
        env["CHROME_PATH"] = args.chrome_path
    env["QA_OUTPUT"] = str(output / "browser")
    report = {"started_at": datetime.now(timezone.utc).isoformat(), "passed": False,
              "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip(),
              "working_tree_changes": subprocess.check_output(["git", "status", "--short"], cwd=str(ROOT), text=True).splitlines(),
              "output": str(output)}
    server = None
    server_log = None
    try:
        run([sys.executable, "-m", "unittest", "tests.test_showcase", "-v"], output / "financial-controls.log", env)
        with tempfile.TemporaryDirectory(prefix="aimsigh-independent-qa-") as state:
            base = args.base_url
            if not base:
                run([sys.executable, "-m", "goodwill_app", "--state-root", state, "demo", "prepare"],
                    output / "prepare.log", env)
                with socket.socket() as temporary_socket:
                    temporary_socket.bind(("127.0.0.1", 0))
                    port = temporary_socket.getsockname()[1]
                command = [sys.executable, "-m", "goodwill_app", "--state-root", state, "demo", "serve",
                           "--port", str(port), "--node", args.node]
                if args.node_modules:
                    command += ["--node-modules", args.node_modules]
                if args.chrome_path:
                    command += ["--chrome-path", args.chrome_path]
                server_log = (output / "server.log").open("w")
                server = subprocess.Popen(command, cwd=str(ROOT), env=env, stdout=server_log, stderr=subprocess.STDOUT)
                base = "http://127.0.0.1:%d" % port
                deadline = time.monotonic() + 90
                while time.monotonic() < deadline:
                    if server.poll() is not None:
                        raise RuntimeError("Demo server exited during startup; inspect server.log")
                    try:
                        with urlopen(base + "/api/showcase/v1/snapshot", timeout=2) as response:
                            if response.status == 200:
                                break
                    except OSError:
                        time.sleep(0.2)
                else:
                    raise RuntimeError("Demo server did not become ready within 90 seconds")
            env["BASE_URL"] = base
            report["base_url"] = base
            run([args.node, "tests/showcase_browser.cjs"], output / "browser.log", env)
            report["passed"] = True
    except Exception as exc:
        report["error"] = str(exc)
    finally:
        if server:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=10)
        if server_log:
            server_log.close()
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        (output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
