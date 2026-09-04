from dataclasses import dataclass


from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.models.resolved_resource import ResolvedResource
from .analysis_runtime import AnalysisRuntime
from .knowledge_runtime import KnowledgeRuntime


@dataclass(slots=True)
class ScanContext:
    """
    Shared state for a compliance scan.

    Runtime analyses progressively enrich this context as the scan
    advances through the pipeline.
    """

    resources: list[ResolvedResource]

    canonical_resources: tuple[CanonicalResource, ...]

    resource_index: ResourceIndex

    knowledge: KnowledgeRuntime

    analysis: AnalysisRuntime
