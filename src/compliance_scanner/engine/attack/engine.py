from compliance_scanner.engine.attack.collection import AttackPathCollection
from compliance_scanner.engine.attack.finder import AttackPathFinder
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.catalog import Catalog
from compliance_scanner.engine.attack.models import AttackPath
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.engine.base import AnalysisEngine
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compliance_scanner.runtime.scan_context import ScanContext


class AttackPathEngine(AnalysisEngine):
    """
    Discovers attack paths across the infrastructure.

    The engine orchestrates attack path analysis by identifying attack
    sources and objectives before delegating path discovery to the
    AttackPathFinder.
    """

    runtime_field = "attack_paths"
    _ENTRY_POINT_CAPABILITY = "public_entry_point"

    _TARGET_CAPABILITY = "data_store"

    def __init__(
        self,
        context: "ScanContext",
        catalog_instance: Catalog = catalog,
        finder: AttackPathFinder | None = None,
    ) -> None:

        super().__init__(context)
        self.catalog = catalog_instance

        self.finder = (
            finder
            if finder is not None
            else AttackPathFinder(
                context.knowledge.relationship_graph,
            )
        )

    def _sources(
        self,
    ) -> tuple[ResolvedResource, ...]:
        return tuple(
            resource
            for resource in self.context.resources
            if self.catalog.has_capability(
                resource,
                self._ENTRY_POINT_CAPABILITY,
            )
        )

    def _targets(
        self,
    ) -> tuple[ResolvedResource, ...]:
        return tuple(
            resource
            for resource in self.context.resources
            if self.catalog.has_capability(
                resource,
                self._TARGET_CAPABILITY,
            )
        )

    def analyze(
        self,
    ) -> AttackPathCollection:

        paths: list[AttackPath] = []

        for source in self._sources():

            for target in self._targets():

                collection = self.finder.find_paths(
                    source,
                    target,
                )

                for path in collection:
                    paths.append(path)

        return AttackPathCollection(
            paths=tuple(paths),
        )
