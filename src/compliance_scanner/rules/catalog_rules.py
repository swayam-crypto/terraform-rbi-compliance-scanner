"""Reusable capability-native rules for catalog attributes.

Rule specifications carry policy; this module only evaluates normalized
catalog attributes. A new provider participates by declaring capabilities and
attribute mappings in YAML, without changing this evaluator.
"""

from dataclasses import dataclass
from typing import Any, Callable

from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.compliance.controls import ComplianceControl

from .base import BaseRule, Finding


Predicate = Callable[[Any], bool]


@dataclass(frozen=True)
class AttributeRuleSpec:
    rule_id: str
    description: str
    regulation_reference: str
    severity: str
    control: ComplianceControl
    required_capabilities: frozenset[str]
    attribute_key: str
    violates: Predicate
    failure_message: str


class CatalogAttributeRule(BaseRule):
    """Evaluate a single canonical attribute for resources with capabilities."""

    def __init__(self, spec: AttributeRuleSpec):
        self.spec = spec
        self.rule_id = spec.rule_id
        self.description = spec.description
        self.regulation_reference = spec.regulation_reference
        self.severity = spec.severity
        self.control = spec.control
        self.required_capabilities = spec.required_capabilities

    def check(self, resource) -> Finding | None:
        if not self.applies_to_resource(resource, catalog):
            return None

        attribute_name = catalog.attribute_name(resource, self.spec.attribute_key)
        if attribute_name is None:
            return None

        value = resource.get(attribute_name)
        if not self.spec.violates(value):
            return None

        return self.finding(
            resource,
            self.spec.failure_message.format(
                resource_name=resource.resource_name,
                attribute=attribute_name,
                value=value,
            ),
        )


def disabled(value: Any) -> bool:
    """True when an opt-in boolean/configuration is absent or disabled."""
    return value is None or value is False or value == {} or value == []


def below(minimum: int) -> Predicate:
    def predicate(value: Any) -> bool:
        try:
            return int(value) < minimum
        except (TypeError, ValueError):
            return True

    return predicate
