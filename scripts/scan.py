"""Decompile-free static scanner: reads a Shortcuts plist, matches each action
against the risk ruleset, returns a tier, a 0-100 score, and findings."""
import plistlib
import sys
from pathlib import Path

import yaml

TIER_ORDER = {"green": 0, "yellow": 1, "red": 2}


def _load_rules(rules_path):
    data = yaml.safe_load(Path(rules_path).read_text())
    by_id = {r["id"]: r for r in data["rules"]}
    return by_id, data["default_unknown"]


def scan_plist(plist_path, rules_path):
    by_id, unknown = _load_rules(rules_path)
    with open(plist_path, "rb") as fh:
        doc = plistlib.load(fh)
    actions = doc.get("WFWorkflowActions", [])

    findings = []
    penalty = 0
    worst = "green"
    for action in actions:
        ident = action.get("WFWorkflowActionIdentifier", "")
        rule = by_id.get(ident)
        if rule is None:
            rule = {**unknown, "id": ident}
        if rule["tier"] == "green" and rule["weight"] == 0:
            continue
        findings.append({"id": rule["id"], "tier": rule["tier"],
                         "weight": rule["weight"], "reason": rule["reason"]})
        penalty += rule["weight"]
        if TIER_ORDER[rule["tier"]] > TIER_ORDER[worst]:
            worst = rule["tier"]

    score = max(0, 100 - penalty)
    return {"score": score, "tier": worst, "badge": worst, "findings": findings}


if __name__ == "__main__":
    import json
    rules = Path(__file__).with_name("risk_rules.yml")
    print(json.dumps(scan_plist(sys.argv[1], rules), indent=2))
