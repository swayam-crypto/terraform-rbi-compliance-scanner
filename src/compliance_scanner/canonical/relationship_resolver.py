from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.engine.relationship.relationship import Relationship

from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.graph.reference_parser import ReferenceParser


class RelationshipResolver:

    def __init__(
        self,
        catalog: Catalog,
    ) -> None:
        self.catalog = catalog

    def extract(
        self,
        resources: list[ResolvedResource],
        index: ResourceIndex,
    ) -> list[Relationship]:
        """
        Extract relationships between normalized resources.
        """

        relationships: list[Relationship] = []

        for resource in resources:

            definition = self.catalog.definition(resource)

            if definition is None:
                continue

            for (
                attribute_name,
                attribute_definition,
            ) in definition.attributes.items():

                relationship = attribute_definition.relationship

                if relationship is None:
                    continue

                attribute_value = resource.attributes.get(attribute_name)

                if attribute_value is None:
                    continue
                parser = ReferenceParser()
                references = parser.parse_references(
                    attribute_value,
                )

                for resource_type, resource_name in references:

                    targets = index.find(
                        resource_type=resource_type,
                        resource_name=resource_name,
                    )

                    if not targets:
                        continue

                    for target in targets:

                        target_definition = self.catalog.definition(target)

                        if target_definition is None:
                            continue

                        if target_definition.canonical_type != relationship.target:
                            continue

                        relationships.append(
                            Relationship(
                                source=resource,
                                target=target,
                                relationship_type=relationship.relationship_type,
                            )
                        )

        return relationships
