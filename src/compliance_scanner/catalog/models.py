from dataclasses import dataclass, field
from typing import Any, Mapping

from compliance_scanner.catalog.attributes import AttributeDefinition
from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.catalog.kinds import ResourceKind


@dataclass(frozen=True)
class ResourceDefinition:
    """
    Canonical provider-independent description of a cloud resource.

    The catalog exists to translate provider-specific resources into
    normalized concepts that the compliance engine can reason about.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    provider: str

    service: str

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    kind: ResourceKind

    canonical_type: CanonicalType

    # Optional identity

    display_name: str = ""

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    capabilities: frozenset[str] = field(
        default_factory=frozenset,
    )

    # ------------------------------------------------------------------
    # Compliance Attributes
    # ------------------------------------------------------------------

    attributes: Mapping[str, AttributeDefinition] = field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    relationships: frozenset[str] = field(
        default_factory=frozenset,
    )

    # ------------------------------------------------------------------
    # Aliases
    # ------------------------------------------------------------------

    aliases: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )
