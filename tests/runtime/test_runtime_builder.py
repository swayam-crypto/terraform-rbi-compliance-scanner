from compliance_scanner.runtime import RuntimeBuilder

from compliance_scanner.models.platform import Platform
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation
from compliance_scanner.parser.provider_utils import infer_provider


def make_resource(
    resource_type: str,
    resource_name: str,
) -> ResolvedResource:
    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=infer_provider(resource_type),
        resource_type=resource_type,
        resource_name=resource_name,
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )


def test_runtime_builder_builds_runtime():

    resources = [
        make_resource(
            "aws_instance",
            "web",
        ),
        make_resource(
            "aws_subnet",
            "private",
        ),
    ]

    context = RuntimeBuilder().build(
        resources,
    )

    assert context.resources == resources

    assert len(context.canonical_resources) == len(resources)

    assert context.resource_index is not None

    assert context.relationship_graph is not None
