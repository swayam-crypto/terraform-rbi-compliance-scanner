from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.engine.relationship.relationship import Relationship

from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.catalog.catalog import Catalog


class RelationshipResolver:

    def __init__(
        self,
        catalog: Catalog,
    ) -> None:
        self.catalog = catalog

    def _normalize_resource_name(
        self,
        resource_name: str,
    ) -> str:
        """
        Remove Terraform index expressions from a resource name.

        Examples:
            private -> private
            private[0] -> private
            private[*] -> private
            private[count.index] -> private
            private[each.key] -> private
        """

        return resource_name.split("[", 1)[0]

    def _flatten_values(
        self,
        value: object,
    ) -> list[str]:
        """
        Recursively flatten Terraform values into a list of strings.
        """

        if isinstance(value, str):
            return [value]

        if isinstance(value, (list, tuple)):
            values: list[str] = []

            for item in value:
                values.extend(self._flatten_values(item))

            return values

        return []

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

        values = self._flatten_values(
            value,
        )

        for item in values:
            parts = item.split(".")

            if len(parts) < 2:
                continue

            resource_type = parts[0]

            resource_name = self._normalize_resource_name(
                parts[1],
            )

            references.append(
                (
                    resource_type,
                    resource_name,
                )
            )

        return references
