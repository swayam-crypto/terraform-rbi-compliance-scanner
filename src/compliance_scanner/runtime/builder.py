from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.canonical.relationship_resolver import (
    RelationshipResolver,
)
from compliance_scanner.canonical.runtime_integration import (
    build_canonical_resources,
)
from compliance_scanner.graph.graph_builder import GraphBuilder
from compliance_scanner.engine.privilege.graph_builder import (
    PrivilegeGraphBuilder,
)
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)
from compliance_scanner.runtime.scan_context import ScanContext
from .analysis_runtime import AnalysisRuntime
from .knowledge_runtime import KnowledgeRuntime


class RuntimeBuilder:
    """
    Constructs the complete runtime required for graph-aware analysis.

    RuntimeBuilder is responsible only for assembling runtime state.
    It does not execute analyses, compliance rules, or reporting.
    """

    def build(
        self,
        resources: list[ResolvedResource],
    ) -> ScanContext:

        canonical_resources = self._build_canonical_resources(
            resources,
        )

        resource_index = self._build_resource_index(
            resources,
        )

        relationships = self._build_relationships(
            resources,
            resource_index,
        )

        relationship_graph = self._build_graph(
            relationships,
        )

        privilege_graph = self._build_privilege_graph(
            resource_index,
        )

        return self._build_context(
            resources,
            canonical_resources,
            resource_index,
            relationship_graph,
            privilege_graph,
        )

    def _build_canonical_resources(
        self,
        resources: list[ResolvedResource],
    ):
        return build_canonical_resources(
            resources,
        )

    def _build_resource_index(
        self,
        resources: list[ResolvedResource],
    ) -> ResourceIndex:
        return ResourceIndex(
            resources,
        )

    def _build_relationships(
        self,
        resources: list[ResolvedResource],
        resource_index: ResourceIndex,
    ):
        return RelationshipResolver(
            catalog,
        ).extract(
            resources,
            resource_index,
        )

    def _build_graph(
        self,
        relationships,
    ):
        return GraphBuilder().build(
            relationships,
        )

    def _build_privilege_graph(
        self,
        resource_index: ResourceIndex,
    ):
        return PrivilegeGraphBuilder().build(
            resource_index,
        )

    def _build_context(
        self,
        resources: list[ResolvedResource],
        canonical_resources,
        resource_index: ResourceIndex,
        relationship_graph,
        privilege_graph,
    ) -> ScanContext:

        knowledge = KnowledgeRuntime(
            relationship_graph=relationship_graph,
            privilege_graph=privilege_graph,
        )

        analysis = AnalysisRuntime()

        return ScanContext(
            resources=resources,
            canonical_resources=canonical_resources,
            resource_index=resource_index,
            knowledge=knowledge,
            analysis=analysis,
        )
