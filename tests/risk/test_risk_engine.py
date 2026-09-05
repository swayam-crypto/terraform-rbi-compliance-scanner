from compliance_scanner.engine.risk.collection import RiskCollection
from compliance_scanner.engine.risk.engine import RiskEngine
from compliance_scanner.runtime import RuntimeBuilder
from compliance_scanner.engine.risk.models import (
    RiskFinding,
    RiskLevel,
)


def test_risk_engine_returns_empty_collection():

    context = RuntimeBuilder().build([])

    result = RiskEngine(context).analyze()

    assert isinstance(result, RiskCollection)

    assert result.findings == ()
