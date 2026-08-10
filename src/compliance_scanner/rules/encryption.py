"""
RBI-002: Encryption at rest check.

Flags storage resources (S3, RDS, DynamoDB) that don't have
encryption explicitly enabled.
"""

from compliance_scanner.catalog.global_catalog import catalog

from .base import BaseRule, Finding
from compliance_scanner.compliance.control_catalog import ENCRYPTION_AT_REST

class EncryptionAtRestRule(BaseRule):
    rule_id = "RBI-002"
    description = "Storage resources must have encryption at rest enabled"
    regulation_reference = "RBI Cybersecurity Framework — Data Protection requirement"
    severity = "high"
    required_capabilities = frozenset({"data_store", "encryption_at_rest"})
    control = ENCRYPTION_AT_REST

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None

        attribute_name = catalog.attribute_name(resource, "encryption")
        if attribute_name is None:
            return None

        value = resource.get(attribute_name)

        is_encrypted = bool(value) and value is not False
        if not is_encrypted:
            return self.finding(
                resource,
                (
                    f"Resource '{resource.resource_name}' does not have encryption at rest "
                    f"explicitly enabled ('{attribute_name}' missing or false)."
                ),
            )

        return None
