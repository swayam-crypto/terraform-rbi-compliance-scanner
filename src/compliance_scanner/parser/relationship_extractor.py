from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.graph.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.graph.resource_index import ResourceIndex

from typing import Final

# Maps Terraform attribute names to:
# (RelationshipType, Expected Target Resource Type)

ATTRIBUTE_RELATIONSHIPS: Final[dict[str, tuple[RelationshipType, str]]] = {
    # Networking
    "subnet_id": (
        RelationshipType.USES_SUBNET,
        "aws_subnet",
    ),
    "vpc_id": (
        RelationshipType.USES_VPC,
        "aws_vpc",
    ),
    "vpc_security_group_ids": (
        RelationshipType.ATTACHED_TO_SECURITY_GROUP,
        "aws_security_group",
    ),
    # Encryption
    "kms_key_id": (
        RelationshipType.USES_KMS_KEY,
        "aws_kms_key",
    ),
    # Load Balancing
    "target_group_arn": (
        RelationshipType.USES_TARGET_GROUP,
        "aws_lb_target_group",
    ),
    # Storage
    "bucket": (RelationshipType.ATTACHED_TO_BUCKET, "aws_s3_bucket"),
}


class RelationshipExtractor:

    def extract(
        self,
        resources: list[ResolvedResource],
        index: ResourceIndex,
    ) -> list[Relationship]:
        """
        Extract relationships between normalized resources.

        Args:
            resources: Resources to inspect.
            index: Index used to resolve referenced resources.

        Returns:
            A list of discovered relationships.
        """

        relationships: list[Relationship] = []

        for resource in resources:
            for attribute_name, attribute_value in resource.attributes.items():
                if attribute_name not in ATTRIBUTE_RELATIONSHIPS:
                    continue

                mapping = ATTRIBUTE_RELATIONSHIPS[attribute_name]
                relationship_type, target_resource_type = mapping

                references = self._parse_references(attribute_value)

                for resource_type, resource_name in references:

                    if resource_type != target_resource_type:
                        continue

                    targets = index.find(
                        resource_type=resource_type,
                        resource_name=resource_name,
                    )

                    if not targets:
                        continue

                    relationships.append(
                        Relationship(
                            source=resource,
                            target=targets[0],
                            relationship_type=relationship_type,
                        )
                    )

        # Resolve the reference
        # Find the target resource
        # Create a Relationship
        # Append it to relationships
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
