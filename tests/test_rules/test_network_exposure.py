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


def test_does_not_flag_public_non_sensitive_bucket():
    rule = NetworkExposureRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="marketing_assets",
        resource_config={"acl": "public-read", "tags": {"purpose": "public-assets"}},
    )
    assert result is None


def test_flags_publicly_accessible_sensitive_database():
    rule = NetworkExposureRule()
    result = rule.check(
        resource_type="aws_db_instance",
        resource_name="payment_db",
        resource_config={"publicly_accessible": True, "tags": {"data_type": "payment"}},
    )
    assert result is not None
    assert result.rule_id == "RBI-004"
