"""
Parses inline suppression comments from raw Terraform file text.

Why this is a separate module from terraform_parser.py: HCL parsers
(including python-hcl2) strip comments when they parse into a data
structure — comments simply aren't part of the resulting dict. So
suppression directives can't be read from the parsed resource data at
all; they have to be read from the raw file text directly, then matched
back to the resource they precede.

Syntax supported:
    # rbi-scan:ignore RBI-001 reason="explanation"
    # rbi-scan:ignore-all reason="explanation"

Placement: the comment must appear on its own line, directly above the
resource block it applies to (blank lines and other comment lines in
between are allowed; anything else breaks the association).
"""

import re
from pathlib import Path

RESOURCE_LINE = re.compile(r'^\s*resource\s+"([^"]+)"\s+"([^"]+)"\s*{')
IGNORE_RULE = re.compile(r'^\s*#\s*rbi-scan:ignore\s+(\S+)(?:\s+reason="([^"]*)")?\s*$')
IGNORE_ALL = re.compile(r'^\s*#\s*rbi-scan:ignore-all(?:\s+reason="([^"]*)")?\s*$')
COMMENT_OR_BLANK = re.compile(r'^\s*(#.*)?$')


def extract_suppressions(file_path: str) -> dict:
    """
    Scan a .tf file for suppression comments and map them to the
    resource they precede.

    Returns: {(resource_type, resource_name): {"all": bool, "rules": set[str], "reasons": dict[str, str]}}
    """
    suppressions: dict = {}
    pending_rules: set = set()
    pending_all = False
    pending_reasons: dict = {}

    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        resource_match = RESOURCE_LINE.match(line)
        if resource_match:
            if pending_rules or pending_all:
                key = (resource_match.group(1), resource_match.group(2))
                suppressions[key] = {
                    "all": pending_all,
                    "rules": pending_rules,
                    "reasons": pending_reasons,
                }
            pending_rules = set()
            pending_all = False
            pending_reasons = {}
            continue

        ignore_all_match = IGNORE_ALL.match(line)
        if ignore_all_match:
            pending_all = True
            if ignore_all_match.group(1):
                pending_reasons["*"] = ignore_all_match.group(1)
            continue

        ignore_rule_match = IGNORE_RULE.match(line)
        if ignore_rule_match:
            rule_id = ignore_rule_match.group(1)
            pending_rules.add(rule_id)
            if ignore_rule_match.group(2):
                pending_reasons[rule_id] = ignore_rule_match.group(2)
            continue

        # Any other comment or blank line doesn't break the pending
        # suppression (allows multi-line reasons / spacing). Anything
        # else (real code) resets it — the suppression only applies to
        # the very next resource block.
        if not COMMENT_OR_BLANK.match(line):
            pending_rules = set()
            pending_all = False
            pending_reasons = {}

    return suppressions


def is_suppressed(rule_id: str, resource_type: str, resource_name: str, suppressions: dict) -> bool:
    """Check whether a specific rule finding for a resource should be suppressed."""
    entry = suppressions.get((resource_type, resource_name))
    if entry is None:
        return False
    if entry["all"]:
        return True
    return rule_id in entry["rules"]