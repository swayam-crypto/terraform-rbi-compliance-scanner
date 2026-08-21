from dataclasses import dataclass

from compliance_scanner.attack.models import AttackPath
from collections.abc import Iterator


@dataclass(
    frozen=True,
    slots=True,
)
class AttackPathCollection:
    """
    Represents the attack paths discovered during infrastructure
    analysis.

    The collection is immutable and provides a reusable result that
    higher analysis layers may consume.
    """

    paths: tuple[AttackPath, ...]

    def __contains__(
        self,
        path: AttackPath,
    ) -> bool:
        return path in self.paths

    def __len__(
        self,
    ) -> int:
        return len(self.paths)

    def __iter__(
        self,
    ) -> Iterator[AttackPath]:
        return iter(self.paths)

    def __bool__(
        self,
    ) -> bool:
        return bool(self.paths)

    def __getitem__(
        self,
        index: int,
    ) -> AttackPath:
        return self.paths[index]
