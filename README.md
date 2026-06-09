# awesome-shortcuts

> ⚠️ **Requires iOS 27 · macOS 27 · watchOS 27** (the 2026 releases). The developer beta is available now — install it to use these shortcuts.

The safety-rated app store for Apple Shortcuts. Every shortcut is decompiled and
scored for safety — each score reflects what a shortcut *can do*, not proof of intent.

More private than running an agent: no resident process, no credentials to leak, **no sandbox VM needed** (OpenClaw · NemoClaw · Hermes · OpenShell all require one) — Shortcuts runs on-device behind Apple's permission prompts, so the OS *is* the sandbox.

It works *with* Siri AI, not against it: **Siri** runs your shortcuts by voice, **Apple Intelligence** powers their reasoning on-device (the "Use Model" action), and you keep full custom control.

Because that reasoning runs on-device or via **Apple Private Cloud Compute** — never stored, never used for training, cryptographically verifiable — even **high-risk personal data** (health, location, private notes) is safe to feed an agent here. See [Why Shortcuts?](docs/why-shortcuts.md) for the full privacy/security case.

**Every entry installs in one tap from a real Apple iCloud link** — no clicking
through to another repo. Browse, check the safety score, tap Install.

Runs on: 📱 iOS · 💻 macOS · ⌚ watchOS

Each shortcut has a one-tap **Install** link *and* a 📋 **prompt** — a plain-English
recipe you can read before installing (or hand to your own agent to rebuild it).

| Safety | Score | Shortcut | Install | Prompt | Category | Runs on | What it does |
| :----: | :---: | -------- | :-----: | :----: | -------- | :-----: | ------------ |
| 🟡 | 95 | [Blue Shirt Craig](shortcuts/blue-shirt-craig/) | — | [📋](shortcuts/blue-shirt-craig/prompt.md) | Fun | 📱 💻 | A random absurd fact about Craig Federighi's legendary blue shirt — then offers to find you one. 👕✈️ |
| 🟡 | 85 | [Show Clipboard](shortcuts/show-clipboard/) | — | [📋](shortcuts/show-clipboard/prompt.md) | Utilities | 📱 💻 | Displays the current clipboard contents. |
| 🟡 | 80 | [Shortcut Smith](shortcuts/shortcut-smith/) | — | [📋](shortcuts/shortcut-smith/prompt.md) | Developer | 📱 💻 | An agentic shortcut that builds shortcuts for you: describe what you want, it asks a model for a step-by-step recipe (in this repo's prompt format) and saves it to build or submit. Shortcuts making shortcuts. |
| 🟡 | 65 | [Self-Improving Agent](shortcuts/self-improving-agent/) | — | [📋](shortcuts/self-improving-agent/prompt.md) | Developer | 📱 💻 | A scheduled memory-loop: reads a growing memory file, asks a model what to improve and what to build next, appends the learning back. The system self-improves over runs. More customizable than Siri — it does what you wire. |
| 🟡 | 65 | [Usage Coach](shortcuts/usage-coach/) | — | [📋](shortcuts/usage-coach/prompt.md) | Productivity | 📱 💻 | An agentic improving shortcut: reads a screenshot of your Screen Time, asks a vision model to spot time sinks, and recommends shortcuts to reclaim that time — logging the plan weekly. Works off a screenshot you take (iOS exposes no Screen Time data). |
| 🟡 | 60 | [PI Weekly Briefing](shortcuts/pi-weekly-briefing/) | — | [📋](shortcuts/pi-weekly-briefing/prompt.md) | Productivity | 📱 💻 | A weekly research-lab briefing: the week's calendar + the latest arXiv in your field, then deep-links into Slack/email/Zoom to triage. Run it every Monday. Customizable per PI. |
| 🟡 | 50 | [Zone 5 Logger](shortcuts/zone5-logger/) | — | [📋](shortcuts/zone5-logger/prompt.md) | Health | 📱 ⌚ | Auto-logs Zone 5 heart-rate sessions from Apple Watch to a GitHub CSV (date, peak HR). Inspired by Helgerud 2007. Sends health data off-device — read the prompt before installing. |
| 🟡 | 30 | [Life Agent](shortcuts/life-agent/) | — | [📋](shortcuts/life-agent/prompt.md) | Productivity | 📱 | One personal agent that fuses the signals only Shortcuts can read — heart rate, calendar, location, Focus, battery — and asks a model what to do next. A cloud agent can read none of these; this is the device-only moat. Reads a lot, so it scores low on purpose: you see everything it touches. |
