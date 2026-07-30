# Terraform RBI Compliance Scanner

[![PyPI version](https://img.shields.io/pypi/v/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![Python](https://img.shields.io/pypi/pyversions/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Terraform static analysis tool that validates Infrastructure as Code (IaC) against **Reserve Bank of India (RBI)** cybersecurity guidance and **India's Digital Personal Data Protection Act (DPDPA)** requirements.

Unlike traditional Infrastructure-as-Code security scanners, this project focuses on **regulatory compliance**, helping engineering teams identify infrastructure configurations that may violate Indian financial and data protection regulations before deployment.

---

# Why this project exists

Most Infrastructure-as-Code scanners answer questions like:

> "Is this infrastructure secure?"

This project answers questions like:

> "Is this infrastructure compliant with RBI cybersecurity guidance and India's DPDPA requirements?"

Those are fundamentally different problems.

Existing tools such as **Checkov**, **tfsec**, and **Terrascan** primarily detect cloud security misconfigurations. They generally do not encode India-specific regulatory requirements such as:

- Data localization
- Financial data protection
- Infrastructure compliance controls
- Regulatory audit requirements

This project aims to bridge that gap.

---

# Features

- RBI-focused Terraform compliance checks
- DPDPA-aware infrastructure validation
- Terraform static analysis
- Terraform Plan (`tfplan.json`) scanning
- Human-readable CLI output
- JSON reporting
- SARIF reporting (GitHub Code Scanning compatible)
- Parallel scanning
- Streaming scan mode
- Incremental scan cache
- Inline suppression comments
- Python API
- Command-line interface
- CI/CD friendly
- Published on PyPI
- Extensible rule engine
- Foundation for graph-based infrastructure analysis

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
```

---

# Implemented Compliance Rules

- ✅ RBI-001 – Data Localization
- ✅ RBI-002 – Encryption at Rest
- ✅ RBI-003 – Audit Log Retention
- ✅ RBI-004 – Network Exposure
- ✅ RBI-005 – IAM Least Privilege

See `docs/RULES.md` for complete rule documentation and regulatory references.

---

# Suppressing Findings

Suppress an individual rule:

```hcl
# rbi-scan:ignore RBI-001 reason="Internal logs bucket"

resource "aws_s3_bucket" "internal_logs" {
    ...
}
```

Suppress all rules for a resource:

```hcl
# rbi-scan:ignore-all reason="Legacy infrastructure"

resource "aws_s3_bucket" "legacy_bucket" {
    ...
}
```

Suppressed findings remain visible through suppression statistics to maintain audit transparency.

---

# Output Formats

Supported output formats:

- Human-readable CLI
- JSON
- SARIF (GitHub Code Scanning)

---

# Performance

Designed for both small Terraform projects and enterprise-scale repositories.

Performance features include:

- Parallel parsing
- Incremental cache
- Streaming scan mode
- Constant-memory scanning

Example:

```python
for finding in rbi.scan_large("./large-repository"):
    print(finding.rule_id, finding.message)
```

---

# Architecture

```
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
Resolved Resources
        │
        ▼
Resource Index
        │
        ▼
Relationship Builder
        │
        ▼
Relationship Graph
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

The scanner now includes the architectural foundation for graph-based compliance analysis. Future releases will populate the relationship graph to enable cross-resource compliance rules.

Implementation details:

```
docs/ARCHITECTURE.md
```

---

# CI/CD Integration

The repository includes GitHub Actions workflows.

## Continuous Integration

```
.github/workflows/scan.yml
```

Runs:

- Unit tests
- Compliance scans
- Example infrastructure validation

## Continuous Delivery

```
.github/workflows/publish.yml
```

Automatically publishes new releases to PyPI using Trusted Publishing whenever a GitHub Release is created.

---

# Running From Source

Clone the repository:

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git

cd terraform-rbi-compliance-scanner
```

Install:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

---

# Roadmap

## Completed

- ✅ Terraform HCL parsing
- ✅ Terraform Plan scanning
- ✅ Streaming scan engine
- ✅ Parallel parsing
- ✅ Incremental cache
- ✅ RBI-001 to RBI-005
- ✅ JSON & SARIF reporting
- ✅ Inline suppressions
- ✅ Resource Index
- ✅ Relationship Graph infrastructure

## In Progress

- 🚧 Terraform relationship extraction
- 🚧 Cross-resource compliance analysis

## Planned

- Azure support
- Google Cloud support
- Additional RBI controls
- Graph-aware compliance rules
- Plugin architecture
- Compliance reporting improvements

---

# Contributing

Contributions are welcome.

If you'd like to improve rules, add provider support, improve performance, or enhance documentation, feel free to open an issue or submit a pull request.

---

# Disclaimer

This project automates infrastructure compliance checks but **does not guarantee regulatory compliance**.

Actual compliance depends on infrastructure configuration, organizational controls, operational procedures, and regulatory interpretation.

Always validate findings with your security or compliance team before relying on them for production environments.

---

# License

MIT License