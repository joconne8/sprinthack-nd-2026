#!/usr/bin/env python3
"""Check one assignment's prerequisites and print its ready-to-paste prompt.

Read-only: never starts agents, changes git, or calls external services.
Evidence checks validate supplied records, not their truth or test execution.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?", help="Task ID, e.g. GOV-01 or ING-02")
    parser.add_argument("--list", action="store_true", help="List every packet")
    parser.add_argument("--acceptance", type=Path,
                        help="Human-reviewed accepted task evidence JSON")
    parser.add_argument("--emit-blocked", action="store_true",
                        help="Print a blocked prompt for review; does NOT clear its gates")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "assignments.json").read_text())
    cards = {card["id"]: card for card in manifest["assignments"]}
    records = {}
    if args.acceptance:
        payload = json.loads(args.acceptance.read_text())
        records = payload.get("accepted_tasks", {})
        if not isinstance(records, dict):
            raise ValueError("accepted_tasks must be an object keyed by task ID")
    if args.list:
        for card in manifest["assignments"]:
            print(f"{card['id']:8} {card['mode']:20} {card['priority']:2} "
                  f"{card['scope']:7} deps={','.join(card['dependencies']) or '-'} "
                  f"{card['packet_path']}")
        return 0
    if not args.task or args.task not in cards:
        parser.error("Specify a known task ID or --list")
    card = cards[args.task]
    blockers = []
    for dependency in card["dependencies"]:
        record = records.get(dependency) or {}
        required = ["reviewer", "evidence", "tests", "accepted_commit"]
        if record.get("accepted") is not True:
            blockers.append(f"{dependency}: human acceptance not recorded")
            continue
        if any(not record.get(field) for field in required):
            blockers.append(f"{dependency}: reviewer/commit/evidence/test records incomplete")
            continue
        if not re.fullmatch(r"[0-9a-fA-F]{40}", record["accepted_commit"]):
            blockers.append(f"{dependency}: expected full 40-character commit SHA")
            continue
        if not isinstance(record["evidence"], list) or not isinstance(record["tests"], list):
            blockers.append(f"{dependency}: evidence and tests must be arrays")
            continue
        if any(not isinstance(test, dict) or not test.get("command")
               or test.get("result") != "pass"
               or not test.get("log") for test in record["tests"]):
            blockers.append(f"{dependency}: passing checks with command and log required")
    print(f"Assignment: {card['id']} — {card['title']}")
    print("Mode:", card["mode"], "| max elapsed minutes:", card["limits"]["max_minutes"])
    print("Do not execute live/pilot actions. Supervisor packets are coordination-only.")
    print("This checker does not verify artifact content, run tests, or launch workers.")
    if blockers:
        print("\nBLOCKED:\n- " + "\n- ".join(blockers))
        if not args.emit_blocked:
            return 2
        print("\nREVIEW COPY ONLY — prerequisites remain blocked.")
    else:
        print("\nPrerequisite records structurally complete; manually verify artifacts, "
              "current issue comments, runtime and lane claim before executing.")
    # Runtime/artifact decisions must use the actual checkout, not stale packaging.
    print("\n----- READY-TO-PASTE PACKET -----\n")
    path = root / card["packet_path"]
    print(path.read_text())
    return 2 if blockers else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f"Assignment check failed: {exc}", file=sys.stderr)
        sys.exit(1)