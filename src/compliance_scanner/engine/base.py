from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from compliance_scanner.runtime.scan_context import ScanContext


class AnalysisEngine(ABC):
    """
    Base class for every analysis engine.
    """

    runtime_field: str

    def __init__(
        self,
        context: ScanContext,
    ) -> None:
        self.context = context

    @abstractmethod
    def analyze(self):
        """
        Execute the analysis.
        """
        raise NotImplementedError
