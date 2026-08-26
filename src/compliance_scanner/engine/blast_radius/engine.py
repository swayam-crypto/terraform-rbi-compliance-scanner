from compliance_scanner.engine.blast_radius.finder import BlastRadiusFinder
from compliance_scanner.engine.blast_radius.collection import BlastRadiusCollection
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.runtime.scan_context import ScanContext


class BlastRadiusEngine:
    """
    Runtime entry point for blast radius analysis.
    """

    def __init__(
        self,
        context: ScanContext,
    ):
        self.context = context

    def analyze(
        self,
    ) -> BlastRadiusCollection:

        query = GraphQuery(
            self.context.relationship_graph,
        )

        finder = BlastRadiusFinder(
            query,
        )

        return finder.analyze(
            self.context.resources,
        )
