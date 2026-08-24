from compliance_scanner.attack.collection import AttackPathCollection
from compliance_scanner.attack.models import AttackPath

from compliance_scanner.graph.graph_predicates import GraphPredicates
from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.graph.relationship_graph import RelationshipGraph

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


def test_attack_path():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path(load_balancer) is not None


def test_attack_path_size():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_size(load_balancer) == 2


def test_attack_path_contains():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_contains(
        load_balancer,
        database,
    )


def test_attack_path_contains_capability():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_contains_capability(
        load_balancer,
        "data_store",
    )


def test_attack_path_contains_capabilities():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_contains_capabilities(
        load_balancer,
        frozenset({"data_store"}),
    )


def test_attack_path_contains_type():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_contains_type(
        load_balancer,
        CanonicalType.DATABASE,
    )


def test_attack_path_contains_kind():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    collection = AttackPathCollection(
        (
            AttackPath(
                source=load_balancer,
                target=database,
                resources=(
                    load_balancer,
                    database,
                ),
                relationships=(),
            ),
        )
    )

    predicates = GraphPredicates(
        GraphQuery(RelationshipGraph()),
        attack_paths=collection,
    )

    assert predicates.attack_path_contains_kind(
        load_balancer,
        ResourceKind.DATA,
    )
