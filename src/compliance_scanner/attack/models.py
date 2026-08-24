from dataclasses import dataclass

from compliance_scanner.graph.relationship import Relationship
from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass(frozen=True, slots=True)
class AttackPath:
    """
    Represents one attack path through the infrastructure graph.

    An AttackPath describes an ordered sequence of infrastructure
    relationships that allow an attacker to move from one resource
    to another.

    The model is intentionally infrastructure-focused.

    It does not include compliance information, risk scoring,
    severity or exploit metadata.

    Those concerns belong to higher analysis layers.
    """

    source: ResolvedResource

    target: ResolvedResource

    resources: tuple[ResolvedResource, ...]

    relationships: tuple[Relationship, ...]
