from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.rules.audit_logging import AuditLogRetentionRule


def test_flags_retention_below_180_days():
    rule = AuditLogRetentionRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_cloudwatch_log_group"),
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        attributes={"retention_in_days": 30},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-003"


def test_does_not_flag_retention_at_180_days():
    rule = AuditLogRetentionRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_cloudwatch_log_group"),
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        attributes={"retention_in_days": 180},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_retention_above_180_days():
    rule = AuditLogRetentionRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_cloudwatch_log_group"),
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        attributes={"retention_in_days": 365},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_does_not_flag_unset_retention():
    """Unset retention defaults to AWS 'Never Expire', which satisfies >= 180 days."""
    rule = AuditLogRetentionRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_cloudwatch_log_group"),
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = AuditLogRetentionRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        resource_type="aws_s3_bucket",
        resource_name="some_bucket",
        attributes={"retention_in_days": 1},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None
