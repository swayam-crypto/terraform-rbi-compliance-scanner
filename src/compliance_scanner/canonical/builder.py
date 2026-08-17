from types import MappingProxyType
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.models.resolved_resource import ResolvedResource


class CanonicalResourceBuilder:
    """
    Builds immutable CanonicalResource objects from parser output
    and catalog definitions.
    """

    def build(
        self,
        resource: ResolvedResource,
        definition: ResourceDefinition,
    ) -> CanonicalResource:

        return CanonicalResource(
            platform=resource.platform,
            provider=resource.provider,
            canonical_type=definition.canonical_type,
            resource_name=resource.resource_name,
            attributes=MappingProxyType(dict(resource.attributes)),
            capabilities=definition.capabilities,
            metadata=definition.metadata,
            source=resource.source,
        )
