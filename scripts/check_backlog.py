#!/usr/bin/env python3
"""Check that every backlog file has valid front matter.

Run from the repo root:
    python3 scripts/check_backlog.py

Checks, for each file in backlog/**/EVA-*.md:
  - front matter exists between --- lines
  - required fields are present: id, type, title, status
  - id matches the file name (EVA-S0001-... has id EVA-S0001)
  - status is one of the allowed values
  - estimate_hours, when present, is a number
  - no two files share the same id
Exit code 1 if anything is wrong, so CI turns red.
"""
import pathlib
import re
import sys

REQUIRED = ("id", "type", "title", "status")
STATUSES = {"Backlog", "Ready", "In Progress", "In Review", "Done"}

errors = []
seen = {}
files = sorted(pathlib.Path("backlog").rglob("EVA-*.md"))

for path in files:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{path}: no front matter found")
        continue
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.split("#")[0].strip()

    for field in REQUIRED:
        if not meta.get(field):
            errors.append(f"{path}: missing '{field}'")

    item_id = meta.get("id", "")
    if item_id and not path.name.startswith(item_id + "-") and path.stem != item_id:
        errors.append(f"{path}: id '{item_id}' does not match the file name")
    if item_id in seen:
        errors.append(f"{path}: duplicate id '{item_id}' (also in {seen[item_id]})")
    seen[item_id] = path

    status = meta.get("status", "")
    # epics use free text such as "In Progress"; accept the board values only
    if status and status not in STATUSES:
        errors.append(f"{path}: status '{status}' is not one of {sorted(STATUSES)}")

    hours = meta.get("estimate_hours")
    if hours:
        try:
            float(hours)
        except ValueError:
            errors.append(f"{path}: estimate_hours '{hours}' is not a number")

print(f"Checked {len(files)} backlog files.")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("All backlog files look good.")
