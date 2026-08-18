from dataclasses import is_dataclass
from types import MappingProxyType

from compliance_scanner.canonical.context import CanonicalContext


def test_context_is_dataclass():
    assert is_dataclass(CanonicalContext)


def test_context_default_attributes_are_empty():
    context = CanonicalContext(
        resource=None,
        definition=None,
    )

    assert context.canonical_attributes == {}
    assert isinstance(
        context.canonical_attributes,
        MappingProxyType,
    )
