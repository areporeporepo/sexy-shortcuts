# awesome-shortcuts — Design Spec

**Date:** 2026-06-09
**Status:** Approved (pending spec review)
**Target platform:** iOS 27 / macOS (2026 release), Shortcuts.app current format

## 0. Why Shortcuts? (opening pitch — also the README intro)

If you want maximum automation leverage on your iPhone with maximum privacy and
security, **Shortcuts is the engine.** Here's the honest case for why.

**It runs at a privilege level no third-party app or agent can reach.** Shortcuts is
Apple's *first-party* automation layer. Through App Intents and system actions it can
drive other apps, touch Files / Photos / Health / Home / Contacts / Messages / Focus,
and fire automations from time, location, NFC tags, and device state — capabilities the
OS exposes to Shortcuts and to nothing else a normal user can install. A regular app
lives in its own box; Shortcuts is the sanctioned bridge *between* the boxes.

**Correction to a common claim:** Shortcuts does **not** have unrestricted access to "all
files." No iOS app does — that's iOS sandboxing working as designed, and it's a feature,
not a limitation. What Shortcuts *does* have is the **broadest sanctioned reach** available
to a normal user: the full Files document tree (with your grant), system + cross-app
actions via App Intents, and deep OS automation hooks. Breadth *inside* the sandbox — that
is the point, and it's a stronger claim than "access to everything" because it's true.

**This is where it beats agent frameworks on privacy and security.** Tools like Hermes,
OpenClaw, and Claude Code are powerful, but they get that power by running an autonomous
process on your machine with your shell, your files, and your credentials. The trust
boundary becomes *"this program can do anything I can do."* Your machine is exposed by
design. Shortcuts inverts that: it executes **on-device**, gated by **Apple's per-action
permission prompts**, with **no resident agent holding your shell.** You get automation
leverage without handing a program your whole computer. For a huge class of tasks —
"every morning, pull X, transform it, send it to Y" — that is strictly the safer engine.

**Phone-native — no laptop required. It's "OpenClaw without a laptop."** This is the
biggest, broadest part of the case. Agent frameworks need a *computer* running an
autonomous process. Shortcuts runs **on the iPhone itself** — no Mac, no resident agent,
no shell — and still reaches across your apps. It automates whatever apps *expose*: the
share sheet, App Intents, URL schemes, plus OS triggers (NFC tap, time of day, location,
Focus mode, "when this app opens"). That means real flows built around the apps you
actually live in — e.g. act on the TikTok/Instagram/YouTube video you're viewing (save it,
re-share it, run it through a transform, log it), post on a schedule, or fire an automation
when you arrive somewhere — **all from the phone, all sandboxed.** It is agent-like leverage
in your pocket without exposing a machine.

> Honest boundary: Shortcuts drives apps through the hooks those apps publish — it is **not**
> an arbitrary in-app UI scraper. "Do things with TikTok" means "use what TikTok exposes to
> Shortcuts (share sheet, intents, links)," not "remote-control TikTok's screen." Stated this
> way it's both true and still impressive — and the precision is the credibility.

**It replaces a lot.** A single shortcut can stand in for a pile of single-purpose
utility apps and the risky one-off scripts people otherwise run with broad permissions.
Fewer apps, fewer trackers, fewer processes with access to your stuff.

**Why this repo, then.** Shortcuts' one residual risk is a shortcut that *abuses* the
permissions you granted it — e.g. a "Run Shell Script" action on Mac, or a step that
quietly POSTs your clipboard to some URL. That's precisely the gap this repo's automated
**safety score** closes: every shortcut is decompiled and scanned so you can *see* what it
can do before you run it. "Why Shortcuts" and "why a scored repo" are the same story — the
safest automation engine, plus the missing trust layer on top of it.

**Complementary, not a competitor — and it replaces *some* things.** Shortcuts is not an
agent; it can't reason over a repo or do open-ended work, and we never claim it beats coding
agents at their job. The right framing is two-layer: agents (Claude Code, etc.) *think and
plan*; Shortcuts is the **safe, on-device execution layer** they — or you — hand fixed,
permissioned actions to. Alongside that, a good shortcut outright **replaces** a pile of
single-purpose utility apps and risky one-off scripts. So: complements your agents, replaces
your junk apps. That positioning wins more users than "better than Claude Code" ever would.

