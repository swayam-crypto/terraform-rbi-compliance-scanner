from unittest.mock import Mock

import pytest

from compliance_scanner.canonical.pipeline import CanonicalPipeline
from compliance_scanner.canonical.resource import CanonicalResource
from compliance_scanner.canonical.exceptions import (
    UnknownCanonicalResourceError,
)

from compliance_scanner.catalog.canonical_types import CanonicalType
from compliance_scanner.models.platform import Platform
from compliance_scanner.models.provider import CloudProvider
from compliance_scanner.models.resolved_resource import ResolvedResource
from compliance_scanner.models.source_location import SourceLocation


def make_resource():

    return ResolvedResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        resource_type="aws_s3_bucket",
        resource_name="bucket",
        attributes={},
        default_attributes={},
        source=SourceLocation(),
    )


def make_canonical():

    return CanonicalResource(
        platform=Platform.TERRAFORM,
        provider=CloudProvider.AWS,
        canonical_type=CanonicalType.OBJECT_STORAGE,
        resource_name="bucket",
        attributes={},
        capabilities=frozenset(),
        metadata={},
        source=SourceLocation(),
    )


def test_pipeline_returns_builder_result():

    catalog = Mock()

    builder = Mock()

    attribute_mapper = Mock()

    resource = make_resource()

    definition = Mock()

    canonical = make_canonical()

    catalog.definition.return_value = definition

    builder.build.return_value = canonical

    pipeline = CanonicalPipeline(
        catalog,
        builder,
        attribute_mapper,
    )

    result = pipeline.transform(resource)

    assert result is canonical


def test_pipeline_queries_catalog():

    catalog = Mock()

    builder = Mock()

    attribute_mapper = Mock()

    resource = make_resource()

    definition = Mock()

    builder.build.return_value = make_canonical()

    catalog.definition.return_value = definition

    pipeline = CanonicalPipeline(
        catalog,
        builder,
        attribute_mapper,
    )

    pipeline.transform(resource)

    catalog.definition.assert_called_once_with(resource)


def test_pipeline_calls_builder():

    catalog = Mock()

    builder = Mock()

    attribute_mapper = Mock()

    resource = make_resource()

    definition = Mock()

    builder.build.return_value = make_canonical()

    catalog.definition.return_value = definition

    pipeline = CanonicalPipeline(
        catalog,
        builder,
        attribute_mapper,
    )

    pipeline.transform(resource)

    builder.build.assert_called_once()
    attribute_mapper.map.assert_called_once()

    context = attribute_mapper.map.call_args.args[0]

    assert context.resource is resource
    assert context.definition is definition


def test_pipeline_unknown_resource():

    catalog = Mock()

    builder = Mock()

    attribute_mapper = Mock()

    catalog.definition.return_value = None

    pipeline = CanonicalPipeline(
        catalog,
        builder,
        attribute_mapper,
    )

    with pytest.raises(
        UnknownCanonicalResourceError,
    ):
        pipeline.transform(
            make_resource(),
        )
