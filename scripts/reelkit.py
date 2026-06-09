"""Turn a shortcut entry (meta + scan) into a ready-to-post short-form video kit:
caption, hashtags, and a 3-beat on-screen text overlay. Pure text — no APIs, no posting."""
import json
import sys
from pathlib import Path

import yaml

BADGE = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
ROOT = Path(__file__).parents[1]


def build_kit(entry):
    s = entry["scan"]
    badge = BADGE[s["badge"]]
    caption = (
        f"Stop downloading an app for this. 📱 {entry['name']} — {entry['description']}\n\n"
        f"{badge} Safety score: {s['score']}/100 (we scan every shortcut so you don't get a virus).\n"
        f"One tap to install — link in bio 👆 {entry['source']}"
    )
    hashtags = [
        "#shortcuts", "#appleshortcuts", "#iphonetips", "#ios",
        f"#{entry['category'].lower().replace(' ', '')}", "#iphonehacks", "#productivity",
    ]
    overlay = [
        "POV: you stop paying for an app that does THIS 👇",
        f"{entry['name']}: {entry['description']}",
        f"{badge} {s['score']}/100 safe • one tap to install • link in bio",
    ]
    return {"caption": caption, "hashtags": hashtags, "overlay": overlay}


def _load_entry(slug):  # pragma: no cover - filesystem glue
    d = ROOT / "shortcuts" / slug
    entry = yaml.safe_load((d / "meta.yml").read_text())
    entry["scan"] = json.loads((d / "scan.json").read_text())
    return entry


if __name__ == "__main__":  # pragma: no cover - CLI glue
    print(json.dumps(build_kit(_load_entry(sys.argv[1])), ensure_ascii=False, indent=2))
