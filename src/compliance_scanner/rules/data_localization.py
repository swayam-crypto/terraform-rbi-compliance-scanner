"""
RBI-001: Data localization check.

RBI's guidelines require that certain categories of payment/financial
system data be stored only within India. This rule flags AWS resources
that hold or reference financial data but are provisioned outside
India's AWS region (ap-south-1 / ap-south-2).

This is a STARTER rule — extend `SENSITIVE_TAGS` and `CHECKED_RESOURCES`
as you study the RBI framework further.
"""

from compliance_scanner.catalog.global_catalog import catalog

from .base import BaseRule, Finding
from compliance_scanner.compliance.control_catalog import DATA_RESIDENCY

INDIA_REGIONS = {"ap-south-1", "ap-south-2"}

# Tag values that signal "this holds financial/customer data"
SENSITIVE_TAG_HINTS = {"financial", "payment", "customer", "transaction", "pii", "kyc"}


class DataLocalizationRule(BaseRule):
    rule_id = "RBI-001"
    description = "Financial/customer data must reside in an Indian AWS region"
    regulation_reference = "RBI Cybersecurity Framework — Data Localization requirement"
    severity = "critical"
    required_capabilities = frozenset({"data_store", "data_residency"})
    control = DATA_RESIDENCY

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None

        # Heuristic: does the resource name or tags suggest sensitive data?
        tags = resource.attributes.get("tags", {}) or {}
        tag_values = " ".join(str(v).lower() for v in tags.values())
        name_and_tags = f"{resource.resource_name.lower()} {tag_values}"

        looks_sensitive = any(hint in name_and_tags for hint in SENSITIVE_TAG_HINTS)
        if not looks_sensitive:
            return None  # can't confirm this resource holds regulated data — skip

        region_attribute = catalog.attribute_name(resource, "region")
        region = resource.get(region_attribute) if region_attribute else None

        if region is None:
            # No region found anywhere — flag as unknown/unverified
            return self.finding(
                resource,
                (
                    f"Resource '{resource.resource_name}' appears to hold sensitive "
                    f"financial/customer data but has no region specified (neither on "
                    f"the resource nor in a provider block). Cannot verify RBI data "
                    f"localization compliance."
                ),
            )

        if region not in INDIA_REGIONS:
            return self.finding(
                resource,
                (
                    f"Resource '{resource.resource_name}' appears to hold sensitive financial/"
                    f"customer data but is provisioned in '{region}', outside India. "
                    f"RBI data localization rules likely require ap-south-1 or ap-south-2."
                ),
            )

        return None
