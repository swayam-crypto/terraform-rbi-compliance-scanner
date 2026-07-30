from collections import defaultdict
from collections.abc import Iterator

from compliance_scanner.parser.terraform_parser import ResolvedResource

from .relationship import Relationship


class ResourceGraph:
    """Stores relationships between Terraform resources and provides efficient lookups."""

    def __init__(self) -> None:
        self._relationships: list[Relationship] = []
        self._forward: dict[ResolvedResource, list[Relationship]] = defaultdict(list)
        self._reverse: dict[ResolvedResource, list[Relationship]] = defaultdict(list)

    def __len__(self) -> int:
        return len(self._relationships)

    def __iter__(self) -> Iterator[Relationship]:
        return iter(self._relationships)

    def add(self, relationship: Relationship) -> None:
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
