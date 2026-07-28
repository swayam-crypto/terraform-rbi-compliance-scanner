from compliance_scanner.parser.terraform_parser import ResolvedResource
from compliance_scanner.rules.data_localization import DataLocalizationRule


def test_flags_sensitive_data_outside_india():
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_transactions",
        config={
            "region": "us-east-1",
            "tags": {"data_type": "financial"},
        },
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-001"
    assert result.severity == "critical"


def test_does_not_flag_sensitive_data_in_india():
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="kyc_documents",
        config={
            "region": "ap-south-1",
            "tags": {"data_type": "kyc"},
        },
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_non_sensitive_resource():
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="static_website_assets",
        config={
            "region": "us-east-1",
            "tags": {"purpose": "public-assets"},
        },
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_lambda_function",
        resource_name="some_function",
        config={"region": "us-east-1"},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_flags_when_region_in_provider_not_resource():
    """Provider sets us-east-1, resource omits region — should still flag."""
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_transactions",
        config={
            "tags": {"data_type": "financial"},
        },
        provider_defaults={"region": "us-east-1"},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-001"


def test_passes_when_provider_region_is_india():
    """Provider sets ap-south-1, resource omits region — should pass."""
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_transactions",
        config={
            "tags": {"data_type": "financial"},
        },
        provider_defaults={"region": "ap-south-1"},
    )
    result = rule.check(resource)
    assert result is None


def test_resource_region_overrides_provider():
    """Resource-level region should win over provider default."""
    rule = DataLocalizationRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_transactions",
        config={
            "region": "us-east-1",
            "tags": {"data_type": "financial"},
        },
        provider_defaults={"region": "ap-south-1"},
    )
    result = rule.check(resource)
    assert result is not None
    assert "us-east-1" in result.message