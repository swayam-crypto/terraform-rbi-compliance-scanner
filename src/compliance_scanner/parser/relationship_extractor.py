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
                print(f"{resource.resource_type}.{resource.resource_name}")
                print(attribute_name, attribute_value)

        # Resolve the reference
        # Find the target resource
        # Create a Relationship
        # Append it to relationships
        relationships: list[Relationship] = []

        return relationships
