# Contributing

1. Open a **Submit a shortcut** issue and paste your iCloud share link.
2. CI fetches the unsigned shortcut, decompiles it, and posts a safety score.
3. A maintainer reviews the flagged actions and, if accepted, opens a PR that adds
   `shortcuts/<slug>/` with the frozen `shortcut.plist`, `meta.yml`, and `scan.json`.
4. On merge, the README leaderboard and `SAFETY.md` regenerate automatically.

## Safety rules

- 🔴 Red shortcuts (shell/SSH/JS execution, exfiltration) are blocked from auto-merge
  and require a documented maintainer override.
- The score reflects what a shortcut *can do* — it is not proof of intent. Always read
  the shortcut's `SAFETY.md` before importing.

## Running the tooling locally

```bash
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python -m pytest -q -m "not network"   # tests
./.venv/bin/python -m scripts.vet_pr               # scan all shortcuts -> scan.json
./.venv/bin/python -m scripts.build_readme         # regenerate README + SAFETY.md
./.venv/bin/python -m scripts.reelkit <slug>       # generate a TikTok/Reels content kit
```
