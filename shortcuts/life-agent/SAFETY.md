# Safety report: Life Agent

🟡 **YELLOW** — Score: 30/100

> This score reflects which capabilities the shortcut requests, not proof of intent.

## Flagged actions
- 🟡 `is.workflow.actions.gethealthsample` (−15): Reads Health data (e.g. heart rate).
- 🟡 `is.workflow.actions.getupcomingevents` (−15): Reads your calendar events.
- 🟡 `is.workflow.actions.getcurrentlocation` (−15): Reads your current location.
- 🟡 `is.workflow.actions.getcurrentfocus` (−5): Reads your current Focus mode.
- 🟡 `is.workflow.actions.downloadurl` (−20): Sends a network request / downloads from a URL — possible exfiltration.
