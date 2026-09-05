from compliance_scanner.catalog.relationship_types import RelationshipType
from compliance_scanner.canonical.relationship_resolver import RelationshipResolver
from compliance_scanner.graph.resource_index import ResourceIndex

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.engine.relationship.relationship import Relationship


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
    Build a ResourceIndex and run the RelationshipResolver.
    """

    resources = list(resources)

    index = ResourceIndex(resources)

    extractor = RelationshipResolver(catalog)

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
    assert relationship.relationship_type == RelationshipType.SUBNET


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
    assert relationship.relationship_type == RelationshipType.VPC


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

    assert relationships[0].relationship_type == (RelationshipType.SECURITY_GROUP)

    assert relationships[1].relationship_type == (RelationshipType.SECURITY_GROUP)

    targets = {relationship.target.resource_name for relationship in relationships}

    assert targets == {
        "web",
        "db",
    }


def test_extract_kms_key_relationship():
    kms_key = make_resource(
        "aws_kms_key",
        "storage_key",
    )

    bucket = make_resource(
        "aws_s3_bucket",
        "customer_data",
        {
            "kms_key_id": "aws_kms_key.storage_key.id",
        },
    )

    relationships = extract_relationships(
        kms_key,
        bucket,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == bucket
    assert relationship.target == kms_key
    assert relationship.relationship_type == RelationshipType.KMS_KEY


def test_extract_target_group_relationship():
    target_group = make_resource(
        "aws_lb_target_group",
        "web_tg",
    )

    listener = make_resource(
        "aws_lb_listener",
        "https",
        {
            "target_group_arn": "aws_lb_target_group.web_tg.arn",
        },
    )

    relationships = extract_relationships(
        target_group,
        listener,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == listener
    assert relationship.target == target_group
    assert relationship.relationship_type == RelationshipType.TARGET_GROUP


def test_extract_bucket_relationship():
    bucket = make_resource(
        "aws_s3_bucket",
        "logs",
    )

    bucket_policy = make_resource(
        "aws_s3_bucket_policy",
        "logs_policy",
        {
            "bucket": "aws_s3_bucket.logs.id",
        },
    )

    relationships = extract_relationships(
        bucket,
        bucket_policy,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source == bucket_policy
    assert relationship.target == bucket
    assert relationship.relationship_type == RelationshipType.OBJECT_STORAGE
