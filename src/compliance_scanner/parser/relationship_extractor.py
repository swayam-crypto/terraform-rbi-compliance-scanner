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
    "bucket_policy": (
        RelationshipType.ATTACHED_TO_BUCKET_POLICY,
        "aws_s3_bucket_policy",
    ),
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

                reference = self._parse_reference(attribute_value)

                if reference is None:
                    continue
                resource_type, resource_name = reference

                if resource_type != target_resource_type:
                    continue
                targets = index.find(
                    resource_type=resource_type,
                    resource_name=resource_name,
                )
                if not targets:
                    continue
                target = targets[0]
                relationships.append(
                    Relationship(
                        source=resource,
                        target=target,
                        relationship_type=relationship_type,
                    )
                )

        # Resolve the reference
        # Find the target resource
        # Create a Relationship
        # Append it to relationships
        return relationships

    def _parse_reference(
        self,
        value: str,
    ) -> tuple[str, str] | None:

        if not isinstance(value, str):
            return None

        parts = value.split(".")

        if len(parts) < 3:
            return None

        resource_type = parts[0]
        resource_name = parts[1]

        return (
            resource_type,
            resource_name,
        )
