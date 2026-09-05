from __future__ import annotations

from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)

from .resolver import IdentityResolver


class IdentityResolverRegistry:

    def __init__(self):

        self._resolvers: dict[
            str,
            IdentityResolver,
        ] = {}

    def register(
        self,
        provider: str,
        resolver: IdentityResolver,
    ) -> None:

        self._resolvers[provider] = resolver

    def resolve(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:

        resolver = self._resolvers.get(
            resource.provider,
        )

        if resolver is None:
            return ()

        return resolver.resolve(resource)
