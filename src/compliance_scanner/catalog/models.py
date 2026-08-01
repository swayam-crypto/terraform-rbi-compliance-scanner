from dataclasses import dataclass, field


@dataclass(frozen=True)
class ResourceDefinition:
    """
    Canonical description of a cloud resource.

    Multiple IaC resource types may map to the same logical resource.
    """

    canonical_type: str

    provider: str

    service: str

    aliases: tuple[str, ...] = ()

    capabilities: frozenset[str] = field(
        default_factory=frozenset,
    )
