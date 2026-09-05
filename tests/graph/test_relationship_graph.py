from compliance_scanner.engine.relationship.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.graph.graph_builder import GraphBuilder
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def make_resource(resource_type: str, resource_name: str) -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name=resource_name,
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )


def test_builder_returns_empty_graph():
    from compliance_scanner.core import ResourceIndex

    index = ResourceIndex([])

    graph = GraphBuilder().build(index)

    assert len(graph) == 0


def test_graph_adds_relationship():
    from compliance_scanner.engine.relationship.relationship_graph import (
        RelationshipGraph,
    )

    bucket = make_resource("aws_s3_bucket", "logs")
    policy = make_resource("aws_s3_bucket_policy", "logs_policy")

    relationship = Relationship(
        source=bucket,
        target=policy,
        relationship_type=RelationshipType.OBJECT_STORAGE,
    )

    graph = RelationshipGraph()

    graph.add(relationship)

    assert graph.outgoing(bucket) == (relationship,)
    assert graph.incoming(policy) == (relationship,)


def test_unrelated_resource_returns_empty():
    from compliance_scanner.engine.relationship.relationship_graph import (
        RelationshipGraph,
    )

    bucket = make_resource("aws_s3_bucket", "logs")

    graph = RelationshipGraph()

    assert graph.outgoing(bucket) == ()
    assert graph.incoming(bucket) == ()
