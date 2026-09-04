from compliance_scanner.engine.attack.engine import AttackPathEngine
from compliance_scanner.engine.blast_radius.engine import BlastRadiusEngine
from compliance_scanner.engine.identity.engine import IdentityEngine

from compliance_scanner.runtime.analysis_runtime import AnalysisRuntime
from compliance_scanner.runtime.scan_context import ScanContext


class AnalysisBuilder:
    """
    Executes runtime analysis engines and produces
    the AnalysisRuntime.
    """

    def build(
        self,
        context: ScanContext,
    ) -> AnalysisRuntime:

        analysis = context.analysis

        analysis.attack_paths = AttackPathEngine(
            context,
        ).analyze()

        analysis.blast_radius = BlastRadiusEngine(
            context,
        ).analyze()

        analysis.identity_analysis = IdentityEngine(
            context,
        ).analyze()

        return analysis
