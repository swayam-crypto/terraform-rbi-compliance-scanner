from __future__ import annotations

from compliance_scanner.engine.risk.collection import RiskCollection
from compliance_scanner.runtime.scan_context import ScanContext
from compliance_scanner.models.resolved_resource import ResolvedResource

from .models import (
    RiskFinding,
    RiskLevel,
)


class RiskAnalyzer:
    """
    Correlates analysis results into risk findings.
    """

    def __init__(
        self,
        context: ScanContext,
    ):
        self.context = context

    def analyze(
        self,
    ) -> RiskCollection:

        findings = (
            *self._analyze_attack_paths(),
            *self._analyze_blast_radius(),
            *self._analyze_identity(),
        )

        return RiskCollection(
            findings=tuple(findings),
        )

    def _analyze_attack_paths(
        self,
    ) -> tuple[RiskFinding, ...]:

        return ()

    def _analyze_blast_radius(
        self,
    ) -> tuple[RiskFinding, ...]:

        return ()

    def _analyze_identity(
        self,
    ) -> tuple[RiskFinding, ...]:

        return ()

    def _is_database(
        self,
        resource: ResolvedResource,
    ) -> bool:

        return resource.resource_type in {
            "aws_db_instance",
            "aws_rds_cluster",
            "aws_rds_cluster_instance",
        }

    def _analyze_attack_paths(
        self,
    ) -> tuple[RiskFinding, ...]:

        attack_paths = self.context.analysis.attack_paths

        if attack_paths is None:
            return ()

        findings: list[RiskFinding] = []

        for attack_path in attack_paths:

            if not self._is_database(
                attack_path.target,
            ):
                continue

            findings.append(
                RiskFinding(
                    resource=attack_path.target,
                    level=RiskLevel.CRITICAL,
                    reasons=("Attack path reaches a database.",),
                )
            )

        return tuple(findings)
