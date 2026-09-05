from compliance_scanner.engine.relationship.relationship import Relationship
from compliance_scanner.graph.relationship_graph import RelationshipGraph
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.catalog.relationship_types import RelationshipType


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


def make_relationship(
    source: ResolvedResource,
    target: ResolvedResource,
    relationship_type: RelationshipType = RelationshipType.SUBNET,
) -> Relationship:
    return Relationship(
        source=source,
        target=target,
        relationship_type=relationship_type,
    )


def test_add_relationship():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    relationship = make_relationship(
        instance,
        subnet,
    )

    graph.add_relationship(
        relationship,
    )

    assert graph.edge_count() == 1


def test_outgoing_relationships():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    relationship = make_relationship(
        instance,
        subnet,
    )

    graph.add_relationship(
        relationship,
    )

    assert graph.outgoing(
        instance,
    ) == (relationship,)


def test_incoming_relationships():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    relationship = make_relationship(
        instance,
        subnet,
    )

    graph.add_relationship(
        relationship,
    )

    assert graph.incoming(
        subnet,
    ) == (relationship,)


def test_neighbors():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    graph.add_relationship(
        make_relationship(
            instance,
            subnet,
        )
    )

    assert graph.neighbors(
        instance,
    ) == (subnet,)


def test_has_edge():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    graph.add_relationship(
        make_relationship(
            instance,
            subnet,
        )
    )

    assert graph.has_edge(
        instance,
        subnet,
    )

    assert not graph.has_edge(
        subnet,
        instance,
    )


def test_edge_count():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    sg = make_resource(
        "aws_security_group",
        "web",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    graph.add_relationship(
        make_relationship(
            instance,
            subnet,
        )
    )

    graph.add_relationship(
        make_relationship(
            instance,
            sg,
            RelationshipType.SECURITY_GROUP,
        )
    )

    assert graph.edge_count() == 2


def test_node_count():

    graph = RelationshipGraph()

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    sg = make_resource(
        "aws_security_group",
        "web",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    graph.add_relationship(
        make_relationship(
            instance,
            subnet,
        )
    )

    graph.add_relationship(
        make_relationship(
            instance,
            sg,
            RelationshipType.SECURITY_GROUP,
        )
    )

    assert graph.node_count() == 3


def test_empty_graph():

    graph = RelationshipGraph()

    assert graph.edge_count() == 0
    assert graph.node_count() == 0
    assert tuple(graph.relationships()) == ()


def test_multiple_outgoing_relationships():

    graph = RelationshipGraph()

    instance = make_resource(
        "aws_instance",
        "web",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    sg = make_resource(
        "aws_security_group",
        "web",
    )

    graph.add_relationship(
        make_relationship(
            instance,
            subnet,
        )
    )

    graph.add_relationship(
        make_relationship(
            instance,
            sg,
            RelationshipType.SECURITY_GROUP,
        )
    )

    assert len(graph.outgoing(instance)) == 2
