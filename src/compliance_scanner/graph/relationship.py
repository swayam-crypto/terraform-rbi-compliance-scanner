from dataclasses import dataclass
from enum import Enum

from compliance_scanner.models.resolved_resource import ResolvedResource

from typing import Any
from dataclasses import dataclass, field


class RelationshipType(Enum):
    ATTACHED_TO_SECURITY_GROUP = "security_group"
    USES_SUBNET = "subnet"
    USES_VPC = "vpc"
    SUBNET_GROUP = "subnet_group"
    ATTACHED_TO_IAM_POLICY = "iam_policy"
    ATTACHED_TO_BUCKET = "bucekt"
    USES_KMS_KEY = "kms_key"
    USES_TARGET_GROUP = "target_group"


@dataclass(frozen=True)
class Relationship:
    source: ResolvedResource
    target: ResolvedResource
    relationship_type: RelationshipType
    metadata: dict[str, Any] = field(default_factory=dict)
