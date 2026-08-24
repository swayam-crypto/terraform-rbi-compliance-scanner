from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.graph.graph_predicates import GraphPredicates
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.graph_rules.base import GraphRule
from compliance_scanner.rules.base import Finding
from compliance_scanner.scan_context import ScanContext


class PublicDatabaseExposureRule(GraphRule):

    rule_id = "GRAPH-001"

    description = "Detect databases reachable from public entry points."

    regulation_reference = "RBI Cyber Security Framework"

    severity = "critical"

    required_capabilities = frozenset({"public_entry_point"})

    def check_graph(
        self,
        context: ScanContext,
    ) -> list[Finding]:

        predicates = GraphPredicates(
            GraphQuery(
                context.relationship_graph,
            ),
            attack_paths=context.attack_paths,
            blast_radius=context.blast_radius,
        )

        findings: list[Finding] = []

        for resource in context.resources:

            if not catalog.has_capabilities(
                resource,
                self.required_capabilities,
            ):
                continue

            if not predicates.attack_path_contains_capability(
                resource,
                "data_store",
            ):
                continue

            findings.append(
                Finding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    resource_type=resource.resource_type,
                    resource_name=resource.resource_name,
                    message="Public entry point can reach a database.",
                    regulation_reference=self.regulation_reference,
                )
            )

        return findings
