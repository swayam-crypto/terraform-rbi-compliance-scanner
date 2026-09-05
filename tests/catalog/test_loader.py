from pathlib import Path
from types import MappingProxyType

import pytest

from compliance_scanner.catalog.attributes import (
    AttributeDefinition,
    AttributeType,
)
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind
from compliance_scanner.catalog.loader import CatalogLoader
from compliance_scanner.catalog.registry import CatalogRegistry
from compliance_scanner.catalog.relationship_types import RelationshipType
from compliance_scanner.catalog.exceptions import CatalogValidationError
from compliance_scanner.catalog.canonical_types import CanonicalType

from textwrap import dedent
from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)


def write_catalog(
    path: Path,
    content: str,
) -> None:
    """
    Helper for writing temporary catalog YAML files.
    """

    path.write_text(
        dedent(content).strip() + "\n",
        encoding="utf-8",
    )


def test_load_catalog(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS DB Instance

          kind: data
          canonical_type: database

          capabilities:
            - encryption
            - backup
            - logging

          attributes:
            encryption:
              name: storage_encrypted
              type: boolean
              default: false
              description: Storage encryption.

          relationships:
            - subnet
            - security_group
            - kms_key

          aliases:
            - AWS::RDS::DBInstance

          metadata:
            deprecated: false
    """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert registry.has("aws_db_instance")

    definition = registry.get("aws_db_instance")

    assert definition is not None

    assert definition.provider == "aws"
    assert definition.service == "rds"
    assert definition.display_name == "Amazon RDS DB Instance"

    assert definition.kind == ResourceKind.DATA
    assert definition.canonical_type == CanonicalType.DATABASE

    assert definition.capabilities == frozenset(
        {
            "encryption",
            "backup",
            "logging",
        }
    )

    assert definition.relationships == frozenset(
        {
            "subnet",
            "security_group",
            "kms_key",
        }
    )

    assert definition.aliases == ("AWS::RDS::DBInstance",)

    assert definition.metadata["deprecated"] is False


def test_attributes_are_converted(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds

          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes:
            encryption:
              name: storage_encrypted
              type: boolean
              default: false
              description: Encryption flag.
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    definition = registry.get("aws_db_instance")

    assert definition is not None

    attribute = definition.attributes["encryption"]

    assert isinstance(
        attribute,
        AttributeDefinition,
    )

    assert attribute.name == "storage_encrypted"

    assert attribute.type == AttributeType.BOOLEAN

    assert attribute.default is False


def test_attributes_are_immutable(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds

          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes:

            encryption:
              name: storage_encrypted
              type: boolean
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    definition = registry.get("aws_db_instance")

    assert definition is not None

    assert isinstance(
        definition.attributes,
        MappingProxyType,
    )

    with pytest.raises(TypeError):

        definition.attributes["new"] = AttributeDefinition(
            name="dummy",
            type=AttributeType.STRING,
        )


def test_metadata_is_immutable(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds

          display_name: Amazon RDS

          kind: data
          canonical_type: database

          metadata:
            deprecated: false
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    definition = registry.get("aws_db_instance")

    assert definition is not None

    assert isinstance(
        definition.metadata,
        MappingProxyType,
    )

    with pytest.raises(TypeError):

        definition.metadata["deprecated"] = True


def test_load_directory(tmp_path: Path):

    aws = tmp_path / "aws.yaml"

    azure = tmp_path / "azure.yaml"

    write_catalog(
        aws,
        """
        aws_db_instance:
          provider: aws
          service: rds

          display_name: Amazon RDS

          kind: data
          canonical_type: database
        """,
    )

    write_catalog(
        azure,
        """
        azurerm_storage_account:
          provider: azure
          service: storage

          display_name: Azure Storage Account
          
          kind: storage
          canonical_type: object_storage
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load_directory(
        registry,
        str(tmp_path),
    )

    assert registry.has("aws_db_instance")

    assert registry.has("azurerm_storage_account")


def test_missing_required_field(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_invalid_kind(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Test

          kind: invalid_kind
          canonical_type: database
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_invalid_canonical_type(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Test

          kind: data
          canonical_type: invalid_type
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_invalid_attribute_type(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Test

          kind: data
          canonical_type: database

          attributes:
            encryption:
              name: storage_encrypted
              type: invalid
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_missing_attribute_name(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes:
            encryption:
              type: boolean
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_missing_attribute_type(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes:
            encryption:
             name: storage_encrypted
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_duplicate_aliases(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          aliases:
            - AWS::RDS::DBInstance
            - AWS::RDS::DBInstance
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_duplicate_attribute_names(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes:
            encryption:
              name: storage_encrypted
              type: boolean

            another:
              name: storage_encrypted
              type: boolean
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_empty_required_field(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: ""
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    with pytest.raises(ValueError):
        loader.load(
            registry,
            str(yaml_file),
        )


def test_empty_attributes_are_allowed(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          attributes: {}
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert len(registry) == 1


def test_empty_aliases_are_allowed(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          aliases: []
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert len(registry) == 1


def test_empty_relationships_are_allowed(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          relationships: []
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert len(registry) == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("capabilities", "encryption"),
        ("capabilities", "[encryption, 1]"),
        ("relationships", "subnet"),
        ("relationships", "[subnet, 1]"),
        ("relationships", "[{name: subnet}]"),
    ],
)
def test_collection_fields_must_be_lists_of_strings(
    tmp_path: Path, field: str, value: str
):
    yaml_file = tmp_path / "aws.yaml"
    write_catalog(
        yaml_file,
        f"""
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS
          kind: data
          canonical_type: database
          {field}: {value}
        """,
    )

    with pytest.raises(CatalogValidationError):
        CatalogLoader().load(CatalogRegistry(), str(yaml_file))


def test_descriptive_resource_relationships_are_allowed(tmp_path: Path):
    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_s3_bucket:
          provider: aws
          service: s3
          display_name: Amazon S3 Bucket
          kind: storage
          canonical_type: object_storage
          relationships:
            - bucket_policy
            - kms_key
        """,
    )

    registry = CatalogRegistry()
    CatalogLoader().load(registry, str(yaml_file))

    definition = registry.get("aws_s3_bucket")

    assert definition is not None
    assert definition.relationships == frozenset(
        {
            "bucket_policy",
            "kms_key",
        }
    )


def test_duplicate_resource_relationships_are_rejected(tmp_path: Path):
    yaml_file = tmp_path / "aws.yaml"
    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS
          kind: data
          canonical_type: database
          relationships: [subnet, subnet]
        """,
    )

    with pytest.raises(CatalogValidationError, match="Duplicate relationship entries"):
        CatalogLoader().load(CatalogRegistry(), str(yaml_file))


def test_valid_capabilities_and_relationships_are_loaded(tmp_path: Path):
    yaml_file = tmp_path / "aws.yaml"
    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS
          kind: data
          canonical_type: database
          capabilities: [encryption_at_rest, backup]
          relationships: [subnet, kms_key]
        """,
    )

    registry = CatalogRegistry()
    CatalogLoader().load(registry, str(yaml_file))

    definition = registry.get("aws_db_instance")
    assert definition is not None
    assert definition.capabilities == frozenset({"encryption_at_rest", "backup"})
    assert definition.relationships == frozenset({"subnet", "kms_key"})


def test_empty_metadata_are_allowed(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
        aws_db_instance:
          provider: aws
          service: rds
          display_name: Amazon RDS

          kind: data
          canonical_type: database

          metadata: {}
        """,
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert len(registry) == 1


def test_attribute_relationship_metadata(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
aws_instance:
  provider: aws
  service: ec2

  display_name: EC2 Instance

  kind: compute
  canonical_type: virtual_machine

  attributes:
    subnet_id:
      name: subnet_id
      type: string

      relationship:
        type: subnet
        target: subnet
""",
    )

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    definition = registry.get("aws_instance")

    attribute = definition.attributes["subnet_id"]

    assert attribute.relationship is not None

    assert attribute.relationship.relationship_type == RelationshipType.SUBNET
    assert attribute.relationship.target == CanonicalType.SUBNET
    assert attribute.relationship.required is False


def test_attribute_privilege_relationship_metadata(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
aws_instance:
  provider: aws
  service: ec2

  display_name: EC2 Instance

  kind: compute
  canonical_type: virtual_machine

  attributes:
    iam_instance_profile:
      name: iam_instance_profile
      type: string

      privilege_relationship:
        type: identity
        target: identity
""",
    )

    registry = CatalogRegistry()

    CatalogLoader().load(
        registry,
        str(yaml_file),
    )

    definition = registry.get(
        "aws_instance",
    )

    attribute = definition.attributes["iam_instance_profile"]

    assert attribute.privilege_relationship is not None

    assert (
        attribute.privilege_relationship.relationship_type
        == PrivilegeRelationshipType.IDENTITY
    )

    assert attribute.privilege_relationship.target == CanonicalType.IDENTITY

    assert attribute.privilege_relationship.required is False


def test_required_privilege_relationship(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
aws_instance:
  provider: aws
  service: ec2

  display_name: EC2 Instance

  kind: compute
  canonical_type: virtual_machine

  attributes:
    iam_instance_profile:
      name: iam_instance_profile
      type: string

      privilege_relationship:
        type: identity
        target: identity
        required: true
""",
    )

    registry = CatalogRegistry()

    CatalogLoader().load(
        registry,
        str(yaml_file),
    )

    definition = registry.get(
        "aws_instance",
    )

    relationship = definition.attributes["iam_instance_profile"].privilege_relationship

    assert relationship.required is True


def test_invalid_privilege_relationship_type(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
aws_instance:
  provider: aws
  service: ec2

  display_name: EC2 Instance

  kind: compute
  canonical_type: virtual_machine

  attributes:
    iam_instance_profile:
      name: iam_instance_profile
      type: string

      privilege_relationship:
        type: invalid
        target: identity
""",
    )

    with pytest.raises(
        CatalogValidationError,
    ):
        CatalogLoader().load(
            CatalogRegistry(),
            str(yaml_file),
        )


def test_invalid_privilege_relationship_target(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    write_catalog(
        yaml_file,
        """
aws_instance:
  provider: aws
  service: ec2

  display_name: EC2 Instance

  kind: compute
  canonical_type: virtual_machine

  attributes:
    iam_instance_profile:
      name: iam_instance_profile
      type: string

      privilege_relationship:
        type: identity
        target: invalid_target
""",
    )

    with pytest.raises(
        CatalogValidationError,
    ):
        CatalogLoader().load(
            CatalogRegistry(),
            str(yaml_file),
        )
