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

## Safer, more personal, and zero-setup vs. agent frameworks

Agent frameworks — OpenClaw, NemoClaw, Hermes-style agents, and the sandboxed runtimes like
OpenShell they run inside — are powerful, but their power comes from running a **resident
process with broad access** to a machine. That is *why* they need a sandbox VM/container in
the first place: you have to wrap an autonomous, credential-holding process to contain what
it might do. Shortcuts inverts the whole model.

| | Agent frameworks (OpenClaw · NemoClaw · Hermes · OpenShell) | Apple Shortcuts |
| --- | --- | --- |
| Where it runs | A resident process, usually inside a sandbox VM/container | On-device, first-party — **no sandbox needed; the OS is the sandbox** |
| Trust boundary | "can do anything you can" — must be externally contained | Apple's per-action permission prompts, on every run |
| Setup | Runtime, keys, sandbox environment to stand up | Zero — built into iOS 27 / macOS 27 / watchOS 27 |
| Your data | Flows through the agent's process/credentials | Stays on your device; each grant is explicit and revocable |
| Personalization | Configured per agent | Bound to **your** device, **your** Health/Calendar/Photos, **your** permissions |
| Best at | Open-ended reasoning, coding, long autonomous tasks | Fast, safe, repeatable, deeply personal on-device actions |

So for the lane it's built for — *"do this with my data, on my phone, safely, every time"* —
Shortcuts is **more secure, more private, and more personal** than any agent framework,
because there's no autonomous process and no machine to expose. **Honest boundary (again):**
this is not a claim that Shortcuts out-reasons agents — it doesn't. They *think*; Shortcuts
*acts*, privately. Use both: the agent plans, the shortcut executes on-device.

## More customizable than Siri — and works *with* Siri AI, not against it

Siri and Apple Intelligence do what **Apple ships** — a fixed set of built-in behaviors you
can't reshape. A Shortcut does what **you wire**: your own action chain, your own logic and
conditions, your own model call, your own data flow, your own memory file.

But this isn't Shortcuts *vs.* Siri — they **complement each other**, in both directions:

- **Siri runs your shortcuts.** Say "Hey Siri, <name>" and your custom flow executes —
  Siri becomes the voice front-end to anything you build.
- **Your shortcuts use Apple Intelligence.** The on-device **"Use Model"** action lets a
  shortcut call Apple's private, on-device model — so the agents in this repo can run their
  reasoning step with *zero network and no API key*, fully inside Apple Intelligence.
- **Siri suggests your shortcuts** at the right moment based on context.

So the stack is: **Apple Intelligence provides the on-device brains, Siri provides the
voice, and Shortcuts provide the custom, permissioned hands.** You get more customization
than Siri alone could ever offer, while staying inside the same on-device, permissioned
sandbox — none of the exposure of running your own agent.

## Why this repo

Shortcuts' one residual risk is a shortcut that *abuses* the permissions you granted it —
a "Run Shell Script" action on Mac, or a step that quietly POSTs your clipboard to a URL.
That's exactly the gap this repo's automated **safety score** closes: every shortcut is
decompiled and scanned so you can *see* what it can do before you run it. The safest
automation engine, plus the missing trust layer on top of it.
