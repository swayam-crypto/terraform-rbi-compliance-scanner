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

from .base import BaseRule, Finding

CHECKED_RESOURCES = {"aws_s3_bucket", "aws_db_instance"}

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
    applies_to = list(CHECKED_RESOURCES)

    def check(self, resource) -> Finding | None:
        if resource.resource_type not in CHECKED_RESOURCES:
            return None

        tags = resource.config.get("tags", {}) or {}

        tag_values = " ".join(str(v).lower() for v in tags.values())

        resource_name = resource.resource_name.lower()

        bucket_name = str(resource.config.get("bucket", "")).lower()

        db_identifier = str(resource.config.get("identifier", "")).lower()

        search_text = " ".join(
            [
                f"{resource_name}",
                f"{bucket_name}",
                f"{db_identifier}",
                f"{tag_values}",
            ]
        )

        looks_sensitive = any(hint in search_text for hint in SENSITIVE_KEYWORDS)

        if not looks_sensitive:
            return None  # same conservative approach as RBI-001 — skip if unconfirmed

        if resource.resource_type == "aws_s3_bucket":
            acl = resource.config.get("acl")

            if isinstance(acl, str):
                acl = acl.strip().lower()

            if acl in PUBLIC_ACLS:
                return Finding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    resource_type=resource.resource_type,
                    resource_name=resource.resource_name,
                    message=(
                        f"Bucket '{resource.resource_name}' appears to contain sensitive data "
                        f"and uses the '{acl}' ACL, which may allow public access."
                    ),
                    regulation_reference=self.regulation_reference,
                    file_path=resource.file_path,
                )

        if resource.resource_type == "aws_db_instance":
            publicly_accessible = resource.config.get("publicly_accessible")
            if publicly_accessible is True:
                return Finding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    resource_type=resource.resource_type,
                    resource_name=resource.resource_name,
                    message=(
                        f"Database '{resource.resource_name}' appears to hold sensitive data "
                        f"but has publicly_accessible = true."
                    ),
                    regulation_reference=self.regulation_reference,
                    file_path=resource.file_path,
                )

        return None
