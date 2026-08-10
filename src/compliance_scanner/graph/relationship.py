from dataclasses import dataclass, field
from enum import Enum
from typing import Any


from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.catalog.relationship_types import RelationshipType


@dataclass(frozen=True)
class Relationship:
    source: ResolvedResource
    target: ResolvedResource
    relationship_type: RelationshipType
    metadata: dict[str, Any] = field(default_factory=dict)
