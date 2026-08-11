"""
RBI-004: Public network exposure check for sensitive data stores.

Grounding — IMPORTANT DISTINCTION FROM RBI-001/RBI-003:
Unlike data localization (a specific circular) or log retention (a
specific numeric CERT-In mandate), there is no single RBI circular that
says "S3 buckets must not be public." Instead, this rule is a technical
interpretation of a broader, repeatedly stated principle across:

- RBI's Cyber Security Framework for Banks (2016) — expects "access
  controls" and protection of customer data from unauthorized access
- India's DPDPA 2023, Section 8(5) — data fiduciaries must implement
  "reasonable security safeguards" to prevent personal data breaches

Treat this rule as a defensible technical control mapped to a broad
regulatory principle, not a citation of an exact numeric rule. Document
this distinction if you present this project — it's more honest than
implying every rule has a specific circular behind it, and reviewers
who know the space will respect that precision.
"""

from compliance_scanner.catalog.global_catalog import catalog

from .base import BaseRule, Finding
from compliance_scanner.compliance.control_catalog import PUBLIC_SENSITIVE_DATA

PUBLIC_ACLS = {"public-read", "public-read-write", "authenticated-read"}

SENSITIVE_KEYWORDS = {
    "financial",
    "payment",
    "customer",
    "transaction",
    "pii",
    "kyc",
    "account",
    "bank",
    "client",
    "user",
    "loan",
    "card",
    "statement",
    "invoice",
    "payroll",
    "identity",
    "personal",
}


class NetworkExposureRule(BaseRule):
    rule_id = "RBI-004"
    description = "Resources holding sensitive data must not be publicly accessible"
    regulation_reference = (
        "Technical interpretation of RBI Cyber Security Framework (2016) access "
        "control expectations and DPDPA 2023 Section 8(5) reasonable security "
        "safeguards — not a specific numeric circular"
    )
    severity = "critical"
    required_capabilities = frozenset({"data_store", "public_access_configuration"})
    control = PUBLIC_SENSITIVE_DATA

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None

        tags = resource.attributes.get("tags", {}) or {}

        tag_values = " ".join(str(v).lower() for v in tags.values())

        resource_name = resource.resource_name.lower()

        resource_name_attribute = catalog.attribute_name(resource, "resource_name")
        configured_name = str(
            resource.get(resource_name_attribute) if resource_name_attribute else ""
        ).lower()

        search_text = " ".join(
            [
                f"{resource_name}",
                f"{configured_name}",
                f"{tag_values}",
            ]
        )

        looks_sensitive = any(hint in search_text for hint in SENSITIVE_KEYWORDS)

        if not looks_sensitive:
            return None  # same conservative approach as RBI-001 — skip if unconfirmed

        public_access_attribute = catalog.attribute_name(resource, "public_access")
        public_access = resource.get(public_access_attribute) if public_access_attribute else None
        normalized_access = (
            public_access.strip().lower()
            if isinstance(public_access, str)
            else public_access
        )

        is_public = normalized_access in PUBLIC_ACLS or normalized_access is True
        if is_public:
            return self.finding(
                resource,
                (
                    f"Resource '{resource.resource_name}' appears to contain sensitive data "
                    f"but has public access configured via '{public_access_attribute}'."
                ),
            )

        return None
