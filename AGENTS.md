# AGENTS.md — what to tell your agent

awesome-shortcuts is built to be contributed to **by your AI agent** (Claude Code, Codex,
etc.). Paste the block below to your agent and it can open a correct PR for you.

---

## Copy-paste this to your agent

> You are contributing a shortcut to the `awesome-shortcuts` repo. Do this:
>
> 1. Create `shortcuts/<slug>/shortcut.plist` — the shortcut's actions as an **unsigned XML
>    plist** with a top-level `WFWorkflowActions` array. Each action is a dict with
>    `WFWorkflowActionIdentifier` (e.g. `is.workflow.actions.gettext`) and
>    `WFWorkflowActionParameters`. Validate with `plutil -lint`.
> 2. Create `shortcuts/<slug>/meta.yml` with: `name`, `slug`, `author`, `category`
>    (Productivity/Utilities/Media/Health/Home/Developer/Fun), `source` (the real
>    `https://www.icloud.com/shortcuts/<ID>` link — never a placeholder or a link you don't
>    control), `description`, `platforms` (subset of `[ios, ipados, macos, watchos]` — only
>    list a platform where every action actually works; anything opening Safari or rich UI
>    is **not** watchOS), `date_added`, `tags`.
> 3. Run `python -m scripts.vet_pr` (scores it) then `python -m scripts.build_readme`
>    (regenerates README + the shortcut's `SAFETY.md` + `prompt.md`).
> 4. Run `python -m pytest -q -m "not network"` — all tests must pass.
> 5. Open a PR using the template. Paste the score line from step 3.
>
> Hard rules:
> - **Be honest about what the shortcut can do.** Shortcuts cannot read Slack/Gmail message
>   content, scrape app UI, or self-modify. Don't claim capabilities the OS doesn't expose.
> - **No 🔴 red actions** (`runshellscript`, `runsshscript`, `runjavascriptonwebpage`, or
>   off-device exfiltration) without a documented reason — they're blocked from auto-merge.
> - The `prompt.md` is auto-generated from the actions, so it always matches reality. Don't
>   hand-write it; just make the actions correct.

---

## How scoring works (so your agent can predict the badge)

The scanner reads each action and applies `scripts/risk_rules.yml`: score = 100 − Σ(penalties),
tier = the worst action's tier. 🟢 green = device-local only · 🟡 yellow = reads
private data / network / leaves the app · 🔴 red = arbitrary code or exfiltration.
Unknown actions default to yellow and are logged to `.learnings/unknown-actions.md` for
promotion into the ruleset (the scanner improves over time).

See `CONTRIBUTING.md` for the human flow and `docs/why-shortcuts.md` for the project's pitch.
