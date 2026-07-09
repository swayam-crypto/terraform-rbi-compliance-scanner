"""
RBI-002: Encryption at rest check.

Flags storage resources (S3, RDS, DynamoDB) that don't have
encryption explicitly enabled.
"""

from .base import BaseRule, Finding

CHECKED_RESOURCES = {"aws_s3_bucket", "aws_db_instance", "aws_dynamodb_table"}

# Terraform attribute name that indicates encryption, per resource type
ENCRYPTION_ATTR = {
    "aws_s3_bucket": "server_side_encryption_configuration",
    "aws_db_instance": "storage_encrypted",
    "aws_dynamodb_table": "server_side_encryption",
}


class EncryptionAtRestRule(BaseRule):
    rule_id = "RBI-002"
    description = "Storage resources must have encryption at rest enabled"
    regulation_reference = "RBI Cybersecurity Framework — Data Protection requirement"
    severity = "high"
    applies_to = list(CHECKED_RESOURCES)

    def check(self, resource_type: str, resource_name: str, resource_config: dict) -> Finding | None:
        if resource_type not in CHECKED_RESOURCES:
            return None

        attr = ENCRYPTION_ATTR[resource_type]
        value = resource_config.get(attr)

        is_encrypted = bool(value) and value is not False
        if not is_encrypted:
            return Finding(
                rule_id=self.rule_id,
                severity=self.severity,
                resource_type=resource_type,
                resource_name=resource_name,
                message=(
                    f"Resource '{resource_name}' does not have encryption at rest "
                    f"explicitly enabled ('{attr}' missing or false)."
                ),
                regulation_reference=self.regulation_reference,
            )

        return None
