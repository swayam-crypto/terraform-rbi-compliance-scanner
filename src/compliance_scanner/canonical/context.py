from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from compliance_scanner.catalog.models import ResourceDefinition
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass
class CanonicalContext:
    """
    Shared transformation context for the Canonical Cloud Model Pipeline.

    Each pipeline stage enriches this context with additional semantic
    information before the CanonicalBuilder constructs the final
    CanonicalResource.
    """

    resource: ResolvedResource

    definition: ResourceDefinition

    canonical_type: CanonicalType | None = None

    canonical_attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
