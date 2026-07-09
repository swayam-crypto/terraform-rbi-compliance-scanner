from compliance_scanner.rules.audit_logging import AuditLogRetentionRule


def test_flags_retention_below_180_days():
    rule = AuditLogRetentionRule()
    result = rule.check(
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        resource_config={"retention_in_days": 30},
    )
    assert result is not None
    assert result.rule_id == "RBI-003"


def test_does_not_flag_retention_at_180_days():
    rule = AuditLogRetentionRule()
    result = rule.check(
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        resource_config={"retention_in_days": 180},
    )
    assert result is None


def test_does_not_flag_retention_above_180_days():
    rule = AuditLogRetentionRule()
    result = rule.check(
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        resource_config={"retention_in_days": 365},
    )
    assert result is None


def test_does_not_flag_unset_retention():
    """Unset retention defaults to AWS 'Never Expire', which satisfies >= 180 days."""
    rule = AuditLogRetentionRule()
    result = rule.check(
        resource_type="aws_cloudwatch_log_group",
        resource_name="app_logs",
        resource_config={},
    )
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = AuditLogRetentionRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="some_bucket",
        resource_config={"retention_in_days": 1},
    )
    assert result is None
