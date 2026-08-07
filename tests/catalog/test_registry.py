from types import MappingProxyType

import pytest

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry

EMPTY_MAPPING = MappingProxyType({})


def make_definition() -> ResourceDefinition:
    return ResourceDefinition(
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
        aliases=("AWS::RDS::DBInstance",),
        relationships=frozenset(
            {
                "subnet",
                "security_group",
                "kms_key",
            }
        ),
        metadata=EMPTY_MAPPING,
    )


def test_all():

    registry = CatalogRegistry()

    definition = make_definition()

    registry.register(
        "aws_db_instance",
        definition,
    )

    resources = registry.all()

    assert resources == (definition,)


def test_clear():

    registry = CatalogRegistry()

    registry.register(
        "aws_db_instance",
        make_definition(),
    )

    registry.clear()

    assert len(registry) == 0


def test_contains():

    registry = CatalogRegistry()

    registry.register(
        "aws_db_instance",
        make_definition(),
    )

    assert "aws_db_instance" in registry


def test_len():

    registry = CatalogRegistry()

    assert len(registry) == 0

    registry.register(
        "aws_db_instance",
        make_definition(),
    )

    assert len(registry) == 1


def test_register_duplicate():

    registry = CatalogRegistry()

    definition = make_definition()

    registry.register(
        "aws_db_instance",
        definition,
    )

    with pytest.raises(ValueError):
        registry.register(
            "aws_db_instance",
            definition,
        )
