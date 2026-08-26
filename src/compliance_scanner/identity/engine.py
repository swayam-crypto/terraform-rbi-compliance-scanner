from compliance_scanner.graph.privilege_graph import PrivilegeGraph
from compliance_scanner.identity.collection import IdentityCollection
from compliance_scanner.identity.finder import IdentityFinder
from compliance_scanner.scan_context import ScanContext


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
            self.context.privilege_graph,
        )

        return finder.analyze(
            self.context.resources,
        )
