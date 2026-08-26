"""
Base class for all graph-aware compliance rules.

Unlike normal rules, graph rules reason about relationships between
multiple resources using the RelationshipGraph.
"""

from compliance_scanner.rules.base import BaseRule, Finding
from compliance_scanner.runtime.scan_context import ScanContext


class GraphRule(BaseRule):
    """
    Base class for graph-aware compliance rules.

    Graph rules inspect the entire infrastructure graph instead of
    individual resources.
    """

    def check_graph(
        self,
        context: ScanContext,
    ) -> list[Finding]:
        raise NotImplementedError("Graph rules must implement check_graph().")
