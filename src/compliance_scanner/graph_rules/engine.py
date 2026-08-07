from compliance_scanner.graph_rules import GRAPH_RULES
from compliance_scanner.scan_context import ScanContext
from compliance_scanner.rules.base import Finding


class GraphRuleEngine:
    """
    Executes every registered graph rule.
    """

    def execute(
        self,
        context: ScanContext,
    ) -> list[Finding]:

        findings: list[Finding] = []

        for rule in GRAPH_RULES:
            findings.extend(rule.check_graph(context))

        return findings
