from pathlib import Path

from compliance_scanner.catalog.loader import CatalogLoader
from compliance_scanner.catalog.registry import CatalogRegistry


def test_load_catalog(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    yaml_file.write_text("""
aws_db_instance:
  canonical_type: database
  provider: aws
  service: rds

  capabilities:
    - database
    - encryption
    - backup
    - logging

  aliases:
    - AWS::RDS::DBInstance
    - aws:rds/instance:Instance

  relationships:
    - subnet
    - security_group
    - kms_key

aws_s3_bucket:
  canonical_type: storage
  provider: aws
  service: s3

  capabilities:
    - storage
    - encryption

  aliases:
    - AWS::S3::Bucket

  relationships:
    - bucket_policy
    - kms_key
        """)

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    assert registry.has("aws_db_instance")
    assert registry.has("aws_s3_bucket")

    database = registry.get("aws_db_instance")

    assert database is not None

    assert database.canonical_type == "database"
    assert database.provider == "aws"
    assert database.service == "rds"

    assert database.capabilities == frozenset(
        {
            "database",
            "encryption",
            "backup",
            "logging",
        }
    )

    assert database.relationships == frozenset(
        {
            "subnet",
            "security_group",
            "kms_key",
        }
    )

    assert database.aliases == (
        "AWS::RDS::DBInstance",
        "aws:rds/instance:Instance",
    )


def test_load_directory(tmp_path: Path):

    aws = tmp_path / "aws.yaml"

    azure = tmp_path / "azure.yaml"

    aws.write_text("""
aws_db_instance:
  canonical_type: database
  provider: aws
  service: rds
""")

    azure.write_text("""
azurerm_storage_account:
  canonical_type: storage
  provider: azure
  service: storage
""")

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load_directory(
        registry,
        str(tmp_path),
    )

    assert registry.has("aws_db_instance")
    assert registry.has("azurerm_storage_account")
    database = registry.get("aws_db_instance")

    assert database is not None
    assert database.provider == "aws"
    assert database.service == "rds"

    storage = registry.get("azurerm_storage_account")

    assert storage is not None
    assert storage.provider == "azure"
    assert storage.service == "storage"


def test_load_catalog_defaults(tmp_path: Path):

    yaml_file = tmp_path / "aws.yaml"

    yaml_file.write_text("""
aws_db_instance:
  canonical_type: database
  provider: aws
  service: rds
""")

    registry = CatalogRegistry()

    loader = CatalogLoader()

    loader.load(
        registry,
        str(yaml_file),
    )

    database = registry.get("aws_db_instance")

    assert database is not None

    assert database.capabilities == frozenset()
    assert database.relationships == frozenset()
    assert database.aliases == ()
