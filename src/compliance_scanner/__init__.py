"""
rbi-compliance-scanner — Terraform static analysis for RBI/DPDPA
compliance requirements.

Public API. Everything a developer needs is importable directly from
this top-level package — they should never need to reach into
compliance_scanner.engine or compliance_scanner.rules.base directly.

Example:
    import compliance_scanner as rbi

    findings = rbi.scan("./my-terraform-project")
    for f in findings:
        print(f.severity, f.message)

    # or scan raw HCL text instead of a directory on disk
    findings = rbi.scan_string(my_terraform_text)
"""

from compliance_scanner.engine import scan_directory, scan_directory_large
from compliance_scanner.parser.terraform_parser import parse_terraform_string
from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import BaseRule, Finding
from compliance_scanner.reporting import to_json

__version__ = "0.1.0"


def scan(path: str) -> list[Finding]:
    """Scan a directory of Terraform files. Main entry point for most users."""
    return scan_directory(path)


def scan_large(path: str, workers: int | None = None, use_cache: bool = True):
    """
    Scan a large directory (thousands to hundreds of thousands of
    files). Returns a generator — iterate it directly to process
    findings as they're found, or wrap in list() for everything at
    once. Uses parallel parsing and caches unchanged files between
    runs (cache file: .rbi_scan_cache.json in the current directory).

    Example:
        for finding in rbi.scan_large("./huge-infra-repo"):
            print(finding.severity, finding.message)
    """
    return scan_directory_large(path, workers=workers, use_cache=use_cache)


def scan_string(terraform_text: str) -> list[Finding]:
    """
    Scan raw Terraform text directly, without needing it saved as a
    file. Useful for CI systems that already have the config in memory,
    or for testing a snippet quickly.
    """
    resources = parse_terraform_string(terraform_text)
    findings: list[Finding] = []
    for resource_type, named_configs in resources.items():
        for resource_name, config in named_configs.items():
            for rule in ALL_RULES:
                if resource_type not in rule.applies_to:
                    continue
                result = rule.check(resource_type, resource_name, config)
                if result is not None:
                    findings.append(result)
    return findings


__all__ = [
    "scan",
    "scan_large",
    "scan_string",
    "to_json",
    "BaseRule",
    "Finding",
    "ALL_RULES",
    "__version__",
]

