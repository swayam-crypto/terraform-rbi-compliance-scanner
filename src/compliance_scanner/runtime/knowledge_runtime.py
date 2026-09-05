from __future__ import annotations

from dataclasses import dataclass

from compliance_scanner.engine.relationship.relationship_graph import (
    RelationshipGraph,
)
from compliance_scanner.engine.privilege.graph import (
    PrivilegeGraph,
)


@dataclass(slots=True)
class KnowledgeRuntime:
    """
    Immutable knowledge produced during the runtime.

    This contains objective facts discovered about the
    infrastructure. It does not contain analysis results.
    """

    relationship_graph: RelationshipGraph
    privilege_graph: PrivilegeGraph
