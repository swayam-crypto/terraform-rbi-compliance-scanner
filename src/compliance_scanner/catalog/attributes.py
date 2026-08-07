from dataclasses import dataclass
from enum import Enum
from typing import Any


class AttributeType(str, Enum):
    """
    Supported attribute data types.
    """

    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"
    ENUM = "enum"
    LIST = "list"
    OBJECT = "object"


@dataclass(frozen=True)
class AttributeDefinition:
    """
    Describes a compliance-relevant attribute for a resource.
    """

    name: str

    type: AttributeType

    default: Any | None = None

    description: str = ""
