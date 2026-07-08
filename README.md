# terraform-rbi-compliance-scanner

A Terraform static analysis tool that checks infrastructure code against
RBI cybersecurity guidance and India's DPDPA data protection
requirements not just generic cloud security best practices.

Most open-source IaC scanners (Checkov, tfsec, Terrascan) check for
general misconfigurations like "is this S3 bucket public." They don't
know anything about India-specific regulatory requirements like data
localization mandates for financial data. This tool fills that gap.

## Why this exists

"Is my S3 bucket public?" and "does my S3 bucket meet Indian data
localization requirements?" are different questions and only the first
one is covered by existing scanning tools. This project encodes the
second kind of question as automated, CI/CD-enforceable rules.

## Quick start

```bash
git clone https://github.com/swayam-crypto/terraform-rbi-compliance-scanner.git
cd terraform-rbi-compliance-scanner
pip install -r requirements.txt

PYTHONPATH=src python -m compliance_scanner.cli --path ./examples/sample_infra
```

## Rules implemented

See [docs/RULES.md](docs/RULES.md) for the full list and what each one
checks.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the parser,
rule engine, and reporting layers fit together, and the reasoning behind
the design choices.

## Running tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=src python -m pytest tests/ -v
```

## CI/CD integration

This repo includes a working GitHub Actions workflow
(`.github/workflows/scan.yml`) that runs the test suite and scans the
example infrastructure on every push and pull request, failing the
build if a critical violation is found. Point `--path` at your own
Terraform directory to use it on real infrastructure.

## Status

Early-stage, actively being built. Currently implements 2 of a planned
6 rules. Not yet validated by a compliance professional — see the
disclaimer in [docs/RULES.md](docs/RULES.md).

## License

MIT
