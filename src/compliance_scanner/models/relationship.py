from dataclasses import dataclass
from enum import Enum

from compliance_scanner.models.resolved_resource import ResolvedResource


class RelationshipType(Enum):
    SECURITY_GROUP = "security_group"
    SUBNET = "subnet"
    VPC = "vpc"
    SUBNET_GROUP = "subnet_group"
    IAM_POLICY = "iam_policy"
    BUCKET_POLICY = "bucket_policy"
    KMS_KEY = "kms_key"
    TARGET_GROUP = "target_group"


@dataclass(frozen=True)
class Relationship:
    source: ResolvedResource
    target: ResolvedResource
    relationship_type: RelationshipType
