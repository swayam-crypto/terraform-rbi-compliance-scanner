"""
Parses .tf files into a plain Python structure the rule engine can read.

Uses python-hcl2 to do the actual HCL parsing — we just normalize its
output into a simpler {resource_type: {resource_name: {...attrs}}} shape.
"""

from pathlib import Path
import hcl2


def _strip_quotes(value):
    """
    python-hcl2 (8.x) sometimes preserves literal surrounding quote
    characters in parsed string values/keys, e.g. '"us-east-1"' instead
    of 'us-east-1'. Recursively clean these so downstream rule code can
    compare plain strings.
    """
    if isinstance(value, str):
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            return value[1:-1]
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


def parse_terraform_file(file_path: str) -> dict:
    """Parse a single .tf file, return {resource_type: {name: config}}."""
    resources: dict = {}

    with open(file_path, "r") as f:
        raw = hcl2.load(f)

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


def parse_terraform_directory(dir_path: str) -> dict:
    """Parse every .tf file in a directory, merge into one resource map."""
    all_resources: dict = {}
    for tf_file in Path(dir_path).glob("*.tf"):
        file_resources = parse_terraform_file(str(tf_file))
        for resource_type, named_configs in file_resources.items():
            all_resources.setdefault(resource_type, {})
            all_resources[resource_type].update(named_configs)
    return all_resources
