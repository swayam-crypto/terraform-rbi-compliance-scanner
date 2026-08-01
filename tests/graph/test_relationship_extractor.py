from compliance_scanner.graph.relationship import RelationshipType
from compliance_scanner.parser.relationship_extractor import RelationshipExtractor
from compliance_scanner.graph.resource_index import ResourceIndex

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def make_resource(
    resource_type: str,
    resource_name: str,
    attributes: dict | None = None,
) -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name=resource_name,
        attributes=attributes or {},
        default_attributes={},
        source=SourceLocation(),
    )


def test_extract_vpc_relationship():
    vpc = make_resource(
        "aws_vpc",
        "main",
    )

    subnet = make_resource(
        "aws_subnet",
        "private",
        {
            "vpc_id": "aws_vpc.main.id",
        },
    )

    resources = [
        vpc,
        subnet,
    ]

    index = ResourceIndex(resources)

    extractor = RelationshipExtractor()

    relationships = extractor.extract(
        resources,
        index,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == subnet
    assert relationship.target == vpc
    assert relationship.relationship_type == RelationshipType.USES_VPC


def test_extract_subnet_relationship():
    subnet = make_resource(
        "aws_subnet",
        "private",
    )

    instance = make_resource(
        "aws_instance",
        "web",
        {
            "subnet_id": "aws_subnet.private.id",
        },
    )

    resources = [
        subnet,
        instance,
    ]

    index = ResourceIndex(resources)

    extractor = RelationshipExtractor()

    relationships = extractor.extract(
        resources,
        index,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == instance
    assert relationship.target == subnet
    assert relationship.relationship_type == RelationshipType.USES_SUBNET
