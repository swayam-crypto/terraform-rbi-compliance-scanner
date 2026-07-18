"""
Parses .tf files into a plain Python structure the rule engine can read.

Uses python-hcl2 to do the actual HCL parsing — we just normalize its
output into a simpler {resource_type: {resource_name: {...attrs}}} shape.
"""
import hcl2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import io


def _strip_quotes(value):
    """
    python-hcl2 (8.x) sometimes preserves literal surrounding quote
    characters in parsed string values/keys, e.g. '"us-east-1"' instead
    of 'us-east-1'. Recursively clean these so downstream rule code can
    compare plain strings.

    Also unescapes backslash-escaped quotes and backslashes inside the
    string (e.g. an inline JSON policy written as "{\"Action\": \"*\"}")
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

def _extract_resources(raw: dict) -> dict:
    """
    Shared normalization logic used by both file-based and string-based
    parsing. Takes hcl2's raw parsed output, returns the clean
    {resource_type: {resource_name: {...attrs}}} shape.
    """
    resources: dict = {}
    for block in raw.get("resource", []):
        for raw_resource_type, named_configs in block.items():
            resource_type = _strip_quotes(raw_resource_type)
            resources.setdefault(resource_type, {})
            for raw_resource_name, config in named_configs.items():
                resource_name = _strip_quotes(raw_resource_name)
                cleaned = _strip_quotes(config)
                # hcl2 wraps single-value lists — flatten for easier access
                flat_config = {
                    k: (v[0] if isinstance(v, list) and len(v) == 1 else v)
                    for k, v in cleaned.items()
                }
                resources[resource_type][resource_name] = flat_config
    return resources


def parse_terraform_string(raw_text: str) -> dict:
    """
    Parse raw HCL text directly, without needing it saved as a file
    first. Useful when Terraform config arrives as a string — e.g.
    pulled from an API response, a CI artifact, or piped input —
    rather than sitting on disk as a .tf file.
    """
    raw = hcl2.load(io.StringIO(raw_text))
    return _extract_resources(raw)


def parse_terraform_file(file_path: str) -> dict:
    """Parse a single .tf file, return {resource_type: {name: config}}."""
    with open(file_path, "r") as f:
        raw = hcl2.load(f)
    return _extract_resources(raw)


def parse_terraform_directory(dir_path: str) -> dict:
    """
    Parse every .tf file under a directory, including nested module
    subfolders, and merge into one resource map.

    Uses rglob (recursive glob) instead of glob so it finds files in
    subdirectories too — real Terraform projects are rarely flat.
    """
    all_resources: dict = {}
    for tf_file in Path(dir_path).rglob("*.tf"):
        file_resources = parse_terraform_file(str(tf_file))
        for resource_type, named_configs in file_resources.items():
            all_resources.setdefault(resource_type, {})
            all_resources[resource_type].update(named_configs)
    return all_resources


def parse_terraform_directory_parallel(dir_path: str, workers: int | None = None) -> dict:
    """
    Same as parse_terraform_directory, but parses files across multiple
    CPU cores in parallel. Use this for large datasets (thousands of
    files) — HCL parsing is CPU-bound and single-file parsing doesn't
    benefit from more workers, but scanning many files does.

    workers=None lets Python pick based on available CPU cores.
    """
    tf_files = [str(p) for p in Path(dir_path).rglob("*.tf")]
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
    Generator version for large datasets. Parses files in parallel but
    YIELDS each file's resources as soon as it's ready, instead of
    waiting for the entire directory and building one giant dict.

    Why this matters at scale: parse_terraform_directory_parallel still
    holds every resource from every file in memory at once before
    returning. At 100,000 files that's a real memory cost. This version
    lets the caller (the scan engine) process and discard each file's
    resources immediately, so peak memory stays roughly constant
    regardless of dataset size.

    Yields: (file_path, {resource_type: {resource_name: config}})
    """
    tf_files = [str(p) for p in Path(dir_path).rglob("*.tf")]
    if not tf_files:
        return

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(parse_terraform_file, f): f for f in tf_files
        }
        for future in as_completed(futures):
            file_path = futures[future]
            yield file_path, future.result()
