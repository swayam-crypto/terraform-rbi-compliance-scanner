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

from compliance_scanner.core import (
    scan_directory,
    scan_directory_large,
    scan_plan,
)

from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)
from compliance_scanner.parser.terraform_parser import (
    _resolve_provider_for_resource,
)
from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import BaseRule, Finding
from compliance_scanner.reporting import to_json
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.catalog.global_catalog import catalog

__version__ = "0.8.0"


def scan(path: str, suppressed_count: list | None = None) -> list[Finding]:
    """
    Scan a directory of Terraform files. Main entry point for most users.

    Pass a list like [0] as suppressed_count to read back how many
    findings were suppressed via inline `# rbi-scan:ignore` comments:
        counter = [0]
        findings = rbi.scan(path, suppressed_count=counter)
        print(f"{counter[0]} findings suppressed")
    """
    return scan_directory(path, suppressed_count=suppressed_count)


def scan_large(
    path: str,
    workers: int | None = None,
    use_cache: bool = True,
    suppressed_count: list | None = None,
):
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
    return scan_directory_large(
        path, workers=workers, use_cache=use_cache, suppressed_count=suppressed_count
    )


def scan_string(terraform_text: str) -> list[Finding]:
    """
    Scan raw Terraform text directly, without needing it saved as a
    file. Useful for CI systems that already have the config in memory,
    or for testing a snippet quickly.
    """
    import hcl2
    import io
    from compliance_scanner.parser.terraform_parser import (
        _extract_resources,
        _extract_providers,
    )

    raw = hcl2.load(io.StringIO(terraform_text))
    resources = _extract_resources(raw)
    providers = _extract_providers(raw)

    findings: list[Finding] = []
    for resource_type, named_configs in resources.items():
        provider_defaults = _resolve_provider_for_resource(resource_type, providers)
        for resource_name, config in named_configs.items():
            resource = ResolvedResource(
                platform=Platform.TERRAFORM,
                provider=infer_provider(resource_type),
                resource_type=resource_type,
                resource_name=resource_name,
                attributes=config,
                default_attributes=provider_defaults,
                source=SourceLocation(
                    file_path="<string>",
                ),
            )
            for rule in ALL_RULES:
                if not rule.applies_to_resource(resource, catalog):
                    continue
                result = rule.check(resource)
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
    "scan_directory",
    "scan_directory_large",
    "scan_plan",
]
