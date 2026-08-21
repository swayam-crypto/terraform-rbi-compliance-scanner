from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.attack.algorithms import ShortestPathAlgorithm
from compliance_scanner.attack.collection import AttackPathCollection


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
    ) -> AttackPathCollection:

        algorithm = ShortestPathAlgorithm(
            self.graph,
        )

        path = algorithm.find_path(
            source,
            target,
        )

        if path is None:
            return AttackPathCollection(
                paths=(),
            )

        return AttackPathCollection(
            paths=(path,),
        )
