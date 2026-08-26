from compliance_scanner.engine.identity.collection import IdentityCollection
from compliance_scanner.engine.identity.models import EffectiveIdentity
from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.models.resolved_resource import ResolvedResource


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

    def identity(
        self,
        resource: ResolvedResource,
    ) -> EffectiveIdentity:

        return EffectiveIdentity(
            resource=resource,
            identities=(),
            permissions=(),
        )

    def analyze(
        self,
        resources: list[ResolvedResource],
    ) -> IdentityCollection:

        return IdentityCollection(
            tuple(self.identity(resource) for resource in resources)
        )
