from dataclasses import dataclass

from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass(frozen=True, slots=True)
class BlastRadius:
    """
    Resources reachable from a compromised source resource.
    """

    source: ResolvedResource

    affected_resources: tuple[ResolvedResource, ...]
