from __future__ import annotations

from dataclasses import dataclass

from .models import RiskFinding


@dataclass(frozen=True, slots=True)
class RiskCollection:
    """
    Collection of risk findings.
    """

    findings: tuple[RiskFinding, ...] = ()
