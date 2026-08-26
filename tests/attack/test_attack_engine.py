from compliance_scanner.engine.attack.engine import AttackPathEngine
from compliance_scanner.engine.attack.collection import AttackPathCollection


class FakeFinder:

    def __init__(
        self,
        collection: AttackPathCollection,
    ):
        self.collection = collection
        self.calls = []

    def find_paths(
        self,
        source,
        target,
    ):
        self.calls.append(
            (
                source,
                target,
            )
        )

        return self.collection


class FakeCatalog:

    def __init__(
        self,
        entry_points,
        targets,
    ):
        self.entry_points = set(entry_points)
        self.targets = set(targets)

    def has_capability(
        self,
        resource,
        capability,
    ):

        if capability == AttackPathEngine.ENTRY_POINT_CAPABILITY:
            return resource in self.entry_points

        if capability == AttackPathEngine.TARGET_CAPABILITY:
            return resource in self.targets

        return False
