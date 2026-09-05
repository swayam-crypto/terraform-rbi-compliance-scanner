from __future__ import annotations

from dataclasses import dataclass

from compliance_scanner.engine.attack.collection import (
    AttackPathCollection,
)
from compliance_scanner.engine.blast_radius.collection import (
    BlastRadiusCollection,
)
from compliance_scanner.engine.identity.collection import (
    IdentityCollection,
)
from compliance_scanner.engine.risk.collection import RiskCollection


@dataclass(slots=True)
class AnalysisRuntime:
    """
    Results produced by analysis engines.

    These are conclusions derived from the knowledge runtime.
    """

    attack_paths: AttackPathCollection | None = None

    blast_radius: BlastRadiusCollection | None = None

    identity_analysis: IdentityCollection | None = None

    risk: RiskCollection | None = None
