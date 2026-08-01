from pathlib import Path

import yaml

from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry


class CatalogLoader:

    def load(
        self,
        registry: CatalogRegistry,
        file_path: str,
    ) -> None:
        """
        Load resource definitions from a YAML file into the registry.
        """

        with Path(file_path).open(
            "r",
            encoding="utf-8",
        ) as file:
            data = yaml.safe_load(file)

        if data is None:
            return

        for resource_type, resource_data in data.items():

            definition = ResourceDefinition(
                canonical_type=resource_data["canonical_type"],
                provider=resource_data["provider"],
                service=resource_data["service"],
            )

            registry.register(
                resource_type,
                definition,
            )

    def load_directory(
        self,
        registry: CatalogRegistry,
        directory: str,
    ) -> None:
        """
        Load every YAML file in the given directory
        """

        from pathlib import Path

        for yaml_file in Path(directory).glob("*.yaml"):
            self.load(
                registry,
                str(yaml_file),
            )
