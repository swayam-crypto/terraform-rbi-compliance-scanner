"""
Parser for Terraform Plan JSON files.

Converts Terraform's evaluated plan output into the same
ResolvedResource objects used by the Terraform parser.

This allows the rule engine to scan Terraform Plans without
changing any compliance rules.
"""

import json

from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def parse_plan_file(path: str) -> list[ResolvedResource]:
    """
    Parse a Terraform plan JSON file.

    Expected input:

        terraform show -json tfplan > tfplan.json

    Returns
    -------
    list[ResolvedResource]
    """

    with open(path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    planned_values = plan.get("planned_values", {})
    root_module = planned_values.get("root_module")

    if root_module is None:
        return []

    resources: list[ResolvedResource] = []

    _extract_module_resources(root_module, resources)

    return resources


def _extract_module_resources(
    module: dict,
    resources: list[ResolvedResource],
):
    """
    Recursively extract resources from a Terraform plan module.

    Terraform Plans may contain:

        root_module
            ├── resources
            └── child_modules
                    ├── resources
                    └── child_modules
    """

    for resource in module.get("resources", []):

        resources.append(
            ResolvedResource(
                platform=Platform.TERRAFORM,
                provider=infer_provider(resource["type"]),
                resource_type=resource["type"],
                resource_name=resource["name"],
                attributes=resource.get("values", {}),
                default_attributes={},
                source=SourceLocation(
                    resource_address=resource.get("address", ""),
                ),
            )
        )

    for child in module.get("child_modules", []):

        _extract_module_resources(child, resources)
