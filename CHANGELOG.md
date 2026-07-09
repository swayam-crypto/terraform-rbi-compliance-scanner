# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/), versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]
- RBI-004: network exposure rule (planned for v0.2.0)
- RBI-005: least privilege / wildcard IAM rule (planned for v0.2.0)

## [0.1.0] - 2026-07-10
### Added
- Terraform HCL parser (`parse_terraform_file`, `parse_terraform_directory`, `parse_terraform_string`)
- Rule engine with pluggable rule interface (`BaseRule`, `Finding`)
- RBI-001: Data localization check (RBI Circular DPSS.CO.OD.No.2785/06.08.005/2017-2018)
- RBI-002: Encryption at rest check
- RBI-003: Audit log retention check, 180-day minimum (CERT-In Cybersecurity Directions 2022)
- Large-dataset support: parallel parsing, streaming scan, file-change caching
- CLI (`rbi-scan`) and Python library API (`import compliance_scanner as rbi`)
- GitHub Actions CI pipeline (tests + example scan on every push)
- Full test suite (17 tests)