> Tone note for the README: confident but never overstated. Every privilege claim must
> survive a power-user fact-check. We win the credibility fight by being *more* precise
> than the competition, not louder. Frame Shortcuts as **complementary** to agents and a
> **replacement** for utility-app sprawl — never as a rival to coding agents.

## 1. Purpose & Goal

A community GitHub repository that collects Apple Shortcuts from around the world,
with one thing no existing collection has: **every shortcut is automatically scanned
and scored for safety**. The safety score *is* the product — it's the trust signal and
the virality hook ("the only shortcut repo that scores every shortcut for safety").

**Positioning:** *Shortcuts are the new apps.* As app fatigue grows, a good shortcut
replaces a single-purpose app — and this repo is the **safety-rated app store** for them:
browse, see exactly what each one can do (the score), install with one tap. That framing —
an app store where every "app" is open, free, and safety-graded — is the whole pitch.

**Primary success metric:** stars (be the most-starred shortcuts repo).
**Secondary:** contributions per week, % of shortcuts with a green safety badge.

### Two repos
- `awesome-shortcuts` — **canonical**. All PRs, issues, and stars land here.
- `sexy-shortcuts` — **read-only auto-mirror** (personal-taste brand / second funnel),
  push-mirrored from canonical on every merge. Zero double-work.

## 2. Competitive Landscape (research 2026-06-09)

| Repo | What it is | Weakness |
|---|---|---|
| `myusuf3/appleshortcuts` | "awesome shareable apple/siri shortcuts" | personal dump, no vetting |
| `cinaq/apple-shortcuts` | daily-task automations | small, personal |
| `twilsonco/SiriShortcuts`, `ticky/siri-shortcuts` | personal collections | several marked "Outdated!" |
| `brucebentley` catalog | 125+ shortcuts + Action Directory | a gist, unmaintained, no contribution flow |
| `huaminghuangtw/Apple-Shortcuts-Gallery` | curated gallery | no safety vetting |

**Confirmed gap:** none do automated safety scanning or scoring; most are stale personal
dumps rather than maintained, contributable community hubs. The Bruce Bentley "Action
Directory" (125+ documented actions) is a ready-made taxonomy we reuse to weight the scanner.

## 3. The Safety Problem & How We Solve It (core technical risk)

Apple Shortcuts are not text/prompts. Shared `.shortcut` files are **AEA-signed/encrypted**
(since iOS 15), so a raw signed file is opaque to both our scanner and human PR reviewers.
A `.shortcut` can contain genuinely dangerous actions (run shell/SSH/JS, POST to a URL,
read contacts/location), and an iCloud link can be swapped server-side *after* vetting.

**Solution — snapshot the unsigned plist at PR time:**

- **Unsigned shortcut:** rename `.shortcut` → `.plist`, then `plutil -convert xml1`. Trivial.
- **iCloud link:** the unsigned plist is reachable via
  `https://www.icloud.com/shortcuts/api/records/<ID>` → JSON → download URL → binary plist
  → `plutil -convert xml1`. **CI fetches and freezes this at PR time**, which both makes the
  content human-/machine-readable *and* eliminates the "link swapped later" risk (we store
  the snapshot, not the live link).

**iOS 27 caveat:** iOS 27 was announced at WWDC this week (June 2026). The AEA/signing
format may have changed. **Implementation must re-validate the decompile path against a real
iOS 27 `.shortcut` and iCloud link before building the rest.** This is the first build step;
if it fails, the whole approach needs revisiting.

## 4. Repository Structure

