from collections import defaultdict
from collections.abc import Iterable

from compliance_scanner.engine.relationship.relationship import Relationship
from compliance_scanner.models.resolved_resource import ResolvedResource


class RelationshipGraph:
    """
    Directed graph of infrastructure relationships.
    """

    def __init__(self) -> None:

        self._outgoing: dict[
            ResolvedResource,
            list[Relationship],
        ] = defaultdict(list)

        self._incoming: dict[
            ResolvedResource,
            list[Relationship],
        ] = defaultdict(list)

    def add_relationship(
        self,
        relationship: Relationship,
    ) -> None:

        self._outgoing[relationship.source].append(
            relationship,
        )

        self._incoming[relationship.target].append(
            relationship,
        )

    def outgoing(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:

        return tuple(
            self._outgoing.get(
                resource,
                (),
            )
        )

    def incoming(
        self,
        resource: ResolvedResource,
    ) -> tuple[Relationship, ...]:

        return tuple(
            self._incoming.get(
                resource,
                (),
            )
        )

    def neighbors(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:

        return tuple(relationship.target for relationship in self.outgoing(resource))

    def relationships(
        self,
    ) -> Iterable[Relationship]:

        for relationships in self._outgoing.values():
            yield from relationships

    def has_edge(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:

        return any(
            relationship.target == target for relationship in self.outgoing(source)
        )

    def edge_count(
        self,
    ) -> int:

        return sum(len(relationships) for relationships in self._outgoing.values())

    def node_count(
        self,
    ) -> int:

        return len(set(self._outgoing) | set(self._incoming))
