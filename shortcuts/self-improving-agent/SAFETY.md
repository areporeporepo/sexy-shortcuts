# Safety report: Self-Improving Agent

🟡 **YELLOW** — Score: 65/100

> This score reflects which capabilities the shortcut requests, not proof of intent.

## Flagged actions
- 🟡 `is.workflow.actions.documentpicker.open` (−10): Reads a file from Files/iCloud Drive.
- 🟡 `is.workflow.actions.downloadurl` (−20): Sends a network request / downloads from a URL — possible exfiltration.
- 🟡 `is.workflow.actions.documentpicker.save` (−5): Saves/overwrites a file in Files/iCloud Drive.
