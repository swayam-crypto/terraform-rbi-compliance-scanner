from compliance_scanner.runtime.analysis_runtime import AnalysisRuntime
from compliance_scanner.runtime.scan_context import ScanContext
from compliance_scanner.engine.registry import ANALYSIS_ENGINES


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

        for engine_cls in ANALYSIS_ENGINES:

            engine = engine_cls(context)

            result = engine.analyze()

            setattr(
                analysis,
                engine.runtime_field,
                result,
            )

        return analysis
