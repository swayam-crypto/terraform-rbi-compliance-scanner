from compliance_scanner.engine.relationship.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph

from compliance_scanner.graph.resource_index import ResourceIndex

from compliance_scanner.graph_rules.public_database_exposure import (
    PublicDatabaseExposureRule,
)

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation

from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.runtime.scan_context import ScanContext
from compliance_scanner.canonical.runtime_integration import (
    build_canonical_resources,
)
from compliance_scanner.engine.attack.collection import AttackPathCollection
from compliance_scanner.engine.attack.models import AttackPath
from compliance_scanner.engine.privilege.graph import PrivilegeGraph


def make_resource(
    resource_type: str,
    resource_name: str,
) -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name=resource_name,
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )


def make_context(
    resources,
    relationship_graph,
    attack_paths=None,
    blast_radius=None,
):
    return ScanContext(
        resources=resources,
        canonical_resources=build_canonical_resources(resources),
        resource_index=ResourceIndex(resources),
        relationship_graph=relationship_graph,
        privilege_graph=PrivilegeGraph(),
        attack_paths=attack_paths,
        blast_radius=blast_radius,
    )


def test_public_database_exposure_detected():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    resources = [load_balancer, database]

    attack_paths = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    context = make_context(
        resources=resources, relationship_graph=graph, attack_paths=attack_paths
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check_graph(context)

    assert len(finding) == 1
    assert finding[0].rule_id == "GRAPH-001"


def test_database_not_reachable():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph = RelationshipGraph()

    resources = [load_balancer, database]

    context = make_context(
        resources=resources,
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check_graph(context)

    assert finding == []


def test_non_public_resource_returns_none():

    instance = make_resource(
        "aws_instance",
        "web",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=instance,
            target=database,
            relationship_type=RelationshipType.KMS_KEY,
        )
    )

    resources = [instance, database]

    attack_paths = AttackPathCollection(
        (
            AttackPath(
                source=instance,
                target=database,
                resources=(
                    instance,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    context = make_context(
        resources=resources,
        relationship_graph=graph,
        attack_paths=attack_paths,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check_graph(context)

    assert finding == []


def test_public_resource_without_database_dependency():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=subnet,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    resources = [load_balancer, subnet]

    context = make_context(
        resources=resources,
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check_graph(context)

    assert finding == []
