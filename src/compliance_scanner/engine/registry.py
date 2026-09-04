from compliance_scanner.engine.attack.engine import AttackPathEngine
from compliance_scanner.engine.blast_radius.engine import BlastRadiusEngine
from compliance_scanner.engine.identity.engine import IdentityEngine

ANALYSIS_ENGINES = (
    AttackPathEngine,
    BlastRadiusEngine,
    IdentityEngine,
)
