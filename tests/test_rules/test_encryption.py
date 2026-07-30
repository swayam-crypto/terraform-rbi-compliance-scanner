from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.rules.encryption import EncryptionAtRestRule


def test_flags_s3_bucket_without_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        resource_type="aws_s3_bucket",
        resource_name="unencrypted_bucket",
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is not None
    assert result.rule_id == "RBI-002"


def test_does_not_flag_s3_bucket_with_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_s3_bucket"),
        resource_type="aws_s3_bucket",
        resource_name="encrypted_bucket",
        attributes={
            "server_side_encryption_configuration": {
                "rule": {
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256"
                    }
                }
            }
        },
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_flags_db_instance_without_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_db_instance"),
        resource_type="aws_db_instance",
        resource_name="unencrypted_db",
        attributes={"storage_encrypted": False},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is not None


def test_does_not_flag_db_instance_with_encryption():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_db_instance"),
        resource_type="aws_db_instance",
        resource_name="encrypted_db",
        attributes={"storage_encrypted": True},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None


def test_ignores_unrelated_resource_types():
    rule = EncryptionAtRestRule()
    resource = ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider("aws_lambda_function"),
        resource_type="aws_lambda_function",
        resource_name="some_function",
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )
    result = rule.check(resource)
    assert result is None