```
shortcuts/
  <slug>/
    shortcut.plist         # decompiled, human-readable XML — the source of truth, diffable in PRs
    shortcut.shortcut      # convenience import file (re-signed "for anyone"); optional if signing unavailable in CI
    meta.yml               # name, author, category, source iCloud link, tags, date_added
    icon.png               # optional screenshot
    SAFETY.md              # AUTO-GENERATED: score, badge, list of flagged actions w/ rationale
README.md                  # AUTO-GENERATED index: leaderboard by score, grouped by category, badges
CONTRIBUTING.md            # one-step flow: open an issue/PR with an iCloud link; CI does the rest
scripts/
  decompile.py             # iCloud link OR .shortcut -> unsigned XML plist
  scan.py                  # parse WFWorkflowActions -> risk findings -> 0..100 score + badge
  build_readme.py          # regenerate README + per-shortcut SAFETY.md from meta + scan output
  risk_rules.yml           # action-identifier -> risk weight + human explanation (the "benchmark" ruleset)
.github/
  workflows/
    vet.yml                # on PR: decompile -> scan -> comment score -> block if red
    index.yml              # on merge to main: rebuild README + SAFETY.md, commit
    mirror.yml             # on merge to main: push-mirror to sexy-shortcuts
  ISSUE_TEMPLATE/
    submit-shortcut.yml    # structured submission: iCloud link + name + category + description
```

Each unit has one job and a clear interface:
- `decompile.py`: input = iCloud URL or path; output = unsigned XML plist + extracted metadata.
- `scan.py`: input = plist + `risk_rules.yml`; output = JSON findings (score, badge, flagged actions).
- `build_readme.py`: input = all `meta.yml` + scan JSON; output = `README.md` + each `SAFETY.md`.

These are independently testable (feed fixtures, assert output) and composed by CI.

## 5. The Safety Scanner = "The Benchmark"

`scan.py` walks `WFWorkflowActions` in the plist and matches each action's identifier
against `risk_rules.yml`. Score = `100 − Σ(weighted penalties)`, clamped to `[0, 100]`.

| Tier | Example action identifiers | Why |
|---|---|---|
| 🔴 Red (high) | `runshellscript`, `runsshscript`, `runjavascript`, `url`/`downloadurl` POST to non-allowlisted host, `base64encode` adjacent to a network call | arbitrary code / exfiltration |
| 🟡 Yellow (medium) | `getcontacts`, `getcurrentlocation`, `getclipboard`, photos access, `openapp`, file download | privacy-sensitive / side effects |
| 🟢 Green (low) | text, math, formatting, UI, device-local-only actions | benign |

Output per shortcut:
- **Score 0–100 + 🟢/🟡/🔴 badge** rendered in README and `SAFETY.md`.
- A human-readable list of every flagged action and *why* (transparency builds trust).

Red-tier shortcuts are **blocked from auto-merge** and require explicit maintainer override
with a documented reason. The badge in the README is the screenshot-bait / social proof.

> The scoring is a heuristic, not a guarantee. `SAFETY.md` and README state this plainly:
> the score reflects *which capabilities a shortcut requests*, not proof of intent. We never
> claim a shortcut is "safe" — we claim it has been scanned and what it can do is disclosed.

## 6. Contributor Flow

1. Contributor opens an issue using `submit-shortcut.yml` with an **iCloud share link** +
   name + category + description.
2. `vet.yml` runs `decompile.py` (fetch + freeze unsigned plist) → `scan.py` → posts the
   score + flagged actions as a comment.
3. On acceptance, a maintainer (or a bot) opens a PR that drops the frozen `shortcut.plist`,
   `meta.yml`, and scan output into `shortcuts/<slug>/`.
4. On merge: `index.yml` regenerates README + `SAFETY.md`; `mirror.yml` syncs `sexy-shortcuts`.

## 7. Virality Mechanics (structural, not bolted on)

- Auto-generated **leaderboard** README sorted by safety score + popularity.
- Per-shortcut **safety badge** = social proof + shareable screenshot.
- `awesome-` naming + GitHub topics (`apple-shortcuts`, `ios-shortcuts`, `siri-shortcuts`) for discovery.
- One-step contribution (just paste a link) lowers the contribution barrier to near zero.
- `sexy-shortcuts` mirror = a second brand/funnel for free.

### Distribution engine: TikTok + Instagram Reels (the primary growth channel)

This is the strategy, not an afterthought. Shortcuts are **uniquely suited to short-form
vertical video** in a way almost no developer project is: a useful shortcut is a complete,
satisfying 15-second phone screen-recording. The viral loop:

