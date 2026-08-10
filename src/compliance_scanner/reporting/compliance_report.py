"""Framework-aware reporting projections."""
from collections import Counter, defaultdict
from compliance_scanner.rules.base import Finding


def filter_by_framework(findings: list[Finding], framework: str | None) -> list[Finding]:
    if not framework:
        return findings
    wanted = framework.casefold()
    return [finding for finding in findings if any(mapping["framework"].casefold() == wanted for mapping in finding.framework_mappings)]


def summarize(findings: list[Finding]) -> dict[str, object]:
    frameworks: dict[str, int] = defaultdict(int)
    for finding in findings:
        for mapping in finding.framework_mappings:
            frameworks[mapping["framework"]] += 1
    return {"total": len(findings), "by_severity": dict(Counter(f.severity for f in findings)), "by_category": dict(Counter(f.category for f in findings)), "by_framework": dict(frameworks), "by_provider": dict(Counter(f.resource_type.split("_", 1)[0] for f in findings))}
