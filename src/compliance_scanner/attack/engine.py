from compliance_scanner.attack.collection import AttackPathCollection
from compliance_scanner.attack.finder import AttackPathFinder
from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.scan_context import ScanContext


class AttackPathEngine:
    """
    Discovers attack paths across the infrastructure.

    The engine orchestrates attack path analysis by identifying attack
    sources and objectives before delegating path discovery to the
    AttackPathFinder.
    """

    ENTRY_POINT_CAPABILITY = "public_entry_point"

    TARGET_CAPABILITY = "data_store"

    def __init__(
        self,
        context: ScanContext,
    ) -> None:
        self.context = context

        self.finder = AttackPathFinder(
            context.relationship_graph,
        )

    def analyze(
        self,
    ) -> AttackPathCollection:

        paths = []

        sources = [
            resource
            for resource in self.context.resources
            if catalog.has_capability(
                resource,
                self.ENTRY_POINT_CAPABILITY,
            )
        ]

        targets = [
            resource
            for resource in self.context.resources
            if catalog.has_capability(
                resource,
                self.TARGET_CAPABILITY,
            )
        ]

        for source in sources:

            for target in targets:

                collection = self.finder.find_paths(
                    source,
                    target,
                )

                paths.extend(collection)

        return AttackPathCollection(
            paths=tuple(paths),
        )
