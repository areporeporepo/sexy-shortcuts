from pathlib import Path
from scripts.learn import collect_unknown

FIX = Path(__file__).parent / "fixtures"
RULES = Path(__file__).parents[1] / "scripts" / "risk_rules.yml"

UNKNOWN_PLIST = (
    '<?xml version="1.0"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
    '"http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict>'
    '<key>WFWorkflowActions</key><array><dict>'
    '<key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.madeup</string>'
    '<key>WFWorkflowActionParameters</key><dict/></dict></array></dict></plist>'
)


def test_collect_unknown_finds_unruled_action(tmp_path):
    sc = tmp_path / "shortcuts" / "x"
    sc.mkdir(parents=True)
    (sc / "shortcut.plist").write_text(UNKNOWN_PLIST)
    counts, where = collect_unknown(tmp_path / "shortcuts", RULES)
    assert counts["is.workflow.actions.madeup"] == 1
    assert "x" in where["is.workflow.actions.madeup"]


def test_known_actions_not_flagged(tmp_path):
    sc = tmp_path / "shortcuts" / "green"
    sc.mkdir(parents=True)
    (sc / "shortcut.plist").write_bytes((FIX / "green_text.plist").read_bytes())
    counts, _ = collect_unknown(tmp_path / "shortcuts", RULES)
    # gettext and showresult both have rules -> nothing unknown
    assert counts == {}
