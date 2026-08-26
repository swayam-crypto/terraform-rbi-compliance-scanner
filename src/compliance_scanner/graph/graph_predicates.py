from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.blast_radius.models import BlastRadius
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.attack.models import AttackPath
from compliance_scanner.attack.collection import AttackPathCollection
from compliance_scanner.blast_radius.collection import BlastRadiusCollection

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
        attack_paths: AttackPathCollection | None = None,
        blast_radius: BlastRadiusCollection | None = None,
        catalog_instance: Catalog = catalog,
    ):
        self.query = query
        self.catalog = catalog_instance
        self._attack_paths = attack_paths
        self._blast_radius = blast_radius

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

        #   Blast_Radius

    def blast_radius(
        self,
        resource: ResolvedResource,
    ) -> BlastRadius | None:
        """
        Return the blast radius for the resource.
        """

        if self._blast_radius is None:
            return None

        return self._blast_radius.for_resource(
            resource,
        )

    def blast_radius_size(
        self,
        resource: ResolvedResource,
    ) -> int:
        """
        Return the number of affected resources.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return 0

        return len(
            blast_radius.affected_resources,
        )

    def blast_radius_contains(
        self,
        resource: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """
        Return whether the blast radius contains the target.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return False

        return target in blast_radius.affected_resources

    def blast_radius_contains_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> bool:
        """
        Return whether the blast radius contains a resource
        declaring the capability.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return False

        return any(
            self.catalog.has_capability(
                candidate,
                capability,
            )
            for candidate in blast_radius.affected_resources
        )

    def blast_radius_contains_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> bool:
        """
        Return whether the blast radius contains a resource
        declaring every requested capability.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return False

        return any(
            self.catalog.has_capabilities(
                candidate,
                capabilities,
            )
            for candidate in blast_radius.affected_resources
        )

    def blast_radius_contains_type(
        self,
        resource: ResolvedResource,
        canonical_type: CanonicalType,
    ) -> bool:
        """
        Return whether the blast radius contains a resource
        of the given canonical type.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return False

        return any(
            self.catalog.canonical_type(
                candidate,
            )
            == canonical_type
            for candidate in blast_radius.affected_resources
        )

    def blast_radius_contains_kind(
        self,
        resource: ResolvedResource,
        kind: ResourceKind,
    ) -> bool:
        """
        Return whether the blast radius contains a resource
        of the given resource kind.
        """

        blast_radius = self.blast_radius(
            resource,
        )

        if blast_radius is None:
            return False

        return any(
            (
                definition := self.catalog.definition(
                    candidate,
                )
            )
            is not None
            and definition.kind == kind
            for candidate in blast_radius.affected_resources
        )

    #   Attack_Path
    def attack_path(
        self,
        resource: ResolvedResource,
    ) -> AttackPath | None:
        """
        Return the attack path for the resource.
        """

        if self._attack_paths is None:
            return None

        return self._attack_paths.for_resource(
            resource,
        )

    def attack_path_size(
        self,
        resource: ResolvedResource,
    ) -> int:
        """
        Return the number of resources contained in the attack path.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return 0

        return len(
            attack_path.resources,
        )

    def attack_path_contains(
        self,
        resource: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """
        Return whether the attack path contains the target resource.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return False

        return target in attack_path.resources

    def attack_path_contains_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> bool:
        """
        Return whether the attack path contains a resource
        declaring the capability.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return False

        return any(
            self.catalog.has_capability(
                candidate,
                capability,
            )
            for candidate in attack_path.resources
        )

    def attack_path_contains_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> bool:
        """
        Return whether the attack path contains a resource
        declaring every requested capability.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return False

        return any(
            self.catalog.has_capabilities(
                candidate,
                capabilities,
            )
            for candidate in attack_path.resources
        )

    def attack_path_contains_type(
        self,
        resource: ResolvedResource,
        canonical_type: CanonicalType,
    ) -> bool:
        """
        Return whether the attack path contains a resource
        of the given canonical type.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return False

        return any(
            self.catalog.canonical_type(
                candidate,
            )
            == canonical_type
            for candidate in attack_path.resources
        )

    def attack_path_contains_kind(
        self,
        resource: ResolvedResource,
        kind: ResourceKind,
    ) -> bool:
        """
        Return whether the attack path contains a resource
        of the given resource kind.
        """

        attack_path = self.attack_path(
            resource,
        )

        if attack_path is None:
            return False

        return any(
            (
                definition := self.catalog.definition(
                    candidate,
                )
            )
            is not None
            and definition.kind == kind
            for candidate in attack_path.resources
        )
