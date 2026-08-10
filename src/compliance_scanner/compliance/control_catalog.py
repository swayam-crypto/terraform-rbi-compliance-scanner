"""The initial v0.8 control catalog.

These controls deliberately contain no AWS or Terraform vocabulary. Provider
specific detection remains in rule implementations and resource catalogs.
"""

from .controls import ComplianceControl, FrameworkMapping


DATA_RESIDENCY = ComplianceControl(
    control_id="CCIP-DATA-RESIDENCY-001",
    title="Regulated data must remain in an approved jurisdiction",
    category="data_protection",
    severity="critical",
    remediation="Store regulated data only in an approved region and declare the region explicitly.",
    framework_mappings=(
        FrameworkMapping("RBI", "Data localization", "RBI Cyber Security Framework — Data Localization requirement"),
        FrameworkMapping("DPDP", "Cross-border data processing", "Digital Personal Data Protection Act 2023"),
    ),
)

ENCRYPTION_AT_REST = ComplianceControl(
    control_id="CCIP-ENCRYPTION-AT-REST-001",
    title="Data stores must encrypt data at rest",
    category="data_protection",
    severity="high",
    remediation="Enable encryption at rest and use a managed customer or provider key according to policy.",
    framework_mappings=(
        FrameworkMapping("RBI", "Data protection", "RBI Cybersecurity Framework — Data Protection requirement"),
        FrameworkMapping("DPDP", "Reasonable security safeguards", "DPDP Act 2023, Section 8(5)"),
        FrameworkMapping("CIS", "Data protection", "CIS cloud provider benchmarks — encryption at rest controls"),
    ),
)

AUDIT_LOG_RETENTION = ComplianceControl(
    control_id="CCIP-AUDIT-LOG-RETENTION-001",
    title="Security logs must meet the minimum retention period",
    category="logging_monitoring",
    severity="high",
    remediation="Set log retention to at least 180 days and protect logs from unauthorized alteration.",
    framework_mappings=(
        FrameworkMapping("CERT-In", "ICT log retention", "CERT-In Cybersecurity Directions 2022, Direction (iv)"),
        FrameworkMapping("RBI", "Security monitoring", "RBI Cyber Security Framework — audit and monitoring expectations"),
    ),
)

PUBLIC_SENSITIVE_DATA = ComplianceControl(
    control_id="CCIP-PUBLIC-SENSITIVE-DATA-001",
    title="Sensitive data stores must not be publicly accessible",
    category="network_security",
    severity="critical",
    remediation="Remove public access, restrict network paths to approved principals, and verify access controls.",
    framework_mappings=(
        FrameworkMapping("RBI", "Access control", "RBI Cyber Security Framework (2016) access control expectations"),
        FrameworkMapping("DPDP", "Reasonable security safeguards", "DPDP Act 2023, Section 8(5)"),
        FrameworkMapping("CIS", "Public access prevention", "CIS cloud provider benchmarks — public exposure controls"),
    ),
)

LEAST_PRIVILEGE = ComplianceControl(
    control_id="CCIP-LEAST-PRIVILEGE-001",
    title="Identity policies must enforce least privilege",
    category="identity_access_management",
    severity="high",
    remediation="Replace wildcard permissions with the minimum scoped actions and resources required.",
    framework_mappings=(
        FrameworkMapping("RBI", "Access control", "RBI Cyber Security Framework (2016) least-privilege expectations"),
        FrameworkMapping("CIS", "IAM least privilege", "CIS cloud provider benchmarks — IAM controls"),
    ),
)
