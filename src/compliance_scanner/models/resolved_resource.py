from dataclasses import dataclass
from typing import Any

from .platform import Platform
from .provider import CloudProvider
from .source_location import SourceLocation


@dataclass(frozen=True)
class ResolvedResource:
    """
    Platform-independent representation of an infrastructure resource.

    Every parser (Terraform, CloudFormation, Pulumi, Bicep,
    Kubernetes, etc.) should normalize resources into this model.
    """

    platform: Platform
    provider: CloudProvider

    resource_type: str
    resource_name: str

    attributes: dict[str, Any]
    default_attributes: dict[str, Any]

    source: SourceLocation

    def get(self, key: str, default: Any = None) -> Any:
        """
        Return a property value.

        Resource properties always override provider defaults.
        """

        if key in self.attributes and self.attributes[key] is not None:
            return self.attributes[key]

        return self.default_attributes.get(key, default)
