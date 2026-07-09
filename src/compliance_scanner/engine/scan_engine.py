"""
The scan engine: takes a directory of Terraform files, runs every
registered rule against every resource, and collects findings.

This is the orchestration layer. Parser and rules don't know about
each other — the engine is what connects them.
"""

from compliance_scanner.parser import parse_terraform_directory
from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import Finding


def scan_directory(dir_path: str) -> list[Finding]:
    """Run all rules against all Terraform resources in a directory."""
    resources = parse_terraform_directory(dir_path)
    findings: list[Finding] = []

    for resource_type, named_configs in resources.items():
        for resource_name, config in named_configs.items():
            for rule in ALL_RULES:
                if resource_type not in rule.applies_to:
                    continue
                result = rule.check(resource_type, resource_name, config)
                if result is not None:
                    result.file_path = dir_path
                    findings.append(result)

    return findings
