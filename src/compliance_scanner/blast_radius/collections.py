from compliance_scanner.blast_radius.models import BlastRadius
from compliance_scanner.models.resolved_resource import ResolvedResource


class BlastRadiusCollection:
    """
    Read-only collection of blast radius analyses.
    """

    def __init__(
        self,
        blast_radii: tuple[BlastRadius, ...],
    ):
        self._blast_radii = blast_radii

        self._by_source = {
            blast_radius.source: blast_radius for blast_radius in blast_radii
        }

    def __iter__(self):
        return iter(self._blast_radii)

    def __len__(self):
        return len(self._blast_radii)

    def all(
        self,
    ) -> tuple[BlastRadius, ...]:
        return self._blast_radii

    def for_resource(
        self,
        resource: ResolvedResource,
    ) -> BlastRadius | None:
        return self._by_source.get(resource)
