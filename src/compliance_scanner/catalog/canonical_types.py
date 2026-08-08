from enum import StrEnum


class CanonicalType(StrEnum):

    # Compute
    VIRTUAL_MACHINE = "virtual_machine"
    SERVERLESS_FUNCTION = "serverless_function"
    CONTAINER_CLUSTER = "container_cluster"
    CONTAINER_SERVICE = "container_service"

    # Data
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"

    # Storage
    OBJECT_STORAGE = "object_storage"
    BLOCK_STORAGE = "block_storage"
    FILE_STORAGE = "file_storage"

    # Networking
    LOAD_BALANCER = "load_balancer"
    API_GATEWAY = "api_gateway"
    CDN = "cdn"
    VPC = "vpc"
    SUBNET = "subnet"
    ROUTE_TABLE = "route_table"
    ROUTE = "route"
    SECURITY_GROUP = "security_group"
    NETWORK_ACL = "network_acl"
    INTERNET_GATEWAY = "internet_gateway"
    NAT_GATEWAY = "nat_gateway"
    ELASTIC_IP = "elastic_ip"

    # Security
    KMS_KEY = "kms_key"
    IAM_ROLE = "iam_role"
    IAM_POLICY = "iam_policy"
    SECRET = "secret"
    CERTIFICATE = "certificate"

    # Monitoring
    LOG_GROUP = "log_group"
    METRIC = "metric"
    ALARM = "alarm"

    # DNS
    DNS_ZONE = "dns_zone"
    DNS_RECORD = "dns_record"

    # AttributeType
    BOOLEAN = "boolean"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    OBJECT = "object"
    LIST = "list"
