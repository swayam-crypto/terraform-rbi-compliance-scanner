from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.canonical_types import CanonicalType


class GraphPredicates:
    """
    High-level business predicates for graph-aware compliance rules.

    Compliance rules should use this class instead of interacting with
    GraphQuery directly.
    """

    def __init__(
        self,
        query: GraphQuery,
        catalog_instance: Catalog = catalog,
    ):
        self.query = query
        self.catalog = catalog_instance

    def reachable_resources(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        """
        Return every resource reachable from the given resource.
        """
        return self.query.reachable_resources(resource)

    def is_reachable(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """
        Return True if target is reachable from source.
        """
        return self.query.is_reachable(
            source,
            target,
        )

    def depends_on(
        self,
        resource: ResolvedResource,
        resource_type: str,
    ) -> bool:
        """
        Return True if the resource depends on at least one resource
        of the specified type.
        """
        return self.query.has_dependency(
            resource,
            resource_type,
        )

    def depends_on_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> bool:
        """Return whether a reachable resource declares all capabilities."""
        return any(
            self.catalog.has_capabilities(candidate, capabilities)
            for candidate in self.reachable_resources(resource)
        )

    def is_database(
        self,
        resource: ResolvedResource,
    ) -> bool:
        """
        Return True if the resource is classified as a database.
        """

        return self.catalog.canonical_type(resource) == CanonicalType.DATABASE

    def is_public_entry_point(
        self,
        resource: ResolvedResource,
    ) -> bool:
        """
        Return True if the resource can act as a public entry point.
        """

        return self.catalog.has_capability(
            resource,
            "public_entry_point",
        )
