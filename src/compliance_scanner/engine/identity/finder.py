from compliance_scanner.engine.identity.collection import IdentityCollection
from compliance_scanner.engine.identity.models import (
    EffectiveIdentity,
    EffectivePermission,
)
from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.models.resolved_resource import ResolvedResource
from .resolver import IdentityResolver


class IdentityFinder:
    """
    Computes the effective identity of infrastructure resources.

    The initial implementation establishes the runtime architecture.
    Provider-specific privilege resolution will be introduced in
    future iterations.
    """

    def __init__(
        self,
        graph: PrivilegeGraph,
    ) -> None:
        self.graph = graph
        self.resolver = IdentityResolver()

    def _identities(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:

        return self.resolver.resolve(
            resource,
        )

    def _identity_chain(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:

        return ()

    def _permissions(
        self,
        resource: ResolvedResource,
    ) -> tuple[EffectivePermission, ...]:

        return ()

    def identity(
        self,
        resource: ResolvedResource,
    ) -> EffectiveIdentity:

        return EffectiveIdentity(
            resource=resource,
            identities=self._identities(resource),
            identity_chain=self._identity_chain(resource),
            permissions=self._permissions(resource),
        )

    def analyze(
        self,
        resources: list[ResolvedResource],
    ) -> IdentityCollection:

        return IdentityCollection(
            tuple(self.identity(resource) for resource in resources)
        )
