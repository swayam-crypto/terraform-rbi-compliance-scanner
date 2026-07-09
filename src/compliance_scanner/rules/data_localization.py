"""
RBI-001: Data localization check.

RBI's guidelines require that certain categories of payment/financial
system data be stored only within India. This rule flags AWS resources
that hold or reference financial data but are provisioned outside
India's AWS region (ap-south-1 / ap-south-2).

This is a STARTER rule — extend `SENSITIVE_TAGS` and `CHECKED_RESOURCES`
as you study the RBI framework further.
"""

from .base import BaseRule, Finding

INDIA_REGIONS = {"ap-south-1", "ap-south-2"}

# Resource types where data residency matters most
CHECKED_RESOURCES = {
    "aws_s3_bucket",
    "aws_db_instance",
    "aws_dynamodb_table",
    "aws_rds_cluster",
}

# Tag values that signal "this holds financial/customer data"
SENSITIVE_TAG_HINTS = {"financial", "payment", "customer", "transaction", "pii", "kyc"}


class DataLocalizationRule(BaseRule):
    rule_id = "RBI-001"
    description = "Financial/customer data must reside in an Indian AWS region"
    regulation_reference = "RBI Cybersecurity Framework — Data Localization requirement"
    severity = "critical"
    applies_to = list(CHECKED_RESOURCES)

    def check(self, resource_type: str, resource_name: str, resource_config: dict) -> Finding | None:
        if resource_type not in CHECKED_RESOURCES:
            return None

        # Heuristic: does the resource name or tags suggest sensitive data?
        tags = resource_config.get("tags", {}) or {}
        tag_values = " ".join(str(v).lower() for v in tags.values())
        name_and_tags = f"{resource_name.lower()} {tag_values}"

        looks_sensitive = any(hint in name_and_tags for hint in SENSITIVE_TAG_HINTS)
        if not looks_sensitive:
            return None  # can't confirm this resource holds regulated data — skip

        # Region can come from a provider block or resource-level attribute
        region = resource_config.get("region") or resource_config.get("provider_region")

        if region and region not in INDIA_REGIONS:
            return Finding(
                rule_id=self.rule_id,
                severity=self.severity,
                resource_type=resource_type,
                resource_name=resource_name,
                message=(
                    f"Resource '{resource_name}' appears to hold sensitive financial/"
                    f"customer data but is provisioned in '{region}', outside India. "
                    f"RBI data localization rules likely require ap-south-1 or ap-south-2."
                ),
                regulation_reference=self.regulation_reference,
            )

        return None
