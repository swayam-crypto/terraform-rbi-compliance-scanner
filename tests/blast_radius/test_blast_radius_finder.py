from compliance_scanner.blast_radius.finder import BlastRadiusFinder
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


def test_blast_radius():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    finder = BlastRadiusFinder(
        GraphQuery(graph),
    )

    blast_radius = finder.blast_radius(
        load_balancer,
    )

    assert blast_radius.source == load_balancer

    assert blast_radius.affected_resources == (database,)


def test_analyze():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    finder = BlastRadiusFinder(
        GraphQuery(graph),
    )

    collection = finder.analyze(
        [
            load_balancer,
            database,
        ]
    )

    assert len(collection) == 2

    assert (
        collection.for_resource(
            load_balancer,
        )
        is not None
    )


def test_multi_hop_blast_radius():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    instance = make_resource(
        "aws_instance",
        "web",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    kms = make_resource(
        "aws_kms_key",
        "main",
    )

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=instance,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    graph.add(
        Relationship(
            source=instance,
            target=database,
            relationship_type=RelationshipType.SUBNET,
        )
    )

    graph.add(
        Relationship(
            source=database,
            target=kms,
            relationship_type=RelationshipType.KMS_KEY,
        )
    )

    finder = BlastRadiusFinder(
        GraphQuery(graph),
    )

    #
    # Load Balancer
    #

    blast_radius = finder.blast_radius(
        load_balancer,
    )

    assert blast_radius.affected_resources == (
        instance,
        database,
        kms,
    )

    #
    # Instance
    #

    blast_radius = finder.blast_radius(
        instance,
    )

    assert blast_radius.affected_resources == (
        database,
        kms,
    )

    #
    # Database
    #

    blast_radius = finder.blast_radius(
        database,
    )

    assert blast_radius.affected_resources == (kms,)

    #
    # KMS Key
    #

    blast_radius = finder.blast_radius(
        kms,
    )

    assert blast_radius.affected_resources == ()
