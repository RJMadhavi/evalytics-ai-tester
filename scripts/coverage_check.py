#!/usr/bin/env python3
"""Module coverage check for the Evalytics QA repo.

Reads:
  docs/modules.yaml          the list of modules (M01-M18)
  backlog/stories/*.md       stories; their YAML front matter has `covers: [M09, ...]`
  test-cases/*.yaml|*.yml|*.md   optional; a test case links to a story with
                                 `story: EVA-S0012` or `stories: [EVA-S0012, ...]`

Prints:
  - in-scope modules with no story            (gap)
  - in-scope modules with stories but no test case
  - skipped modules and the reason            (the "untested areas" list)
  - problems: duplicate IDs, unknown modules in `covers`, stories with no `covers`

Usage:
  pip install pyyaml
  python scripts/coverage_check.py            # report only, always exits 0 unless the files are unreadable
  python scripts/coverage_check.py --strict   # exit 1 if a P0/P1 module has no story, or any problem is found
  python scripts/coverage_check.py --root /path/to/repo
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")


def read_front_matter(path: Path) -> dict:
    """Return the YAML front matter of a .md file, or {} if there is none."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        print(f"WARNING: bad front matter in {path}: {exc}", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def read_yaml_file(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"WARNING: bad YAML in {path}: {exc}", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def load_modules(root: Path) -> list[dict]:
    path = root / "docs" / "modules.yaml"
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    data = read_yaml_file(path)
    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        sys.exit(f"ERROR: {path} has no `modules:` list")
    return modules


def load_stories(root: Path) -> list[dict]:
    stories = []
    for path in sorted((root / "backlog" / "stories").glob("*.md")):
        fm = read_front_matter(path)
        if not fm:
            continue
        fm["_file"] = str(path.relative_to(root))
        stories.append(fm)
    return stories


def load_test_cases(root: Path) -> list[dict]:
    cases = []
    folder = root / "test-cases"
    if not folder.exists():
        return cases
    for path in sorted(folder.iterdir()):
        if path.suffix in (".yaml", ".yml"):
            data = read_yaml_file(path)
        elif path.suffix == ".md":
            data = read_front_matter(path)
        else:
            continue
        if data:
            data["_file"] = str(path.relative_to(root))
            cases.append(data)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="repo root (default: current directory)")
    parser.add_argument("--strict", action="store_true", help="exit 1 on P0/P1 gaps or problems")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    modules = load_modules(root)
    stories = load_stories(root)
    cases = load_test_cases(root)

    module_ids = [m["id"] for m in modules]
    problems: list[str] = []

    # --- problems: duplicate IDs -------------------------------------------------
    seen: dict[str, str] = {}
    for s in stories:
        sid = s.get("id")
        if not sid:
            problems.append(f"{s['_file']}: story has no `id`")
            continue
        if sid in seen:
            problems.append(f"duplicate story ID {sid}: {seen[sid]} and {s['_file']}")
        seen[sid] = s["_file"]

    # --- map modules -> stories --------------------------------------------------
    stories_by_module: dict[str, list[str]] = {mid: [] for mid in module_ids}
    for s in stories:
        covers = as_list(s.get("covers"))
        if not covers:
            problems.append(f"{s['_file']}: story has no `covers` (which module does it test?)")
        for mid in covers:
            if mid not in stories_by_module:
                problems.append(f"{s['_file']}: `covers` names unknown module {mid}")
            else:
                stories_by_module[mid].append(s.get("id", s["_file"]))

    # --- map stories -> test cases -----------------------------------------------
    cases_by_story: dict[str, list[str]] = {}
    for c in cases:
        links = as_list(c.get("story")) + as_list(c.get("stories"))
        for sid in links:
            cases_by_story.setdefault(sid, []).append(c.get("id", c["_file"]))

    # --- report -------------------------------------------------------------------
    in_scope = [m for m in modules if m.get("scope") == "in"]
    skipped = [m for m in modules if m.get("scope") == "skipped"]
    print(f"Modules: {len(modules)} total, {len(in_scope)} in scope, {len(skipped)} skipped")
    print(f"Stories found: {len(stories)}    Test cases found: {len(cases)}\n")

    print("IN-SCOPE MODULES")
    print(f"  {'ID':<5}{'Pri':<5}{'Stories':<9}{'TestCases':<11}Name")
    gaps_story: list[dict] = []
    gaps_case: list[dict] = []
    for m in in_scope:
        sids = stories_by_module[m["id"]]
        ncases = sum(len(cases_by_story.get(sid, [])) for sid in sids)
        flag = ""
        if not sids:
            gaps_story.append(m)
            flag = "  <- NO STORY"
        elif cases and ncases == 0:
            gaps_case.append(m)
            flag = "  <- no test case"
        print(f"  {m['id']:<5}{m.get('priority', '?'):<5}{len(sids):<9}{ncases:<11}{m['name']}{flag}")

    print("\nGAPS")
    if gaps_story:
        for m in gaps_story:
            print(f"  [{m.get('priority', '?')}] {m['id']} {m['name']}: no story covers it")
    else:
        print("  every in-scope module has at least one story")
    if gaps_case:
        for m in gaps_case:
            print(f"  [{m.get('priority', '?')}] {m['id']} {m['name']}: stories exist but no test case links to them")
    elif not cases:
        print("  (no test cases found yet, so test-case coverage was not checked)")

    print("\nSKIPPED MODULES (untested areas for the final report)")
    if skipped:
        for m in skipped:
            reason = m.get("reason") or "NO REASON GIVEN"
            if not m.get("reason"):
                problems.append(f"{m['id']} is skipped but has no `reason` in modules.yaml")
            print(f"  {m['id']} {m['name']}: {reason} (since {m.get('skipped_on', '?')})")
    else:
        print("  none")

    print("\nPROBLEMS")
    if problems:
        for p in problems:
            print(f"  - {p}")
    else:
        print("  none")

    if args.strict:
        blocking = [m for m in gaps_story if m.get("priority") in ("P0", "P1")]
        if blocking or problems:
            print("\nSTRICT MODE: failing (P0/P1 module without a story, or problems above).")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
