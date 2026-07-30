from compliance_scanner.engine.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.engine.relationship_builder import RelationshipBuilder
from compliance_scanner.parser.terraform_parser import ResolvedResource


def make_resource(resource_type: str, resource_name: str) -> ResolvedResource:
    return ResolvedResource(
        resource_type=resource_type,
        resource_name=resource_name,
        config={},
        provider_defaults={},
    )


def test_builder_returns_empty_graph():
    from compliance_scanner.engine import ResourceIndex

    index = ResourceIndex([])

    graph = RelationshipBuilder().build(index)

    assert len(graph) == 0


def test_graph_adds_relationship():
    from compliance_scanner.engine.relationship_graph import ResourceGraph

    bucket = make_resource("aws_s3_bucket", "logs")
    policy = make_resource("aws_s3_bucket_policy", "logs_policy")

    relationship = Relationship(
        source=bucket,
        target=policy,
        relationship_type=RelationshipType.BUCKET_POLICY,
    )

    graph = ResourceGraph()

    graph.add(relationship)

    assert graph.outgoing(bucket) == (relationship,)
    assert graph.incoming(policy) == (relationship,)


def test_unrelated_resource_returns_empty():
    from compliance_scanner.engine.relationship_graph import ResourceGraph

    bucket = make_resource("aws_s3_bucket", "logs")

    graph = ResourceGraph()

    assert graph.outgoing(bucket) == ()
    assert graph.incoming(bucket) == ()
