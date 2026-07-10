from compliance_scanner.rules.network_exposure import NetworkExposureRule


def test_flags_public_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        resource_config={"acl": "public-read", "tags": {"data_type": "customer"}},
    )
    assert result is not None
    assert result.rule_id == "RBI-004"

def test_does_not_flag_private_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        resource_config={"acl": "private", "tags": {"data_type": "customer"}},
    )
    assert result is None