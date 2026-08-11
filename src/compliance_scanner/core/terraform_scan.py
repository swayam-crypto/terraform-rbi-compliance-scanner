"""Terraform-specific scan entry points built on generic orchestration."""

from pathlib import Path

from compliance_scanner.core.scan_engine import _run_rules_on_resources, scan_resources
from compliance_scanner.parser.cache import DEFAULT_CACHE_PATH, get_cached_or_none, load_cache, save_cache, update_cache_entry
from compliance_scanner.parser.suppressions import extract_suppressions
from compliance_scanner.parser.terraform_adapter import TerraformParser
from compliance_scanner.parser.terraform_parser import _resolve_provider_for_resource, parse_terraform_file_with_providers
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def scan_directory(dir_path: str, suppressed_count: list | None = None):
    if suppressed_count is None:
        suppressed_count = [0]
    path = Path(dir_path)
    terraform_files = [file_path for file_path in path.rglob("*.tf") if ".terraform" not in file_path.parts]
    if not terraform_files:
        raise ValueError(f"No Terraform (.tf) files found in '{dir_path}'.")

    resources = TerraformParser().parse_directory(path)
    suppressions_by_file = {str(file_path): extract_suppressions(str(file_path)) for file_path in terraform_files}
    return scan_resources(resources, suppressed_count=suppressed_count, suppressions_by_file=suppressions_by_file)


def scan_plan(plan_path: str, suppressed_count: list | None = None):
    if suppressed_count is None:
        suppressed_count = [0]
    resources = TerraformParser().parse_plan(Path(plan_path))
    if not resources:
        raise ValueError(f"No resources found in Terraform plan '{plan_path}'.")
    return scan_resources(resources, suppressed_count=suppressed_count, finding_file_path=plan_path, include_graph_rules=False)


def _resolve_resources(file_resources: dict, all_providers: dict) -> list[ResolvedResource]:
    resolved: list[ResolvedResource] = []
    for file_path, resources in file_resources.items():
        for resource_type, named_configs in resources.items():
            provider_defaults = _resolve_provider_for_resource(resource_type, all_providers)
            for resource_name, config in named_configs.items():
                resolved.append(ResolvedResource(Platform.TERRAFORM, infer_provider(resource_type), resource_type, resource_name, config, provider_defaults, SourceLocation(file_path=file_path)))
    return resolved


def scan_directory_large(dir_path: str, workers: int | None = None, use_cache: bool = True, cache_path: str = DEFAULT_CACHE_PATH, suppressed_count: list | None = None):
    """Existing Terraform streaming/cached scan path; behavior intentionally unchanged."""
    if suppressed_count is None:
        suppressed_count = [0]
    cache = load_cache(cache_path) if use_cache else {}
    files_to_parse, cached_files = [], []
    all_files = [str(path) for path in Path(dir_path).rglob("*.tf") if ".terraform" not in path.parts]
    if not all_files:
        raise ValueError(f"No Terraform (.tf) files found in '{dir_path}'.")
    all_providers: dict = {}
    for file_path in all_files:
        cached_resources = get_cached_or_none(file_path, cache) if use_cache else None
        (cached_files if cached_resources is not None else files_to_parse).append((file_path, cached_resources) if cached_resources is not None else file_path)
    for file_path in files_to_parse + [file_path for file_path, _ in cached_files]:
        try:
            _, providers = parse_terraform_file_with_providers(file_path)
            all_providers.update(providers)
        except Exception:
            pass
    for file_path, resources in cached_files:
        resolved = _resolve_resources({file_path: resources}, all_providers)
        yield from _run_rules_on_resources(resolved, file_path, extract_suppressions(file_path), suppressed_count)
    if files_to_parse:
        from concurrent.futures import ProcessPoolExecutor, as_completed
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(parse_terraform_file_with_providers, file_path): file_path for file_path in files_to_parse}
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    resources, providers = future.result()
                except Exception:
                    continue
                all_providers.update(providers)
                if use_cache:
                    update_cache_entry(file_path, resources, cache)
                resolved = _resolve_resources({file_path: resources}, all_providers)
                yield from _run_rules_on_resources(resolved, file_path, extract_suppressions(file_path), suppressed_count)
    if use_cache:
        save_cache(cache, cache_path)
