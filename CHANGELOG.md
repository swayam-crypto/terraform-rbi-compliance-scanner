# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- Introduced `ResourceIndex` for efficient resource lookup during compliance analysis.
- Added `RelationshipGraph` as the foundation for graph-based infrastructure analysis.
- Added `RelationshipBuilder` to construct infrastructure relationship graphs.
- Added `ScanContext` to encapsulate scan state across the scanning pipeline.

### Changed

- Refactored the scanning pipeline to integrate relationship graph construction.
- All scan entry points now build a shared scan context for future graph-aware rule execution.
- Improved internal architecture to support future cross-resource compliance analysis.

### Planned

- Terraform relationship extraction.
- Graph-aware compliance rules.
- RBI-006: MFA enforcement rule.
- RBI-007: Clock synchronization rule.
- Baseline/ignore file for adopting the scanner on legacy infrastructure.
- Azure provider support.
- Google Cloud provider support.

---

## [0.3.0] - 2026-07-30

### Added

- Terraform Plan (`tfplan.json`) scanning support.
- Streaming scan mode for large Terraform repositories.
- Inline suppression comments for compliance findings.
- Cache support for faster repeated scans.

### Improved

- Enhanced RBI-004 detection for sensitive resources.
- Sensitive resource detection now checks:
  - Resource names
  - S3 bucket names
  - RDS identifiers
  - Tag values
- Improved ACL normalization and reporting.
- Centralized `ResolvedResource` creation across all scan modes.

### Fixed

- IAM Least Privilege rule correctly ignores `Deny` statements.

---

## [0.2.0] - 2026-07-11

### Added

- RBI-004: Network exposure check — flags sensitive S3 buckets and databases that are publicly accessible.
- RBI-005: IAM Least Privilege check — flags IAM policies granting wildcard (`*`) actions or resources.
- Added tests covering both new compliance rules.

---

## [0.1.0] - 2026-07-10

### Added

- Terraform HCL parser (`parse_terraform_file`, `parse_terraform_directory`, `parse_terraform_string`).
- Rule engine with pluggable rule interface (`BaseRule`, `Finding`).
- RBI-001: Data Localization check (RBI Circular DPSS.CO.OD.No.2785/06.08.005/2017-2018).
- RBI-002: Encryption at Rest check.
- RBI-003: Audit Log Retention check (CERT-In Cyber Security Directions, 2022) enforcing a minimum of 180 days.
- Large-scale scanning support with parallel parsing, streaming scan mode, and incremental file cache.
- Command-line interface (`rbi-scan`) and Python API.
- GitHub Actions CI pipeline (tests and sample infrastructure scanning).
- Initial test suite.