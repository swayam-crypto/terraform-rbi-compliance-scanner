"""
Base class for all compliance rules.

Every rule (data localization, encryption, audit logging, etc.) inherits
from this class. This keeps the rule interface consistent so the scan
engine can load and run any number of rules without knowing their details.
"""

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
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


class BaseRule:
    """
    Subclass this for every new compliance rule.

    rule_id: short unique code, e.g. "RBI-001"
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
