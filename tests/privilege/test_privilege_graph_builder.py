from compliance_scanner.engine.privilege.graph_builder import (
    PrivilegeGraphBuilder,
)
from compliance_scanner.engine.privilege.privilege_relationship import (
    PrivilegeRelationship,
)
from compliance_scanner.graph.resource_index import ResourceIndex

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.engine.privilege.graph import PrivilegeGraph


def test_builder_returns_graph():

    builder = PrivilegeGraphBuilder()

    graph = builder.build(
        ResourceIndex([]),
    )

    assert isinstance(
        graph,
        PrivilegeGraph,
    )


def test_builder_returns_empty_graph():

    builder = PrivilegeGraphBuilder()

    graph = builder.build(
        ResourceIndex([]),
    )

    assert (
        len(
            graph,
        )
        == 0
    )


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


class FakeResolver:

    def __init__(
        self,
        relationships: list[PrivilegeRelationship],
    ):
        self.relationships = relationships
        self.calls = 0

    def resolve(
        self,
        resource,
        resource_index,
    ):
        self.calls += 1

        if self.calls == 1:
            return self.relationships

        return []


def test_build_empty_graph():

    resolver = FakeResolver([])

    builder = PrivilegeGraphBuilder(
        resolver,
    )

    graph = builder.build(
        ResourceIndex([]),
    )

    assert len(graph) == 0


def test_build_single_relationship():

    role = make_resource(
        "aws_iam_role",
        "web",
    )

    instance = make_resource(
        "aws_instance",
        "frontend",
    )

    relationship = PrivilegeRelationship(
        source=instance,
        target=role,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    resolver = FakeResolver(
        [
            relationship,
        ]
    )

    builder = PrivilegeGraphBuilder(
        resolver,
    )

    graph = builder.build(
        ResourceIndex(
            [
                instance,
                role,
            ]
        )
    )

    assert len(graph) == 1


def test_build_multiple_relationships():

    role = make_resource(
        "aws_iam_role",
        "web",
    )

    policy = make_resource(
        "aws_iam_policy",
        "readonly",
    )

    relationship1 = PrivilegeRelationship(
        source=make_resource(
            "aws_instance",
            "frontend",
        ),
        target=role,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    relationship2 = PrivilegeRelationship(
        source=role,
        target=policy,
        relationship_type=PrivilegeRelationshipType.IDENTITY,
    )

    resolver = FakeResolver(
        [
            relationship1,
            relationship2,
        ]
    )

    builder = PrivilegeGraphBuilder(
        resolver,
    )

    graph = builder.build(
        ResourceIndex(
            [
                relationship1.source,
                role,
                policy,
            ]
        )
    )

    assert len(graph) == 2


def test_builder_calls_resolver_for_each_resource():

    instance = make_resource(
        "aws_instance",
        "frontend",
    )

    role = make_resource(
        "aws_iam_role",
        "web",
    )

    resolver = FakeResolver([])

    builder = PrivilegeGraphBuilder(
        resolver,
    )

    builder.build(
        ResourceIndex(
            [
                instance,
                role,
            ]
        )
    )

    assert resolver.calls == 2
