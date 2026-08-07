from enum import Enum


class ResourceKind(str, Enum):
    """
    High-level classification of cloud resources.

    These categories are intentionally provider-agnostic.
    """

    COMPUTE = "compute"

    STORAGE = "storage"

    DATA = "data"

    NETWORK = "network"

    SECURITY = "security"

    IDENTITY = "identity"

    CONTAINER = "container"

    ANALYTICS = "analytics"

    INTEGRATION = "integration"

    MANAGEMENT = "management"

    OBSERVABILITY = "observability"

    AI = "ai"

    OTHER = "other"
