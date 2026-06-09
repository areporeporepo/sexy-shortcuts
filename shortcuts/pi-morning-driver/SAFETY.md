# Safety report: PI Morning Driver

🟡 **YELLOW** — Score: 50/100

> This score reflects which capabilities the shortcut requests, not proof of intent.

## Flagged actions
- 🟡 `is.workflow.actions.getupcomingevents` (−15): Reads your calendar events.
- 🟡 `is.workflow.actions.getweatherconditions` (−10): Reads weather for your current location.
- 🟡 `is.workflow.actions.downloadurl` (−20): Sends a network request / downloads from a URL — possible exfiltration.
- 🟡 `is.workflow.actions.openurl` (−5): Opens a URL in the browser — a visible side effect, leaves the app.
