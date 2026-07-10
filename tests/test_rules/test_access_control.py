import json

from compliance_scanner.rules.access_control import LeastPrivilegeRule


def test_flags_wildcard_action():
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "arn:aws:s3:::mybucket"}]
    })
    result = rule.check(
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        resource_config={"policy": policy},
    )
    assert result is not None
    assert result.rule_id == "RBI-005"


def test_flags_wildcard_resource():
    rule = LeastPrivilegeRule()
    policy = json.dumps({
        "Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}]
    })
    result = rule.check(
        resource_type="aws_iam_policy",
        resource_name="overly_broad_policy",
        resource_config={"policy": policy},
    )
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
    result = rule.check(
        resource_type="aws_iam_policy",
        resource_name="scoped_policy",
        resource_config={"policy": policy},
    )
    assert result is None


def test_handles_missing_policy_gracefully():
    rule = LeastPrivilegeRule()
    result = rule.check(
        resource_type="aws_iam_policy",
        resource_name="empty",
        resource_config={},
    )
    assert result is None
