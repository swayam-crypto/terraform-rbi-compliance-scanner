"""
The scan engine: takes a directory of Terraform files, runs every
registered rule against every resource, and collects findings.

This is the orchestration layer. Parser and rules don't know about
each other — the engine is what connects them.

Two entry points:
- scan_directory: simple, in-memory, fine for small-to-medium projects
- scan_directory_large: streaming + parallel + cached, for datasets in
  the thousands-to-hundreds-of-thousands of files range

Both respect inline suppression comments (see parser/suppressions.py).
Suppressed findings are not silently dropped — they're counted via the
`suppressed_count` list argument, so CLI/reporting can show "N findings
suppressed" rather than a scan that looks cleaner than it actually is.
"""

from pathlib import Path

from compliance_scanner.parser.terraform_parser import parse_terraform_file
from compliance_scanner.parser.suppressions import extract_suppressions, is_suppressed
from compliance_scanner.parser.cache import (
    load_cache,
    save_cache,
    get_cached_or_none,
    update_cache_entry,
    DEFAULT_CACHE_PATH,
)
from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import Finding


def _run_rules_on_resources(resources: dict, file_path: str, suppressions: dict, suppressed_count: list):
    """
    Shared rule-checking logic used by both scan modes.

    suppressed_count is a single-element list used as a mutable counter
    (e.g. [0]) so the caller can read how many findings were suppressed
    after the generator is exhausted — plain integers can't be mutated
    through a shared reference the way a list can.
    """
    for resource_type, named_configs in resources.items():
        for resource_name, config in named_configs.items():
            for rule in ALL_RULES:
                if resource_type not in rule.applies_to:
                    continue
                result = rule.check(resource_type, resource_name, config)
                if result is None:
                    continue
                if is_suppressed(rule.rule_id, resource_type, resource_name, suppressions):
                    suppressed_count[0] += 1
                    continue
                result.file_path = file_path
                yield result


def scan_directory(dir_path: str, suppressed_count: list | None = None) -> list[Finding]:
    """
    Run all rules against all Terraform resources in a directory.

    Simple and in-memory — parses everything, then checks everything.
    Good default for typical projects. For datasets in the thousands
    of files, use scan_directory_large instead.

    Pass a list like [0] as suppressed_count to read back how many
    findings were suppressed via inline comments after the call:
        counter = [0]
        findings = scan_directory(path, suppressed_count=counter)
        print(f"{counter[0]} findings suppressed")
    """
    if suppressed_count is None:
        suppressed_count = [0]

    all_findings: list[Finding] = []
    for tf_file in Path(dir_path).rglob("*.tf"):
        file_path = str(tf_file)
        resources = parse_terraform_file(file_path)
        suppressions = extract_suppressions(file_path)
        all_findings.extend(_run_rules_on_resources(resources, file_path, suppressions, suppressed_count))

    return all_findings


def scan_directory_large(
    dir_path: str,
    workers: int | None = None,
    use_cache: bool = True,
    cache_path: str = DEFAULT_CACHE_PATH,
    suppressed_count: list | None = None,
):
    """
    Generator version for large datasets (thousands to hundreds of
    thousands of files). Three things make this scale where
    scan_directory doesn't:

    1. Parses files in parallel across CPU cores
    2. Yields findings as each file finishes, instead of waiting for
       the whole dataset — peak memory stays roughly constant
    3. Skips re-parsing files that haven't changed since the last run
       (via the on-disk cache), which matters most on repeated CI scans

    Suppression comments are re-checked even on cache hits, since
    comments are cheap to re-scan and might change independently of the
    cached resource data.

    This is a generator — iterate it directly, or wrap in list() if you
    need everything at once:
        findings = list(scan_directory_large("./big-repo"))
    """
    if suppressed_count is None:
        suppressed_count = [0]

    cache = load_cache(cache_path) if use_cache else {}
    files_to_parse = []

    all_files = [str(p) for p in Path(dir_path).rglob("*.tf")]

    for file_path in all_files:
        cached_resources = get_cached_or_none(file_path, cache) if use_cache else None
        if cached_resources is not None:
            suppressions = extract_suppressions(file_path)
            yield from _run_rules_on_resources(cached_resources, file_path, suppressions, suppressed_count)
        else:
            files_to_parse.append(file_path)

    if files_to_parse:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(parse_terraform_file, f): f for f in files_to_parse}
            for future in as_completed(futures):
                file_path = futures[future]
                resources = future.result()
                if use_cache:
                    update_cache_entry(file_path, resources, cache)
                suppressions = extract_suppressions(file_path)
                yield from _run_rules_on_resources(resources, file_path, suppressions, suppressed_count)

    if use_cache:
        save_cache(cache, cache_path)