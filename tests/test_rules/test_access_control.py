import json

from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.rules.access_control import LeastPrivilegeRule
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def test_flags_wildcard_action():
    rule = LeastPrivilegeRule()
    policy = json.dumps(
        {
            "Statement": [
                {"Effect": "Allow", "Action": "*", "Resource": "arn:aws:s3:::mybucket"}
            ]
        }
    )
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        attributes={"policy": policy},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-005"


def test_flags_wildcard_resource():
    rule = LeastPrivilegeRule()
    policy = json.dumps(
        {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}]}
    )
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_iam_policy"),
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        attributes={"policy": policy},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is not None


def test_does_not_flag_scoped_policy():
    rule = LeastPrivilegeRule()
    policy = json.dumps(
        {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::specific-bucket/*",
                }
            ]
        }
    )
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_iam_policy"),
        resource_type="aws_iam_policy",
        resource_name="scoped_policy",
        attributes={"policy": policy},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_handles_missing_policy_gracefully():
    rule = LeastPrivilegeRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_iam_policy"),
        resource_type="aws_iam_policy",
        resource_name="empty",
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_deny_wildcard():
    """Deny statements with wildcards are security best practice, not violations."""
    rule = LeastPrivilegeRule()
    policy = json.dumps(
        {"Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}]}
    )
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_iam_policy"),
        resource_type="aws_iam_policy",
        resource_name="explicit_deny",
        attributes={"policy": policy},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None
