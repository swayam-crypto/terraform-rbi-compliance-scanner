"""
Production rule registry. Import every rule here so the scan engine can
discover them automatically without you editing engine code each time you add
one.

``GRAPH_RULES`` is the sole graph-rule registry executed by production scans.
The similarly named collection in ``compliance_scanner.graph_rules`` is an
experimental/future-only rule-pack surface and is intentionally not imported
here.

To add a new rule:
1. Create a new file in this folder, e.g. audit_logging.py
2. Define a class inheriting BaseRule
3. Import it below and add it to ALL_RULES
"""

from .data_localization import DataLocalizationRule
from .encryption import EncryptionAtRestRule
from .audit_logging import AuditLogRetentionRule
from .network_exposure import NetworkExposureRule
from .access_control import LeastPrivilegeRule
from .graph_base import GraphRule
from .kms_dependency import KMSDependencyRule
from .baseline import (
    BASELINE_RULES,
    RDP_RESTRICTION_RULE,
    SSH_RESTRICTION_RULE,
    UnrestrictedIngressRule,
)

ALL_RULES = [
    DataLocalizationRule(),
    EncryptionAtRestRule(),
    AuditLogRetentionRule(),
    NetworkExposureRule(),
    LeastPrivilegeRule(),
    *BASELINE_RULES,
    SSH_RESTRICTION_RULE,
    RDP_RESTRICTION_RULE,
    UnrestrictedIngressRule(),
]

GRAPH_RULES = [
    # Production graph-rule registry consumed by core.scan_engine.
    KMSDependencyRule(),
]
