from __future__ import annotations

from compliance_scanner.runtime.scan_context import ScanContext
from compliance_scanner.engine.blast_radius.models import BlastRadius

from .models import (
    RiskFinding,
    RiskLevel,
)


class BlastRadiusRiskAnalyzer:
    """
    Identifies resources with a large blast radius.
    """

    HIGH_THRESHOLD = 10
    CRITICAL_THRESHOLD = 25

    def __init__(
        self,
        context: ScanContext,
    ):
        self.context = context

    def analyze(
        self,
    ) -> tuple[RiskFinding, ...]:

        blast_radius = self.context.analysis.blast_radius

        if blast_radius is None:
            return ()

        findings: list[RiskFinding] = []

        for radius in blast_radius:

            severity = self._severity(radius)

            if severity is None:
                continue

            findings.append(
                RiskFinding(
                    resource=radius.source,
                    title=self._title(severity),
                    level=severity,
                    reasons=(self._reason(radius),),
                )
            )

        return tuple(findings)

    def _severity(
        self,
        radius: BlastRadius,
    ) -> RiskLevel | None:

        affected = len(
            radius.affected_resources,
        )

        if affected >= self.CRITICAL_THRESHOLD:
            return RiskLevel.CRITICAL

        if affected >= self.HIGH_THRESHOLD:
            return RiskLevel.HIGH

        return None

    def _title(
        self,
        severity: RiskLevel,
    ) -> str:

        if severity is RiskLevel.CRITICAL:
            return "Critical Blast Radius"

        return "High Blast Radius"

    def _reason(
        self,
        radius: BlastRadius,
    ) -> str:

        affected = len(
            radius.affected_resources,
        )

        return (
            f"Compromise of this resource could affect "
            f"{affected} downstream resources."
        )
