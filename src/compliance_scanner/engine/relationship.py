from dataclasses import dataclass
from enum import Enum

from compliance_scanner.parser.terraform_parser import ResolvedResource


class RelationshipType(Enum):
    BUCKET_POLICY = "bucket_policy"
    SECURITY_GROUP = "security_group"
    IAM_POLICY = "iam_policy"
    KMS_KEY = "kms_key"


@dataclass(frozen=True)
class Relationship:
    source: ResolvedResource
    target: ResolvedResource
    relationship_type: RelationshipType
