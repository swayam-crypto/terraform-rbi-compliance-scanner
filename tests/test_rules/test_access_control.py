import json

from compliance_scanner.parser.terraform_parser import ResolvedResource
from compliance_scanner.rules.access_control import LeastPrivilegeRule


def test_flags_wildcard_action():
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "arn:aws:s3:::mybucket"}]
    })
    resource = ResolvedResource(
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        config={"policy": policy},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-005"


def test_flags_wildcard_resource():
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}]
    })
    resource = ResolvedResource(
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        config={"policy": policy},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None


def test_does_not_flag_scoped_policy():
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::specific-bucket/*",
        }]
    })
    resource = ResolvedResource(
        resource_type="aws_iam_policy",
        resource_name="scoped_policy",
        config={"policy": policy},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_handles_missing_policy_gracefully():
    rule = LeastPrivilegeRule()
    resource = ResolvedResource(
        resource_type="aws_iam_policy",
        resource_name="empty",
        config={},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_deny_wildcard():
    """Deny statements with wildcards are security best practice, not violations."""
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}]
    })
    resource = ResolvedResource(
        resource_type="aws_iam_policy",
        resource_name="explicit_deny",
        config={"policy": policy},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None