from pathlib import Path

from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.loader import CatalogLoader
from compliance_scanner.catalog.registry import CatalogRegistry


def _build_catalog() -> Catalog:
    """
    Build and initialize the global catalog.
    """

    registry = CatalogRegistry()

    loader = CatalogLoader()

    data_directory = Path(__file__).parent / "data"

    loader.load_directory(
        registry,
        str(data_directory),
    )

    return Catalog(registry)


catalog = _build_catalog()
