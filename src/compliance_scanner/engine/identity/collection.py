from collections.abc import Iterator

from compliance_scanner.engine.identity.models import EffectiveIdentity
from compliance_scanner.models.resolved_resource import ResolvedResource


class IdentityCollection:
    """
    Read-only collection of effective identity analyses.

    The collection provides efficient lookup by resource while remaining
    immutable from the perspective of higher runtime layers.
    """

    def __init__(
        self,
        identities: tuple[EffectiveIdentity, ...],
    ) -> None:
        self._identities = identities

        self._by_resource = {identity.resource: identity for identity in identities}

    def __iter__(
        self,
    ) -> Iterator[EffectiveIdentity]:
        return iter(
            self._identities,
        )

    def __len__(
        self,
    ) -> int:
        return len(
            self._identities,
        )

    def __bool__(
        self,
    ) -> bool:
        return bool(
            self._identities,
        )

    def __contains__(
        self,
        identity: EffectiveIdentity,
    ) -> bool:
        return identity in self._identities

    def __getitem__(
        self,
        index: int,
    ) -> EffectiveIdentity:
        return self._identities[index]

    def all(
        self,
    ) -> tuple[EffectiveIdentity, ...]:
        return self._identities

    def for_resource(
        self,
        resource: ResolvedResource,
    ) -> EffectiveIdentity | None:
        return self._by_resource.get(
            resource,
        )
