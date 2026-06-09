# Why Shortcuts?

If you want maximum automation leverage on your iPhone with maximum privacy and
security, **Shortcuts is the engine.** Here's the honest case.

## It runs at a privilege level no third-party app or agent can reach

Shortcuts is Apple's *first-party* automation layer. Through App Intents and system
actions it can drive other apps, touch Files / Photos / Health / Home / Contacts /
Messages / Focus, and fire automations from time, location, NFC tags, and device state —
capabilities the OS exposes to Shortcuts and to nothing else a normal user can install.
A regular app lives in its own box; Shortcuts is the sanctioned bridge *between* the boxes.

**A common claim, corrected:** Shortcuts does **not** have unrestricted access to "all
files." No iOS app does — that's iOS sandboxing working as designed. What Shortcuts *does*
have is the **broadest sanctioned reach** available to a normal user: the full Files
document tree (with your grant), system + cross-app actions via App Intents, and deep OS
automation hooks. Breadth *inside* the sandbox — that is the point, and it's a stronger
claim than "access to everything" because it's true.

## Phone-native — no laptop required. "OpenClaw without a laptop."

Agent frameworks (Claude Code, Hermes, OpenClaw) get their power by running an autonomous
process on a *computer* with your shell, your files, and your credentials. The trust
boundary becomes *"this program can do anything I can do"* — your machine is exposed by
design. Shortcuts inverts that: it runs **on the iPhone itself**, gated by **Apple's
per-action permission prompts**, with **no resident agent holding your shell.**

It still reaches across your apps — automating whatever they expose (share sheet, App
Intents, URL schemes) plus OS triggers (NFC, time, location, Focus, "when this app
opens"). So you can build real flows around the apps you live in — act on a TikTok /
Instagram / YouTube video you're viewing, post on a schedule, react to arriving somewhere —
**all from the phone, all sandboxed.** Agent-like leverage in your pocket without exposing
a machine.

> Honest boundary: Shortcuts drives apps through the hooks those apps publish — it is **not**
> an arbitrary in-app UI scraper. "Do things with TikTok" means "use what TikTok exposes to
> Shortcuts," not "remote-control its screen."

## Complementary, not a competitor — and it replaces *some* things

Shortcuts is not an agent; it can't reason over a repo or do open-ended work, and it does
not beat coding agents at their job. Two layers: agents *think and plan*; Shortcuts is the
**safe, on-device execution layer** they — or you — hand fixed, permissioned actions to.
Alongside that, a good shortcut outright **replaces** a pile of single-purpose utility apps
and risky one-off scripts. Complements your agents, replaces your junk apps.

## Why this repo

Shortcuts' one residual risk is a shortcut that *abuses* the permissions you granted it —
a "Run Shell Script" action on Mac, or a step that quietly POSTs your clipboard to a URL.
That's exactly the gap this repo's automated **safety score** closes: every shortcut is
decompiled and scanned so you can *see* what it can do before you run it. The safest
automation engine, plus the missing trust layer on top of it.
