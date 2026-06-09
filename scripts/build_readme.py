"""Generate the README leaderboard and per-shortcut SAFETY.md from each
shortcut's meta.yml + scan.json. Pure render functions are unit-tested; the
filesystem glue (load_entries / main) walks shortcuts/<slug>/."""
import json
import plistlib
from pathlib import Path

import yaml

BADGE = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
PLATFORM = {"ios": "📱", "macos": "💻", "watchos": "⌚", "ipados": "📱"}
ROOT = Path(__file__).parents[1]
RULES = ROOT / "scripts" / "risk_rules.yml"


def action_descriptions(rules_path=RULES):
    """Map each known action id to its human-readable reason (reused as the prompt step)."""
    data = yaml.safe_load(Path(rules_path).read_text())
    return {r["id"]: r["reason"] for r in data["rules"]}


def load_actions(plist_path):
    with open(plist_path, "rb") as fh:
        doc = plistlib.load(fh)
    return doc.get("WFWorkflowActions", [])


def render_prompt(entry, actions, descriptions):
    """A plain-English, copy-pasteable recipe derived from the shortcut's actions, so the
    prompt always matches what the shortcut actually does."""
    lines = [
        f"# {entry['name']} — prompt",
        "",
        "> A plain-English recipe of this shortcut, auto-generated from its actions so it",
        "> always matches what the shortcut really does. Read it before you install — or hand",
        "> it to your own agent to rebuild the shortcut from scratch.",
        "",
        entry["description"],
        "",
        "## Steps",
        "",
    ]
    n = 1
    for a in actions:
        ident = a.get("WFWorkflowActionIdentifier", "")
        if ident == "is.workflow.actions.comment":
            continue
        lines.append(f"{n}. {descriptions.get(ident, f'`{ident}`')}")
        n += 1
    lines += ["", f"**Install:** {entry['source']}", ""]
    return "\n".join(lines)


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
        "",
        "More private than running an agent: no resident process, no credentials to leak, "
        "**no sandbox VM needed** (OpenClaw · NemoClaw · Hermes · OpenShell all require one) — "
        "Shortcuts runs on-device behind Apple's permission prompts, so the OS *is* the sandbox.",
        "",
        "It works *with* Siri AI, not against it: **Siri** runs your shortcuts by voice, "
        "**Apple Intelligence** powers their reasoning on-device (the \"Use Model\" action), "
        "and you keep full custom control.",
        "",
        "Because that reasoning runs on-device or via **Apple Private Cloud Compute** — never "
        "stored, never used for training, cryptographically verifiable — even **high-risk data** "
        "(health, location, private notes, and enterprise **IP**) is safe to feed an agent here. "
        "Same architecture, personal or enterprise. "
        "See [Why Shortcuts?](docs/why-shortcuts.md) for the full privacy/security case.",
        "",
        "**Every entry installs in one tap from a real Apple iCloud link** — no clicking",
        "through to another repo. Browse, check the safety score, tap Install.",
        "",
        "Runs on: 📱 iOS · 💻 macOS · ⌚ watchOS",
        "",
        "Each shortcut has a one-tap **Install** link *and* a 📋 **prompt** — a plain-English",
        "recipe you can read before installing (or hand to your own agent to rebuild it).",
        "",
        "| Safety | Score | Shortcut | Install | Prompt | Category | Runs on | What it does |",
        "| :----: | :---: | -------- | :-----: | :----: | -------- | :-----: | ------------ |",
    ]
    for e in rows:
        s = e["scan"]
        out.append(
            f"| {BADGE[s['badge']]} | {s['score']} | "
            f"[{e['name']}](shortcuts/{e['slug']}/) | {install_link(e)} | "
            f"[📋](shortcuts/{e['slug']}/prompt.md) | {e['category']} | "
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
    descriptions = action_descriptions()
    for e in entries:
        d = ROOT / "shortcuts" / e["slug"]
        (d / "SAFETY.md").write_text(render_safety(e))
        actions = load_actions(d / "shortcut.plist")
        (d / "prompt.md").write_text(render_prompt(e, actions, descriptions))
    print(f"rebuilt README + {len(entries)} SAFETY.md + {len(entries)} prompt.md files")


if __name__ == "__main__":
    main()
