#!/usr/bin/env python3
"""Attach existing Goodwill issues to a private GitHub Project using local gh auth.

Does not create issues, start agents, merge code, or deploy. Requires explicit
--allow-create if no matching project exists. Never reads or stores credentials.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def gh(*args, json_output=False):
    command = ["gh", *map(str, args)]
    if json_output:
        command += ["--format", "json"]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            f"GitHub CLI operation failed: {' '.join(command)}\n{result.stderr.strip()}"
        )
    return json.loads(result.stdout) if json_output else result.stdout.strip()


def rows(value, key):
    if isinstance(value, list):
        return value
    result = value.get(key)
    if not isinstance(result, list):
        raise RuntimeError(f"Unexpected GitHub CLI JSON: expected {key} array")
    return result


def content_url(item):
    content = item.get("content") or {}
    return content.get("url") or item.get("url")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path(__file__).with_name("backlog.json"))
    parser.add_argument("--owner", default="joconne8")
    parser.add_argument("--title", default="Goodwill — Three-Phase Delivery & Agents")
    parser.add_argument("--project-number", type=int)
    parser.add_argument("--allow-create", action="store_true",
                        help="Authorize creating a new private project if none matches")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    cards = manifest["cards"]
    if len({c["url"] for c in cards}) != len(cards):
        raise RuntimeError("Manifest has duplicate card URLs")
    gh("auth", "status")  # Uses the user's existing local credential store.
    listing = gh("project", "list", "--owner", args.owner,
                 "--limit", "100", json_output=True)
    projects = rows(listing, "projects")
    matches = [
        p for p in projects
        if (p.get("number") == args.project_number if args.project_number
            else p.get("title") == args.title)
    ]
    if len(matches) > 1:
        raise RuntimeError("Multiple matching projects; specify --project-number")
    if not matches:
        if args.project_number:
            raise RuntimeError("Requested project was not in the accessible listing")
        if len(projects) >= 100:
            raise RuntimeError("Project listing may be incomplete; select project explicitly")
        if not args.allow_create:
            raise RuntimeError(
                "No matching project. Select --project-number or authorize --allow-create."
            )
        project = gh("project", "create", "--owner", args.owner,
                     "--title", args.title, json_output=True)
        project_number = project["number"]
        # Set visibility before adding repository content.
        gh("project", "edit", project_number, "--owner", args.owner,
           "--visibility", "PRIVATE",
           "--description", "Goodwill acquisition, trusted data, dashboard and bounded agents.",
           "--readme",
           "Shared context and dependency hub: " + manifest["hub_url"]
           + "\nRead repository AGENTS.md and each issue before claiming work."
           + "\nNo production activity or unattended merges are authorized.")
    else:
        project = matches[0]
        project_number = project["number"]
        # Do not make an existing public board private without approval.
        if project.get("public") is True:
            raise RuntimeError(
                "Existing project is public; select a private project before adding private context."
            )
        if project.get("public") is not False:
            raise RuntimeError(
                "Project visibility was not reported; verify a private project before proceeding."
            )
    project_id = project.get("id")
    if not isinstance(project_id, str) or not project_id.startswith("PVT_"):
        raise RuntimeError("Missing GraphQL project ID in gh JSON; upgrade/verify GitHub CLI")
    gh("project", "link", project_number, "--owner", args.owner,
       "--repo", manifest["repository"])

    select_fields = {
        "Delivery phase": ["Governance", "Phase 1 — Ingestion", "Phase 2 — Data",
                           "Phase 3 — Application", "Engineering", "Rollout"],
        "Delivery priority": ["P0", "P1", "P2"],
        "Delivery scope": ["weekend", "stretch", "pilot"],
        "Agent workflow": ["Backlog", "Blocked", "In progress", "Review", "Done"],
    }
    text_fields = ["Task ID", "Agent lane", "Dependencies", "Human gate"]
    fields_result = gh("project", "field-list", project_number, "--owner", args.owner,
                       "--limit", "100", json_output=True)
    fields = {f["name"]: f for f in rows(fields_result, "fields")}
    for name, options in select_fields.items():
        if name not in fields:
            gh("project", "field-create", project_number, "--owner", args.owner,
               "--name", name, "--data-type", "SINGLE_SELECT",
               "--single-select-options", ",".join(options))
    for name in text_fields:
        if name not in fields:
            gh("project", "field-create", project_number, "--owner", args.owner,
               "--name", name, "--data-type", "TEXT")
    fields_result = gh("project", "field-list", project_number, "--owner", args.owner,
                       "--limit", "100", json_output=True)
    fields = {f["name"]: f for f in rows(fields_result, "fields")}
    for name, options in select_fields.items():
        available = {o["name"] for o in fields[name].get("options", [])}
        if not set(options).issubset(available):
            raise RuntimeError(f"Existing field {name} lacks required options; reconcile manually")

    item_result = gh("project", "item-list", project_number, "--owner", args.owner,
                     "--limit", "1000", json_output=True)
    items = rows(item_result, "items")
    if len(items) >= 1000:
        raise RuntimeError("Item listing may be incomplete; do not risk duplicate additions")
    existing = {content_url(item): item for item in items if content_url(item)}
    added = 0
    for card in cards:
        # Adding an issue already present is avoided. Current priority/status/owner
        # fields on existing items are intentionally preserved on rerun.
        if card["url"] in existing:
            print(f"Already attached (fields preserved): {card['id']} {card['url']}")
            continue
        item = gh("project", "item-add", project_number, "--owner", args.owner,
                  "--url", card["url"], json_output=True)
        existing[card["url"]] = item
        added += 1
        values = {
            "Delivery phase": card["phase"],
            "Delivery priority": card["priority"],
            "Delivery scope": card["scope"],
            "Agent workflow": card["initial_workflow"],
            "Task ID": card["id"],
            "Agent lane": card["lane"],
            "Dependencies": ", ".join(card.get("dependency_urls", [])) or "None",
            "Human gate": "Required" if card.get("human_gate") else "Check contracts/evidence",
        }
        for name, value in values.items():
            field = fields[name]
            flags = ["project", "item-edit", "--id", item["id"],
                     "--project-id", project_id, "--field-id", field["id"]]
            if name in select_fields:
                option = next(o for o in field["options"] if o["name"] == value)
                flags += ["--single-select-option-id", option["id"]]
            else:
                flags += ["--text", value]
            gh(*flags)
        print(f"Added and initialized: {card['id']} {card['url']}")
    # Include the existing data PR as evidence, without manufacturing a new task.
    pr_url = manifest.get("existing_pull_request_url")
    if pr_url and pr_url not in existing:
        gh("project", "item-add", project_number, "--owner", args.owner,
           "--url", pr_url)
    final = rows(gh("project", "item-list", project_number, "--owner", args.owner,
                    "--limit", "1000", json_output=True), "items")
    actual_urls = {content_url(item) for item in final}
    missing = [card["id"] for card in cards if card["url"] not in actual_urls]
    if missing:
        raise RuntimeError("Verification failed; missing cards: " + ", ".join(missing))
    print(f"Verified {len(cards)} repository cards; {added} newly attached.")
    print(project.get("url") or
          f"https://github.com/users/{args.owner}/projects/{project_number}")
    print("Create/save Board and table views in GitHub UI; group by Agent workflow.")
    print("This script does not start agents, merge code, or deploy.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        print(
            "Resolve local GitHub CLI authentication/Projects permissions. "
            "For OAuth CLI login, gh auth refresh -s project may be appropriate. "
            "Never paste tokens into chat.",
            file=sys.stderr,
        )
        sys.exit(1)