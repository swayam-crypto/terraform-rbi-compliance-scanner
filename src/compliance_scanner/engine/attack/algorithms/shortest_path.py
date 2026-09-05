from collections import deque

from compliance_scanner.engine.attack.models import AttackPath
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph
from compliance_scanner.models.resolved_resource import ResolvedResource


class ShortestPathAlgorithm:
    """
    Discovers the shortest attack path between two resources.

    This class performs graph traversal only.

    It does not evaluate compliance, calculate risk or simulate attacks.
    """

    def __init__(
        self,
        graph: RelationshipGraph,
    ) -> None:
        self.graph = graph

    def find_path(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> AttackPath | None:
        """
        Return the shortest attack path between the source and target
        resources.

        Returns None if no path exists.
        """

        queue = deque(
            [
                (
                    source,
                    (source,),
                    (),
                )
            ]
        )

        visited = {source}

        while queue:

            current, resources, relationships = queue.popleft()

            if current == target:
                return AttackPath(
                    source=source,
                    target=target,
                    resources=resources,
                    relationships=relationships,
                )

            for relationship in self.graph.outgoing(current):

                neighbor = relationship.target

                if neighbor in visited:
                    continue

                visited.add(neighbor)

                queue.append(
                    (
                        neighbor,
                        resources + (neighbor,),
                        relationships + (relationship,),
                    )
                )

        return None
