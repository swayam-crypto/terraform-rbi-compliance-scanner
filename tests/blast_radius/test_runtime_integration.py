from compliance_scanner.engine.blast_radius.engine import BlastRadiusEngine
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


def test_blast_radius_runtime_integration():

    resources = [
        make_resource(
            "aws_lb",
            "public",
        ),
        make_resource(
            "aws_db_instance",
            "database",
        ),
    ]

    context = RuntimeBuilder().build(
        resources,
    )

    context.analysis.blast_radius = BlastRadiusEngine(
        context,
    ).analyze()

    assert context.analysis.blast_radius is not None

    assert len(context.analysis.blast_radius) == len(resources)
