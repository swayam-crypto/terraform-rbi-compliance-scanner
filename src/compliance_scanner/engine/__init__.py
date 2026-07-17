"""
The scan engine: takes a directory of Terraform files, runs every
registered rule against every resource, and collects findings.

This is the orchestration layer. Parser and rules don't know about
each other — the engine is what connects them.

Two entry points:
- scan_directory: simple, in-memory, fine for small-to-medium projects
- scan_directory_large: streaming + parallel + cached, for datasets in
  the thousands-to-hundreds-of-thousands of files range
"""

from compliance_scanner.parser import parse_terraform_directory
from compliance_scanner.parser.terraform_parser import iter_terraform_directory
from compliance_scanner.parser.cache import (
    load_cache,
    save_cache,
    get_cached_or_none,
    update_cache_entry,
    DEFAULT_CACHE_PATH,
)
from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import Finding
from .scan_engine import scan_directory


def _run_rules_on_resources(resources: dict, file_path: str):
    """Shared rule-checking logic used by both scan modes."""
    for resource_type, named_configs in resources.items():
        for resource_name, config in named_configs.items():
            for rule in ALL_RULES:
                if resource_type not in rule.applies_to:
                    continue
                result = rule.check(resource_type, resource_name, config)
                if result is not None:
                    result.file_path = file_path
                    yield result


def scan_directory(dir_path: str) -> list[Finding]:
    """
    Run all rules against all Terraform resources in a directory.

    Simple and in-memory — parses everything, then checks everything.
    Good default for typical projects. For datasets in the thousands
    of files, use scan_directory_large instead.
    """
    resources = parse_terraform_directory(dir_path)
    return list(_run_rules_on_resources(resources, dir_path))


def scan_directory_large(
    dir_path: str,
    workers: int | None = None,
    use_cache: bool = True,
    cache_path: str = DEFAULT_CACHE_PATH,
):
    """
    Generator version for large datasets (thousands to hundreds of
    thousands of files). Three things make this scale where
    scan_directory doesn't:

    1. Parses files in parallel across CPU cores (iter_terraform_directory)
    2. Yields findings as each file finishes, instead of waiting for
       the whole dataset — peak memory stays roughly constant
    3. Skips re-parsing files that haven't changed since the last run
       (via the on-disk cache), which matters most on repeated CI scans

    This is a generator — iterate it directly, or wrap in list() if you
    need everything at once:
        findings = list(scan_directory_large("./big-repo"))
    """
    cache = load_cache(cache_path) if use_cache else {}
    files_to_parse = []

    # Separate cache hits (skip parsing) from files that need parsing
    from pathlib import Path
    all_files = [str(p) for p in Path(dir_path).rglob("*.tf")]

    for file_path in all_files:
        cached_resources = get_cached_or_none(file_path, cache) if use_cache else None
        if cached_resources is not None:
            # Cache hit — yield findings straight from cached data, no parsing
            yield from _run_rules_on_resources(cached_resources, file_path)
        else:
            files_to_parse.append(file_path)

    # Only files that changed (or first run) go through parallel parsing
    if files_to_parse:
        from concurrent.futures import ProcessPoolExecutor, as_completed
        from compliance_scanner.parser.terraform_parser import parse_terraform_file

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(parse_terraform_file, f): f for f in files_to_parse}
            for future in as_completed(futures):
                file_path = futures[future]
                resources = future.result()
                if use_cache:
                    update_cache_entry(file_path, resources, cache)
                yield from _run_rules_on_resources(resources, file_path)

    if use_cache:
        save_cache(cache, cache_path)