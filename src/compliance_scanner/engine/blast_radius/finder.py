from compliance_scanner.engine.blast_radius.collection import BlastRadiusCollection
from compliance_scanner.engine.blast_radius.models import BlastRadius
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.models.resolved_resource import ResolvedResource


class BlastRadiusFinder:
    """
    Computes blast radius using graph reachability.
    """

    def __init__(
        self,
        query: GraphQuery,
    ):
        self.query = query

    def blast_radius(
        self,
        resource: ResolvedResource,
    ) -> BlastRadius:

        affected_resources = self.query.reachable_resources(
            resource,
        )

        return BlastRadius(
            source=resource,
            affected_resources=affected_resources,
        )

    def analyze(
        self,
        resources: list[ResolvedResource],
    ) -> BlastRadiusCollection:

        return BlastRadiusCollection(
            tuple(self.blast_radius(resource) for resource in resources)
        )
