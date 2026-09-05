from __future__ import annotations

from dataclasses import dataclass

from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.graph.resource_index import ResourceIndex

from .knowledge_runtime import KnowledgeRuntime


@dataclass(slots=True)
class KnowledgeResult:
    """
    Complete output produced by the KnowledgeBuilder.
    """

    canonical_resources: tuple[CanonicalResource, ...]

    resource_index: ResourceIndex

    knowledge: KnowledgeRuntime
