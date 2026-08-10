"""IaC parser contract used by the compliance engine boundary."""
from pathlib import Path
from typing import Protocol
from compliance_scanner.models.resolved_resource import ResolvedResource


class InfrastructureParser(Protocol):
    def parse_directory(self, path: Path) -> list[ResolvedResource]: ...
    def parse_plan(self, path: Path) -> list[ResolvedResource]: ...
