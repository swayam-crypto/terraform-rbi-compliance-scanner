# Terraform RBI Compliance Scanner

[![PyPI version](https://img.shields.io/pypi/v/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![Python](https://img.shields.io/pypi/pyversions/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern Infrastructure-as-Code (IaC) compliance scanner that analyzes Terraform configurations against **Reserve Bank of India (RBI)** cybersecurity guidance and **India's Digital Personal Data Protection Act (DPDPA)** requirements.

Unlike traditional IaC security scanners that focus primarily on security best practices, this project focuses on **regulatory compliance**, enabling organizations to identify infrastructure configurations that may violate Indian regulatory requirements before deployment.

---

# Why this project exists

Most Infrastructure-as-Code scanners answer questions like:

> "Is this infrastructure secure?"

This project answers a different question:

> "Is this infrastructure compliant with RBI cybersecurity guidance and India's Digital Personal Data Protection Act?"

Those are fundamentally different problems.

Traditional tools such as:

- Checkov
- tfsec
- Terrascan

primarily detect cloud security misconfigurations.

They generally do **not** encode jurisdiction-specific regulatory controls such as:

- Data localization
- Financial data protection
- Regulatory audit requirements
- Infrastructure compliance controls

Terraform RBI Compliance Scanner bridges that gap by treating compliance as a first-class concern.
---

# Documentation

Project documentation is organized as follows:

| Document | Description |
|----------|-------------|
| `docs/ARCHITECTURE.md` | Overall scanner architecture |
| `docs/catalog.md` | Catalog system and YAML schema |
| `docs/RULES.md` | Compliance rule documentation |

---

# Features

## Compliance Engine

- RBI cybersecurity compliance checks
- DPDPA infrastructure validation
- Graph-aware compliance rules
- Cross-resource compliance analysis
- Extensible rule engine

---

## Terraform Analysis

- Terraform HCL parsing
- Terraform Plan (`tfplan.json`) scanning
- Resource indexing
- Relationship extraction
- Relationship graph construction
- Graph predicate engine

---

## Resource Catalog

The scanner includes a strongly typed resource catalog capable of describing cloud resources independently of any provider.

Features include:

- Immutable resource definitions
- Canonical resource classification
- Resource capabilities
- Resource relationships
- Rich attribute definitions
- Provider aliases
- YAML-based catalog
- Runtime validation
- Typed loading pipeline

Documentation:

```
docs/catalog.md
```

---

## Reporting

Supported output formats:

- Human-readable CLI
- JSON
- SARIF (GitHub Code Scanning)

---

## Performance

Designed for repositories ranging from small Terraform projects to enterprise-scale infrastructure.

Performance features include:

- Parallel scanning
- Streaming scan mode
- Incremental cache
- Constant-memory processing

---

## Developer Experience

- Python API
- Command-line interface
- CI/CD friendly
- PyPI package
- Extensible architecture
- Comprehensive test suite

---

# Installation

Install from PyPI:

```bash
pip install rbi-compliance-scanner
```

For development:

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git

cd terraform-rbi-compliance-scanner

pip install -e .
pip install -r requirements-dev.txt
```

---

# Quick Start

Scan a Terraform directory:

```bash
rbi-scan --path ./examples/sample_infra
```

Scan a Terraform plan:

```bash
terraform plan -out=tfplan

terraform show -json tfplan > tfplan.json

rbi-scan --plan tfplan.json
```

---

# Python API

The scanner can also be used as a Python library.

```python
import compliance_scanner as rbi

findings = rbi.scan("./terraform-project")

for finding in findings:
    print(
        finding.severity,
        finding.rule_id,
        finding.message,
    )
```

Large repositories can be streamed:

```python
for finding in rbi.scan_large("./large-repository"):
    print(
        finding.rule_id,
        finding.message,
    )
```

---

# Example Output

```text
3 compliance violation(s) found

[CRITICAL] RBI-001

Resource:

aws_s3_bucket.customer_transactions

Issue:

Sensitive financial data appears to be deployed outside India.

Recommendation:

Deploy regulated customer data inside
ap-south-1 or ap-south-2 unless an approved
regulatory exception exists.
```

---

# Implemented Compliance Rules

Current rules include:

| Rule | Description |
|------|-------------|
| RBI-001 | Data Localization |
| RBI-002 | Encryption at Rest |
| RBI-003 | Audit Log Retention |
| RBI-004 | Network Exposure |
| RBI-005 | IAM Least Privilege |

Complete rule documentation:

```
docs/RULES.md
```

---

# Suppressing Findings

Suppress an individual rule:

```hcl
# rbi-scan:ignore RBI-001 reason="Internal logs bucket"

resource "aws_s3_bucket" "internal_logs" {
    ...
}
```

Suppress all rules:

```hcl
# rbi-scan:ignore-all reason="Legacy infrastructure"

resource "aws_s3_bucket" "legacy_bucket" {
    ...
}
```

Suppressed findings remain visible in suppression statistics to preserve audit transparency.

---

# Output Formats

The scanner currently supports:

- Human-readable CLI
- JSON
- SARIF (GitHub Code Scanning)
---

# Performance

The scanner is designed to scale from small Terraform projects to enterprise infrastructure repositories.

Performance optimizations include:

- Parallel resource parsing
- Streaming scan mode
- Incremental scan cache
- Constant-memory scanning
- Efficient graph traversal
- Lazy relationship resolution

Example:

```python
for finding in rbi.scan_large("./large-repository"):
    print(
        finding.rule_id,
        finding.message,
    )
```

---

# Architecture

The compliance engine follows a layered architecture that separates parsing, resource modeling, graph analysis, and compliance evaluation.

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
Graph Predicates
        │
        ▼
Compliance Rule Engine
        │
        ▼
Compliance Findings
        │
 ┌──────┴──────────┐
 │                 │
 ▼                 ▼
JSON             SARIF
```

This architecture enables rules to reason about relationships between cloud resources instead of evaluating each resource independently.

---

# Resource Catalog

One of the core components of the scanner is the **typed resource catalog**.

Instead of hardcoding AWS resource knowledge throughout the codebase, every supported resource is described by a `ResourceDefinition`.

Each resource definition contains:

- Provider
- Cloud service
- Display name
- Resource kind
- Canonical resource type
- Capabilities
- Relationships
- Attributes
- Aliases
- Metadata

All resource definitions are immutable after loading.

---

## Catalog Architecture

```
catalog/
│
├── attributes.py
├── canonical_types.py
├── kinds.py
├── models.py
├── loader.py
├── registry.py
├── catalog.py
├── global_catalog.py
└── data/
    └── aws.yaml
```

Responsibilities:

| Component | Purpose |
|----------|----------|
| `attributes.py` | Defines supported attribute types |
| `canonical_types.py` | Defines provider-independent resource classifications |
| `kinds.py` | High-level resource categories |
| `models.py` | Immutable catalog models |
| `loader.py` | Loads and validates YAML catalogs |
| `registry.py` | Stores resource definitions |
| `catalog.py` | Query interface used by the compliance engine |
| `global_catalog.py` | Singleton catalog instance |
| `data/` | YAML catalog definitions |

---

## Resource Definition Model

Each catalog entry describes a resource using a strongly typed model.

Example:

```yaml
aws_db_instance:
  provider: aws
  service: rds
  display_name: Amazon RDS DB Instance

  kind: data
  canonical_type: database

  capabilities:
    - encryption
    - backup
    - logging

  attributes:

    encryption:
      name: storage_encrypted
      type: boolean
      default: false

  relationships:
    - subnet
    - security_group
    - kms_key

  aliases:
    - AWS::RDS::DBInstance

  metadata:
    deprecated: false
```

---

## Canonical Resource Types

Resources are classified independently of cloud providers.

Examples include:

- Database
- Object Storage
- Load Balancer
- Virtual Machine
- Security Group
- Subnet
- IAM Role
- KMS Key

This allows compliance rules to work across multiple cloud providers without being tightly coupled to AWS-specific resource names.

---

## Resource Kinds

Every resource also belongs to a high-level category.

Current kinds include:

- Compute
- Data
- Storage
- Network
- Security
- Identity

Kinds provide another abstraction layer for future graph-based reasoning.

---

## Catalog Validation

Every catalog file is validated before loading.

Validation currently checks:

- Required fields
- Valid resource kinds
- Valid canonical types
- Valid attribute types
- Duplicate attribute names
- Duplicate aliases
- Missing attribute metadata

Invalid catalog entries produce descriptive validation errors during startup.

---

## Immutability

Catalog models are immutable.

This guarantees that:

- Rules cannot accidentally modify catalog metadata.
- Provider definitions remain consistent.
- Shared catalog instances are thread-safe.
- Runtime behavior remains deterministic.

---

## Documentation

Additional documentation is available in:

```
docs/catalog.md
```

Architecture documentation:

```
docs/ARCHITECTURE.md
```

Rule documentation:

```
docs/RULES.md
```

---

# Graph-Based Compliance Engine

Traditional IaC scanners evaluate resources independently.

This scanner introduces a graph-aware compliance engine capable of reasoning about infrastructure relationships.

Examples include:

- Public load balancer exposing a database
- Internet Gateway connected to sensitive workloads
- Security Group inheritance
- Shared KMS keys
- Cross-resource encryption analysis
- Future network reachability analysis

The graph layer enables richer compliance rules that are difficult or impossible to implement using resource-by-resource analysis alone.

---

# Current Architecture Status

The following major components have been implemented:

- Terraform parser
- Resource index
- Relationship graph
- Graph traversal engine
- Graph predicates
- Typed resource catalog
- YAML catalog loader
- Catalog validation
- Immutable catalog models
- Compliance rule engine
- JSON reporting
- SARIF reporting
- Incremental scan cache

These components form the architectural foundation for future provider support and advanced compliance analysis.
---

# CI/CD Integration

The repository includes GitHub Actions workflows for automated testing, validation, and publishing.

## Continuous Integration

```
.github/workflows/scan.yml
```

Runs:

- Unit tests
- Terraform example validation
- Compliance rule verification
- Catalog validation
- Static analysis

Every pull request is validated before merging.

---

## Continuous Delivery

```
.github/workflows/publish.yml
```

New releases are automatically published to PyPI using **Trusted Publishing** whenever a GitHub Release is created.

---

# Running From Source

Clone the repository:

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git

cd terraform-rbi-compliance-scanner
```

Install development dependencies:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test module:

```bash
pytest tests/catalog/test_loader.py -v
```

---

# Project Structure

```
terraform-rbi-compliance-scanner/
│
├── src/
│   └── compliance_scanner/
│       ├── catalog/
│       ├── engine/
│       ├── graph/
│       ├── graph_rules/
│       ├── parser/
│       ├── reporters/
│       ├── rules/
│       └── models/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RULES.md
│   └── catalog.md
│
├── tests/
│
├── examples/
│
└── pyproject.toml
```

---

# Testing

The project uses **pytest** with a growing suite of unit tests covering:

- Catalog loading
- Catalog validation
- Resource models
- Registry
- Relationship graph
- Graph predicates
- Graph rules
- Rule engine
- Terraform parser
- Reporting
- Suppressions

Example:

```bash
pytest
```

or

```bash
pytest -v
```

Maintaining high test coverage is an important project goal. New features should include appropriate unit tests.

---

# Roadmap

## ✅ Completed

- Terraform HCL parsing
- Terraform Plan scanning
- RBI compliance rule engine
- DPDPA infrastructure validation
- JSON reporting
- SARIF reporting
- Incremental scan cache
- Streaming scan engine
- Parallel scanning
- Resource indexing
- Relationship graph
- Graph predicates
- Cross-resource rule framework
- Typed resource catalog
- Immutable catalog models
- Rich YAML catalog schema
- Catalog validation
- Comprehensive catalog test suite

---

## 🚧 In Progress

Current development focuses on expanding the cloud resource catalog and enabling richer graph-based compliance analysis.

---

## 📌 Planned

### Cloud Providers

- Expanded AWS resource catalog
- Microsoft Azure support
- Google Cloud Platform support
- Kubernetes resources

### Compliance Frameworks

- Additional RBI controls
- CIS Benchmarks
- NIST Cybersecurity Framework
- ISO 27001 mappings
- SOC 2 mappings
- PCI DSS mappings

### Compliance Engine

- Advanced graph traversal
- Multi-hop dependency analysis
- Risk propagation
- Compliance evidence generation
- Control-to-resource mapping
- Compliance scoring

### Developer Experience

- Plugin architecture
- Rule SDK
- Custom provider support
- Enhanced CLI
- HTML reporting
- Interactive compliance reports
- Catalog statistics dashboard

---

# Design Principles

The project is built around several core principles.

## Provider Independence

Compliance rules should reason about **resource behavior**, not provider-specific names.

For example:

- AWS RDS
- Azure SQL Database
- Google Cloud SQL

can all be classified as the canonical type:

```
Database
```

allowing a single compliance rule to evaluate all providers consistently.

---

## Strong Typing

Core models use immutable, strongly typed data structures to improve:

- Reliability
- Maintainability
- Testability
- Refactoring safety

---

## Graph-Based Analysis

Infrastructure should not be analyzed one resource at a time.

Many compliance requirements depend on relationships between resources.

Examples include:

- Public exposure
- Network reachability
- Encryption dependencies
- IAM trust chains
- Shared infrastructure

The graph engine enables these scenarios.

---

## Extensibility

The architecture is designed to support:

- Additional cloud providers
- New compliance frameworks
- Custom rule packs
- External plugins
- Enterprise integrations

without requiring major architectural changes.

---

# Contributing

Contributions are welcome.

Areas where contributions are especially valuable include:

- Compliance rules
- Cloud provider support
- Performance improvements
- Documentation
- Testing
- Bug fixes
- Architecture improvements

Before opening a pull request:

1. Run the full test suite.
2. Ensure new functionality includes unit tests.
3. Update documentation where applicable.
4. Follow the existing project style.

---

# Disclaimer

This project automates infrastructure compliance checks but **does not guarantee regulatory compliance**.

Actual compliance depends on many factors outside Infrastructure as Code, including:

- Organizational policies
- Operational controls
- Security procedures
- Human processes
- Regulatory interpretation
- Legal requirements

The scanner should be used as an engineering aid rather than a substitute for professional compliance assessments.

Always validate findings with your security, legal, and compliance teams before relying on them in production environments.

---

# License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.