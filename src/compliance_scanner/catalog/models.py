from dataclasses import dataclass, field


@dataclass(frozen=True)
class ResourceDefinition:
    """
    Canonical description of a cloud resource.
    """

    canonical_type: str

    provider: str

    service: str

    capabilities: frozenset[str] = field(
        default_factory=frozenset,
    )

    aliases: tuple[str, ...] = ()

    relationships: frozenset[str] = field(
        default_factory=frozenset,
    )
