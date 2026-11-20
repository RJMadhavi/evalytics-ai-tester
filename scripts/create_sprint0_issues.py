#!/usr/bin/env python3
"""Create GitHub issues for Sprint 0 from backlog/*.md and add them to the EvalyticsQA project.

Requires the GitHub CLI (gh), logged in with project access:
    gh auth login
    gh auth refresh -s project

Usage (run from the repo root):
    python3 scripts/create_sprint0_issues.py          # dry run, prints what it would do
    python3 scripts/create_sprint0_issues.py --run    # really creates the Sprint 0 issues

To create other stories, name them and the sprint:
    python3 scripts/create_sprint0_issues.py --ids EVA-S0020,EVA-S0021 --sprint "Sprint 1"
    python3 scripts/create_sprint0_issues.py --ids EVA-S0020,EVA-S0021 --sprint "Sprint 1" --run

Issues that already exist (same title) are skipped, so a second run does not create duplicates.
"""
import argparse, json, pathlib, re, subprocess, sys

OWNER = "RJMadhavi"
REPO = "RJMadhavi/evalytics-ai-tester"
PROJECT = "5"                 # the project number, shown as #5 on the Projects tab
DEFAULT_SPRINT_NAME = "Sprint 0"   # iteration title you set in the Sprint field
SPRINT_FIELD = "Sprint"
ESTIMATE_FIELD = "Estimates"
STATUS_FIELD = "Status"

parser = argparse.ArgumentParser(description="Create GitHub issues from backlog files")
parser.add_argument("--run", action="store_true", help="really create issues (default is a dry run)")
parser.add_argument("--ids", help="comma separated story ids, for example EVA-S0020,EVA-S0021")
parser.add_argument("--sprint", help="iteration title to put them in, for example 'Sprint 1'")
ARGS = parser.parse_args()
DRY = not ARGS.run
WANTED = {i.strip() for i in ARGS.ids.split(",")} if ARGS.ids else None
SPRINT_NAME = ARGS.sprint or ("Sprint 1" if WANTED else DEFAULT_SPRINT_NAME)


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Command failed: {' '.join(cmd)}\n{r.stderr}")
    return r.stdout.strip()


def parse(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.split("#")[0].strip()
    return meta, m.group(2).strip()


items = []
for folder in ("backlog/stories", "backlog/tasks"):
    for p in sorted(pathlib.Path(folder).glob("EVA-*.md")):
        meta, body = parse(p)
        if WANTED is not None:
            if meta.get("id") in WANTED:
                items.append((meta, body, p))
        elif meta.get("sprint") == "S00":
            items.append((meta, body, p))

print(f"Found {len(items)} item(s) for {SPRINT_NAME}.")
if WANTED:
    missing = WANTED - {m["id"] for m, _, _ in items}
    if missing:
        sys.exit(f"Not found in backlog/: {sorted(missing)}")
if DRY:
    for meta, _, p in items:
        print(f"  [{meta['id']}] {meta['title']}  ({meta.get('estimate_hours', '?')} h)  <- {p}")
    print("\nDry run only. Add --run to create them.")
    sys.exit(0)

QUERY = """
query($owner: String!, $num: Int!) {
  user(login: $owner) {
    projectV2(number: $num) {
      id
      fields(first: 50) {
        nodes {
          ... on ProjectV2Field { id name }
          ... on ProjectV2IterationField {
            id name
            configuration { iterations { id title } }
          }
          ... on ProjectV2SingleSelectField { id name options { id name } }
        }
      }
    }
  }
}
"""
data = json.loads(sh(["gh", "api", "graphql", "-f", f"query={QUERY}",
                      "-f", f"owner={OWNER}", "-F", f"num={PROJECT}"]))
project = data["data"]["user"]["projectV2"]
if not project:
    sys.exit(f"Project number {PROJECT} not found for {OWNER}. Check PROJECT at the top of the script.")
by_name = {f["name"]: f for f in project["fields"]["nodes"] if f}
for needed in (SPRINT_FIELD, ESTIMATE_FIELD, STATUS_FIELD):
    if needed not in by_name:
        sys.exit(f"Field '{needed}' not found in the project. Found: {list(by_name)}")

iteration = next((i for i in by_name[SPRINT_FIELD].get("configuration", {}).get("iterations", [])
                  if i["title"] == SPRINT_NAME), None)
if not iteration:
    sys.exit(f"Iteration '{SPRINT_NAME}' not found in the Sprint field.")
ready = next((o for o in by_name[STATUS_FIELD].get("options", []) if o["name"] == "Ready"), None)

for meta, body, p in items:
    title = f"[{meta['id']}] {meta['title']}"
    existing = json.loads(sh(["gh", "issue", "list", "--repo", REPO, "--state", "all",
                              "--search", f"[{meta['id']}] in:title", "--json", "number,title"]))
    if any(e["title"] == title for e in existing):
        print(f"Skipped {title}: an issue with this title already exists (#{existing[0]['number']})")
        continue
    footer = f"\n\n---\nSource file: `{p}`  \nEstimate: {meta.get('estimate_hours', '?')} h"
    url = sh(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body + footer])
    item = json.loads(sh(["gh", "project", "item-add", PROJECT, "--owner", OWNER,
                          "--url", url, "--format", "json"]))["id"]
    base = ["gh", "project", "item-edit", "--id", item, "--project-id", project["id"]]
    sh(base + ["--field-id", by_name[SPRINT_FIELD]["id"], "--iteration-id", iteration["id"]])
    if meta.get("estimate_hours"):
        sh(base + ["--field-id", by_name[ESTIMATE_FIELD]["id"], "--number", meta["estimate_hours"]])
    if ready:
        sh(base + ["--field-id", by_name[STATUS_FIELD]["id"], "--single-select-option-id", ready["id"]])
    print(f"Created {title}  ->  {url}")

print("Done. Open the project table and check Sprint, Estimates and Status.")
