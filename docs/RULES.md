# Compliance rules

Each rule maps a specific, checkable technical requirement to a general
principle from RBI's cybersecurity guidance for regulated entities and
India's Digital Personal Data Protection Act (DPDPA).

**Important:** these rules are a starting technical interpretation, not
legal advice. Verify wording against the current RBI framework and DPDPA
text before relying on this tool for real compliance decisions.

| Rule ID | Name | Severity | What it checks |
|---------|------|----------|-----------------|
| RBI-001 | Data localization | Critical | Resources tagged/named as holding financial or customer data must be in an Indian AWS region (ap-south-1/ap-south-2) |
| RBI-002 | Encryption at rest | High | S3/RDS/DynamoDB resources must have encryption explicitly configured |

## Planned rules (not yet implemented)

- **RBI-003 — Audit log retention:** CloudTrail/logging resources must retain logs for a minimum period
- **RBI-004 — Access control:** IAM policies attached to sensitive resources must not grant wildcard (`*`) actions
- **RBI-005 — Network exposure:** Databases/storage holding sensitive data must not be publicly accessible
- **RBI-006 — MFA enforcement:** IAM users with console access must have MFA configured

## Adding a new rule

1. Create `src/compliance_scanner/rules/your_rule_name.py`
2. Subclass `BaseRule` from `rules/base.py`
3. Implement `check()` — return a `Finding` on violation, `None` if compliant
4. Register it in `src/compliance_scanner/rules/__init__.py`
5. Add tests in `tests/test_rules/`
6. Document it in the table above
