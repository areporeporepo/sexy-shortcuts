from pathlib import Path
from scripts.vet_pr import vet_directory

FIX = Path(__file__).parent / "fixtures"
RULES = Path(__file__).parents[1] / "scripts" / "risk_rules.yml"


def test_vet_directory_returns_red_for_shell(tmp_path):
    sc = tmp_path / "shortcuts" / "bad"
    sc.mkdir(parents=True)
    (sc / "shortcut.plist").write_bytes((FIX / "red_shell.plist").read_bytes())
    results, has_red = vet_directory(tmp_path / "shortcuts", RULES)
    assert has_red is True
    assert results["bad"]["tier"] == "red"


def test_vet_directory_clean_for_green(tmp_path):
    sc = tmp_path / "shortcuts" / "ok"
    sc.mkdir(parents=True)
    (sc / "shortcut.plist").write_bytes((FIX / "green_text.plist").read_bytes())
    results, has_red = vet_directory(tmp_path / "shortcuts", RULES)
    assert has_red is False
    assert results["ok"]["score"] == 100
