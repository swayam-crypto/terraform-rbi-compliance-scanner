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
from collections import defaultdict
from compliance_scanner.parser.plan_parser import parse_plan_file
from compliance_scanner.parser.terraform_parser import (
    parse_terraform_file,
    parse_terraform_file_with_providers,
    _resolve_provider_for_resource,
)
from compliance_scanner.parser.suppressions import extract_suppressions, is_suppressed
from compliance_scanner.parser.cache import (
    load_cache,
    save_cache,
    get_cached_or_none,
    update_cache_entry,
    DEFAULT_CACHE_PATH,
)

from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider

from compliance_scanner.rules import ALL_RULES
from compliance_scanner.rules.base import Finding

from compliance_scanner.parser.relationship_extractor import RelationshipExtractor

from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.graph.graph_builder import GraphBuilder
from compliance_scanner.scan_context import ScanContext


def _run_rules_on_resources(
    resources: list[ResolvedResource],
    file_path: str,
    suppressions: dict,
    suppressed_count: list,
):
    """
    Shared rule-checking logic used by both scan modes.

    suppressed_count is a single-element list used as a mutable counter
    (e.g. [0]) so the caller can read how many findings were suppressed
    after the generator is exhausted — plain integers can't be mutated
    through a shared reference the way a list can.
    """
    for resource in resources:
        for rule in ALL_RULES:
            if resource.resource_type not in rule.applies_to:
                continue
            result = rule.check(resource)
            if result is None:
                continue
            if is_suppressed(
                rule.rule_id,
                resource.resource_type,
                resource.resource_name,
                suppressions,
            ):
                suppressed_count[0] += 1
                continue
            result.file_path = file_path
            yield result


def _collect_providers_and_resources(dir_path: str) -> tuple[dict, dict]:
    """
    First pass: collect all providers from all files, and all resources.
    Returns (all_providers, {file_path: resources_dict}).
    """
    all_providers: dict = {}
    file_resources: dict = {}

    for tf_file in Path(dir_path).rglob("*.tf"):
        if ".terraform" in tf_file.parts:
            continue
        resources, providers = parse_terraform_file_with_providers(str(tf_file))
        file_resources[str(tf_file)] = resources
        all_providers.update(providers)

    return all_providers, file_resources


def _resolve_resources(
    file_resources: dict, all_providers: dict
) -> list[ResolvedResource]:
    """Convert raw resource dicts into ResolvedResource objects with provider defaults."""
    resolved: list[ResolvedResource] = []
    for file_path, resources in file_resources.items():
        for resource_type, named_configs in resources.items():
            provider_defaults = _resolve_provider_for_resource(
                resource_type, all_providers
            )
            for resource_name, config in named_configs.items():
                resolved.append(
                    ResolvedResource(
                        platform=Platform.TERRAFORM,
                        provider=infer_provider(resource_type),
                        resource_type=resource_type,
                        resource_name=resource_name,
                        attributes=config,
                        default_attributes=provider_defaults,
                        source=SourceLocation(
                            file_path=file_path,
                        ),
                    )
                )
    return resolved


def scan_directory(
    dir_path: str, suppressed_count: list | None = None
) -> list[Finding]:
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

    all_providers, file_resources = _collect_providers_and_resources(dir_path)

    if not file_resources:
        raise ValueError(f"No Terraform (.tf) files found in '{dir_path}'.")

    all_findings: list[Finding] = []

    resolved_resources = _resolve_resources(file_resources, all_providers)

    index = ResourceIndex(resolved_resources)

    relationships = RelationshipExtractor().extract(
        resolved_resources,
        index,
    )
    graph = GraphBuilder().build(relationships)

    context = ScanContext(
        resources=resolved_resources,
        resource_index=index,
        relationship_graph=graph,
    )

    resources_by_file: dict[str, list[ResolvedResource]] = defaultdict(list)

    for resource in resolved_resources:
        resources_by_file[resource.source.file_path].append(resource)

    for file_path, resolved in resources_by_file.items():
        suppressions = extract_suppressions(file_path)

        all_findings.extend(
            _run_rules_on_resources(
                resolved,
                file_path,
                suppressions,
                suppressed_count,
            )
        )

    return all_findings


def scan_plan(
    plan_path: str,
    suppressed_count: list | None = None,
) -> list[Finding]:
    """
    Run all compliance rules against a Terraform Plan JSON file.
    """

    if suppressed_count is None:
        suppressed_count = [0]

    resources = parse_plan_file(plan_path)

    if not resources:
        raise ValueError(f"No resources found in Terraform plan '{plan_path}'.")

    findings = list(
        _run_rules_on_resources(
            resources=resources,
            file_path=plan_path,
            suppressions={},
            suppressed_count=suppressed_count,
        )
    )

    return findings


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
    cached_files = []

    all_files = [
        str(p) for p in Path(dir_path).rglob("*.tf") if ".terraform" not in p.parts
    ]
    if not all_files:
        raise ValueError(f"No Terraform (.tf) files found in '{dir_path}'.")

    # First, collect all providers (need to parse all files for this)
    all_providers: dict = {}
    for file_path in all_files:
        cached_resources = get_cached_or_none(file_path, cache) if use_cache else None
        if cached_resources is not None:
            cached_files.append((file_path, cached_resources))
        else:
            files_to_parse.append(file_path)

    # Parse non-cached files to collect their providers too
    for file_path in files_to_parse:
        try:
            _, providers = parse_terraform_file_with_providers(file_path)
            all_providers.update(providers)
        except Exception:
            pass  # Will be re-parsed in parallel later; skip provider extraction for now

    # Also extract providers from cached files
    for file_path, _ in cached_files:
        try:
            _, providers = parse_terraform_file_with_providers(file_path)
            all_providers.update(providers)
        except Exception:
            pass

    # Process cached files first
    for file_path, resources in cached_files:
        resolved = _resolve_resources(
            {file_path: resources},
            all_providers,
        )
        suppressions = extract_suppressions(file_path)
        yield from _run_rules_on_resources(
            resolved, file_path, suppressions, suppressed_count
        )

    # Process uncached files in parallel
    if files_to_parse:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(parse_terraform_file_with_providers, f): f
                for f in files_to_parse
            }
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    resources, providers = future.result()
                except Exception:
                    continue  # Skip files that fail to parse
                all_providers.update(providers)
                if use_cache:
                    update_cache_entry(file_path, resources, cache)

                # Re-resolve with updated providers
                resolved = _resolve_resources(
                    {file_path: resources},
                    all_providers,
                )

                suppressions = extract_suppressions(file_path)
                yield from _run_rules_on_resources(
                    resolved, file_path, suppressions, suppressed_count
                )

    if use_cache:
        save_cache(cache, cache_path)
