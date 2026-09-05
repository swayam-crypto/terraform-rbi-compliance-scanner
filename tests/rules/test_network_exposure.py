from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.rules.network_exposure import NetworkExposureRule


def test_flags_public_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        attributes={"acl": "public-read", "tags": {"data_type": "customer"}},
        default_attributes={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-004"


def test_does_not_flag_private_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        attributes={"acl": "private", "tags": {"data_type": "customer"}},
        default_attributes={},
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_public_non_sensitive_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="marketing_assets",
        attributes={"acl": "public-read", "tags": {"purpose": "public-assets"}},
        default_attributes={},
    )
    result = rule.check(resource)
    assert result is None


def test_flags_publicly_accessible_sensitive_database():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_db_instance"),
        source=SourceLocation(),
        resource_type="aws_db_instance",
        resource_name="payment_db",
        attributes={"publicly_accessible": True, "tags": {"data_type": "payment"}},
        default_attributes={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-004"


def test_flags_authenticated_read_sensitive_s3_bucket():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        attributes={
            "acl": "authenticated-read",
            "tags": {"data_type": "customer"},
        },
        default_attributes={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"


def test_acl_normalization():
    rule = NetworkExposureRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="customer_records",
        attributes={
            "acl": "  PuBlIc-ReAd  ",
            "tags": {"data_type": "customer"},
        },
        default_attributes={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"


def test_flags_sensitive_bucket_name():
    rule = NetworkExposureRule()

    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        source=SourceLocation(),
        resource_type="aws_s3_bucket",
        resource_name="bucket1",
        attributes={
            "bucket": "customer-pii-backups",
            "acl": "public-read",
        },
        default_attributes={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"


def test_flags_sensitive_database_identifier():
    rule = NetworkExposureRule()

    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_db_instance"),
        source=SourceLocation(),
        resource_type="aws_db_instance",
        resource_name="db1",
        attributes={
            "identifier": "payment-db",
            "publicly_accessible": True,
        },
        default_attributes={},
    )

    result = rule.check(resource)

    assert result is not None
    assert result.rule_id == "RBI-004"
