from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    """
    Describes where a resource originated from.
    """

    file_path: str
    line: int | None = None
    column: int | None = None
