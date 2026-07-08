from compliance_scanner.rules.data_localization import DataLocalizationRule


def test_flags_sensitive_data_outside_india():
    rule = DataLocalizationRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="customer_transactions",
        resource_config={
            "region": "us-east-1",
            "tags": {"data_type": "financial"},
        },
    )
    assert result is not None
    assert result.rule_id == "RBI-001"
    assert result.severity == "critical"


def test_does_not_flag_sensitive_data_in_india():
    rule = DataLocalizationRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="kyc_documents",
        resource_config={
            "region": "ap-south-1",
            "tags": {"data_type": "kyc"},
        },
    )
    assert result is None


def test_does_not_flag_non_sensitive_resource():
    rule = DataLocalizationRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="static_website_assets",
        resource_config={
            "region": "us-east-1",
            "tags": {"purpose": "public-assets"},
        },
    )
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = DataLocalizationRule()
    result = rule.check(
        resource_type="aws_lambda_function",
        resource_name="some_function",
        resource_config={"region": "us-east-1"},
    )
    assert result is None
