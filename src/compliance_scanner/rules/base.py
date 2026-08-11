"""
Base class for all compliance rules.

Every rule (data localization, encryption, audit logging, etc.) inherits
from this class. This keeps the rule interface consistent so the scan
engine can load and run any number of rules without knowing their details.
"""

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from compliance_scanner.compliance.controls import ComplianceControl

if TYPE_CHECKING:
    from compliance_scanner.catalog.catalog import Catalog
    from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass
class Finding:
    """A single compliance violation found during a scan."""

    rule_id: str
    severity: str  # "critical" | "high" | "medium" | "low"
    resource_type: str
    resource_name: str
    message: str
    regulation_reference: str
    file_path: str = ""
    metadata: dict = field(default_factory=dict)
    control_id: str = ""
    category: str = ""
    remediation: str = ""
    framework_mappings: list[dict[str, str]] = field(default_factory=list)


class BaseRule:
    """
    Subclass this for every new compliance rule.

    rule_id: legacy scanner identifier, e.g. "RBI-001". It remains stable
        for suppressions and existing integrations.
    control: framework-neutral security control evaluated by this rule.
    description: one-line human explanation, shown in reports
    regulation_reference: which RBI/DPDPA clause this maps to
    applies_to: list of Terraform resource types this rule checks,
    e.g. ["aws_s3_bucket", "aws_db_instance"]
    """

    rule_id: str = "UNSET"
    description: str = ""
    regulation_reference: str = ""
    severity: str = "medium"
    applies_to: list[str] = []
    required_capabilities: frozenset[str] = frozenset()
    control: ComplianceControl | None = None

    def applies_to_resource(
        self,
        resource: "ResolvedResource",
        catalog: "Catalog",
    ) -> bool:
        """Determine eligibility from catalog capabilities when declared.

        ``applies_to`` is retained as a compatibility path for rules that have
        not yet migrated. Capability-based rules fail closed for resource types
        absent from the catalog, preventing accidental provider coupling.
        """
        if self.required_capabilities:
            return catalog.has_capabilities(resource, self.required_capabilities)
        return resource.resource_type in self.applies_to

    def finding(
        self,
        resource: "ResolvedResource",
        message: str,
        *,
        file_path: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Finding:
        """Create a finding with canonical control metadata attached."""
        control = self.control
        return Finding(
            rule_id=self.rule_id,
            severity=self.severity,
            resource_type=resource.resource_type,
            resource_name=resource.resource_name,
            message=message,
            regulation_reference=self.regulation_reference,
            file_path=file_path if file_path is not None else resource.source.file_path,
            metadata=metadata or {},
            control_id=control.control_id if control else "",
            category=control.category if control else "",
            remediation=control.remediation if control else "",
            framework_mappings=(
                [mapping.as_dict() for mapping in control.framework_mappings]
                if control
                else []
            ),
        )

    def check(self, resource: "ResolvedResource") -> Finding | None:
        """
        Override this in each rule subclass.

        Use resource.get("attribute_name") to read attributes — this
        automatically falls back to provider defaults when the resource
        doesn't specify the attribute directly.

        Return a Finding if the resource violates the rule.
        Return None if the resource is compliant.
        """
        raise NotImplementedError("Each rule must implement check()")
