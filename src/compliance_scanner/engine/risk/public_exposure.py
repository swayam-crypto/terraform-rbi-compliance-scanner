from __future__ import annotations

from compliance_scanner.runtime.scan_context import ScanContext
from .models import (
    RiskFinding,
    RiskLevel,
)
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.canonical_types import CanonicalType

_SENSITIVE_TYPES = frozenset(
    {
        CanonicalType.DATABASE,
        CanonicalType.SECRET,
        CanonicalType.KMS_KEY,
    }
)


class PublicExposureAnalyzer:
    """
    Identifies sensitive resources reachable from public entry points.
    """

    def __init__(
        self,
        context: ScanContext,
    ):
        self.context = context

    def _severity(
        self,
        canonical: CanonicalType,
    ) -> RiskLevel:

        if canonical in (
            CanonicalType.DATABASE,
            CanonicalType.SECRET,
        ):
            return RiskLevel.CRITICAL

        if canonical == CanonicalType.KMS_KEY:
            return RiskLevel.HIGH

        return RiskLevel.MEDIUM

    def _title(
        self,
        canonical: CanonicalType,
    ) -> str:

        if canonical == CanonicalType.DATABASE:
            return "Public Database Exposure"

        if canonical == CanonicalType.SECRET:
            return "Public Secret Exposure"

        if canonical == CanonicalType.KMS_KEY:
            return "Public KMS Exposure"

        return "Public Sensitive Resource Exposure"

    def _is_sensitive_resource(
        self,
        canonical: CanonicalType,
    ) -> bool:

        return canonical in _SENSITIVE_TYPES

    def _reason(
        self,
        canonical: CanonicalType,
    ) -> str:

        if canonical == CanonicalType.DATABASE:
            return "A public attack path reaches a managed database."

        if canonical == CanonicalType.SECRET:
            return "A public attack path reaches a secret."

        if canonical == CanonicalType.KMS_KEY:
            return "A public attack path reaches a KMS key."

        return "A public attack path reaches a sensitive resource."

    def analyze(
        self,
    ) -> tuple[RiskFinding, ...]:

        attack_paths = self.context.analysis.attack_paths

        if attack_paths is None:
            return ()

        findings: list[RiskFinding] = []

        for attack_path in attack_paths:

            canonical = catalog.canonical_type(
                attack_path.target,
            )

            if not self._is_sensitive_resource(canonical):
                continue

            findings.append(
                RiskFinding(
                    resource=attack_path.target,
                    title=self._title(canonical),
                    level=self._severity(canonical),
                    reasons=(self._reason(canonical),),
                )
            )

        return tuple(findings)
