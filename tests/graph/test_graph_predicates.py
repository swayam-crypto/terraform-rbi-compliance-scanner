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


def test_depends_on_type():

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

    assert predicates.depends_on_type(
        instance,
        "aws_kms_key",
    )

    assert not predicates.depends_on_type(
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


def test_has_capability():

    graph = RelationshipGraph()

    predicates = GraphPredicates(GraphQuery(graph))

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    assert predicates.has_capability(
        load_balancer,
        "public_entry_point",
    )

    assert not predicates.has_capability(
        instance,
        "public_entry_point",
    )


def test_has_capabilities():

    graph = RelationshipGraph()

    predicates = GraphPredicates(GraphQuery(graph))

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    assert predicates.has_capabilities(
        database,
        frozenset({"data_store"}),
    )

    assert not predicates.has_capabilities(
        instance,
        frozenset({"data_store"}),
    )


def test_depends_on_capability():

    graph = RelationshipGraph()

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.depends_on_capability(
        load_balancer,
        "data_store",
    )

    assert not predicates.depends_on_capability(
        database,
        "data_store",
    )


def test_depends_on_data_store():

    graph = RelationshipGraph()

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.depends_on_data_store(
        load_balancer,
    )

    assert not predicates.depends_on_data_store(
        database,
    )


def test_depends_on_compute():

    graph = RelationshipGraph()

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    graph.add(
        Relationship(
            source=load_balancer,
            target=instance,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    predicates = GraphPredicates(GraphQuery(graph))

    assert predicates.depends_on_compute(
        load_balancer,
    )


def test_depends_on_network():

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

    assert predicates.depends_on_network(
        instance,
    )
