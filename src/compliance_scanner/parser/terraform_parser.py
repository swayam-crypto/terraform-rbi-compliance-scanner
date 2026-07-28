"""
Parses .tf files into a plain Python structure the rule engine can read.

Uses python-hcl2 to do the actual HCL parsing — we just normalize its
output into a simpler shape.
"""
import hcl2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import io
from dataclasses import dataclass


def _strip_quotes(value):
    """
    python-hcl2 (8.x) sometimes preserves literal surrounding quote
    characters in parsed string values/keys, e.g. '"us-east-1"' instead
    of 'us-east-1'. Recursively clean these so downstream rule code can
    compare plain strings.

    Also unescapes backslash-escaped quotes and backslashes inside the
    string (e.g. an inline JSON policy written as "{\\"Action\\": \\"*\\"}")
    since python-hcl2 leaves these escape sequences untouched rather
    than resolving them the way real HCL semantics require.
    """
    if isinstance(value, str):
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            inner = value[1:-1]
            inner = inner.replace('\\"', '"').replace('\\\\', '\\')
            return inner
        return value
    if isinstance(value, list):
        return [_strip_quotes(v) for v in value]
    if isinstance(value, dict):
        return {
            _strip_quotes(k): _strip_quotes(v)
            for k, v in value.items()
            if k != "__is_block__"
        }
    return value


def _flatten_config(config: dict) -> dict:
    """Flatten single-element lists that hcl2 wraps values in."""
    return {
        k: (v[0] if isinstance(v, list) and len(v) == 1 else v)
        for k, v in config.items()
    }


def _extract_resources(raw: dict) -> dict:
    """
    Shared normalization logic. Returns {resource_type: {resource_name: {...attrs}}}.
    """
    resources: dict = {}
    for block in raw.get("resource", []):
        for raw_resource_type, named_configs in block.items():
            resource_type = _strip_quotes(raw_resource_type)
            resources.setdefault(resource_type, {})
            for raw_resource_name, config in named_configs.items():
                resource_name = _strip_quotes(raw_resource_name)
                cleaned = _strip_quotes(config)
                resources[resource_type][resource_name] = _flatten_config(cleaned)
    return resources


def _extract_providers(raw: dict) -> dict:
    """
    Extract provider blocks and their configuration.
    Returns: {provider_name: {config_dict}}
    e.g., {"aws": {"region": "us-east-1"}, "aws.mumbai": {"region": "ap-south-1"}}
    """
    providers: dict = {}
    for block in raw.get("provider", []):
        for provider_name, config in block.items():
            provider_name = _strip_quotes(provider_name)
            cleaned = _strip_quotes(config)
            providers[provider_name] = _flatten_config(cleaned)
    return providers


def _resolve_provider_for_resource(resource_type: str, providers: dict) -> dict:
    """
    Map a resource type to its provider defaults.
    aws_s3_bucket -> aws provider
    azurerm_storage_account -> azurerm provider
    """
    prefix = resource_type.split("_")[0]
    
    # Check for aliased provider first (e.g., "aws.mumbai")
    for provider_name, config in providers.items():
        if provider_name.startswith(f"{prefix}."):
            return config
        if provider_name == prefix:
            return config
    
    return {}


@dataclass
class ResolvedResource:
    """
    A Terraform resource with its provider defaults merged in.
    
    Resource-level attributes always win over provider defaults,
    matching Terraform's actual behavior.
    """
    resource_type: str
    resource_name: str
    config: dict
    provider_defaults: dict
    file_path: str = ""

    def get(self, key: str, default=None):
        """
        Look up an attribute. Resource-level value wins over provider default.
        This mirrors how Terraform resolves values.
        """
        if key in self.config and self.config[key] is not None:
            return self.config[key]
        return self.provider_defaults.get(key, default)


def parse_terraform_string(raw_text: str) -> dict:
    """
    Parse raw HCL text directly, without needing it saved as a file first.
    Returns {resource_type: {resource_name: config}} for backward compat.
    """
    raw = hcl2.load(io.StringIO(raw_text))
    return _extract_resources(raw)


def parse_terraform_file(file_path: str) -> dict:
    """Parse a single .tf file, return {resource_type: {name: config}}."""
    with open(file_path, "r") as f:
        raw = hcl2.load(f)
    return _extract_resources(raw)


def parse_terraform_file_with_providers(file_path: str) -> tuple[dict, dict]:
    """
    Parse a single .tf file and return (resources, providers).
    """
    with open(file_path, "r") as f:
        raw = hcl2.load(f)
    return _extract_resources(raw), _extract_providers(raw)


def parse_terraform_directory(dir_path: str) -> dict:
    """
    Parse every .tf file under a directory and merge into one resource map.
    Excludes .terraform/ directories (downloaded provider/modules).
    """
    all_resources: dict = {}
    for tf_file in Path(dir_path).rglob("*.tf"):
        if ".terraform" in tf_file.parts:
            continue
        file_resources = parse_terraform_file(str(tf_file))
        for resource_type, named_configs in file_resources.items():
            all_resources.setdefault(resource_type, {})
            all_resources[resource_type].update(named_configs)
    return all_resources


def parse_terraform_directory_parallel(dir_path: str, workers: int | None = None) -> dict:
    """
    Same as parse_terraform_directory, but parses files across multiple
    CPU cores in parallel.
    """
    tf_files = [str(p) for p in Path(dir_path).rglob("*.tf") if ".terraform" not in p.parts]
    if not tf_files:
        return {}

    all_resources: dict = {}
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for file_resources in executor.map(parse_terraform_file, tf_files):
            for resource_type, named_configs in file_resources.items():
                all_resources.setdefault(resource_type, {})
                all_resources[resource_type].update(named_configs)

    return all_resources


def iter_terraform_directory(dir_path: str, workers: int | None = None):
    """
    Generator version for large datasets. Yields (file_path, resources) tuples.
    Excludes .terraform/ directories.
    """
    tf_files = [str(p) for p in Path(dir_path).rglob("*.tf") if ".terraform" not in p.parts]
    if not tf_files:
        return

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(parse_terraform_file, f): f for f in tf_files
        }
        for future in as_completed(futures):
            file_path = futures[future]
            yield file_path, future.result()


def parse_terraform_directory_resolved(dir_path: str) -> list[ResolvedResource]:
    """
    Parse all .tf files, collect providers from all files, then resolve
    each resource against its matching provider defaults.
    
    This is the provider-aware parsing that fixes the region inheritance bug.
    """
    # First pass: collect all providers and resources
    all_providers: dict = {}
    file_data: dict = {}  # {file_path: (resources, providers)}
    
    for tf_file in Path(dir_path).rglob("*.tf"):
        if ".terraform" in tf_file.parts:
            continue
        resources, providers = parse_terraform_file_with_providers(str(tf_file))
        file_data[str(tf_file)] = resources
        all_providers.update(providers)
    
    # Second pass: resolve each resource
    resolved: list[ResolvedResource] = []
    for file_path, resources in file_data.items():
        for resource_type, named_configs in resources.items():
            provider_defaults = _resolve_provider_for_resource(resource_type, all_providers)
            for resource_name, config in named_configs.items():
                resolved.append(ResolvedResource(
                    resource_type=resource_type,
                    resource_name=resource_name,
                    config=config,
                    provider_defaults=provider_defaults,
                    file_path=file_path,
                ))
    
    return resolved