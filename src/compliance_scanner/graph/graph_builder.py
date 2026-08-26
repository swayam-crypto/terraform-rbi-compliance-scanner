from compliance_scanner.engine.relationship.relationship import Relationship
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph


class GraphBuilder:

    def build(self, relationships: list[Relationship,]) -> RelationshipGraph:
        graph = RelationshipGraph()

        for relationship in relationships:
            graph.add(relationship)

        return graph
