from types import MappingProxyType

from compliance_scanner.canonical.builder import CanonicalResourceBuilder
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
import pytest
from compliance_scanner.canonical.context import CanonicalContext

EMPTY_MAPPING = MappingProxyType({})


def make_resource() -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        resource_type="aws_s3_bucket",
        resource_name="bucket",
        attributes={
            "versioning": True,
            "encryption": True,
        },
        default_attributes={},
        source=SourceLocation(
            file_path="main.tf",
            line=10,
            column=2,
        ),
    )


def make_definition() -> ResourceDefinition:
    return ResourceDefinition(
        provider="aws",
        service="s3",
        display_name="Amazon S3 Bucket",
        kind=ResourceKind.STORAGE,
        canonical_type=CanonicalType.OBJECT_STORAGE,
        capabilities=frozenset(
            {
                "versioning",
                "encryption",
            }
        ),
        attributes=EMPTY_MAPPING,
        relationships=frozenset(),
        aliases=(),
        metadata=MappingProxyType(
            {
                "maturity": "stable",
            }
        ),
    )


from types import MappingProxyType


def test_builder_creates_canonical_resource():

    builder = CanonicalResourceBuilder()

    resource = make_resource()

    definition = make_definition()

    context = CanonicalContext(
        resource=resource,
        definition=definition,
    )

    context.canonical_attributes = MappingProxyType(
        {
            "versioning": True,
            "encryption": True,
        }
    )

    canonical = builder.build(context)

    assert canonical.platform is Platform.TERRAFORM
    assert canonical.provider is CloudProvider.AWS
    assert canonical.canonical_type is CanonicalType.OBJECT_STORAGE
    assert canonical.resource_name == "bucket"

    assert canonical.attributes["versioning"] is True
    assert canonical.attributes["encryption"] is True

    assert canonical.capabilities == frozenset(
        {
            "versioning",
            "encryption",
        }
    )

    assert canonical.metadata["maturity"] == "stable"

    assert canonical.source.file_path == "main.tf"


from types import MappingProxyType


def test_builder_uses_canonical_attributes():

    builder = CanonicalResourceBuilder()

    resource = make_resource()

    definition = make_definition()

    context = CanonicalContext(
        resource=resource,
        definition=definition,
    )

    context.canonical_attributes = MappingProxyType(
        {
            "versioning": True,
        }
    )

    canonical = builder.build(context)

    resource.attributes["versioning"] = False

    assert canonical.attributes["versioning"] is True


def test_attributes_are_immutable():

    builder = CanonicalResourceBuilder()

    resource = make_resource()

    definition = make_definition()

    context = CanonicalContext(
        resource=resource,
        definition=definition,
    )

    canonical = builder.build(context)

    with pytest.raises(TypeError):
        canonical.attributes["new"] = True
