from dataclasses import dataclass

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)


@dataclass(frozen=True)
class PrivilegeRelationshipDefinition:
    """
    Defines a privilege relationship between resources.
    """

    relationship_type: PrivilegeRelationshipType

    target: CanonicalType

    required: bool = False
