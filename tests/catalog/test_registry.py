from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry
import pytest


def register(
    self,
    resource_type: str,
    definition: ResourceDefinition,
) -> None:
    """
    Register a resource definition.

    Raises:
        ValueError: If the resource type has already been registered.
    """
    if resource_type in self._resources:
        raise ValueError(f"Resource type '{resource_type}' is already registered.")

    self._resources[resource_type] = definition


def test_all():

    registry = CatalogRegistry()

    definition = ResourceDefinition(
        canonical_type="database",
        provider="aws",
        service="rds",
    )

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
        ResourceDefinition(
            canonical_type="database",
            provider="aws",
            service="rds",
        ),
    )

    registry.clear()

    assert len(registry) == 0


def test_contains():

    registry = CatalogRegistry()

    registry.register(
        "aws_db_instance",
        ResourceDefinition(
            canonical_type="database",
            provider="aws",
            service="rds",
        ),
    )

    assert "aws_db_instance" in registry


def test_len():

    registry = CatalogRegistry()

    assert len(registry) == 0

    registry.register(
        "aws_db_instance",
        ResourceDefinition(
            canonical_type="database",
            provider="aws",
            service="rds",
        ),
    )

    assert len(registry) == 1


def test_register_duplicate():

    registry = CatalogRegistry()

    definition = ResourceDefinition(
        canonical_type="database",
        provider="aws",
        service="rds",
    )

    registry.register(
        "aws_db_instance",
        definition,
    )

    with pytest.raises(ValueError):
        registry.register(
            "aws_db_instance",
            definition,
        )
