from compliance_scanner.parser.terraform_parser import ResolvedResource
from compliance_scanner.rules.network_exposure import NetworkExposureRule


def test_flags_public_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        config={"acl": "public-read", "tags": {"data_type": "customer"}},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-004"


def test_does_not_flag_private_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        config={"acl": "private", "tags": {"data_type": "customer"}},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_public_non_sensitive_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="marketing_assets",
        config={"acl": "public-read", "tags": {"purpose": "public-assets"}},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_flags_publicly_accessible_sensitive_database():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_db_instance",
        resource_name="payment_db",
        config={"publicly_accessible": True, "tags": {"data_type": "payment"}},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-004"


def test_flags_authenticated_read_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        config={
            "acl": "authenticated-read",
            "tags": {"data_type": "customer"},
        },
        provider_defaults={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"


def test_acl_normalization():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        config={
            "acl": "  PuBlIc-ReAd  ",
            "tags": {"data_type": "customer"},
        },
        provider_defaults={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"
