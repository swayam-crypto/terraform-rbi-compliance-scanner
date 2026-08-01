from collections import defaultdict
from collections.abc import Iterator

from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.graph.relationship import (
    Relationship,
    RelationshipType,
)


class RelationshipGraph:
    """Stores relationships between Terraform resources and provides efficient lookups."""

    def _key(self, resource: ResolvedResource) -> str:
        return f"{resource.resource_type}.{resource.resource_name}"

    def __init__(self) -> None:
        self._relationships: list[Relationship] = []
        self._forward: dict[ResolvedResource, list[Relationship]] = defaultdict(list)
        self._reverse: dict[ResolvedResource, list[Relationship]] = defaultdict(list)

    def __len__(self) -> int:
        return len(self._relationships)

    def __iter__(self) -> Iterator[Relationship]:
        return iter(self._relationships)

    def add(self, relationship: Relationship) -> None:
        """Add a relationship to the graph if it doesn't already exist."""
        if relationship in self._relationships:
            return

        self._relationships.append(relationship)
        self._forward[relationship.source].append(relationship)
        self._reverse[relationship.target].append(relationship)

    def outgoing(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return tuple(self._forward.get(resource, ()))

    def incoming(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:
        return tuple(self._reverse.get(resource, ()))

    def related(
        self,
        resource: ResolvedResource,
    ) -> tuple[
        tuple[Relationship, ...],
        tuple[Relationship, ...],
    ]:
        return (
            self.outgoing(resource),
            self.incoming(resource),
        )

    def relationships(self) -> tuple[Relationship, ...]:
        """Return all relationships in the graph."""
        return tuple(self._relationships)

    def has_relationship(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """Return True if a relationship exists from source to target."""
        return any(
            relationship.target == target for relationship in self.outgoing(source)
        )

    def outgoing_by_type(
        self,
        resource: ResolvedResource,
        relationship_type: RelationshipType,
    ) -> tuple[Relationship, ...]:
        return tuple(
            relationship
            for relationship in self.outgoing(resource)
            if relationship.relationship_type == relationship_type
        )

    def neighbors(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        return tuple(relationship.target for relationship in self.outgoing(resource))
