from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.reporting import filter_by_framework, summarize
from compliance_scanner.rules.registry import ALL_RULES


def resource(resource_type: str, attributes: dict) -> ResolvedResource:
    return ResolvedResource(Platform.TERRAFORM, infer_provider(resource_type), resource_type, "test", attributes, {}, SourceLocation())


def test_v080_registers_twenty_controls_with_stable_ids():
    ids = {rule.rule_id for rule in ALL_RULES}
    assert len(ALL_RULES) >= 20
    assert {f"RBI-{number:03d}" for number in range(1, 21)}.issubset(ids)


def test_baseline_backup_rule_uses_catalog_attribute():
    rule = next(rule for rule in ALL_RULES if rule.rule_id == "RBI-006")
    assert rule.check(resource("aws_db_instance", {"backup_retention_period": 1})) is not None
    assert rule.check(resource("aws_db_instance", {"backup_retention_period": 7})) is None


def test_baseline_network_rules_detect_public_administration_ports():
    ssh_rule = next(rule for rule in ALL_RULES if rule.rule_id == "RBI-018")
    finding = ssh_rule.check(resource("aws_security_group", {"ingress": [{"from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]}]}))
    assert finding is not None
    assert finding.control_id == "CCIP-SSH-RESTRICTION-001"


def test_framework_reporting_filters_and_summarizes_mappings():
    rule = next(rule for rule in ALL_RULES if rule.rule_id == "RBI-006")
    finding = rule.check(resource("aws_db_instance", {"backup_retention_period": 1}))
    assert len(filter_by_framework([finding], "CIS")) == 1
    assert summarize([finding])["by_framework"]["RBI"] == 1
