"""
Caches parsed Terraform file results so repeated scans of a large
dataset don't re-parse files that haven't changed.

Why this matters: in a real CI pipeline, most commits touch a handful
of .tf files, not all of them. Without caching, a 100,000-file repo
gets fully re-parsed on every single push, which wastes minutes on
every CI run for no reason. With caching, only changed files get
re-parsed; everything else is read straight from the cache.

Cache key: file path + mtime + size. If any of these change, the file
is treated as modified and re-parsed. This is a cheap, "good enough"
check — it doesn't hash file contents (slower), but mtime+size changing
is a reliable enough signal for how Terraform files are actually edited.
"""

import json
import os
from pathlib import Path

DEFAULT_CACHE_PATH = ".rbi_scan_cache.json"


def _file_signature(file_path: str) -> tuple:
    stat = os.stat(file_path)
    return (stat.st_mtime, stat.st_size)


def load_cache(cache_path: str = DEFAULT_CACHE_PATH) -> dict:
    """Load the cache file from disk. Returns empty dict if none exists yet."""
    if not Path(cache_path).exists():
        return {}
    try:
        with open(cache_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Corrupted or unreadable cache — safer to start fresh than crash
        return {}


def save_cache(cache: dict, cache_path: str = DEFAULT_CACHE_PATH) -> None:
    with open(cache_path, "w") as f:
        json.dump(cache, f)


def get_cached_or_none(file_path: str, cache: dict):
    """
    Returns the cached parsed resources for this file if the file
    hasn't changed since it was cached, otherwise returns None
    (meaning: caller should re-parse it).
    """
    entry = cache.get(file_path)
    if entry is None:
        return None

    current_mtime, current_size = _file_signature(file_path)
    if entry["mtime"] == current_mtime and entry["size"] == current_size:
        return entry["resources"]

    return None  # file changed since last scan


def update_cache_entry(file_path: str, resources: dict, cache: dict) -> None:
    mtime, size = _file_signature(file_path)
    cache[file_path] = {"mtime": mtime, "size": size, "resources": resources}
