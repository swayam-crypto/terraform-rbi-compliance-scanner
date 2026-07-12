# terraform-rbi-compliance-scanner

[![PyPI version](https://img.shields.io/pypi/v/rbi-compliance-scanner.svg)](https://pypi.org/project/rbi-compliance-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Terraform static analysis tool that checks infrastructure code against
RBI cybersecurity guidance and India's DPDPA data protection
requirements — not just generic cloud security best practices.

Most open-source IaC scanners (Checkov, tfsec, Terrascan) check for
general misconfigurations like "is this S3 bucket public." They don't
know anything about India-specific regulatory requirements like data
localization mandates for financial data. This tool fills that gap.

## Why this exists

"Is my S3 bucket public?" and "does my S3 bucket meet Indian data
localization requirements?" are different questions and only the first
one is covered by existing scanning tools. This project encodes the
second kind of question as automated, CI/CD-enforceable rules.

## Install

```bash
pip install rbi-compliance-scanner
```

## Quick Start

```bash
rbi-scan --path ./examples/sample_infra
```

or use itt as a Python library:

```python
import compliance_scanner as rbi

findings = rbi.scan("./my-terraform-project")
for f in findings:
    print(f.severity, f.rule_id, f.message)
```

Example output:

```
3 compliance violation(s) found:

[CRITICAL] RBI-001 — aws_s3_bucket.customer_transactions
  Resource 'customer_transactions' appears to hold sensitive financial/
  customer data but is provisioned in 'us-east-1', outside India.
  RBI data localization rules likely require ap-south-1 or ap-south-2.
  Reference: RBI Cybersecurity Framework — Data Localization requirement
```

## Rules implemented

5 rules covering data localization, encryption, audit log retention,
network exposure, and IAM least-privilege access. See
[docs/RULES.md](docs/RULES.md) for the full list, severity levels, and
which rules map to a specific numbered regulation vs. a broader
principle-based interpretation.

## Large-dataset support

For scanning large Terraform repositories (thousands of files),
`rbi.scan_large()` provides parallel parsing and file-change caching so
repeated CI scans only re-process what actually changed:

```python
for finding in rbi.scan_large("./huge-infra-repo"):
    print(finding.severity, finding.message)
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the parser,
rule engine, and reporting layers fit together, and the reasoning behind
the design choices.

## Contributing / running from source

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git
cd terraform-rbi-compliance-scanner
pip install -e .
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## CI/CD integration

This repo includes working GitHub Actions workflows:
- `.github/workflows/scan.yml` — runs the test suite on every push/PR,
  demos the scanner catching a known violation, and gates the build
  against a fully compliant example
- `.github/workflows/publish.yml` — publishes to PyPI automatically via
  trusted publishing whenever a GitHub Release is created

Point `--path` at your own Terraform directory to use the scanner on
real infrastructure.

## Status

Published on PyPI, actively being developed. 5 of a planned 8 rules
implemented (see [docs/RULES.md](docs/RULES.md) for the roadmap). Not
yet validated by a compliance professional — see the disclaimer there
before relying on this for real compliance decisions.

## License

MIT
