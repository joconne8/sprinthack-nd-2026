import re, json, subprocess, sys
from pathlib import Path
reg = Path("planning/requirements/register.md").read_text()
ids_registered = set(re.findall(r"REQ-[A-Z]+-\d+", reg))
doc = Path("planning/source-register.md").read_text()
cited = set(re.findall(r"REQ-[A-Z]+-\d+", doc))
missing = sorted(cited - ids_registered)
links = re.findall(r"\]\(([^)#]+)\)", doc)
bad = [l for l in links if not l.startswith("http") and not (Path("planning")/l).exists()]
rows = [l for l in doc.splitlines() if re.match(r"\| \d \|", l)]
out = {"cited_requirements": sorted(cited), "unregistered": missing, "broken_relative_links": bad, "source_rows": len(rows),
       "head": subprocess.check_output(["git","rev-parse","HEAD"], text=True).strip()}
print(json.dumps(out, indent=1)); sys.exit(1 if missing or bad or len(rows)!=9 else 0)
