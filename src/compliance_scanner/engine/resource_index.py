"""Indexed, read-only access to resources participating in a scan.

Cross-resource rules need to query the complete scan set without depending on
how Terraform files or plans were parsed.  ``ResourceIndex`` provides that
boundary while retaining the original resource order for deterministic rules
and reports.
"""

from collections import defaultdict
from collections.abc import Iterable, Iterator

from compliance_scanner.models.resolved_resource import ResolvedResource


class ResourceIndex:
    """Read-only lookup collection for :class:`ResolvedResource` objects.

    A Terraform plan can contain identically named resources in separate
    modules.  Therefore ``find`` always returns every matching resource rather
    than silently selecting one.  Rules that require a single target can make
    an explicit decision when a lookup is ambiguous.
    """

    def __init__(self, resources: Iterable[ResolvedResource] = ()) -> None:
        self._resources = tuple(resources)

        by_type: dict[str, list[ResolvedResource]] = defaultdict(list)
        by_name: dict[str, list[ResolvedResource]] = defaultdict(list)
        by_type_and_name: dict[tuple[str, str], list[ResolvedResource]] = defaultdict(
            list
        )

        for resource in self._resources:
            by_type[resource.resource_type].append(resource)
            by_name[resource.resource_name].append(resource)
            by_type_and_name[(resource.resource_type, resource.resource_name)].append(
                resource
            )

        self._by_type = {key: tuple(value) for key, value in by_type.items()}
        self._by_name = {key: tuple(value) for key, value in by_name.items()}
        self._by_type_and_name = {
            key: tuple(value) for key, value in by_type_and_name.items()
        }

    def __len__(self) -> int:
        return len(self._resources)

    def __iter__(self) -> Iterator[ResolvedResource]:
        return iter(self._resources)

    @property
    def resources(self) -> tuple[ResolvedResource, ...]:
        """All indexed resources, in their original scan order."""
        return self._resources

    @property
    def resource_types(self) -> frozenset[str]:
        """The Terraform resource types represented in the index."""
        return frozenset(self._by_type)

    def of_type(self, resource_type: str) -> tuple[ResolvedResource, ...]:
        """Return resources of ``resource_type``; returns an empty tuple if absent."""
        return self._by_type.get(resource_type, ())

    def named(self, resource_name: str) -> tuple[ResolvedResource, ...]:
        """Return resources with a Terraform logical name across all types."""
        return self._by_name.get(resource_name, ())

    def find(
        self, resource_type: str, resource_name: str
    ) -> tuple[ResolvedResource, ...]:
        """Return exact type-and-name matches; never guesses between modules."""
        return self._by_type_and_name.get((resource_type, resource_name), ())
