from pathlib import Path
from typing import Any, Mapping
from types import MappingProxyType
import yaml

from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry

from compliance_scanner.catalog.attributes import (
    AttributeDefinition,
    AttributeType,
)

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind


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

            self._validate_resource(
                resource_type,
                resource_data,
            )

            definition = self._build_definition(
                resource_data,
            )

            registry.register(
                resource_type,
                definition,
            )

    def _build_definition(
        self,
        resource_data: dict[str, Any],
    ) -> ResourceDefinition:
        """
        Build a ResourceDefinition from a catalog entry.
        """

        return ResourceDefinition(
            provider=resource_data["provider"],
            service=resource_data["service"],
            display_name=resource_data.get(
                "display_name",
                "",
            ),
            kind=self._parse_kind(
                resource_data,
            ),
            canonical_type=self._parse_canonical_type(
                resource_data,
            ),
            capabilities=frozenset(
                resource_data.get(
                    "capabilities",
                    [],
                )
            ),
            attributes=self._build_attributes(
                resource_data.get(
                    "attributes",
                    {},
                )
            ),
            relationships=frozenset(
                resource_data.get(
                    "relationships",
                    [],
                )
            ),
            aliases=tuple(
                resource_data.get(
                    "aliases",
                    [],
                )
            ),
            metadata=MappingProxyType(
                resource_data.get(
                    "metadata",
                    {},
                ),
            ),
        )

    def _build_attributes(
        self,
        attributes: dict[str, Any],
    ) -> Mapping[str, AttributeDefinition]:
        """
        Convert attribute definitions from YAML into
        AttributeDefinition objects.
        """

        definitions: dict[str, AttributeDefinition] = {}

        for (
            attribute_name,
            attribute_data,
        ) in attributes.items():

            definitions[attribute_name] = AttributeDefinition(
                name=attribute_data["name"],
                type=AttributeType(
                    attribute_data["type"],
                ),
                default=attribute_data.get(
                    "default",
                ),
                description=attribute_data.get(
                    "description",
                    "",
                ),
            )

        return MappingProxyType(definitions)

    def _parse_kind(
        self,
        resource_data: dict[str, Any],
    ) -> ResourceKind:
        """
        Parse the resource kind from the catalog entry.
        """

        return ResourceKind(
            resource_data["kind"],
        )

    def _parse_canonical_type(
        self,
        resource_data: dict[str, Any],
    ) -> CanonicalType:
        """
        Parse the canonical resource type from the catalog entry.
        """

        return CanonicalType(
            resource_data["canonical_type"],
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

    def _validate_resource(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:
        """
        Validate a catalog resource before constructing a ResourceDefinition.

        TODO (Future):
        - Verify all required fields exist.
        - Validate ResourceKind values.
        - Validate CanonicalType values.
        - Validate AttributeType values.
        - Ensure aliases are unique.
        - Ensure capability names are valid.
        - Validate relationship names.
        - Detect duplicate canonical resources.
        - Raise CatalogValidationError for invalid catalog entries.
        """

        pass
