# Safety report: Zone 5 Logger

🟡 **YELLOW** — Score: 50/100

> This score reflects which capabilities the shortcut requests, not proof of intent.

## Flagged actions
- 🟡 `is.workflow.actions.gethealthsample` (−15): Reads Health data (e.g. heart rate).
- 🟡 `is.workflow.actions.base64encode` (−15): Base64-encodes data — common before sending a payload to a server.
- 🟡 `is.workflow.actions.downloadurl` (−20): Sends a network request / downloads from a URL — possible exfiltration.
