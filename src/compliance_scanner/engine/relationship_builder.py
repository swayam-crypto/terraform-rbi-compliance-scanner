from compliance_scanner.models.relationship import (
    Relationship,
    RelationshipType,
)
from .resource_index import ResourceIndex
from .relationship_graph import RelationshipGraph


class RelationshipBuilder:

    def build(self, index: ResourceIndex) -> RelationshipGraph:
        graph = RelationshipGraph()

        #
        # Future PRs will populate the graph
        #

        return graph
