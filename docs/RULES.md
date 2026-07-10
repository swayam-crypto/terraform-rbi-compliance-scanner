# Compliance rules

Each rule maps a specific, checkable technical requirement to RBI/CERT-In
cybersecurity guidance or India's Digital Personal Data Protection Act
(DPDPA). Rules fall into two honestly-different categories:

**Specific numeric mandates** — a real regulation states an exact,
checkable requirement (e.g., "180 days"). These citations point to the
actual circular/direction.

**Principle-based interpretations** — a regulation states a broad
requirement (e.g., "have access controls") without a single checkable
number. These rules are a defensible technical interpretation of that
principle, not a citation of an exact rule. This distinction is called
out explicitly in each rule file's docstring and below.

**Important:** verify wording against the current RBI framework, CERT-In
directions, and DPDPA text before relying on this tool for real
compliance decisions. This is a portfolio/learning project, not legal
advice.

| Rule ID | Name | Severity | Type | Regulation |
|---------|------|----------|------|------------|
| RBI-001 | Data localization | Critical | Specific | RBI Circular DPSS.CO.OD.No.2785/06.08.005/2017-2018 (Apr 2018) — payment system data must be stored only in India |
| RBI-002 | Encryption at rest | High | Principle-based | RBI Cyber Security Framework (2016) — data protection expectation |
| RBI-003 | Audit log retention (180 days) | High | **Specific** | CERT-In Cybersecurity Directions 2022, Direction (iv), issued under IT Act Section 70B(6) — ICT logs must be retained 180 days within Indian jurisdiction |
| RBI-004 | Network exposure (no public access for sensitive data) | Critical | Principle-based | RBI Cyber Security Framework (2016) access controls + DPDPA 2023 Section 8(5) reasonable security safeguards |
| RBI-005 | Least privilege (no wildcard IAM) | High | Principle-based | RBI Cyber Security Framework (2016) — Access Control principle |

## Planned for later versions

- **RBI-006 — MFA enforcement:** IAM account password policy should require MFA for console access
- **RBI-007 — Clock synchronization:** flag infrastructure not configured to sync with NIC/NPL NTP servers (CERT-In Directions 2022) — genuinely hard to check via Terraform alone since this is usually an OS-level config, worth researching further before implementing

## Adding a new rule

1. Create `src/compliance_scanner/rules/your_rule_name.py`
2. Subclass `BaseRule` from `rules/base.py`
3. Implement `check()` — return a `Finding` on violation, `None` if compliant
4. **Be honest in the docstring** about whether this maps to a specific numeric regulation or is a principle-based interpretation — see RBI-003 vs RBI-004 for the pattern
5. Register it in `src/compliance_scanner/rules/__init__.py`
6. Add tests in its own file under `tests/test_rules/`
7. Document it in the table above

