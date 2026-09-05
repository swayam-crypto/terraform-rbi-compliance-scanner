from compliance_scanner.engine.blast_radius.finder import BlastRadiusFinder
from compliance_scanner.engine.blast_radius.collection import BlastRadiusCollection
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.runtime.scan_context import ScanContext
from compliance_scanner.engine.base import AnalysisEngine


class BlastRadiusEngine(AnalysisEngine):
    """
    Runtime entry point for blast radius analysis.
    """

    runtime_field = "blast_radius"

    def __init__(
        self,
        context: ScanContext,
    ):
        super().__init__(context)

    def analyze(
        self,
    ) -> BlastRadiusCollection:

        query = GraphQuery(
            self.context.knowledge.relationship_graph,
        )

        finder = BlastRadiusFinder(
            query,
        )

        return finder.analyze(
            self.context.resources,
        )
