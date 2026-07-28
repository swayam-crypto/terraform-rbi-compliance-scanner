from compliance_scanner.parser.terraform_parser import ResolvedResource
from compliance_scanner.rules.encryption import EncryptionAtRestRule


def test_flags_s3_bucket_without_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="unencrypted_bucket",
        config={},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-002"


def test_does_not_flag_s3_bucket_with_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        resource_type="aws_s3_bucket",
        resource_name="encrypted_bucket",
        config={
            "server_side_encryption_configuration": {
                "rule": {"apply_server_side_encryption_by_default": {"sse_algorithm": "AES256"}}
            }
        },
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_flags_db_instance_without_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        resource_type="aws_db_instance",
        resource_name="unencrypted_db",
        config={"storage_encrypted": False},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is not None


def test_does_not_flag_db_instance_with_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        resource_type="aws_db_instance",
        resource_name="encrypted_db",
        config={"storage_encrypted": True},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        resource_type="aws_lambda_function",
        resource_name="some_function",
        config={},
        provider_defaults={},
    )
    result = rule.check(resource)
    assert result is None