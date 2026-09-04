from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)

from compliance_scanner.runtime.scan_context import (
    ScanContext,
)

from .analysis_runtime import (
    AnalysisRuntime,
)

from .knowledge_builder import (
    KnowledgeBuilder,
)


class RuntimeBuilder:
    """
    Assembles the runtime required for the CCIP pipeline.
    """

    def build(
        self,
        resources: list[ResolvedResource],
    ) -> ScanContext:

        (
            canonical_resources,
            resource_index,
            knowledge,
        ) = KnowledgeBuilder().build(
            resources,
        )

        return ScanContext(
            resources=resources,
            canonical_resources=canonical_resources,
            resource_index=resource_index,
            knowledge=knowledge,
            analysis=AnalysisRuntime(),
        )
