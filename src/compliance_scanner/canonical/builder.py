from types import MappingProxyType

from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.canonical.context import CanonicalContext


class CanonicalResourceBuilder:
    """
    Builds immutable CanonicalResource objects from parser output
    and catalog definitions.
    """

    def build(
        self,
        context: CanonicalContext,
    ) -> CanonicalResource:
        resource = context.resource
        definition = context.definition

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
