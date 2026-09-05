from compliance_scanner.catalog.privilege_relationships import (
    PrivilegeRelationshipDefinition,
)
from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)
from compliance_scanner.catalog.canonical_types import CanonicalType


def test_privilege_relationship_definition():

    relationship = PrivilegeRelationshipDefinition(
        relationship_type=PrivilegeRelationshipType.IDENTITY,
        target=CanonicalType.ROLE,
    )

    assert relationship.relationship_type is (PrivilegeRelationshipType.IDENTITY)

    assert relationship.target is CanonicalType.ROLE

    assert relationship.required is False


def test_required_privilege_relationship():

    relationship = PrivilegeRelationshipDefinition(
        relationship_type=PrivilegeRelationshipType.GRANTS,
        target=CanonicalType.POLICY,
        required=True,
    )

    assert relationship.required is True
