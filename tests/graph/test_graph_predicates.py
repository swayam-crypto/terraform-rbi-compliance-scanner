from compliance_scanner.graph.graph_predicates import GraphPredicates
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.graph.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.graph.relationship_graph import RelationshipGraph

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


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


def test_reachable_resources():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    graph.add(
        Relationship(
            source=instance,
            target=subnet,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.reachable_resources(
        instance,
    ) == (subnet,)


def test_is_reachable():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    graph.add(
        Relationship(
            source=instance,
            target=subnet,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.is_reachable(
        instance,
        subnet,
    )


def test_depends_on():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    kms = make_resource(
        "aws_kms_key",
        "main",
    )

    graph.add(
        Relationship(
            source=instance,
            target=kms,
            relationship_type=RelationshipType.KMS_KEY,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.depends_on(
        instance,
        "aws_kms_key",
    )

    assert not predicates.depends_on(
        instance,
        "aws_vpc",
    )


def test_is_database():

    graph = RelationshipGraph()

    query = GraphQuery(graph)

    predicates = GraphPredicates(query)

    database = make_resource(
        "aws_db_instance",
        "main",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    assert predicates.is_database(database)

    assert not predicates.is_database(instance)


def test_is_public_entry_point():

    graph = RelationshipGraph()

    query = GraphQuery(graph)

    predicates = GraphPredicates(query)

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    assert predicates.is_public_entry_point(load_balancer)

    assert not predicates.is_public_entry_point(instance)
