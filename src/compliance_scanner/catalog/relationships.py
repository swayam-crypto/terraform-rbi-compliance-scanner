from dataclasses import dataclass

from compliance_scanner.graph.relationship import RelationshipType


@dataclass(frozen=True)
class RelationshipDefinition:
    """
    Defines a relationship that a resource may have.
    """

    relationship_type: RelationshipType

    required: bool = False
