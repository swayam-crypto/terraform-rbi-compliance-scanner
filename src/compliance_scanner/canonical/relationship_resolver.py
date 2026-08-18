from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.graph.relationship import Relationship

from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.catalog.catalog import Catalog


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

                references = self._parse_references(attribute_value)

                for resource_type, resource_name in references:

                    targets = index.find(
                        resource_type=resource_type,
                        resource_name=resource_name,
                    )

                    if not targets:
                        continue

                    target = targets[0]

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

    def _parse_references(
        self,
        value: object,
    ) -> list[tuple[str, str]]:
        """
        Parse one or more Terraform resource references.

        Examples:
            "aws_subnet.private.id"
                -> [("aws_subnet", "private")]

            [
                "aws_security_group.web.id",
                "aws_security_group.db.id",
            ]
                -> [
                    ("aws_security_group", "web"),
                    ("aws_security_group", "db"),
                ]
        """

        references: list[tuple[str, str]] = []

        values: list[str]

        if isinstance(value, str):
            values = [value]
        elif isinstance(value, list):
            values = [item for item in value if isinstance(item, str)]
        else:
            return references

        for item in values:
            parts = item.split(".")

            if len(parts) < 3:
                continue

            references.append(
                (
                    parts[0],
                    parts[1],
                )
            )

        return references
