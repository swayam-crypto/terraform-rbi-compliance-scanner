"""
Base class for graph-aware compliance rules.

Graph rules analyze relationships between multiple resources rather than
individual resources.
"""

from compliance_scanner.rules.base import BaseRule, Finding
from compliance_scanner.scan_context import ScanContext


class GraphRule(BaseRule):
    """
    Base class for rules that inspect the infrastructure graph.
    """

    def check_graph(
        self,
        context: ScanContext,
    ) -> list[Finding]:
        """
        Analyze the complete infrastructure graph.

        Returns a list of compliance findings.
        """
        raise NotImplementedError("Graph rules must implement check_graph().")
