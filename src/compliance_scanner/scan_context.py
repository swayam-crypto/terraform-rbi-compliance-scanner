from dataclasses import dataclass

from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass(slots=True)
class ScanContext:
    """
    Shared state for a compliance scan.

    As the platform evolves, this object will become the central
    container passed through the scanning pipeline.
    """

    resources: list[ResolvedResource]
    resource_index: ResourceIndex
    relationship_graph: RelationshipGraph
