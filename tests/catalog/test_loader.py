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

aws_s3_bucket:
  canonical_type: storage
  provider: aws
  service: s3
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
