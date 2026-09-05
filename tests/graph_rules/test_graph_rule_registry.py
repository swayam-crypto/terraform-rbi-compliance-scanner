from compliance_scanner.core import scan_directory
from compliance_scanner.core import scan_engine
from compliance_scanner.graph_rules import GRAPH_RULES as experimental_graph_rules
from compliance_scanner.rules import registry as production_registry


class _GraphRuleProbe:
    def __init__(self):
        self.calls = 0

    def check_graph(self, context):
        self.calls += 1
        return []


def _terraform_fixture(tmp_path):
    path = tmp_path / "main.tf"
    path.write_text('resource "aws_s3_bucket" "bucket" {}')
    return path


def test_directory_scan_uses_production_graph_rule_registry(tmp_path):
    _terraform_fixture(tmp_path)
    probe = _GraphRuleProbe()

    # The scan engine intentionally holds the production registry object.
    assert scan_engine.GRAPH_RULES is production_registry.GRAPH_RULES
    production_registry.GRAPH_RULES.append(probe)
    try:
        scan_directory(str(tmp_path))
    finally:
        production_registry.GRAPH_RULES.remove(probe)

    assert probe.calls == 1


def test_directory_scan_does_not_invoke_experimental_graph_rule_registry(tmp_path):
    _terraform_fixture(tmp_path)
    probe = _GraphRuleProbe()

    experimental_graph_rules.append(probe)
    try:
        scan_directory(str(tmp_path))
    finally:
        experimental_graph_rules.remove(probe)

    assert probe.calls == 0
