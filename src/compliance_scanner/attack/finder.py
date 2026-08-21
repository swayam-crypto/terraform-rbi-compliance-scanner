from compliance_scanner.attack.models import AttackPath
from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.models.resolved_resource import ResolvedResource


class AttackPathFinder:
    """
    Discovers attack paths through the infrastructure graph.

    The finder is responsible only for path discovery.

    It performs no compliance evaluation, risk scoring or attack
    simulation.
    """

    def __init__(
        self,
        graph: RelationshipGraph,
    ) -> None:
        self.graph = graph

    def find_paths(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> tuple[AttackPath, ...]:
        raise NotImplementedError
