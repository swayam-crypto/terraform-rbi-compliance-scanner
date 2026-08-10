from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.registry import CatalogRegistry
from compliance_scanner.models.resolved_resource import ResolvedResource


class Catalog:
    """
    Public API for the resource catalog.

    Consumers should use this class instead of accessing the
    registry directly.
    """

    def __init__(
        self,
        registry: CatalogRegistry,
    ):
        self.registry = registry

    def definition(
        self,
        resource: ResolvedResource,
    ) -> ResourceDefinition | None:
        """
        Return the catalog definition for a resource.
        """

        definition = self.registry.get(resource.resource_type)

        return self.registry.get(
            resource.resource_type,
        )

    def has_capability(
        self,
        resource: ResolvedResource,
        capability: str,
    ) -> bool:
        """
        Return True if the resource has the given capability.
        """
        definition = self.definition(resource)

        if definition is None:
            return False

        return capability in definition.capabilities

    def has_capabilities(
        self,
        resource: ResolvedResource,
        capabilities: frozenset[str],
    ) -> bool:
        """Return whether a resource declares every requested capability."""
        definition = self.definition(resource)
        return definition is not None and capabilities.issubset(definition.capabilities)

    def attribute_name(
        self,
        resource: ResolvedResource,
        attribute_key: str,
    ) -> str | None:
        """Resolve a canonical catalog attribute key to a provider attribute name."""
        definition = self.definition(resource)
        if definition is None:
            return None

        attribute = definition.attributes.get(attribute_key)
        return attribute.name if attribute else None

    def canonical_type(
        self,
        resource: ResolvedResource,
    ) -> str | None:
        """
        Return the canonical type of a resource.
        """
        definition = self.definition(resource)

        if definition is None:
            return None

        return definition.canonical_type

    def provider(
        self,
        resource: ResolvedResource,
    ) -> str | None:
        """
        Return the provider of a resource.
        """
        definition = self.definition(resource)

        if definition is None:
            return None

        return definition.provider

    def service(
        self,
        resource: ResolvedResource,
    ) -> str | None:
        """
        Return the cloud service of a resource.
        """
        definition = self.definition(resource)

        if definition is None:
            return None

        return definition.service

    def aliases(
        self,
        resource: ResolvedResource,
    ) -> tuple[str, ...]:
        """
        Return all aliases for a resource.
        """
        definition = self.definition(resource)

        if definition is None:
            return ()

        return definition.aliases

    def relationships(
        self,
        resource: ResolvedResource,
    ) -> frozenset[str]:
        """
        Return all known relationship types for a resource.
        """
        definition = self.definition(resource)

        if definition is None:
            return frozenset()

        return definition.relationships
