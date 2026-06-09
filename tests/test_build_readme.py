from scripts.build_readme import (
    render_readme, render_safety, platform_badges, install_link, render_prompt,
)


def _entry(slug, name, score, tier, category):
    return {
        "slug": slug, "name": name, "category": category,
        "description": f"{name} desc", "source": "https://www.icloud.com/shortcuts/x",
        "scan": {"score": score, "tier": tier, "badge": tier, "findings": []},
    }


def test_render_readme_sorts_by_score_desc_and_shows_badges():
    entries = [
        _entry("a", "Alpha", 70, "yellow", "Productivity"),
        _entry("b", "Bravo", 100, "green", "Productivity"),
    ]
    md = render_readme(entries)
    assert md.index("Bravo") < md.index("Alpha")
    assert "🟢" in md and "🟡" in md
    assert "| Score |" in md


def test_platform_badges_orders_and_defaults():
    assert platform_badges({"platforms": ["watchos", "ios"]}) == "📱 ⌚"
    assert platform_badges({}) == "📱"  # default iOS when unspecified


def test_render_readme_shows_platform_column():
    e = _entry("a", "Alpha", 90, "green", "Fun")
    e["platforms"] = ["ios", "macos", "watchos"]
    md = render_readme([e])
    assert "| Runs on |" in md
    assert "📱 💻 ⌚" in md


def test_install_link_real_vs_placeholder():
    real = "https://www.icloud.com/shortcuts/abc123"
    assert install_link({"source": real}) == f"[⬇️ Install]({real})"
    assert install_link({"source": "https://www.icloud.com/shortcuts/REPLACE_WITH_REAL_ID"}) == "—"
    assert install_link({}) == "—"


def test_render_readme_has_install_column():
    e = _entry("a", "Alpha", 90, "green", "Fun")
    e["source"] = "https://www.icloud.com/shortcuts/realid123"
    md = render_readme([e])
    assert "| Install |" in md
    assert "[⬇️ Install](https://www.icloud.com/shortcuts/realid123)" in md


def test_render_prompt_numbers_steps_and_skips_comments():
    e = _entry("a", "Alpha", 90, "green", "Fun")
    actions = [
        {"WFWorkflowActionIdentifier": "is.workflow.actions.comment"},
        {"WFWorkflowActionIdentifier": "is.workflow.actions.gettext"},
        {"WFWorkflowActionIdentifier": "is.workflow.actions.showresult"},
    ]
    descriptions = {
        "is.workflow.actions.gettext": "Creates static text.",
        "is.workflow.actions.showresult": "Shows a result on screen.",
    }
    md = render_prompt(e, actions, descriptions)
    assert "1. Creates static text." in md
    assert "2. Shows a result on screen." in md
    assert "3." not in md  # the comment was skipped, only 2 numbered steps
    assert "**Install:**" in md


def test_render_safety_lists_findings():
    e = _entry("c", "Charlie", 40, "red", "Utilities")
    e["scan"]["findings"] = [{"id": "is.workflow.actions.runshellscript",
                              "tier": "red", "weight": 60,
                              "reason": "Runs a shell script — arbitrary code execution on macOS."}]
    md = render_safety(e)
    assert "🔴" in md
    assert "Score: 40/100" in md
    assert "Runs a shell script" in md
