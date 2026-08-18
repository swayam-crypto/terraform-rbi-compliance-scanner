from types import MappingProxyType

from compliance_scanner.canonical.attribute_mapper import (
    CanonicalAttributeMapper,
)
from compliance_scanner.canonical.context import CanonicalContext
from compliance_scanner.catalog.attributes import (
    AttributeDefinition,
    AttributeType,
)
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation


def make_resource():

    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        resource_type="aws_s3_bucket",
        resource_name="bucket",
        attributes={
            "server_side_encryption_configuration": True,
            "versioning": True,
            "acl": "private",
            "ignored": "value",
        },
        default_attributes={},
        source=SourceLocation(),
    )


def make_definition():

    return ResourceDefinition(
        provider="aws",
        service="s3",
        display_name="Bucket",
        kind=ResourceKind.STORAGE,
        canonical_type=CanonicalType.OBJECT_STORAGE,
        capabilities=frozenset(),
        relationships=frozenset(),
        aliases=(),
        metadata=MappingProxyType({}),
        attributes=MappingProxyType(
            {
                "encryption": AttributeDefinition(
                    name="server_side_encryption_configuration",
                    type=AttributeType.BOOLEAN,
                ),
                "versioning": AttributeDefinition(
                    name="versioning",
                    type=AttributeType.BOOLEAN,
                ),
                "public_access": AttributeDefinition(
                    name="acl",
                    type=AttributeType.STRING,
                ),
            }
        ),
    )


def test_attribute_mapping():

    context = CanonicalContext(
        resource=make_resource(),
        definition=make_definition(),
    )

    mapper = CanonicalAttributeMapper()

    mapper.map(context)

    assert context.canonical_attributes == {
        "encryption": True,
        "versioning": True,
        "public_access": "private",
    }


def test_mapping_is_immutable():

    context = CanonicalContext(
        resource=make_resource(),
        definition=make_definition(),
    )

    mapper = CanonicalAttributeMapper()

    mapper.map(context)

    assert isinstance(
        context.canonical_attributes,
        MappingProxyType,
    )
