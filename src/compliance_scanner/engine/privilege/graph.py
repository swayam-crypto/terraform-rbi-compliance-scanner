from collections import defaultdict
from collections.abc import Iterator

from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.engine.privilege.privilege_relationship import (
    PrivilegeRelationship,
)
from compliance_scanner.models.resolved_resource import ResolvedResource


class PrivilegeGraph:
    """
    Stores privilege relationships between resources and provides
    efficient lookups.

    Unlike the infrastructure relationship graph, this graph models
    authorization semantics such as identity, trust and permission
    relationships.
    """

    def __init__(self) -> None:
        self._relationships: list[PrivilegeRelationship] = []

        self._forward: dict[
            ResolvedResource,
            list[PrivilegeRelationship],
        ] = defaultdict(list)

        self._reverse: dict[
            ResolvedResource,
            list[PrivilegeRelationship],
        ] = defaultdict(list)

    def __len__(
        self,
    ) -> int:
        return len(self._relationships)

    def __iter__(
        self,
    ) -> Iterator[PrivilegeRelationship]:
        return iter(self._relationships)

    def add(
        self,
        relationship: PrivilegeRelationship,
    ) -> None:
        """
        Add a privilege relationship to the graph if it does not
        already exist.
        """

        if relationship in self._relationships:
            return

        self._relationships.append(
            relationship,
        )

        self._forward[relationship.source].append(
            relationship,
        )

        self._reverse[relationship.target].append(
            relationship,
        )

    def outgoing(
        self,
        resource: ResolvedResource,
    ) -> tuple[PrivilegeRelationship, ...]:
        return tuple(
            self._forward.get(
                resource,
                (),
            )
        )

    def incoming(
        self,
        resource: ResolvedResource,
    ) -> tuple[PrivilegeRelationship, ...]:
        return tuple(
            self._reverse.get(
                resource,
                (),
            )
        )

    def related(
        self,
        resource: ResolvedResource,
    ) -> tuple[
        tuple[PrivilegeRelationship, ...],
        tuple[PrivilegeRelationship, ...],
    ]:
        return (
            self.outgoing(
                resource,
            ),
            self.incoming(
                resource,
            ),
        )

    def relationships(
        self,
    ) -> tuple[PrivilegeRelationship, ...]:
        """
        Return every privilege relationship stored in the graph.
        """

        return tuple(
            self._relationships,
        )

    def has_relationship(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """
        Return True if a privilege relationship exists between
        source and target.
        """

        return any(
            relationship.target == target
            for relationship in self.outgoing(
                source,
            )
        )

    def outgoing_by_type(
        self,
        resource: ResolvedResource,
        relationship_type: PrivilegeRelationshipType,
    ) -> tuple[PrivilegeRelationship, ...]:
        return tuple(
            relationship
            for relationship in self.outgoing(
                resource,
            )
            if relationship.relationship_type == relationship_type
        )

    def neighbors(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        return tuple(
            relationship.target
            for relationship in self.outgoing(
                resource,
            )
        )
