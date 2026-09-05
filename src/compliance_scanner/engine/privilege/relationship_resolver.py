from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.engine.privilege.privilege_relationship import (
    PrivilegeRelationship,
)
from compliance_scanner.graph.resource_index import ResourceIndex
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.graph.reference_parser import (
    ReferenceParser,
)
from compliance_scanner.catalog.canonical_types import CanonicalType


class PrivilegeRelationshipResolver:
    """
    Resolves privilege relationships declared in the catalog into
    runtime PrivilegeRelationship objects.
    """

    def __init__(self, catalog):
        self.catalog = catalog
        self._parser = ReferenceParser()

    def resolve(
        self,
        resource: ResolvedResource,
        resource_index: ResourceIndex,
    ) -> tuple[PrivilegeRelationship, ...]:

        definition = self.catalog.definition(resource)

        if definition is None:
            return ()

        relationships: list[PrivilegeRelationship] = []

        for (
            attribute_name,
            attribute_definition,
        ) in definition.attributes.items():

            privilege_relationship = attribute_definition.privilege_relationship

            if privilege_relationship is None:
                continue

            attribute_value = resource.get(
                attribute_name,
            )

            if attribute_value is None:
                continue

            for target in self._resolve_targets(
                attribute_value,
                resource_index,
                privilege_relationship.target,
            ):
                relationships.append(
                    PrivilegeRelationship(
                        source=resource,
                        target=target,
                        relationship_type=(privilege_relationship.relationship_type),
                    )
                )

        return tuple(relationships)

    def _resolve_targets(
        self,
        value: object,
        resource_index: ResourceIndex,
        expected_type: CanonicalType,
    ) -> tuple[ResolvedResource, ...]:

        parser = ReferenceParser()

        targets: list[ResolvedResource] = []

        references = self._parser.parse_references(value)

        for resource_type, resource_name in references:

            resource = resource_index.get(
                resource_type,
                resource_name,
            )

            if resource is None:
                continue

            definition = self.catalog.definition(
                resource,
            )

            if definition is None:
                continue

            if definition.canonical_type != expected_type:
                continue

            targets.append(
                resource,
            )

        return tuple(targets)
