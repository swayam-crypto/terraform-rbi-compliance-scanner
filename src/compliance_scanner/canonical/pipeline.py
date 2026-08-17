from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.canonical.builder import CanonicalResourceBuilder
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.canonical.exceptions import (
    UnknownCanonicalResourceError,
)
from compliance_scanner.canonical.context import CanonicalContext


class CanonicalPipeline:
    """
    Transforms parser output into the Canonical Cloud Model.

    The pipeline orchestrates the transformation by combining
    parser output with semantic knowledge from the Catalog.
    """

    def __init__(
        self,
        catalog: Catalog,
        builder: CanonicalResourceBuilder,
    ) -> None:
        self._catalog = catalog
        self._builder = builder

    def transform(
        self,
        resource: ResolvedResource,
    ) -> CanonicalResource:

        definition = self._catalog.definition(resource)
        if definition is None:
            raise UnknownCanonicalResourceError(
                resource.resource_type,
            )
        context = CanonicalContext(
            resource=resource,
            definition=definition,
        )

        return self._builder.build(context)
