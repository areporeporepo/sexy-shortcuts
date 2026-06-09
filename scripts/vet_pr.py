"""Scan every shortcuts/<slug>/shortcut.plist, write scan.json next to each, and
exit non-zero if any shortcut is red (blocks auto-merge). Run by CI on each PR."""
import json
import sys
from pathlib import Path

from scripts.scan import scan_plist

ROOT = Path(__file__).parents[1]
RULES = Path(__file__).with_name("risk_rules.yml")


def vet_directory(shortcuts_dir, rules_path=RULES):
    results = {}
    has_red = False
    for plist in sorted(Path(shortcuts_dir).glob("*/shortcut.plist")):
        slug = plist.parent.name
        r = scan_plist(plist, rules_path)
        (plist.parent / "scan.json").write_text(json.dumps(r, indent=2))
        results[slug] = r
        if r["tier"] == "red":
            has_red = True
    return results, has_red


def main():  # pragma: no cover - CI glue
    results, has_red = vet_directory(ROOT / "shortcuts")
    for slug, r in results.items():
        print(f"{r['badge']:>6}  {r['score']:>3}  {slug}")
    if has_red:
        print("::error::One or more shortcuts are RED. Maintainer override required.")
        sys.exit(1)


if __name__ == "__main__":
    main()
