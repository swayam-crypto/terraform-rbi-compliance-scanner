import json

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.reporting.json_reporter import to_json
from compliance_scanner.rules.encryption import EncryptionAtRestRule


def test_rule_findings_include_framework_neutral_control_metadata():
    finding = EncryptionAtRestRule().check(
        ResolvedResource(
            platform=Platform.TERRAFORM,
            provider=infer_provider("aws_s3_bucket"),
            resource_type="aws_s3_bucket",
            resource_name="unencrypted_bucket",
            attributes={},
            default_attributes={},
            source=SourceLocation(),
        )
    )

    assert finding is not None
    assert finding.rule_id == "RBI-002"  # Legacy suppression/integration contract.
    assert finding.control_id == "CCIP-ENCRYPTION-AT-REST-001"
    assert finding.category == "data_protection"
    assert finding.remediation
    assert {mapping["framework"] for mapping in finding.framework_mappings} == {
        "RBI",
        "DPDP",
        "CIS",
    }


def test_json_report_preserves_control_traceability():
    finding = EncryptionAtRestRule().check(
        ResolvedResource(
            platform=Platform.TERRAFORM,
            provider=infer_provider("aws_s3_bucket"),
            resource_type="aws_s3_bucket",
            resource_name="unencrypted_bucket",
            attributes={},
            default_attributes={},
            source=SourceLocation(),
        )
    )

    report = json.loads(to_json([finding]))

    assert report[0]["control_id"] == "CCIP-ENCRYPTION-AT-REST-001"
    assert report[0]["framework_mappings"][0]["framework"] == "RBI"


def test_capability_rule_ignores_resources_that_are_not_data_stores():
    """A KMS key supports encryption but is not itself an encrypted data store."""
    finding = EncryptionAtRestRule().check(
        ResolvedResource(
            platform=Platform.TERRAFORM,
            provider=infer_provider("aws_kms_key"),
            resource_type="aws_kms_key",
            resource_name="key",
            attributes={},
            default_attributes={},
            source=SourceLocation(),
        )
    )

    assert finding is None
