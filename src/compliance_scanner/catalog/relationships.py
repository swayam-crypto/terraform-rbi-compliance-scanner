from dataclasses import dataclass

from compliance_scanner.catalog.relationship_types import RelationshipType
from compliance_scanner.catalog.canonical_types import CanonicalType


@dataclass(frozen=True)
class RelationshipDefinition:
    """
    Defines a relationship that a resource may have.
    """

    relationship_type: RelationshipType
    target: CanonicalType

    required: bool = False
