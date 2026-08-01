from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.graph.traversal import GraphTraversal
from compliance_scanner.models.resolved_resource import ResolvedResource


class GraphQuery:
    """
    High-level query API for RelationshipGraph.

    Rules should use this class instead of interacting with
    GraphTraversal or RelationshipGraph directly.
    """

    def __init__(
        self,
        graph: RelationshipGraph,
    ):
        self.graph = graph
        self.traversal = GraphTraversal(graph)

    def reachable_resources(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        return self.traversal.reachable_from(resource)

    def is_reachable(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        reachable = self.reachable_resources(source)
        return target in reachable

    def resources_of_type(
        self,
        resource: ResolvedResource,
        resource_type: str,
    ) -> tuple[ResolvedResource, ...]:
        """Return all reachable resources of the specified resource type"""

        reachable = self.reachable_resources(resource)
        return tuple(
            reachable_resources
            for reachable_resources in reachable
            if reachable_resources.resource_type == resource_type
        )

    def has_dependency(
        self,
        resource: ResolvedResource,
        resource_type: str,
    ) -> bool:
        """
        Return True if the resource depends on at least one resource
        of the specified type.
        """

        return bool(
            self.resources_of_type(
                resource,
                resource_type,
            )
        )
