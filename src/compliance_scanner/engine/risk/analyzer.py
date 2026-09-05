from __future__ import annotations

from compliance_scanner.engine.risk.collection import RiskCollection
from compliance_scanner.engine.risk.models import RiskFinding
from compliance_scanner.runtime.scan_context import ScanContext


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
