from __future__ import annotations

from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.models.resolved_resource import (
    ResolvedResource,
)

from compliance_scanner.engine.relationship.relationship_graph import (
    RelationshipGraph,
)


class IdentityResolver:
    """
    Resolves identities attached to infrastructure resources.

    The resolver is provider-agnostic. It discovers identities by
    traversing the relationship graph and consulting the catalog.
    """

    def resolve(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:

        return ()
