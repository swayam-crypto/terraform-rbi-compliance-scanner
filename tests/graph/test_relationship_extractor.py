from compliance_scanner.graph.relationship import RelationshipType, Relationship
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


def extract_relationships(
    *resources: ResolvedResource,
) -> list[Relationship]:
    """
    Build a ResourceIndex and run the RelationshipExtractor.
    """

    resources = list(resources)

    index = ResourceIndex(resources)

    extractor = RelationshipExtractor()

    return extractor.extract(
        resources,
        index,
    )


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

    relationships = extract_relationships(
        subnet,
        instance,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == instance
    assert relationship.target == subnet
    assert relationship.relationship_type == RelationshipType.USES_SUBNET


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

    relationships = extract_relationships(
        vpc,
        subnet,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == subnet
    assert relationship.target == vpc
    assert relationship.relationship_type == RelationshipType.USES_VPC


def test_extract_security_group_relationship():
    web_sg = make_resource(
        "aws_security_group",
        "web",
    )
    db_sg = make_resource(
        "aws_security_group",
        "db",
    )
    instance = make_resource(
        "aws_instance",
        "frontend",
        {
            "vpc_security_group_ids": [
                "aws_security_group.web.id",
                "aws_security_group.db.id",
            ],
        },
    )

    relationships = extract_relationships(
        web_sg,
        db_sg,
        instance,
    )

    assert len(relationships) == 2

    assert relationships[0].relationship_type == (
        RelationshipType.ATTACHED_TO_SECURITY_GROUP
    )

    assert relationships[1].relationship_type == (
        RelationshipType.ATTACHED_TO_SECURITY_GROUP
    )

    targets = {relationship.target.resource_name for relationship in relationships}

    assert targets == {
        "web",
        "db",
    }
