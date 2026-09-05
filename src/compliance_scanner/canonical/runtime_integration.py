from collections.abc import Iterable

from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.canonical.attribute_mapper import CanonicalAttributeMapper
from compliance_scanner.canonical.builder import CanonicalResourceBuilder
from compliance_scanner.canonical.pipeline import CanonicalPipeline
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.models.resolved_resource import ResolvedResource

_PIPELINE = CanonicalPipeline(
    catalog=catalog,
    builder=CanonicalResourceBuilder(),
    attribute_mapper=CanonicalAttributeMapper(),
)


def build_canonical_resources(
    resources: Iterable[ResolvedResource],
) -> tuple[CanonicalResource, ...]:
    """
    Transform resolved resources into immutable canonical resources.
    """

    return tuple(_PIPELINE.transform(resource) for resource in resources)
