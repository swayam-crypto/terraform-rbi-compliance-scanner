from compliance_scanner.catalog.privilege_relationship_types import (
    PrivilegeRelationshipType,
)


def test_privilege_relationship_type_values():

    assert PrivilegeRelationshipType.IDENTITY == "identity"

    assert PrivilegeRelationshipType.GRANTS == "grants"


def test_privilege_relationship_type_lookup():

    assert PrivilegeRelationshipType("identity") is PrivilegeRelationshipType.IDENTITY

    assert PrivilegeRelationshipType("grants") is PrivilegeRelationshipType.GRANTS
