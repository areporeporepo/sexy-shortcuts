# Contributing

> 🤖 **Contributing with an AI agent?** See [AGENTS.md](AGENTS.md) for a copy-paste block
> that tells your agent (Claude Code, Codex, …) exactly how to open a correct PR.

Two ways to contribute:

**A. Open a PR directly** (you or your agent) — add `shortcuts/<slug>/shortcut.plist` +
`meta.yml`, run the tooling, and open a PR with the [template](.github/PULL_REQUEST_TEMPLATE.md).
CI scans it and posts the safety score.

**B. Just submit a link** — open a **Submit a shortcut** issue with your iCloud link:
1. CI fetches the unsigned shortcut, decompiles it, and posts a safety score.
2. A maintainer reviews the flagged actions and, if accepted, opens the PR.
3. On merge, the README leaderboard, `SAFETY.md`, and `prompt.md` regenerate automatically.

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
