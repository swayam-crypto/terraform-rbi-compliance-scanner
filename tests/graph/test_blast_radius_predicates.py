from compliance_scanner.engine.blast_radius.collection import BlastRadiusCollection
from compliance_scanner.engine.blast_radius.models import BlastRadius
from compliance_scanner.graph.graph_predicates import GraphPredicates
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind

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

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius(load_balancer) is not None


def test_blast_radius_size():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_size(load_balancer) == 1


def test_blast_radius_contains():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_contains(
        load_balancer,
        database,
    )


def test_blast_radius_contains_capability():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_contains_capability(
        load_balancer,
        "data_store",
    )


def test_blast_radius_contains_capabilities():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_contains_capabilities(
        load_balancer,
        frozenset({"data_store"}),
    )


def test_blast_radius_contains_type():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_contains_type(
        load_balancer,
        CanonicalType.DATABASE,
    )


def test_blast_radius_contains_kind():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=load_balancer,
                affected_resources=(database,),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        blast_radius=collection,
    )

    assert predicates.blast_radius_contains_kind(
        load_balancer,
        ResourceKind.DATA,
    )
