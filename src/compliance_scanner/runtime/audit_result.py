from __future__ import annotations

from dataclasses import dataclass

from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)

from compliance_scanner.canonical.resource import (
    CanonicalResource,
)

from compliance_scanner.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)

from compliance_scanner.runtime.analysis_runtime import (
    AnalysisRuntime,
)


@dataclass(slots=True)
class AuditResult:
    """
    Final runtime artifact produced by the CCIP pipeline.

    Every consumer (CLI, API, Dashboard, Reports, Risk Engine)
    should consume this object rather than individual engines.
    """

    resources: list[ResolvedResource]

    canonical_resources: tuple[CanonicalResource, ...]

    knowledge: KnowledgeRuntime

    analysis: AnalysisRuntime
