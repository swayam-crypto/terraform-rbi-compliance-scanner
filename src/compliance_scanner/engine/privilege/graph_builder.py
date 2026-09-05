from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.graph.resource_index import ResourceIndex


class PrivilegeGraphBuilder:
    """
    Builds the runtime privilege graph.

    The initial implementation returns an empty graph. Future
    implementations will populate privilege relationships from
    provider-specific identity metadata.
    """

    def build(
        self,
        resource_index: ResourceIndex,
    ) -> PrivilegeGraph:
        return PrivilegeGraph()
