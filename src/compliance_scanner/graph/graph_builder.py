from compliance_scanner.graph.relationship import Relationship
from compliance_scanner.graph.relationship_graph import RelationshipGraph
from .resource_index import ResourceIndex


class GraphBuilder:

    def build(self, index: ResourceIndex) -> RelationshipGraph:
        graph = RelationshipGraph()

        #
        # Future PRs will populate the graph
        #

        return graph
