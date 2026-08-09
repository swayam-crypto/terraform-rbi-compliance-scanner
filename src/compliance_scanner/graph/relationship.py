from dataclasses import dataclass, field
from enum import Enum
from typing import Any


from compliance_scanner.models.resolved_resource import ResolvedResource


class RelationshipType(str, Enum):
    VPC = "vpc"
    SUBNET = "subnet"
    ROUTE_TABLE = "route_table"
    ROUTE = "route"

    INTERNET_GATEWAY = "internet_gateway"
    NAT_GATEWAY = "nat_gateway"
    VPC_ENDPOINT = "vpc_endpoint"
    VPC_PEERING_CONNECTION = "vpc_peering_connection"

    ELASTIC_IP = "elastic_ip"

    SECURITY_GROUP = "security_group"
    NETWORK_ACL = "network_acl"
    NETWORK_INTERFACE = "network_interface"

    VIRTUAL_MACHINE = "virtual_machine"

    LOAD_BALANCER = "load_balancer"
    TARGET_GROUP = "target_group"

    API_GATEWAY = "api_gateway"

    KMS_KEY = "kms_key"

    OBJECT_STORAGE = "object_storage"
    DATABASE = "database"

    IAM_ROLE = "iam_role"
    IAM_POLICY = "iam_policy"

    SECRET = "secret"

    CERTIFICATE = "certificate"

    LOG_GROUP = "log_group"

    DNS_ZONE = "dns_zone"
    DNS_RECORD = "dns_record"


@dataclass(frozen=True)
class Relationship:
    source: ResolvedResource
    target: ResolvedResource
    relationship_type: RelationshipType
    metadata: dict[str, Any] = field(default_factory=dict)
