from dataclasses import dataclass, field
from typing import Any

from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass(
    frozen=True,
)
class PrivilegeRelationship:
    """
    Represents an authorization relationship between two resources.

    Unlike infrastructure relationships, privilege relationships
    describe identity, trust and permission semantics.
    """

    source: ResolvedResource

    target: ResolvedResource

    relationship_type: PrivilegeRelationshipType

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
