from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.models.resolved_resource import ResolvedResource

from compliance_scanner.canonical.exceptions import (
    UnknownCanonicalResourceError,
)


class ResourceClassifier:
    """
    Classifies resolved resources into their canonical cloud type.

    The classifier is intentionally stateless. All semantic knowledge
    is provided by the Catalog.
    """

    def __init__(
        self,
        catalog: Catalog,
    ) -> None:
        self._catalog = catalog

    def classify(
        self,
        resource: ResolvedResource,
    ) -> CanonicalType:
        """
        Return the canonical type for a resolved resource.

        Raises:
            KeyError: if the resource is not defined in the catalog.
        """

        definition = self._catalog.definition(resource)

        if definition is None:
            raise UnknownCanonicalResourceError(
                resource.resource_type,
            )

        return definition.canonical_type
