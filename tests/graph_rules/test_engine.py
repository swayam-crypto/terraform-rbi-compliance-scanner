import pytest

from compliance_scanner.graph_rules.engine import GraphRuleEngine
from compliance_scanner.rules.base import Finding


class FakeRule:
    def check_graph(self, context):
        return []


class FakeRuleOne:
    def check_graph(self, context):
        return [
            Finding(
                rule_id="RULE_1",
                severity="HIGH",
                resource_type="aws_instance",
                resource_name="web",
                message="Rule One",
                regulation_reference="TEST",
            )
        ]


class FakeRuleTwo:
    def check_graph(self, context):
        return [
            Finding(
                rule_id="RULE_2",
                severity="MEDIUM",
                resource_type="aws_s3_bucket",
                resource_name="bucket",
                message="Rule Two",
                regulation_reference="TEST",
            )
        ]


def test_execute_returns_empty_when_no_findings(monkeypatch):

    monkeypatch.setattr(
        "compliance_scanner.graph_rules.engine.GRAPH_RULES",
        [
            FakeRule(),
        ],
    )

    engine = GraphRuleEngine()

    findings = engine.execute(None)

    assert findings == []


def test_execute_returns_single_finding(monkeypatch):

    monkeypatch.setattr(
        "compliance_scanner.graph_rules.engine.GRAPH_RULES",
        [
            FakeRuleOne(),
        ],
    )

    engine = GraphRuleEngine()

    findings = engine.execute(None)

    assert len(findings) == 1

    assert findings[0].rule_id == "RULE_1"


def test_execute_returns_multiple_findings(monkeypatch):

    monkeypatch.setattr(
        "compliance_scanner.graph_rules.engine.GRAPH_RULES",
        [
            FakeRuleOne(),
            FakeRuleTwo(),
        ],
    )

    engine = GraphRuleEngine()

    findings = engine.execute(None)

    assert len(findings) == 2

    assert findings[0].rule_id == "RULE_1"

    assert findings[1].rule_id == "RULE_2"
