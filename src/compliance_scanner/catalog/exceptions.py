class CatalogValidationError(ValueError):
    """
    Raised when a catalog entry fails validation.
    """

    def __init__(
        self,
        *,
        resource: str,
        field: str,
        reason: str,
        value: object | None = None,
        expected: str | None = None,
    ) -> None:

        lines = [
            f"Catalog validation failed for '{resource}'",
            f"Field: {field}",
            f"Reason: {reason}",
        ]

        if value is not None:
            lines.append(f"Value: {value}")

        if expected is not None:
            lines.append(f"Expected: {expected}")

        super().__init__("\n".join(lines))
