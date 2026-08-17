from dataclasses import dataclass
from typing import Any, Mapping

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.source_location import SourceLocation


@dataclass(frozen=True)
class CanonicalResource:
    """
    Provider-independent semantic representation of a cloud resource.

    Produced by the Canonical Cloud Model Pipeline and consumed by
    the Compliance Engine and other platform components.
    """

    platform: Platform
    provider: CloudProvider

    canonical_type: CanonicalType

    resource_name: str

    attributes: Mapping[str, Any]

    capabilities: frozenset[str]

    metadata: Mapping[str, Any]

    source: SourceLocation
