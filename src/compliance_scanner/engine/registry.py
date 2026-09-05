from compliance_scanner.engine.attack.engine import AttackPathEngine
from compliance_scanner.engine.base import AnalysisEngine
from compliance_scanner.engine.blast_radius.engine import BlastRadiusEngine
from compliance_scanner.engine.identity.engine import IdentityEngine
from compliance_scanner.engine.risk.engine import RiskEngine

ANALYSIS_ENGINES: tuple[type[AnalysisEngine], ...] = (
    AttackPathEngine,
    BlastRadiusEngine,
    IdentityEngine,
    RiskEngine,
)
