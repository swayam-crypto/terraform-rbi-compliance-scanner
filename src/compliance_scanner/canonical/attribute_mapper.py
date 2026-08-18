from types import MappingProxyType
from typing import Any, Mapping

from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.canonical.context import CanonicalContext


class CanonicalAttributeMapper:
    """
    Maps provider-specific attributes into canonical attribute names
    using catalog attribute definitions.
    """

    def map(
        self,
        context: CanonicalContext,
    ) -> None:

        resource = context.resource
        definition: ResourceDefinition = context.definition

        canonical_attributes: dict[str, Any] = {}

        for (
            canonical_name,
            attribute_definition,
        ) in definition.attributes.items():

            canonical_attributes[canonical_name] = resource.get(
                attribute_definition.name,
                attribute_definition.default,
            )

        context.canonical_attributes = MappingProxyType(
            canonical_attributes,
        )
