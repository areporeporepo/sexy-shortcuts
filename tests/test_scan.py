from pathlib import Path
from scripts.scan import scan_plist

FIX = Path(__file__).parent / "fixtures"
RULES = Path(__file__).parents[1] / "scripts" / "risk_rules.yml"


def test_green_shortcut_scores_100_and_green():
    r = scan_plist(FIX / "green_text.plist", RULES)
    assert r["tier"] == "green"
    assert r["badge"] == "green"
    assert r["score"] == 100
    assert r["findings"] == []


def test_yellow_shortcut_is_yellow_with_penalty():
    r = scan_plist(FIX / "yellow_contacts.plist", RULES)
    assert r["tier"] == "yellow"
    assert r["score"] == 85
    assert any(f["id"] == "is.workflow.actions.getmycontacts" for f in r["findings"])


def test_red_shortcut_is_red():
    r = scan_plist(FIX / "red_shell.plist", RULES)
    assert r["tier"] == "red"
    assert r["badge"] == "red"
    assert r["score"] == 40
    assert r["findings"][0]["reason"].startswith("Runs a shell script")


def test_unknown_action_treated_as_yellow(tmp_path):
    p = tmp_path / "unk.plist"
    p.write_text(
        '<?xml version="1.0"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict>'
        '<key>WFWorkflowActions</key><array><dict>'
        '<key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.madeup</string>'
        '<key>WFWorkflowActionParameters</key><dict/></dict></array></dict></plist>'
    )
    r = scan_plist(p, RULES)
    assert r["tier"] == "yellow"
    assert r["score"] == 90
