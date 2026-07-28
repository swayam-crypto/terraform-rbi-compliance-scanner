"""
Command-line entry point.

Usage:
    rbi-scan --path ./examples/sample_infra
    rbi-scan --path ./examples/sample_infra --format json
    rbi-scan --path ./huge-repo --large
"""

import argparse
import sys
from pathlib import Path
from compliance_scanner.engine import scan_directory, scan_directory_large
from compliance_scanner.reporting import to_json, print_console_summary


def main():
    parser = argparse.ArgumentParser(
        description="RBI/DPDPA Terraform compliance scanner"
    )
    parser.add_argument("--path", required=True, help="Directory containing .tf files")
    parser.add_argument("--format", choices=["console", "json"], default="console")
    parser.add_argument(
        "--fail-on",
        choices=["critical", "high", "medium", "low", "none"],
        default="critical",
        help="Exit with non-zero status if a finding at this severity or above exists",
    )
    parser.add_argument(
        "--large",
        action="store_true",
        help="Use parallel scanning with file-change caching for large repositories",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers for --large mode (default: CPU count)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable file-change caching (only affects --large mode)",
    )
    args = parser.parse_args()

    scan_path = Path(args.path)

    if not scan_path.exists():
        parser.error(f"Path does not exist: {args.path}")

    if not scan_path.is_dir():
        parser.error(f"Path is not a directory: {args.path}")

    suppressed_count = [0]

    try:
        if args.large:
            findings = list(
                scan_directory_large(
                    args.path,
                    workers=args.workers,
                    use_cache=not args.no_cache,
                    suppressed_count=suppressed_count,
                )
            )
        else:
            findings = scan_directory(
                args.path,
                suppressed_count=suppressed_count,
            )

    except ValueError as e:
        parser.error(str(e))

    if args.format == "json":
        print(to_json(findings))
    else:
        print_console_summary(findings)

    if suppressed_count[0] > 0:
        print(
            f"\n{suppressed_count[0]} finding(s) suppressed via inline rbi-scan:ignore comments."
        )

    if args.fail_on == "none":
        sys.exit(0)

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    threshold = severity_order[args.fail_on]
    should_fail = any(severity_order.get(f.severity, 99) <= threshold for f in findings)

    sys.exit(1 if should_fail else 0)


if __name__ == "__main__":
    main()
