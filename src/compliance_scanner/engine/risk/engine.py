from __future__ import annotations

from compliance_scanner.engine.base import AnalysisEngine
from compliance_scanner.runtime.scan_context import ScanContext

from .collection import RiskCollection
from .analyzer import RiskAnalyzer


class RiskEngine(AnalysisEngine):
    """
    Produces overall risk analysis.
    """

    runtime_field = "risk"

    def __init__(
        self,
        context: ScanContext,
    ):
        super().__init__(context)

    def analyze(self):
        return RiskAnalyzer(
            self.context,
        ).analyze()
