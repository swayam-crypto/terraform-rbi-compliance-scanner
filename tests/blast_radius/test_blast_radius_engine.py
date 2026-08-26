from compliance_scanner.engine.blast_radius.engine import BlastRadiusEngine
from compliance_scanner.canonical.runtime_integration import (
    build_canonical_resources,
)
from compliance_scanner.engine.relationship.relationship import (
    Relationship,
    RelationshipType,
)
from compliance_scanner.engine.relationship.relationship_graph import RelationshipGraph
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.runtime.scan_context import ScanContext

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.engine.privilege.graph import PrivilegeGraph


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


def test_engine():

    load_balancer = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    resources = [
        load_balancer,
        database,
    ]

    graph = RelationshipGraph()

    graph.add(
        Relationship(
            source=load_balancer,
            target=database,
            relationship_type=RelationshipType.TARGET_GROUP,
        )
    )

    context = ScanContext(
        resources=resources,
        canonical_resources=build_canonical_resources(
            resources,
        ),
        resource_index=ResourceIndex(
            resources,
        ),
        relationship_graph=graph,
        privilege_graph=PrivilegeGraph(),
    )

    collection = BlastRadiusEngine(
        context,
    ).analyze()

    assert len(collection) == 2

    assert (
        collection.for_resource(
            load_balancer,
        )
        is not None
    )
