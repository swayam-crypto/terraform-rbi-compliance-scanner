from compliance_scanner.core.scan_engine import scan_resources
from compliance_scanner.core import terraform_scan
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def make_resource(resource_type: str, attributes: dict, file_path: str = ""):
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name="test",
        attributes=attributes,
        default_attributes={},
        source=SourceLocation(file_path=file_path or None),
    )


def test_scan_resources_is_source_format_agnostic():
    findings = scan_resources(
        [make_resource("aws_db_instance", {"backup_retention_period": 1})],
        include_graph_rules=False,
    )

    assert {finding.rule_id for finding in findings} >= {"RBI-002", "RBI-006", "RBI-009", "RBI-010"}


def test_directory_scan_routes_through_terraform_parser(tmp_path, monkeypatch):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "placeholder" {}')
    expected = [make_resource("aws_db_instance", {"backup_retention_period": 1}, str(tmp_path / "main.tf"))]
    monkeypatch.setattr(terraform_scan.TerraformParser, "parse_directory", lambda _self, _path: expected)

    findings = terraform_scan.scan_directory(str(tmp_path))

    assert any(finding.rule_id == "RBI-006" for finding in findings)


def test_plan_scan_routes_through_terraform_parser_and_preserves_plan_path(tmp_path, monkeypatch):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text("{}")
    expected = [make_resource("aws_db_instance", {"backup_retention_period": 1})]
    monkeypatch.setattr(terraform_scan.TerraformParser, "parse_plan", lambda _self, _path: expected)

    findings = terraform_scan.scan_plan(str(plan_path))

    assert any(finding.rule_id == "RBI-006" and finding.file_path == str(plan_path) for finding in findings)
