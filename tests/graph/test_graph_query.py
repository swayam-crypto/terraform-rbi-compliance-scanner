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
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    query = GraphQuery(graph)

    reachable = query.reachable_resources(instance)

    assert reachable == (subnet,)


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
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    query = GraphQuery(graph)

    assert query.is_reachable(
        instance,
        subnet,
    )


def test_resources_of_type():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    security_group = make_resource(
        "aws_security_group",
        "web",
    )

    graph.add(
        Relationship(
            source=instance,
            target=subnet,
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    graph.add(
        Relationship(
            source=instance,
            target=security_group,
            relationship_type=RelationshipType.ATTACHED_TO_SECURITY_GROUP,
        )
    )

    query = GraphQuery(graph)

    resources = query.resources_of_type(
        instance,
        "aws_subnet",
    )

    assert resources == (subnet,)


def test_has_dependency():

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
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    query = GraphQuery(graph)

    assert query.has_dependency(
        instance,
        "aws_subnet",
    )

    assert not query.has_dependency(
        instance,
        "aws_vpc",
    )
