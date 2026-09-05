from compliance_scanner.runtime import RuntimeBuilder
from compliance_scanner.engine.risk.collection import RiskCollection


def test_runtime_populates_risk_analysis():

    context = RuntimeBuilder().build([])

    assert context.analysis.risk is not None

    assert isinstance(
        context.analysis.risk,
        RiskCollection,
    )

    assert context.analysis.risk.findings == ()
