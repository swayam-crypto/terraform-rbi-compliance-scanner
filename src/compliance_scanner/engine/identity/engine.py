from compliance_scanner.engine.privilege.graph import PrivilegeGraph
from compliance_scanner.engine.identity.collection import IdentityCollection
from compliance_scanner.engine.identity.finder import IdentityFinder
from compliance_scanner.runtime.scan_context import ScanContext


class IdentityEngine:
    """
    Runtime entry point for identity analysis.

    The engine constructs the privilege graph view required for
    identity analysis before delegating computation to the
    IdentityFinder.
    """

    def __init__(
        self,
        context: ScanContext,
    ) -> None:
        self.context = context

    def analyze(
        self,
    ) -> IdentityCollection:

        finder = IdentityFinder(
            self.context.knowledge.privilege_graph,
        )

        return finder.analyze(
            self.context.resources,
        )
