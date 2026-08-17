class CanonicalModelError(Exception):
    """
    Base exception for Canonical Cloud Model errors.
    """


class UnknownCanonicalResourceError(CanonicalModelError):
    """
    Raised when a resource cannot be classified because it is not
    defined in the catalog.
    """

    def __init__(self, resource_type: str):
        super().__init__(
            f"Unknown resource type '{resource_type}'. "
            "No canonical mapping exists in the catalog."
        )
        self.resource_type = resource_type
