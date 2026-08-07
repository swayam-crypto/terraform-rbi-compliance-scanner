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

        message = (
            "\n"
            "========================================\n"
            "Catalog Validation Error\n"
            "========================================\n\n"
            f"Resource : {resource}\n"
            f"Field    : {field}\n"
        )

        if value is not None:
            message += f"Value    : {value}\n"

        message += f"Reason   : {reason}\n"

        if expected:
            message += f"Expected : {expected}\n"

        super().__init__(message)
