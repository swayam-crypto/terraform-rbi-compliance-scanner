"""
RBI-005: IAM least-privilege check — flags wildcard ("*") permissions.

Grounding: same category as RBI-004 — a broad, repeatedly stated
principle (least-privilege access control, explicitly named in RBI's
Cyber Security Framework for Banks, 2016, under "Access Control"),
not one specific numeric circular. Wildcard IAM actions/resources are
a well-established anti-pattern across every major cloud security
framework (AWS's own Well-Architected Framework included), and this
rule encodes that as a checkable Terraform rule.

Checks aws_iam_policy documents (as JSON strings, which is the
standard way they're written in Terraform) for "*" in Action or
Resource fields.
"""

import json

from .base import BaseRule, Finding

CHECKED_RESOURCES = {"aws_iam_policy", "aws_iam_role_policy"}


class LeastPrivilegeRule(BaseRule):
    rule_id = "RBI-005"
    description = "IAM policies must not grant wildcard (*) actions or resources"
    regulation_reference = (
        "Technical interpretation of RBI Cyber Security Framework (2016) "
        "'Access Control' principle (least privilege) — not a specific numeric circular"
    )
    severity = "high"
    applies_to = list(CHECKED_RESOURCES)

    def check(self, resource_type: str, resource_name: str, resource_config: dict) -> Finding | None:
        if resource_type not in CHECKED_RESOURCES:
            return None

        policy_raw = resource_config.get("policy")
        if not policy_raw:
            return None

        try:
            policy = json.loads(policy_raw) if isinstance(policy_raw, str) else policy_raw
        except (json.JSONDecodeError, TypeError):
            return None  # can't parse — skip rather than guess

        statements = policy.get("Statement", [])
        if isinstance(statements, dict):
            statements = [statements]

        for statement in statements:
            actions = statement.get("Action", [])
            resources = statement.get("Resource", [])
            actions = [actions] if isinstance(actions, str) else actions
            resources = [resources] if isinstance(resources, str) else resources

            if "*" in actions or "*" in resources:
                return Finding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    resource_type=resource_type,
                    resource_name=resource_name,
                    message=(
                        f"IAM policy '{resource_name}' grants a wildcard (*) "
                        f"action or resource, violating least-privilege access control."
                    ),
                    regulation_reference=self.regulation_reference,
                )

        return None
