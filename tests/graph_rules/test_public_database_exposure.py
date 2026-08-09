from compliance_scanner.graph.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.graph.relationship_graph import RelationshipGraph

from compliance_scanner.graph.resource_index import ResourceIndex

from compliance_scanner.graph_rules.public_database_exposure import (
    PublicDatabaseExposureRule,
)

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation

from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.scan_context import ScanContext


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

    context = ScanContext(
        resources=[load_balancer, database],
        resource_index=ResourceIndex([load_balancer, database]),
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check(
        load_balancer,
        context,
    )

    assert finding is not None
    assert finding.rule_id == "GRAPH-001"


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

    context = ScanContext(
        resources=[load_balancer, database],
        resource_index=ResourceIndex([load_balancer, database]),
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check(
        load_balancer,
        context,
    )

    assert finding is None


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

    context = ScanContext(
        resources=[instance, database],
        resource_index=ResourceIndex([instance, database]),
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check(
        instance,
        context,
    )

    assert finding is None


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

    context = ScanContext(
        resources=[load_balancer, subnet],
        resource_index=ResourceIndex([load_balancer, subnet]),
        relationship_graph=graph,
    )

    rule = PublicDatabaseExposureRule()

    finding = rule.check(
        load_balancer,
        context,
    )

    assert finding is None
