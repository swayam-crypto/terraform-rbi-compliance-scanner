"""Terraform implementation of the parser boundary."""

from pathlib import Path
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.plan_parser import parse_plan_file
from compliance_scanner.parser.provider_utils import infer_provider
from compliance_scanner.parser.terraform_parser import (
    _resolve_provider_for_resource,
    parse_terraform_file_with_providers,
)


class TerraformParser:
    def parse_directory(self, path: Path) -> list[ResolvedResource]:
        providers, files = {}, {}
        for file_path in path.rglob("*.tf"):
            if ".terraform" in file_path.parts:
                continue
            resources, discovered = parse_terraform_file_with_providers(str(file_path))
            files[str(file_path)] = resources
            providers.update(discovered)
        return [
            ResolvedResource(
                platform=Platform.TERRAFORM,
                provider=infer_provider(resource_type),
                resource_type=resource_type,
                resource_name=resource_name,
                attributes=config,
                default_attributes=_resolve_provider_for_resource(
                    resource_type, providers
                ),
                source=SourceLocation(file_path=file_path),
            )
            for file_path, resources in files.items()
            for resource_type, named in resources.items()
            for resource_name, config in named.items()
        ]

    def parse_plan(self, path: Path) -> list[ResolvedResource]:
        return parse_plan_file(str(path))
