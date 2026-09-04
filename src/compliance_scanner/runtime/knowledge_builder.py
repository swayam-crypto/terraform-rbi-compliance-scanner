from compliance_scanner.catalog.global_catalog import catalog

from compliance_scanner.canonical.relationship_resolver import (
    RelationshipResolver,
)
from compliance_scanner.canonical.runtime_integration import (
    build_canonical_resources,
)

from compliance_scanner.engine.privilege.graph_builder import (
    PrivilegeGraphBuilder,
)

from compliance_scanner.graph.graph_builder import (
    GraphBuilder,
)

from compliance_scanner.graph.resource_index import (
    ResourceIndex,
)

from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)

from .knowledge_runtime import (
    KnowledgeRuntime,
)


class KnowledgeBuilder:
    """
    Builds every immutable knowledge artifact required
    for runtime analysis.
    """

    def build(
        self,
        resources: list[ResolvedResource],
    ) -> tuple[
        tuple,
        ResourceIndex,
        KnowledgeRuntime,
    ]:

        canonical_resources = build_canonical_resources(
            resources,
        )

        resource_index = ResourceIndex(
            resources,
        )

        relationships = RelationshipResolver(
            catalog,
        ).extract(
            resources,
            resource_index,
        )

        relationship_graph = GraphBuilder().build(
            relationships,
        )

        privilege_graph = PrivilegeGraphBuilder().build(
            resource_index,
        )

        knowledge = KnowledgeRuntime(
            relationship_graph=relationship_graph,
            privilege_graph=privilege_graph,
        )

        return (
            canonical_resources,
            resource_index,
            knowledge,
        )
