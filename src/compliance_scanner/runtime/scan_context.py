from dataclasses import dataclass

from compliance_scanner.engine.attack.collection import AttackPathCollection
from compliance_scanner.engine.blast_radius.collection import BlastRadiusCollection
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.engine.identity.collection import IdentityCollection
from compliance_scanner.models.resolved_resource import ResolvedResource


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

    relationship_graph: RelationshipGraph

    privilege_graph: PrivilegeGraph

    attack_paths: AttackPathCollection | None = None

    blast_radius: BlastRadiusCollection | None = None

    identity_analysis: IdentityCollection | None = None
