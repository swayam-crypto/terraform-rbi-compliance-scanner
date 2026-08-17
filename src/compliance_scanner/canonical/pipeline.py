from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.canonical.builder import CanonicalResourceBuilder
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.canonical.exceptions import (
    UnknownCanonicalResourceError,
)
from compliance_scanner.canonical.context import CanonicalContext
from compliance_scanner.canonical.attribute_mapper import (
    CanonicalAttributeMapper,
)


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
        attribute_mapper: CanonicalAttributeMapper,
    ) -> None:
        self._catalog = catalog
        self._builder = builder
        self._attribute_mapper = attribute_mapper

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

        self._attribute_mapper.map(
            context,
        )

        return self._builder.build(
            context,
        )
