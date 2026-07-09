from compliance_scanner.rules.encryption import EncryptionAtRestRule


def test_flags_s3_bucket_without_encryption():
    rule = EncryptionAtRestRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="unencrypted_bucket",
        resource_config={},
    )
    assert result is not None
    assert result.rule_id == "RBI-002"


def test_does_not_flag_s3_bucket_with_encryption():
    rule = EncryptionAtRestRule()
    result = rule.check(
        resource_type="aws_s3_bucket",
        resource_name="encrypted_bucket",
        resource_config={
            "server_side_encryption_configuration": {
                "rule": {"apply_server_side_encryption_by_default": {"sse_algorithm": "AES256"}}
            }
        },
    )
    assert result is None


def test_flags_db_instance_without_encryption():
    rule = EncryptionAtRestRule()
    result = rule.check(
        resource_type="aws_db_instance",
        resource_name="unencrypted_db",
        resource_config={"storage_encrypted": False},
    )
    assert result is not None


def test_does_not_flag_db_instance_with_encryption():
    rule = EncryptionAtRestRule()
    result = rule.check(
        resource_type="aws_db_instance",
        resource_name="encrypted_db",
        resource_config={"storage_encrypted": True},
    )
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = EncryptionAtRestRule()
    result = rule.check(
        resource_type="aws_lambda_function",
        resource_name="some_function",
        resource_config={},
    )
    assert result is None
