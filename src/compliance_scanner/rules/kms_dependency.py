"""
Graph-aware rule that validates KMS relationships.

Currently this rule only demonstrates graph traversal.
More compliance checks will be added in later versions.
"""

from compliance_scanner.rules.graph_base import GraphRule
from compliance_scanner.rules.base import Finding
from compliance_scanner.graph.relationship import RelationshipType


class KMSDependencyRule(GraphRule):

    rule_id = "GRAPH-001"

    description = "Validate KMS dependencies."

    regulation_reference = "RBI Cybersecurity Framework"

    severity = "medium"

    applies_to = []

    def check_graph(
        self,
        context,
    ) -> list[Finding]:

        findings: list[Finding] = []

        for resource in context.resources:

            if resource.resource_type != "aws_s3_bucket":
                continue

            kms_relationships = context.relationship_graph.outgoing_by_type(
                resource,
                RelationshipType.KMS_KEY,
            )

            #
            # We'll implement the actual validation
            # in the next commit.
            #

            _ = kms_relationships

        return findings
