"""Generate the README leaderboard and per-shortcut SAFETY.md from each
shortcut's meta.yml + scan.json. Pure render functions are unit-tested; the
filesystem glue (load_entries / main) walks shortcuts/<slug>/."""
import json
from pathlib import Path

import yaml

BADGE = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
PLATFORM = {"ios": "📱", "macos": "💻", "watchos": "⌚", "ipados": "📱"}
ROOT = Path(__file__).parents[1]


def install_link(entry):
    """A one-tap Apple iCloud install link — but only when the entry has a real link,
    never for the REPLACE_WITH_REAL_ID placeholder (no dead install buttons)."""
    src = entry.get("source", "")
    if "icloud.com/shortcuts/" in src and "REPLACE" not in src:
        return f"[⬇️ Install]({src})"
    return "—"


def platform_badges(entry):
    """Render an entry's platforms as emoji, in a stable order. Defaults to iOS."""
    plats = entry.get("platforms") or ["ios"]
    order = ["ios", "ipados", "macos", "watchos"]
    badges = []
    for p in order:
        if p in plats and PLATFORM[p] not in badges:
            badges.append(PLATFORM[p])
    return " ".join(badges) or "📱"


def render_safety(entry):
    s = entry["scan"]
    lines = [
        f"# Safety report: {entry['name']}",
        "",
        f"{BADGE[s['badge']]} **{s['tier'].upper()}** — Score: {s['score']}/100",
        "",
        "> This score reflects which capabilities the shortcut requests, not proof of intent.",
        "",
    ]
    if s["findings"]:
        lines.append("## Flagged actions")
        for f in s["findings"]:
            lines.append(f"- {BADGE[f['tier']]} `{f['id']}` (−{f['weight']}): {f['reason']}")
    else:
        lines.append("No flagged actions — device-local only.")
    return "\n".join(lines) + "\n"


def render_readme(entries):
    rows = sorted(entries, key=lambda e: e["scan"]["score"], reverse=True)
    out = [
        "# awesome-shortcuts",
        "",
        "> ⚠️ **Requires iOS 27 · macOS 27 · watchOS 27** (the 2026 releases). "
        "The developer beta is available now — install it to use these shortcuts.",
        "",
        "The safety-rated app store for Apple Shortcuts. Every shortcut is decompiled and",
        "scored for safety — each score reflects what a shortcut *can do*, not proof of intent.",
        "See [Why Shortcuts?](docs/why-shortcuts.md) for the privacy/security case.",
        "",
        "**Every entry installs in one tap from a real Apple iCloud link** — no clicking",
        "through to another repo. Browse, check the safety score, tap Install.",
        "",
        "Runs on: 📱 iOS · 💻 macOS · ⌚ watchOS",
        "",
        "| Safety | Score | Shortcut | Install | Category | Runs on | What it does |",
        "| :----: | :---: | -------- | :-----: | -------- | :-----: | ------------ |",
    ]
    for e in rows:
        s = e["scan"]
        out.append(
            f"| {BADGE[s['badge']]} | {s['score']} | "
            f"[{e['name']}](shortcuts/{e['slug']}/) | {install_link(e)} | {e['category']} | "
            f"{platform_badges(e)} | {e['description']} |"
        )
    return "\n".join(out) + "\n"


def load_entries(shortcuts_dir=ROOT / "shortcuts"):
    entries = []
    for meta_path in sorted(Path(shortcuts_dir).glob("*/meta.yml")):
        d = meta_path.parent
        entry = yaml.safe_load(meta_path.read_text())
        entry["scan"] = json.loads((d / "scan.json").read_text())
        entries.append(entry)
    return entries


def main():  # pragma: no cover - filesystem glue
    entries = load_entries()
    (ROOT / "README.md").write_text(render_readme(entries))
    for e in entries:
        (ROOT / "shortcuts" / e["slug"] / "SAFETY.md").write_text(render_safety(e))
    print(f"rebuilt README + {len(entries)} SAFETY.md files")


if __name__ == "__main__":
    main()
