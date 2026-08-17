from compliance_scanner.canonical import CanonicalResource
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.source_location import SourceLocation

import pytest
from dataclasses import FrozenInstanceError


def make_resource() -> CanonicalResource:
    return CanonicalResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        canonical_type=CanonicalType.OBJECT_STORAGE,
        resource_name="bucket",
        attributes={
            "encryption": True,
            "versioning": True,
        },
        capabilities=frozenset(
            {
                "encryption_at_rest",
                "versioning",
            }
        ),
        metadata={
            "maturity": "stable",
        },
        source=SourceLocation(
            file_path="main.tf",
            line=10,
            column=5,
        ),
    )


def test_canonical_resource_creation():
    resource = make_resource()

    assert resource.platform is Platform.TERRAFORM
    assert resource.provider is CloudProvider.AWS
    assert resource.canonical_type is CanonicalType.OBJECT_STORAGE
    assert resource.resource_name == "bucket"

    assert resource.attributes["encryption"] is True
    assert resource.attributes["versioning"] is True

    assert "versioning" in resource.capabilities

    assert resource.metadata["maturity"] == "stable"


def test_canonical_resource_is_immutable():
    resource = make_resource()

    with pytest.raises(FrozenInstanceError):
        resource.resource_name = "new-name"


def test_canonical_resources_with_same_data_are_equal():
    left = make_resource()
    right = make_resource()

    assert left == right


def test_source_location_is_preserved():
    resource = make_resource()

    assert resource.source.file_path == "main.tf"
    assert resource.source.line == 10
    assert resource.source.column == 5


def test_capabilities_are_immutable():
    resource = make_resource()

    assert isinstance(resource.capabilities, frozenset)