1. **Hook (0–3s):** a relatable pain ("Stop paying for an app that does THIS").
2. **Payoff (3–12s):** screen-record the shortcut running on a real iPhone — instant, tactile.
3. **CTA (12–15s):** "One tap to install — link in bio." Link goes to the repo / the shortcut's
   iCloud link. Caption answers the inevitable *"is this a virus?"* with the 🟢 **safety score**.

Why it compounds:
- **Phone-native = native content.** No laptop, no terminal in frame — it looks like a normal
  iPhone tip, which is exactly what the TikTok/IG algorithms reward.
- **The safety badge is the differentiator made visible.** "The only shortcut repo that scores
  every one for safety" is a one-line caption that builds trust and stands out.
- **Each shortcut = one piece of content.** A repo of N shortcuts is a content calendar of N
  videos. Contributions literally generate marketing material.
- **Funnel:** TikTok/IG Reels → bio link → GitHub repo → ⭐ + new contributors → more shortcuts
  → more videos. The repo and the social channels feed each other.

> Out of scope for the *codebase*, but part of the strategy: a lightweight `MARKETING.md` /
> content playbook can capture hooks, formats, and a posting cadence. The repo's job is to make
> each shortcut trivially demoable and trustworthy; the channels do the distribution.

## 8. Error Handling

- `decompile.py`: iCloud ID not found / API shape changed / not a valid plist → fail the PR
  check with a clear message; never store a partial/unverified artifact.
- `scan.py`: unknown action identifier → counts as **yellow** (unknown ≠ safe) and is logged
  so `risk_rules.yml` can be extended.
- CI: any decompile/scan failure blocks merge (fail-closed — matches the security posture in CLAUDE.md).

## 9. Testing Strategy

- **Fixtures:** a handful of hand-built plists (one obviously-red with `runshellscript`,
  one yellow with `getcontacts`, one all-green) checked into `tests/fixtures/`.
- **`scan.py`:** assert each fixture yields the expected tier/score — the scanner is pure and
  deterministic, so this is straightforward unit testing (TDD).
- **`decompile.py`:** integration test against one real unsigned `.shortcut` and (network-gated)
  one real iCloud link; assert it produces valid XML with a `WFWorkflowActions` array.
- **`build_readme.py`:** golden-file test (given fixture meta + scan JSON, assert generated markdown).

## 10. Build Order

1. **Validate decompile on iOS 27** — prove `.shortcut`→plist and iCloud-link→plist both work
   against a real iOS 27 artifact. Gate: if this fails, stop and rethink.
2. `scan.py` + `risk_rules.yml` + scoring, TDD against fixtures.
3. `build_readme.py` + `SAFETY.md` generation.
4. CI workflows (`vet`, `index`, `mirror`) + issue template + CONTRIBUTING.
5. Seed 2–3 example shortcuts; create `sexy-shortcuts` mirror; publish, set topics.
6. (Later session) Content/seeding pass + launch.

## 11. Content tooling (in scope) vs. auto-posting (out)

**In scope — a content-kit generator (`reelkit.py`):** given a shortcut's `meta.yml` +
`scan.json`, emit a ready-to-post bundle: a caption (hook + "one tap to install — link in
bio"), the safety badge line, suggested hashtags, and an on-screen text overlay script.
Turns every repo entry into shootable marketing material. Pure text generation, no APIs,
zero ToS risk. (See plan Task 13.)

**Out of scope (v1) — automated posting to TikTok/Instagram.** Their APIs heavily restrict
programmatic publishing and it violates ToS for most accounts; automating it risks bans,
which would destroy the distribution strategy it's meant to serve. The human posts; the tool
just makes posting trivial. Revisit only with official Creator/Graph API access.

## 12. Out of Scope (v1 — YAGNI)

- Sandbox/dynamic execution of shortcuts (heavy infra; static scan is the v1 benchmark).
- A web frontend / hosted site (README *is* the UI for v1).
- Auth, accounts, ratings — GitHub stars/issues are the social layer.
- Shortcuts that *target* GitHub/TikTok/IG are welcome as normal **categories** in the
  collection (cheap — just a `category` value), but no special tooling is built for them in v1.
- Automated re-signing of `.shortcut` files if CI signing proves unreliable — fall back to
  storing only the readable plist + iCloud link and let users import from the link.
