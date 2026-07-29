# Terraform RBI Compliance Scanner

[![PyPI version](https://img.shields.io/pypi/v/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![Python](https://img.shields.io/pypi/pyversions/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Terraform static analysis tool that checks Infrastructure as Code (IaC) against **Reserve Bank of India (RBI)** cybersecurity guidance and **India's Digital Personal Data Protection Act (DPDPA)** requirements.

Unlike traditional IaC security scanners, this project focuses on **regulatory compliance**, helping developers identify infrastructure configurations that may violate Indian financial and data protection requirements before deployment.

---

# Why this project exists

Most Infrastructure-as-Code scanners answer questions like:

> "Is this S3 bucket publicly accessible?"

This scanner answers questions like:

> "Does this infrastructure comply with RBI cybersecurity guidance and India's DPDPA requirements?"

Those are very different problems.

Existing tools such as **Checkov**, **tfsec**, and **Terrascan** primarily detect cloud security misconfigurations. They generally do not encode India-specific regulatory requirements such as data localization, financial data protection, or compliance-focused infrastructure rules.

This project fills that gap.

---

# Features

- RBI-focused Terraform compliance checks
- DPDPA-aware infrastructure validation
- Terraform static analysis
- Terraform Plan (`tfplan.json`) scanning
- Human-readable CLI output
- JSON reporting
- SARIF reporting (GitHub Code Scanning compatible)
- Parallel scanning for large repositories
- Incremental scan cache
- Streaming scan mode
- Inline suppression comments
- Python API
- Command-line interface
- CI/CD friendly
- Published on PyPI

---

# Installation

```bash
pip install rbi-compliance-scanner
```

---

# Quick Start

Scan a Terraform project:

```bash
rbi-scan --path ./examples/sample_infra
```

Or use it as a Python library:

```python
import compliance_scanner as rbi

findings = rbi.scan("./my-terraform-project")

for finding in findings:
    print(
        finding.severity,
        finding.rule_id,
        finding.message
    )
```

---

# Example Output

```text
3 compliance violation(s) found:

[CRITICAL] RBI-001 — aws_s3_bucket.customer_transactions

Resource 'customer_transactions' appears to hold sensitive financial
or customer data but is provisioned in 'us-east-1', outside India.

RBI data localization guidance likely requires deployment in
ap-south-1 or ap-south-2.

Reference:
RBI Cybersecurity Framework — Data Localization
```

---

# Rules Implemented

Current compliance rules include:

- ✅ RBI-001 – Data Localization
- ✅ RBI-002 – Encryption
- ✅ RBI-003 – Audit Logging
- ✅ RBI-004 – Network Exposure
- ✅ RBI-005 – IAM Least Privilege

See **docs/RULES.md** for:

- Complete rule descriptions
- Severity levels
- Regulatory references
- Future roadmap

---

# Suppressing False Positives

Suppress an individual rule:

```hcl
# rbi-scan:ignore RBI-001 reason="Internal logs bucket"

resource "aws_s3_bucket" "internal_logs" {
    ...
}
```

Suppress every rule for a resource:

```hcl
# rbi-scan:ignore-all reason="Legacy infrastructure"

resource "aws_s3_bucket" "legacy_bucket" {
    ...
}
```

Suppressed findings are **not silently ignored**.

The scanner reports the total number of suppressed findings so reviewers can identify where suppressions are being used.

---

# Output Formats

The scanner currently supports:

- Human-readable CLI output
- JSON
- SARIF (GitHub Code Scanning compatible)

---

# Performance

Designed for both small Terraform projects and enterprise-scale repositories.

Features include:

- Parallel parsing
- Incremental file cache
- Streaming scan mode
- Constant-memory scanning for large repositories

Example:

```python
for finding in rbi.scan_large("./large-terraform-repository"):
    print(finding.rule_id, finding.message)
```

---

# Architecture

```text
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
Resolved Resources
        │
        ▼
Rule Engine
        │
        ▼
Compliance Findings
        │
 ┌──────┴──────────┐
 │                 │
 ▼                 ▼
JSON             SARIF
```

For implementation details, see:

```
docs/ARCHITECTURE.md
```

---

# CI/CD Integration

The repository includes GitHub Actions workflows.

### Continuous Integration

```
.github/workflows/scan.yml
```

Runs:

- Unit tests
- Compliance scans
- Sample infrastructure validation

### Continuous Delivery

```
.github/workflows/publish.yml
```

Automatically publishes releases to **PyPI** using Trusted Publishing whenever a GitHub Release is published.

---

# Running From Source

Clone the repository:

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git

cd terraform-rbi-compliance-scanner
```

Install the project:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
pytest
```

---

# Roadmap

Current progress:

- ✅ RBI Data Localization
- ✅ Encryption Validation
- ✅ Audit Logging
- ✅ Network Exposure
- ✅ IAM Least Privilege
- 🚧 Cross-Resource Compliance Analysis
- ⏳ Additional RBI Controls
- ⏳ Azure Support
- ⏳ GCP Support

---

# Status

- ✅ Published on PyPI
- ✅ Active development
- ✅ Open Source (MIT License)
- ✅ Community contributions welcome

---

# Disclaimer

This project helps automate infrastructure compliance checks but **does not guarantee regulatory compliance**.

Actual compliance depends on infrastructure configuration, organizational processes, operational controls, and regulatory interpretation.

Always validate findings with your security or compliance team before relying on them for production decisions.

---

# License

MIT License