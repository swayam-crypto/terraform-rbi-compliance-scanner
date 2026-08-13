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
from compliance_scanner.catalog.exceptions import CatalogValidationError

from compliance_scanner.catalog.relationships import (
    RelationshipDefinition,
    RelationshipType,
)


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

            relationship_data = attribute_data.get("relationship")

            definitions[attribute_name] = AttributeDefinition(
                name=attribute_data["name"],
                type=AttributeType(attribute_data["type"]),
                default=attribute_data.get("default"),
                description=attribute_data.get("description", ""),
                relationship=(
                    RelationshipDefinition(
                        relationship_type=RelationshipType(
                            relationship_data["type"],
                        ),
                        target=CanonicalType(
                            relationship_data["target"],
                        ),
                        required=relationship_data.get(
                            "required",
                            False,
                        ),
                    )
                    if relationship_data
                    else None
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

        for yaml_file in Path(directory).rglob("*.yaml"):
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
        """

        self._validate_required_fields(
            resource_type,
            resource_data,
        )

        self._validate_kind(
            resource_type,
            resource_data,
        )

        self._validate_canonical_type(
            resource_type,
            resource_data,
        )

        self._validate_attributes(
            resource_type,
            resource_data,
        )

        self._validate_capabilities(
            resource_type,
            resource_data,
        )

        self._validate_relationships(
            resource_type,
            resource_data,
        )

        self._validate_aliases(
            resource_type,
            resource_data,
        )

    def _validate_required_fields(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:

        required = (
            "provider",
            "service",
            "display_name",
            "kind",
            "canonical_type",
        )

        for field in required:

            if field not in resource_data:

                raise ValueError(f"{resource_type}: missing required field '{field}'.")

            value = resource_data[field]

            if value is None:

                raise ValueError(f"{resource_type}: field '{field}' cannot be null.")

            if isinstance(value, str) and not value.strip():

                raise ValueError(f"{resource_type}: field '{field}' cannot be empty.")

    def _validate_kind(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:

        try:

            ResourceKind(
                resource_data["kind"],
            )

        except ValueError as error:

            raise CatalogValidationError(
                resource=resource_type,
                field="kind",
                value=resource_data["kind"],
                reason="Unknown resource kind.",
                expected=", ".join(kind.value for kind in ResourceKind),
            ) from error

    def _validate_canonical_type(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:

        try:

            CanonicalType(
                resource_data["canonical_type"],
            )

        except ValueError as error:

            raise CatalogValidationError(
                resource=resource_type,
                field="canonical_type",
                value=resource_data["canonical_type"],
                reason="Unknown canonical type.",
                expected=", ".join(value.value for value in CanonicalType),
            ) from error

    def _validate_attributes(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:

        attributes = resource_data.get(
            "attributes",
            {},
        )

        names: set[str] = set()

        for key, attribute in attributes.items():

            if "name" not in attribute:

                raise ValueError(f"{resource_type}.{key}: missing attribute name.")

            if not str(attribute["name"]).strip():

                raise ValueError(
                    f"{resource_type}.{key}: attribute name cannot be empty."
                )

            if "type" not in attribute:

                raise ValueError(f"{resource_type}.{key}: missing attribute type.")

            if not str(attribute["type"]).strip():

                raise ValueError(
                    f"{resource_type}.{key}: attribute type cannot be empty."
                )

            try:

                AttributeType(
                    attribute["type"],
                )

            except ValueError as error:

                raise CatalogValidationError(
                    resource=resource_type,
                    field=f"attributes.{key}.type",
                    value=attribute["type"],
                    reason="Unknown attribute type.",
                    expected=", ".join(value.value for value in AttributeType),
                ) from error

            if attribute["name"] in names:

                raise CatalogValidationError(
                    resource=resource_type,
                    field="attributes",
                    value=attribute["name"],
                    reason="Duplicate attribute name.",
                )

            names.add(
                attribute["name"],
            )

    def _validate_aliases(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:

        aliases = resource_data.get(
            "aliases",
            [],
        )

        if len(aliases) != len(set(aliases)):

            raise CatalogValidationError(
                resource=resource_type,
                field="aliases",
                reason="Duplicate aliases detected.",
            )

    def _validate_capabilities(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:
        """Validate the optional capability collection without constraining vocabulary."""
        capabilities = resource_data.get("capabilities", [])

        if not isinstance(capabilities, list):
            raise CatalogValidationError(
                resource=resource_type,
                field="capabilities",
                value=capabilities,
                reason="Capabilities must be a list of strings.",
            )

        for capability in capabilities:
            if not isinstance(capability, str) or not capability.strip():
                raise CatalogValidationError(
                    resource=resource_type,
                    field="capabilities",
                    value=capability,
                    reason="Capability entries must be non-empty strings.",
                )

    def _validate_relationships(
        self,
        resource_type: str,
        resource_data: dict[str, Any],
    ) -> None:
        """Validate the structure of descriptive resource-level relationship metadata."""
        relationships = resource_data.get("relationships", [])

        if not isinstance(relationships, list):
            raise CatalogValidationError(
                resource=resource_type,
                field="relationships",
                value=relationships,
                reason="Relationships must be a list of strings.",
            )

        for relationship in relationships:
            if not isinstance(relationship, str) or not relationship.strip():
                raise CatalogValidationError(
                    resource=resource_type,
                    field="relationships",
                    value=relationship,
                    reason="Relationship entries must be strings.",
                )

        if len(relationships) != len(set(relationships)):
            raise CatalogValidationError(
                resource=resource_type,
                field="relationships",
                reason="Duplicate relationship entries detected.",
            )
