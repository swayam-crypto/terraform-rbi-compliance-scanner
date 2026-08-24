import pytest

from compliance_scanner.canonical import ResourceClassifier
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.registry import CatalogRegistry
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.canonical import (
    UnknownCanonicalResourceError,
)


def make_catalog() -> Catalog:
    registry = CatalogRegistry()

    registry.register(
        "aws_s3_bucket",
        ResourceDefinition(
            provider="aws",
            service="s3",
            display_name="Amazon S3 Bucket",
            kind=ResourceKind.DATA,
            canonical_type=CanonicalType.OBJECT_STORAGE,
        ),
    )

    return Catalog(registry)


def make_resource(resource_type: str = "aws_s3_bucket") -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        resource_type=resource_type,
        resource_name="bucket",
        attributes={},
        default_attributes={},
        source=SourceLocation(
            file_path="main.tf",
            line=1,
            column=1,
        ),
    )


def test_classifier_returns_canonical_type():
    catalog = make_catalog()
    classifier = ResourceClassifier(catalog)

    resource = make_resource()

    canonical_type = classifier.classify(resource)

    assert canonical_type is CanonicalType.OBJECT_STORAGE


def test_unknown_resource_raises_key_error():
    catalog = make_catalog()
    classifier = ResourceClassifier(catalog)

    resource = make_resource("aws_unknown_resource")

    with pytest.raises(UnknownCanonicalResourceError) as exc_info:
        classifier.classify(resource)

    assert exc_info.value.resource_type == "aws_unknown_resource"
    assert "Unknown resource type 'aws_unknown_resource'" in str(exc_info.value)


def test_classifier_is_deterministic():
    catalog = make_catalog()
    classifier = ResourceClassifier(catalog)

    resource = make_resource()

    assert classifier.classify(resource) == classifier.classify(resource)
