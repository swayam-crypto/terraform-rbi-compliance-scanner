from compliance_scanner.blast_radius.collection import (
    BlastRadiusCollection,
)
from compliance_scanner.blast_radius.models import BlastRadius

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


def test_collection_lookup():

    source = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    blast_radius = BlastRadius(
        source=source,
        affected_resources=(database,),
    )

    collection = BlastRadiusCollection(
        (blast_radius,),
    )

    assert (
        collection.for_resource(
            source,
        )
        == blast_radius
    )


def test_collection_unknown_resource():

    source = make_resource(
        "aws_lb",
        "public",
    )

    database = make_resource(
        "aws_db_instance",
        "database",
    )

    other = make_resource(
        "aws_instance",
        "web",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=source,
                affected_resources=(database,),
            ),
        ),
    )

    assert (
        collection.for_resource(
            other,
        )
        is None
    )


def test_collection_length():

    source = make_resource(
        "aws_lb",
        "public",
    )

    collection = BlastRadiusCollection(
        (
            BlastRadius(
                source=source,
                affected_resources=(),
            ),
        ),
    )

    assert len(collection) == 1


def test_collection_iteration():

    source = make_resource(
        "aws_lb",
        "public",
    )

    blast_radius = BlastRadius(
        source=source,
        affected_resources=(),
    )

    collection = BlastRadiusCollection(
        (blast_radius,),
    )

    assert tuple(collection) == (blast_radius,)


def test_collection_all():

    source = make_resource(
        "aws_lb",
        "public",
    )

    blast_radius = BlastRadius(
        source=source,
        affected_resources=(),
    )

    collection = BlastRadiusCollection(
        (blast_radius,),
    )

    assert collection.all() == (blast_radius,)
