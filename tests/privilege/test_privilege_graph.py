from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.engine.privilege.privilege_relationship import (
    PrivilegeRelationship,
)
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


def test_add_relationship():

    source = make_resource(
        "aws_iam_role",
        "role",
    )

    target = make_resource(
        "aws_instance",
        "instance",
    )

    relationship = PrivilegeRelationship(
        source=source,
        target=target,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert len(graph) == 1


def test_outgoing_relationships():

    source = make_resource(
        "aws_iam_role",
        "role",
    )

    target = make_resource(
        "aws_instance",
        "instance",
    )

    relationship = PrivilegeRelationship(
        source=source,
        target=target,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert graph.outgoing(
        source,
    ) == (relationship,)


def test_incoming_relationships():

    source = make_resource(
        "aws_iam_role",
        "role",
    )

    target = make_resource(
        "aws_instance",
        "instance",
    )

    relationship = PrivilegeRelationship(
        source=source,
        target=target,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert graph.incoming(
        target,
    ) == (relationship,)


def test_has_relationship():

    source = make_resource(
        "aws_iam_role",
        "role",
    )

    target = make_resource(
        "aws_instance",
        "instance",
    )

    relationship = PrivilegeRelationship(
        source=source,
        target=target,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert graph.has_relationship(
        source,
        target,
    )


def test_neighbors():

    source = make_resource(
        "aws_iam_role",
        "role",
    )

    target = make_resource(
        "aws_instance",
        "instance",
    )

    relationship = PrivilegeRelationship(
        source=source,
        target=target,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert graph.neighbors(
        source,
    ) == (target,)
