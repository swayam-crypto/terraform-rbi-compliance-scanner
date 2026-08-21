from compliance_scanner.attack.algorithms.shortest_path import (
    ShortestPathAlgorithm,
)
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


def test_returns_none_when_no_path_exists():

    graph = RelationshipGraph()

    source = make_resource(
        "aws_instance",
        "web",
    )

    target = make_resource(
        "aws_db_instance",
        "database",
    )

    algorithm = ShortestPathAlgorithm(graph)

    assert (
        algorithm.find_path(
            source,
            target,
        )
        is None
    )


def test_finds_direct_path():

    graph = RelationshipGraph()

    source = make_resource(
        "aws_instance",
        "web",
    )

    target = make_resource(
        "aws_subnet",
        "private",
    )

    relationship = Relationship(
        source=source,
        target=target,
        relationship_type=RelationshipType.SUBNET,
    )

    graph.add(relationship)

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        source,
        target,
    )

    assert path is not None

    assert path.source == source

    assert path.target == target

    assert path.relationships == (relationship,)


def test_finds_multi_hop_path():

    graph = RelationshipGraph()

    source = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    target = make_resource(
        "aws_vpc",
        "main",
    )

    relationship_one = Relationship(
        source=source,
        target=subnet,
        relationship_type=RelationshipType.SUBNET,
    )

    relationship_two = Relationship(
        source=subnet,
        target=target,
        relationship_type=RelationshipType.VPC,
    )

    graph.add(relationship_one)

    graph.add(relationship_two)

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        source,
        target,
    )

    assert path is not None

    assert path.relationships == (
        relationship_one,
        relationship_two,
    )


def test_returns_empty_path_when_source_equals_target():

    graph = RelationshipGraph()

    resource = make_resource(
        "aws_instance",
        "web",
    )

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        resource,
        resource,
    )

    assert path is not None

    assert path.source == resource

    assert path.target == resource

    assert path.relationships == ()


def test_avoids_cycles():

    graph = RelationshipGraph()

    resource_a = make_resource(
        "aws_instance",
        "a",
    )

    resource_b = make_resource(
        "aws_subnet",
        "b",
    )

    resource_c = make_resource(
        "aws_vpc",
        "c",
    )

    relationship_ab = Relationship(
        source=resource_a,
        target=resource_b,
        relationship_type=RelationshipType.SUBNET,
    )

    relationship_bc = Relationship(
        source=resource_b,
        target=resource_c,
        relationship_type=RelationshipType.VPC,
    )

    relationship_ca = Relationship(
        source=resource_c,
        target=resource_a,
        relationship_type=RelationshipType.VPC,
    )

    graph.add(relationship_ab)

    graph.add(relationship_bc)

    graph.add(relationship_ca)

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        resource_a,
        resource_c,
    )

    assert path is not None

    assert path.relationships == (
        relationship_ab,
        relationship_bc,
    )


def test_returns_shortest_path():

    graph = RelationshipGraph()

    start = make_resource(
        "aws_instance",
        "start",
    )

    left = make_resource(
        "aws_subnet",
        "left",
    )

    middle = make_resource(
        "aws_security_group",
        "middle",
    )

    end = make_resource(
        "aws_vpc",
        "end",
    )

    direct = Relationship(
        source=start,
        target=end,
        relationship_type=RelationshipType.VPC,
    )

    first = Relationship(
        source=start,
        target=left,
        relationship_type=RelationshipType.SUBNET,
    )

    second = Relationship(
        source=left,
        target=middle,
        relationship_type=RelationshipType.SECURITY_GROUP,
    )

    third = Relationship(
        source=middle,
        target=end,
        relationship_type=RelationshipType.VPC,
    )

    graph.add(first)

    graph.add(second)

    graph.add(third)

    graph.add(direct)

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        start,
        end,
    )

    assert path is not None

    assert path.relationships == (direct,)


def test_returns_none_when_target_is_unreachable_from_connected_graph():

    graph = RelationshipGraph()

    resource_a = make_resource(
        "aws_instance",
        "a",
    )

    resource_b = make_resource(
        "aws_subnet",
        "b",
    )

    resource_c = make_resource(
        "aws_security_group",
        "c",
    )

    resource_d = make_resource(
        "aws_vpc",
        "d",
    )

    graph.add(
        Relationship(
            source=resource_a,
            target=resource_b,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    graph.add(
        Relationship(
            source=resource_c,
            target=resource_d,
            relationship_type=RelationshipType.VPC,
        )
    )

    algorithm = ShortestPathAlgorithm(graph)

    path = algorithm.find_path(
        resource_a,
        resource_d,
    )

    assert path is None
