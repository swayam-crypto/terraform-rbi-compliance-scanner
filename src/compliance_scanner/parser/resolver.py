"""
Expression resolver.

Currently supports:
- jsonencode()

Future support:
- var.*
- local.*
- templatefile()
- file()
- references
- modules
"""

from typing import Any
import io
import hcl2


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
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
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


def _resolve_jsonencode(value: str):
    """
    Resolve Terraform expressions like:

        ${jsonencode({...})}

    by feeding the inner HCL object back into python-hcl2.
    """

    prefix = "${jsonencode("
    suffix = ")}"

    if not (value.startswith(prefix) and value.endswith(suffix)):
        return value

    inner = value[len(prefix) : -len(suffix)]

    wrapped = f"value = {inner}"

    try:
        parsed = hcl2.load(io.StringIO(wrapped))
        return _strip_quotes(parsed["value"])
    except Exception as e:
        print(f"[resolver] Failed to parse jsonencode(): {e}")
        return value


def resolve_value(value: Any) -> Any:
    if isinstance(value, str):
        return _resolve_jsonencode(value)

    if isinstance(value, list):
        return [resolve_value(v) for v in value]

    if isinstance(value, dict):
        return {k: resolve_value(v) for k, v in value.items()}

    return value


def resolve_resource(resource: dict) -> dict:
    return {key: resolve_value(value) for key, value in resource.items()}
