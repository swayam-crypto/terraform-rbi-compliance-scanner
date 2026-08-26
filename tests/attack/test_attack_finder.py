from compliance_scanner.engine.attack.collection import AttackPathCollection
from compliance_scanner.engine.attack.finder import AttackPathFinder
from compliance_scanner.engine.relationship.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph

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


def test_returns_empty_collection_when_no_path_exists():

    graph = RelationshipGraph()

    source = make_resource(
        "aws_instance",
        "web",
    )

    target = make_resource(
        "aws_db_instance",
        "database",
    )

    finder = AttackPathFinder(graph)

    collection = finder.find_paths(
        source,
        target,
    )

    assert isinstance(
        collection,
        AttackPathCollection,
    )

    assert len(collection) == 0


def test_returns_single_attack_path():

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

    finder = AttackPathFinder(graph)

    collection = finder.find_paths(
        source,
        target,
    )

    assert len(collection) == 1

    path = collection[0]

    assert path.source == source

    assert path.target == target

    assert path.relationships == (relationship,)


def test_returns_attack_path_collection():

    graph = RelationshipGraph()

    source = make_resource(
        "aws_instance",
        "web",
    )

    target = make_resource(
        "aws_subnet",
        "private",
    )

    graph.add(
        Relationship(
            source=source,
            target=target,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    finder = AttackPathFinder(graph)

    collection = finder.find_paths(
        source,
        target,
    )

    assert isinstance(
        collection,
        AttackPathCollection,
    )


def test_preserves_relationship_order():

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

    finder = AttackPathFinder(graph)

    collection = finder.find_paths(
        source,
        target,
    )

    path = next(iter(collection))

    assert path.relationships == (
        relationship_one,
        relationship_two,
    )
