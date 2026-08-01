from compliance_scanner.graph.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.graph.traversal import GraphTraversal

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


def test_reachable_from_single_neighbor():
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

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(instance)

    assert reachable == (subnet,)


def test_reachable_from_chain():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    vpc = make_resource(
        "aws_vpc",
        "main",
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
            source=subnet,
            target=vpc,
            relationship_type=RelationshipType.USES_VPC,
        )
    )

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(instance)

    assert reachable == (
        subnet,
        vpc,
    )


def test_reachable_from_branch():

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

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(instance)

    assert set(reachable) == {
        subnet,
        security_group,
    }


def test_reachable_from_cycle():

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

    graph.add(
        Relationship(
            source=resource_a,
            target=resource_b,
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    graph.add(
        Relationship(
            source=resource_b,
            target=resource_c,
            relationship_type=RelationshipType.USES_VPC,
        )
    )

    graph.add(
        Relationship(
            source=resource_c,
            target=resource_a,
            relationship_type=RelationshipType.USES_VPC,
        )
    )

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(resource_a)

    assert set(reachable) == {
        resource_b,
        resource_c,
    }


def test_reachable_from_disconnected_graph():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    orphan = make_resource(
        "aws_vpc",
        "unused",
    )

    graph.add(
        Relationship(
            source=instance,
            target=subnet,
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(instance)

    assert subnet in reachable

    assert orphan not in reachable


def test_reachable_from_diamond_graph():

    graph = RelationshipGraph()

    start = make_resource(
        "aws_instance",
        "start",
    )

    left = make_resource(
        "aws_subnet",
        "left",
    )

    right = make_resource(
        "aws_security_group",
        "right",
    )

    end = make_resource(
        "aws_vpc",
        "end",
    )

    graph.add(
        Relationship(
            source=start,
            target=left,
            relationship_type=RelationshipType.USES_SUBNET,
        )
    )

    graph.add(
        Relationship(
            source=start,
            target=right,
            relationship_type=RelationshipType.ATTACHED_TO_SECURITY_GROUP,
        )
    )

    graph.add(
        Relationship(
            source=left,
            target=end,
            relationship_type=RelationshipType.USES_VPC,
        )
    )

    graph.add(
        Relationship(
            source=right,
            target=end,
            relationship_type=RelationshipType.USES_VPC,
        )
    )

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(start)

    assert set(reachable) == {
        left,
        right,
        end,
    }


def test_reachable_from_empty_graph():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    traversal = GraphTraversal(graph)

    reachable = traversal.reachable_from(instance)

    assert reachable == ()
