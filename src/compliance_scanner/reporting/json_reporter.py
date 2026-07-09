"""Formats findings as JSON, and prints a readable console summary."""

import json
from dataclasses import asdict

from compliance_scanner.rules.base import Finding

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def to_json(findings: list[Finding]) -> str:
    sorted_findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f.severity, 99))
    return json.dumps([asdict(f) for f in sorted_findings], indent=2)


def print_console_summary(findings: list[Finding]) -> None:
    if not findings:
        print("No compliance violations found.")
        return

    sorted_findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f.severity, 99))
    print(f"\n{len(findings)} compliance violation(s) found:\n")
    for f in sorted_findings:
        print(f"[{f.severity.upper()}] {f.rule_id} — {f.resource_type}.{f.resource_name}")
        print(f"  {f.message}")
        print(f"  Reference: {f.regulation_reference}\n")
