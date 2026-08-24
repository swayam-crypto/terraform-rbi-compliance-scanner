from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.canonical_types import CanonicalType

PUBLIC_ENTRY_POINT = "public_entry_point"
DATA_STORE = frozenset({"data_store"})
COMPUTE = frozenset({"compute"})
STORAGE = frozenset({"storage"})
NETWORK = frozenset({"network"})
IDENTITY = frozenset({"identity"})


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

    # Reachability

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

    # Dependencies

    def depends_on_type(
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
            self.has_capabilities(candidate, capabilities)
            for candidate in self.reachable_resources(resource)
        )

    def depends_on_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> bool:
        """
        Return True if a reachable resource declares the capability.
        """

        return self.depends_on_capabilities(
            resource,
            frozenset({capability}),
        )

    def depends_on_data_store(
        self,
        resource: ResolvedResource,
    ) -> bool:
        """
        Return True if the resource depends on a data store.
        """

        return self.depends_on_capabilities(
            resource,
            DATA_STORE,
        )

    def depends_on_compute(
        self,
        resource: ResolvedResource,
    ) -> bool:
        return self.depends_on_capabilities(
            resource,
            COMPUTE,
        )

    def depends_on_storage(
        self,
        resource: ResolvedResource,
    ) -> bool:
        return self.depends_on_capabilities(
            resource,
            STORAGE,
        )

    def depends_on_identity(
        self,
        resource: ResolvedResource,
    ) -> bool:
        return self.depends_on_capabilities(
            resource,
            IDENTITY,
        )

    def depends_on_network(
        self,
        resource: ResolvedResource,
    ) -> bool:
        return self.depends_on_capabilities(
            resource,
            NETWORK,
        )

    #   Classification

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

        return self.has_capability(
            resource,
            PUBLIC_ENTRY_POINT,
        )

    #   Capabilities

    def has_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> bool:
        """
        Return True if the resource declares the given capability
        """

        return self.catalog.has_capability(
            resource,
            capability,
        )

    def has_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> bool:
        """
        Return True if the resource declares every requested capability
        """

        return self.catalog.has_capabilities(
            resource,
            capabilities,
        )
