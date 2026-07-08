"""
Command-line entry point.

Usage:
    python -m compliance_scanner.cli --path ./examples/sample_infra
    python -m compliance_scanner.cli --path ./examples/sample_infra --format json
"""

import argparse
import sys

from compliance_scanner.engine import scan_directory
from compliance_scanner.reporting import to_json, print_console_summary


def main():
    parser = argparse.ArgumentParser(description="RBI/DPDPA Terraform compliance scanner")
    parser.add_argument("--path", required=True, help="Directory containing .tf files")
    parser.add_argument("--format", choices=["console", "json"], default="console")
    parser.add_argument(
        "--fail-on",
        choices=["critical", "high", "medium", "low", "none"],
        default="critical",
        help="Exit with non-zero status if a finding at this severity or above exists",
    )
    args = parser.parse_args()

    findings = scan_directory(args.path)

    if args.format == "json":
        print(to_json(findings))
    else:
        print_console_summary(findings)

    if args.fail_on == "none":
        sys.exit(0)

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    threshold = severity_order[args.fail_on]
    should_fail = any(severity_order.get(f.severity, 99) <= threshold for f in findings)

    sys.exit(1 if should_fail else 0)


if __name__ == "__main__":
    main()
