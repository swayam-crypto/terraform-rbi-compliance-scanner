"""v0.8 capability-native baseline rule pack."""

from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.compliance import baseline_controls as controls

from .base import BaseRule, Finding
from .catalog_rules import AttributeRuleSpec, CatalogAttributeRule, below, disabled


REFERENCE = "Technical control mapping; validate applicability with your compliance team."


BASELINE_RULES = [
    CatalogAttributeRule(AttributeRuleSpec("RBI-006", "Databases must retain backups for at least seven days", REFERENCE, "high", controls.DATABASE_BACKUPS, frozenset({"data_store", "backup"}), "backup_days", below(7), "Database '{resource_name}' has {attribute}={value!r}; at least seven days is required.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-007", "Object storage must have versioning enabled", REFERENCE, "medium", controls.STORAGE_VERSIONING, frozenset({"data_store", "versioning"}), "versioning", disabled, "Storage resource '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-008", "Customer-managed keys must rotate automatically", REFERENCE, "medium", controls.KMS_ROTATION, frozenset({"encryption_key", "key_rotation"}), "key_rotation", disabled, "Encryption key '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-009", "Databases must enable deletion protection", REFERENCE, "high", controls.DATABASE_DELETION_PROTECTION, frozenset({"data_store", "deletion_protection"}), "deletion_protection", disabled, "Database '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-010", "Databases should use multi-zone deployment", REFERENCE, "medium", controls.DATABASE_MULTI_AZ, frozenset({"data_store", "high_availability"}), "multi_az", disabled, "Database '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-011", "Object storage must record access logs", REFERENCE, "medium", controls.STORAGE_ACCESS_LOGGING, frozenset({"data_store", "access_logging"}), "access_logging", disabled, "Storage resource '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-012", "Log groups must be encrypted", REFERENCE, "medium", controls.LOG_ENCRYPTION, frozenset({"audit_logging", "encryption_at_rest"}), "encryption_key", disabled, "Log group '{resource_name}' does not have an encryption key configured.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-013", "Serverless functions must use private networking", REFERENCE, "high", controls.FUNCTION_VPC, frozenset({"serverless_compute", "private_networking"}), "network_attachment", disabled, "Function '{resource_name}' does not have private network configuration.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-014", "Block volumes must be encrypted", REFERENCE, "high", controls.VOLUME_ENCRYPTION, frozenset({"block_storage", "encryption_at_rest"}), "encryption", disabled, "Block volume '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-015", "File systems must be encrypted", REFERENCE, "high", controls.FILE_ENCRYPTION, frozenset({"file_storage", "encryption_at_rest"}), "encryption", disabled, "File system '{resource_name}' does not have {attribute} enabled.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-016", "Message queues must be encrypted", REFERENCE, "high", controls.QUEUE_ENCRYPTION, frozenset({"message_queue", "encryption_at_rest"}), "encryption_key", disabled, "Message queue '{resource_name}' does not have an encryption key configured.")),
    CatalogAttributeRule(AttributeRuleSpec("RBI-017", "Notification topics must be encrypted", REFERENCE, "high", controls.TOPIC_ENCRYPTION, frozenset({"notification", "encryption_at_rest"}), "encryption_key", disabled, "Notification topic '{resource_name}' does not have an encryption key configured.")),
]


class RestrictedIngressRule(BaseRule):
    """Detect an internet CIDR opening a sensitive administrative port."""

    def __init__(self, rule_id: str, port: int, description: str, control):
        self.rule_id, self.port, self.description, self.control = rule_id, port, description, control
        self.regulation_reference, self.severity = REFERENCE, "critical"
        self.required_capabilities = frozenset({"network_security", "ingress_rules"})

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None
        ingress_attribute = catalog.attribute_name(resource, "ingress")
        ingress_rules = resource.get(ingress_attribute) if ingress_attribute else []
        if isinstance(ingress_rules, dict):
            ingress_rules = [ingress_rules]
        for ingress in ingress_rules or []:
            if not isinstance(ingress, dict):
                continue
            from_port, to_port = ingress.get("from_port"), ingress.get("to_port")
            cidrs = ingress.get("cidr_blocks", []) or []
            if (from_port is not None and to_port is not None and from_port <= self.port <= to_port and "0.0.0.0/0" in cidrs):
                return self.finding(resource, f"Security group '{resource.resource_name}' exposes TCP port {self.port} to 0.0.0.0/0.")
        return None


class UnrestrictedIngressRule(RestrictedIngressRule):
    def __init__(self):
        super().__init__("RBI-020", -1, "Security groups must not expose all ports publicly", controls.UNRESTRICTED_INGRESS)

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None
        ingress_attribute = catalog.attribute_name(resource, "ingress")
        for ingress in resource.get(ingress_attribute, []) or []:
            if isinstance(ingress, dict) and ingress.get("protocol") == "-1" and "0.0.0.0/0" in (ingress.get("cidr_blocks", []) or []):
                return self.finding(resource, f"Security group '{resource.resource_name}' allows all protocols and ports from 0.0.0.0/0.")
        return None


SSH_RESTRICTION_RULE = RestrictedIngressRule("RBI-018", 22, "SSH must not be publicly exposed", controls.SSH_RESTRICTED)
RDP_RESTRICTION_RULE = RestrictedIngressRule("RBI-019", 3389, "RDP must not be publicly exposed", controls.RDP_RESTRICTED)
