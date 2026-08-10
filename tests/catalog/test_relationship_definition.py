from compliance_scanner.catalog.relationships import RelationshipDefinition
from compliance_scanner.catalog.relationship_types import RelationshipType
from compliance_scanner.catalog.canonical_types import CanonicalType


def test_relationship_definition():

    relationship = RelationshipDefinition(
        relationship_type=RelationshipType.SUBNET,
        target=CanonicalType.SUBNET,
    )

    assert relationship.relationship_type is RelationshipType.SUBNET

    assert relationship.required is False


def test_required_relationship():

    relationship = RelationshipDefinition(
        relationship_type=RelationshipType.KMS_KEY,
        target=CanonicalType.KMS_KEY,
        required=True,
    )

    assert relationship.relationship_type is RelationshipType.KMS_KEY

    assert relationship.required is True
