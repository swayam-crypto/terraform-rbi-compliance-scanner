"""
RBI-003: Audit log retention check.

Grounding: CERT-In Cybersecurity Directions 2022 (issued 28 April 2022
under Section 70B(6) of the IT Act, 2000) mandate that all service
providers, intermediaries, data centres, body corporates, and government
organisations maintain ICT system logs securely for a ROLLING PERIOD OF
180 DAYS, within Indian jurisdiction. This is a specific, numeric,
binding requirement — not a general best practice.

This rule checks CloudWatch Log Groups (the standard place AWS-hosted
systems send their logs) for a retention period of at least 180 days.

Note on AWS's default behavior: if retention_in_days isn't set at all,
CloudWatch defaults to "Never Expire" — which technically satisfies
"at least 180 days" (infinity >= 180). So this rule only flags log
groups where retention is explicitly set to something LESS than 180 days,
not log groups where it's simply unset.
"""

from .base import BaseRule, Finding

CHECKED_RESOURCES = {"aws_cloudwatch_log_group"}
MINIMUM_RETENTION_DAYS = 180


class AuditLogRetentionRule(BaseRule):
    rule_id = "RBI-003"
    description = "ICT system logs must be retained for at least 180 days (CERT-In mandate)"
    regulation_reference = "CERT-In Cybersecurity Directions 2022, Direction (iv), issued under IT Act Section 70B(6)"
    severity = "high"
    applies_to = list(CHECKED_RESOURCES)

    def check(self, resource_type: str, resource_name: str, resource_config: dict) -> Finding | None:
        if resource_type not in CHECKED_RESOURCES:
            return None

        retention = resource_config.get("retention_in_days")

        # Not set at all == AWS default "Never Expire", which satisfies
        # the 180-day minimum implicitly. Only flag if explicitly too short.
        if retention is None:
            return None

        try:
            retention_days = int(retention)
        except (TypeError, ValueError):
            return None  # unexpected value shape, skip rather than guess

        if retention_days < MINIMUM_RETENTION_DAYS:
            return Finding(
                rule_id=self.rule_id,
                severity=self.severity,
                resource_type=resource_type,
                resource_name=resource_name,
                message=(
                    f"Log group '{resource_name}' has retention_in_days set to "
                    f"{retention_days}, below the CERT-In mandated minimum of "
                    f"{MINIMUM_RETENTION_DAYS} days."
                ),
                regulation_reference=self.regulation_reference,
            )

        return None
