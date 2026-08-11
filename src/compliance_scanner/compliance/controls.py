"""Canonical compliance control metadata.

Controls describe *what* must be true. Framework mappings describe *why*
the control matters to a particular regulation. Rules remain implementation
details that evaluate a control for a specific IaC/provider representation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FrameworkMapping:
    """A control's traceability entry for one compliance framework."""

    framework: str
    requirement: str
    reference: str

    def as_dict(self) -> dict[str, str]:
        return {
            "framework": self.framework,
            "requirement": self.requirement,
            "reference": self.reference,
        }


@dataclass(frozen=True)
class ComplianceControl:
    """Provider- and framework-neutral definition of a security control."""

    control_id: str
    title: str
    category: str
    severity: str
    remediation: str
    framework_mappings: tuple[FrameworkMapping, ...]
