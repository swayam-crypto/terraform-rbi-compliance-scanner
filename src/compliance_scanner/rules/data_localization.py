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

    def check(self, resource) -> Finding | None:
        if resource.resource_type not in CHECKED_RESOURCES:
            return None

        # Heuristic: does the resource name or tags suggest sensitive data?
        tags = resource.config.get("tags", {}) or {}
        tag_values = " ".join(str(v).lower() for v in tags.values())
        name_and_tags = f"{resource.resource_name.lower()} {tag_values}"

        looks_sensitive = any(hint in name_and_tags for hint in SENSITIVE_TAG_HINTS)
        if not looks_sensitive:
            return None  # can't confirm this resource holds regulated data — skip

        # KEY FIX: Use resource.get() which checks provider defaults
        region = resource.get("region")

        if region is None:
            # No region found anywhere — flag as unknown/unverified
            return Finding(
                rule_id=self.rule_id,
                severity=self.severity,
                resource_type=resource.resource_type,
                resource_name=resource.resource_name,
                message=(
                    f"Resource '{resource.resource_name}' appears to hold sensitive "
                    f"financial/customer data but has no region specified (neither on "
                    f"the resource nor in a provider block). Cannot verify RBI data "
                    f"localization compliance."
                ),
                regulation_reference=self.regulation_reference,
                file_path=resource.file_path,
            )

        if region not in INDIA_REGIONS:
            return Finding(
                rule_id=self.rule_id,
                severity=self.severity,
                resource_type=resource.resource_type,
                resource_name=resource.resource_name,
                message=(
                    f"Resource '{resource.resource_name}' appears to hold sensitive financial/"
                    f"customer data but is provisioned in '{region}', outside India. "
                    f"RBI data localization rules likely require ap-south-1 or ap-south-2."
                ),
                regulation_reference=self.regulation_reference,
                file_path=resource.file_path,
            )

        return None