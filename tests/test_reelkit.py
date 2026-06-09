from scripts.reelkit import build_kit

ENTRY = {
    "name": "Show Clipboard", "slug": "show-clipboard", "category": "Utilities",
    "description": "Displays the current clipboard contents.",
    "source": "https://www.icloud.com/shortcuts/abc123",
    "scan": {"score": 85, "tier": "yellow", "badge": "yellow", "findings": []},
}


def test_kit_has_caption_badge_and_cta():
    kit = build_kit(ENTRY)
    assert "🟡" in kit["caption"]
    assert "85/100" in kit["caption"]
    assert "link in bio" in kit["caption"].lower()
    assert ENTRY["source"] in kit["caption"]


def test_kit_hashtags_include_core_and_category():
    kit = build_kit(ENTRY)
    tags = " ".join(kit["hashtags"]).lower()
    assert "#shortcuts" in tags
    assert "#utilities" in tags
    assert all(t.startswith("#") for t in kit["hashtags"])


def test_kit_overlay_has_three_beats():
    kit = build_kit(ENTRY)
    assert len(kit["overlay"]) == 3
    assert "Show Clipboard" in kit["overlay"][1]
