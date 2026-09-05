from compliance_scanner.catalog.global_catalog import catalog
from compliance_scanner.catalog.canonical_types import CanonicalType


def test_global_catalog_loads():

    assert len(catalog.registry) > 0


def test_aws_iam_role_is_registered():

    definition = catalog.registry.get(
        "aws_iam_role",
    )

    assert definition is not None

    assert definition.canonical_type is CanonicalType.ROLE


def test_aws_iam_policy_is_registered():

    definition = catalog.registry.get(
        "aws_iam_policy",
    )

    assert definition is not None

    assert definition.canonical_type is CanonicalType.POLICY
