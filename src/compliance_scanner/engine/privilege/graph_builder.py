from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.graph.resource_index import ResourceIndex

from .relationship_resolver import PrivilegeRelationshipResolver

from compliance_scanner.catalog.global_catalog import catalog


class PrivilegeGraphBuilder:
    """
    Builds the runtime privilege graph.

    The builder delegates privilege relationship discovery to the
    PrivilegeRelationshipResolver and constructs the runtime graph
    from the discovered privilege relationships.
    """

    def __init__(
        self,
        resolver: PrivilegeRelationshipResolver | None = None,
    ) -> None:
        self._resolver = (
            resolver if resolver is not None else PrivilegeRelationshipResolver(catalog)
        )

    def build(
        self,
        resource_index: ResourceIndex,
    ) -> PrivilegeGraph:
        graph = PrivilegeGraph()

        for resource in resource_index:
            relationships = self._resolver.resolve(
                resource,
                resource_index,
            )

            for relationship in relationships:
                graph.add(
                    relationship,
                )

        return graph
