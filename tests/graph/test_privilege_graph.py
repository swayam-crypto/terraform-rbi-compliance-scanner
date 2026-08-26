from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.graph.privilege_graph import PrivilegeGraph
from compliance_scanner.graph.privilege_relationship import (
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


def test_graph_adds_relationship():

    role = make_resource(
        "aws_iam_role",
        "application",
    )

    policy = make_resource(
        "aws_iam_policy",
        "administrator",
    )

    relationship = PrivilegeRelationship(
        source=role,
        target=policy,
        relationship_type=PrivilegeRelationshipType.GRANTS,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    assert graph.outgoing(role) == (relationship,)

    assert graph.incoming(policy) == (relationship,)


def test_unrelated_resource_returns_empty():

    role = make_resource(
        "aws_iam_role",
        "application",
    )

    graph = PrivilegeGraph()

    assert graph.outgoing(role) == ()

    assert graph.incoming(role) == ()


def test_duplicate_relationship_not_added():

    role = make_resource(
        "aws_iam_role",
        "application",
    )

    policy = make_resource(
        "aws_iam_policy",
        "administrator",
    )

    relationship = PrivilegeRelationship(
        source=role,
        target=policy,
        relationship_type=PrivilegeRelationshipType.GRANTS,
    )

    graph = PrivilegeGraph()

    graph.add(
        relationship,
    )

    graph.add(
        relationship,
    )

    assert len(graph) == 1
