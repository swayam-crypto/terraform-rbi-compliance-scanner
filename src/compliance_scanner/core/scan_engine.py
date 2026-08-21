"""Provider- and IaC-neutral compliance scan orchestration."""

from collections import defaultdict
from collections.abc import Mapping

from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.graph.graph_builder import GraphBuilder
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.canonical.relationship_resolver import RelationshipResolver
from compliance_scanner.rules.base import Finding
from compliance_scanner.rules.registry import ALL_RULES, GRAPH_RULES
from compliance_scanner.scan_context import ScanContext
from compliance_scanner.attack.engine import AttackPathEngine


def _run_rules_on_resources(resources, file_path, suppressions, suppressed_count):
    for resource in resources:
        for rule in ALL_RULES:
            if not rule.applies_to_resource(resource, catalog):
                continue
            result = rule.check(resource)
            if result is None:
                continue
            suppression = suppressions.get(
                (resource.resource_type, resource.resource_name)
            )
            if suppression and (
                suppression["all"] or rule.rule_id in suppression["rules"]
            ):
                suppressed_count[0] += 1
                continue
            result.file_path = file_path
            yield result


def _run_graph_rules(context: ScanContext):
    for rule in GRAPH_RULES:
        yield from rule.check_graph(context)


def scan_resources(
    resources,
    *,
    suppressed_count: list | None = None,
    suppressions_by_file: Mapping[str, dict] | None = None,
    finding_file_path: str = "",
    include_graph_rules: bool = True,
) -> list[Finding]:
    """Scan already-normalized resources without knowing their source format.

    ``finding_file_path`` retains the plan-scan reporting contract, while
    ``suppressions_by_file`` lets source-specific adapters supply directives.
    """
    if suppressed_count is None:
        suppressed_count = [0]
    suppressions_by_file = suppressions_by_file or {}

    resources = list(resources)
    findings: list[Finding] = []
    resources_by_file = defaultdict(list)
    for resource in resources:
        resources_by_file[resource.source.file_path or finding_file_path].append(
            resource
        )

    for file_path, grouped_resources in resources_by_file.items():
        findings.extend(
            _run_rules_on_resources(
                grouped_resources,
                file_path,
                suppressions_by_file.get(file_path, {}),
                suppressed_count,
            )
        )

    if include_graph_rules:
        index = ResourceIndex(resources)
        relationships = RelationshipResolver(
            catalog,
        ).extract(
            resources,
            index,
        )

        graph = GraphBuilder().build(
            relationships,
        )

        context = ScanContext(
            resources=resources,
            resource_index=index,
            relationship_graph=graph,
        )

        attack_paths = AttackPathEngine(
            context,
        )

        # Perform infrastructure attack-path analysis before executing
        # graph-aware compliance rules.
        context.attack_paths = attack_paths.analyze()

        findings.extend(
            _run_graph_rules(
                context,
            )
        )

    return findings


# Compatibility entry points. Terraform ownership lives in terraform_scan;
# lazy imports keep this generic module independent of Terraform implementation.
def scan_directory(dir_path: str, suppressed_count: list | None = None):
    from .terraform_scan import scan_directory as terraform_scan_directory

    return terraform_scan_directory(dir_path, suppressed_count=suppressed_count)


def scan_plan(plan_path: str, suppressed_count: list | None = None):
    from .terraform_scan import scan_plan as terraform_scan_plan

    return terraform_scan_plan(plan_path, suppressed_count=suppressed_count)


def scan_directory_large(*args, **kwargs):
    from .terraform_scan import scan_directory_large as terraform_scan_directory_large

    return terraform_scan_directory_large(*args, **kwargs)
