from collections import deque

from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.models.resolved_resource import ResolvedResource


class GraphTraversal:
    """
    Graph traversal algorithms for RelationshipGraph.

    This class provides reusable traversal utilities that power
    graph-aware compliance rules.
    """

    def __init__(
        self,
        graph: RelationshipGraph,
    ):
        self.graph = graph

    def reachable_from(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        """
        Return every resource reachable from the starting resource.
        """
        queue = deque([resource])

        visited = {resource}

        reachable: list[ResolvedResource] = []

        while queue:
            current = queue.popleft()

            for neighbor in self.graph.neighbors(current):

                if neighbor in visited:
                    continue

                visited.add(neighbor)
                reachable.append(neighbor)
                queue.append(neighbor)

        return tuple(reachable)
