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
from .analysis_builder import AnalysisBuilder


class RuntimeBuilder:
    """
    Assembles the runtime required for the CCIP pipeline.
    """

    def build(
        self,
        resources: list[ResolvedResource],
    ) -> ScanContext:

        result = KnowledgeBuilder().build(resources)

        context = ScanContext(
            resources=resources,
            canonical_resources=result.canonical_resources,
            resource_index=result.resource_index,
            knowledge=result.knowledge,
            analysis=AnalysisRuntime(),
        )

        AnalysisBuilder().build(context)

        return context
