"""
Rule registry. Import every rule here so the scan engine can discover
them automatically without you editing engine code each time you add one.

To add a new rule:
1. Create a new file in this folder, e.g. audit_logging.py
2. Define a class inheriting BaseRule
3. Import it below and add it to ALL_RULES
"""

from .data_localization import DataLocalizationRule
from .encryption import EncryptionAtRestRule
from .audit_logging import AuditLogRetentionRule

ALL_RULES = [
    DataLocalizationRule(),
    EncryptionAtRestRule(),
    AuditLogRetentionRule(),
]
