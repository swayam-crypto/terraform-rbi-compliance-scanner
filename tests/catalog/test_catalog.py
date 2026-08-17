from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider

from types import MappingProxyType
import pytest

from compliance_scanner.canonical import (
    UnknownCanonicalResourceError,
)

EMPTY_MAPPING = MappingProxyType({})


def make_resource(
    resource_type: str,
    resource_name: str,
) -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name=resource_name,
        attributes=EMPTY_MAPPING,
        default_attributes={},
        source=SourceLocation(),
    )


def make_catalog() -> Catalog:

    registry = CatalogRegistry()

    registry.register(
        "aws_db_instance",
        ResourceDefinition(
            provider="aws",
            service="rds",
            display_name="Amazon RDS DB Instance",
            kind=ResourceKind.DATA,
            canonical_type=CanonicalType.DATABASE,
            capabilities=frozenset(
                {
                    "backup",
                    "encryption",
                    "logging",
                }
            ),
            attributes=EMPTY_MAPPING,
            aliases=(
                "AWS::RDS::DBInstance",
                "aws:rds/instance:Instance",
            ),
            relationships=frozenset(
                {
                    "subnet",
                    "security_group",
                    "kms_key",
                }
            ),
            metadata=EMPTY_MAPPING,
        ),
    )

    return Catalog(registry)


def test_definition():

    catalog = make_catalog()

    resource = make_database()

    definition = catalog.definition(resource)

    assert definition.canonical_type == CanonicalType.DATABASE


def test_has_capability():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.has_capability(
        resource,
        "backup",
    )


def test_missing_capability():

    catalog = make_catalog()

    resource = make_database()

    assert not catalog.has_capability(
        resource,
        "non_existent_capability",
    )


def test_canonical_type():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.canonical_type(resource) == CanonicalType.DATABASE


def test_provider():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.provider(resource) == "aws"


def make_database() -> ResolvedResource:
    return make_resource(
        "aws_db_instance",
        "database",
    )


def test_kind():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.definition(resource).kind == ResourceKind.DATA


def test_service():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.service(resource) == "rds"


def test_aliases():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.aliases(resource) == (
        "AWS::RDS::DBInstance",
        "aws:rds/instance:Instance",
    )


def test_relationships():

    catalog = make_catalog()

    resource = make_database()

    assert catalog.relationships(resource) == frozenset(
        {
            "subnet",
            "security_group",
            "kms_key",
        }
    )


def test_unknown_resource():

    catalog = make_catalog()

    resource = make_resource(
        "aws_unknown_resource",
        "unknown",
    )

    assert catalog.definition(resource) is None

    assert not catalog.has_capability(
        resource,
        "database",
    )

    assert catalog.canonical_type(resource) is None

    assert catalog.provider(resource) is None

    assert catalog.service(resource) is None

    assert catalog.aliases(resource) == ()

    assert catalog.relationships(resource) == frozenset()
