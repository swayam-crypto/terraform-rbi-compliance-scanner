from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    """
    Describes where a resource originated from.
    """

    file_path: str | None = None
    resource_address: str | None = None
    line: int | None = None
    column: int | None = None
