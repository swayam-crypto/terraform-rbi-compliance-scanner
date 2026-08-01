from compliance_scanner.catalog.models import ResourceDefinition


class CatalogRegistry:
    """
    Stores every known cloud resource definition.
    """

    def __init__(self):

        self._resources: dict[
            str,
            ResourceDefinition,
        ] = {}

    def register(
        self,
        resource_type: str,
        definition: ResourceDefinition,
    ) -> None:
        """
        Register a resource definition.

        Raises:
            ValueError: If the resource type has already been registered.
        """

        if resource_type in self._resources:
            raise ValueError(f"Resource type '{resource_type}' is already registered.")

        self._resources[resource_type] = definition

    def get(
        self,
        resource_type: str,
    ) -> ResourceDefinition | None:

        return self._resources.get(resource_type)

    def has(
        self,
        resource_type: str,
    ) -> bool:

        return resource_type in self._resources

    def all(
        self,
    ) -> tuple[ResourceDefinition, ...]:
        """
        Return all registered resource definitions.
        """
        return tuple(self._resources.values())

    def clear(
        self,
    ) -> None:
        """
        Remove all registered resource definitions.
        """
        self._resources.clear()

    def __len__(
        self,
    ) -> int:
        return len(self._resources)

    def __contains__(
        self,
        resource_type: str,
    ) -> bool:
        return resource_type in self._resources
