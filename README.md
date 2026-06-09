# awesome-shortcuts

> ⚠️ **Requires iOS 27 · macOS 27 · watchOS 27**

The **safety-rated app store for Apple Shortcuts**. Every shortcut is decompiled, scored 🟢/🟡/🔴 for safety, installs in one tap from a real Apple iCloud link, and ships a readable 📋 prompt so you see what it does before you run it.

- 🛡️ **Safety-scored** — every shortcut is scanned; the score shows exactly what it can do.
- ⚡ **One-tap install** — a real Apple iCloud link in every row, not a link to another repo.
- 🔒 **Private by design** — agents reason on-device via the **Apple Foundation Models** or **Private Cloud Compute**, so even high-risk personal data and enterprise IP is safe. No sandbox, no resident agent.

→ **[Why Shortcuts?](docs/why-shortcuts.md)** — the full privacy & security case: on-device Apple Foundation Models, Private Cloud Compute, the device-only data moat, and how this compares to cloud agents.

Runs on: 📱 iOS · 💻 macOS · ⌚ watchOS

| Safety | Score | Shortcut | Install | Prompt | Category | Runs on | What it does |
| :----: | :---: | -------- | :-----: | :----: | -------- | :-----: | ------------ |
| 🟡 | 95 | [Blue Shirt Craig](shortcuts/blue-shirt-craig/) | — | [📋](shortcuts/blue-shirt-craig/prompt.md) | Fun | 📱 💻 | A random absurd fact about Craig Federighi's legendary blue shirt — then offers to find you one. 👕✈️ |
| 🟡 | 85 | [Show Clipboard](shortcuts/show-clipboard/) | — | [📋](shortcuts/show-clipboard/prompt.md) | Utilities | 📱 💻 | Displays the current clipboard contents. |
| 🟡 | 80 | [Shortcut Smith](shortcuts/shortcut-smith/) | — | [📋](shortcuts/shortcut-smith/prompt.md) | Developer | 📱 💻 | An agentic shortcut that builds shortcuts for you: describe what you want, it asks an on-device Apple Foundation Model (AFM 3 Core, via the Use Model action) for a step-by-step recipe in this repo's prompt format, and saves it to build or submit. Shortcuts making shortcuts. |
| 🟡 | 65 | [Self-Improving Agent](shortcuts/self-improving-agent/) | — | [📋](shortcuts/self-improving-agent/prompt.md) | Developer | 📱 💻 | A scheduled memory-loop: reads a growing memory file, asks an on-device Apple Foundation Model (AFM 3 Core) what to improve and what to build next, appends the learning back. The system self-improves over runs. More customizable than Siri — it does what you wire. |
| 🟡 | 65 | [Usage Coach](shortcuts/usage-coach/) | — | [📋](shortcuts/usage-coach/prompt.md) | Productivity | 📱 💻 | An agentic improving shortcut: reads a screenshot of your Screen Time, asks the on-device, natively multimodal Apple Foundation Model (AFM 3 Core Advanced) to spot time sinks, and recommends shortcuts to reclaim that time — logging the plan weekly. Works off a screenshot you take (iOS exposes no Screen Time data). |
| 🟡 | 60 | [PI Weekly Briefing](shortcuts/pi-weekly-briefing/) | — | [📋](shortcuts/pi-weekly-briefing/prompt.md) | Productivity | 📱 💻 | A weekly research-lab briefing: the week's calendar + the latest arXiv in your field, then deep-links into Slack/email/Zoom to triage. Run it every Monday. Customizable per PI. |
| 🟡 | 50 | [Zone 5 Logger](shortcuts/zone5-logger/) | — | [📋](shortcuts/zone5-logger/prompt.md) | Health | 📱 ⌚ | Auto-logs Zone 5 heart-rate sessions from Apple Watch to a GitHub CSV (date, peak HR). Inspired by Helgerud 2007. Sends health data off-device — read the prompt before installing. |
| 🟡 | 30 | [Life Agent](shortcuts/life-agent/) | — | [📋](shortcuts/life-agent/prompt.md) | Productivity | 📱 | One personal agent that fuses the signals only Shortcuts can read — heart rate, calendar, location, Focus, battery — and asks an on-device Apple Foundation Model (AFM 3 Core) what to do next. A cloud agent can read none of these; this is the device-only moat. Reads a lot, so it scores low on purpose: you see everything it touches. |
