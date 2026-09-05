from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from compliance_scanner.models.resolved_resource import ResolvedResource


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class RiskFinding:
    """
    Represents the overall risk assessment for a resource.
    """

    resource: ResolvedResource

    level: RiskLevel

    score: int

    reasons: tuple[str, ...]
