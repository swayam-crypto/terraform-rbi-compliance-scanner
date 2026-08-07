from dataclasses import FrozenInstanceError

import pytest

from compliance_scanner.catalog.attributes import (
    AttributeDefinition,
    AttributeType,
)
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.catalog.models import ResourceDefinition


def test_attribute_definition():

    attribute = AttributeDefinition(
        name="storage_encrypted",
        type=AttributeType.BOOLEAN,
        default=False,
        description="Storage encryption flag.",
    )

    assert attribute.name == "storage_encrypted"
    assert attribute.type == AttributeType.BOOLEAN
    assert attribute.default is False
    assert attribute.description == "Storage encryption flag."


def test_attribute_definition_is_frozen():

    attribute = AttributeDefinition(
        name="storage_encrypted",
        type=AttributeType.BOOLEAN,
    )

    with pytest.raises(FrozenInstanceError):
        attribute.name = "encrypted"


def test_resource_kind():

    assert ResourceKind.COMPUTE.value == "compute"
    assert ResourceKind.STORAGE.value == "storage"
    assert ResourceKind.DATA.value == "data"
    assert ResourceKind.NETWORK.value == "network"
    assert ResourceKind.SECURITY.value == "security"
    assert ResourceKind.IDENTITY.value == "identity"


def test_canonical_type():

    assert CanonicalType.DATABASE.value == "database"
    assert CanonicalType.OBJECT_STORAGE.value == "object_storage"
    assert CanonicalType.VIRTUAL_MACHINE.value == "virtual_machine"


def test_resource_definition():

    definition = ResourceDefinition(
        provider="aws",
        service="rds",
        display_name="Amazon RDS Instance",
        kind=ResourceKind.DATA,
        canonical_type=CanonicalType.DATABASE,
        capabilities=frozenset(
            {
                "database",
                "encryption",
            }
        ),
        attributes={
            "encryption": AttributeDefinition(
                name="storage_encrypted",
                type=AttributeType.BOOLEAN,
                default=False,
            )
        },
        relationships=frozenset(
            {
                "subnet",
                "security_group",
            }
        ),
        aliases=("AWS::RDS::DBInstance",),
        metadata={
            "deprecated": False,
        },
    )

    assert definition.provider == "aws"
    assert definition.service == "rds"
    assert definition.display_name == "Amazon RDS Instance"

    assert definition.kind == ResourceKind.DATA
    assert definition.canonical_type == CanonicalType.DATABASE

    assert "database" in definition.capabilities

    assert definition.attributes["encryption"].name == "storage_encrypted"

    assert definition.attributes["encryption"].type == AttributeType.BOOLEAN

    assert "subnet" in definition.relationships

    assert definition.aliases == ("AWS::RDS::DBInstance",)

    assert definition.metadata["deprecated"] is False


def test_resource_definition_is_frozen():

    definition = ResourceDefinition(
        provider="aws",
        service="rds",
        display_name="Amazon RDS Instance",
        kind=ResourceKind.DATA,
        canonical_type=CanonicalType.DATABASE,
    )

    with pytest.raises(FrozenInstanceError):
        definition.provider = "azure"
