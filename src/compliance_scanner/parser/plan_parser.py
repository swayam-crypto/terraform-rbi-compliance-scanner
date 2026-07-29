"""
Parser for Terraform Plan JSON files.

Converts Terraform's evaluated plan output into the same
ResolvedResource objects used by the Terraform parser.

This allows the rule engine to scan Terraform Plans without
changing any compliance rules.
"""

import json

from compliance_scanner.parser.terraform_parser import ResolvedResource


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
                resource_type=resource["type"],
                resource_name=resource["name"],
                config=resource.get("values", {}),
                provider_defaults={},
                file_path=resource.get("address", ""),
            )
        )

    for child in module.get("child_modules", []):

        _extract_module_resources(child, resources)
