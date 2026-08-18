from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.graph.traversal import GraphTraversal
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.graph.relationship import Relationship


class GraphQuery:
    """
    High-level query API for RelationshipGraph.

    Rules should use this class instead of interacting with
    GraphTraversal or RelationshipGraph directly.
    """

    def __init__(
        self,
        graph: RelationshipGraph,
        catalog_instance: Catalog = catalog,
    ):
        self.graph = graph
        self.traversal = GraphTraversal(graph)
        self.catalog = catalog_instance

    def resources_with_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> tuple[ResolvedResource, ...]:
        """
        Return all reachable resources that declare the given capability.
        """

        return tuple(
            candidate
            for candidate in self.reachable_resources(resource)
            if self.catalog.has_capability(
                candidate,
                capability,
            )
        )

    def resources_with_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> tuple[ResolvedResource, ...]:
        """
        Return all reachable resources that declare every requested capability.
        """

        return tuple(
            candidate
            for candidate in self.reachable_resources(resource)
            if self.catalog.has_capabilities(
                candidate,
                capabilities,
            )
        )

    def resources_of_canonical_type(
        self,
        resource: ResolvedResource,
        canonical_type: CanonicalType,
    ) -> tuple[ResolvedResource, ...]:
        """
        Return all reachable resources having the given canonical type.
        """

        return tuple(
            candidate
            for candidate in self.reachable_resources(resource)
            if self.catalog.canonical_type(candidate) == canonical_type
        )

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

    def outgoing(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return self.graph.outgoing(resource)

    def incoming(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return self.graph.incoming(resource)

    def neighbors(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return self.graph.neighbors(resource)

    def relationships(
        self,
    ) -> tuple[Relationship, ...]:
        return self.graph.relationships()

    def has_relationship(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return self.graph.has_relationship(
            source,
            target,
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
