from compliance_scanner.catalog.relationships import RelationshipDefinition
from compliance_scanner.graph.relationship import RelationshipType


def test_relationship_definition():

    relationship = RelationshipDefinition(
        relationship_type=RelationshipType.SUBNET,
    )

    assert relationship.relationship_type is RelationshipType.SUBNET

    assert relationship.required is False


def test_required_relationship():

    relationship = RelationshipDefinition(
        relationship_type=RelationshipType.KMS_KEY,
        required=True,
    )

    assert relationship.relationship_type is RelationshipType.KMS_KEY

    assert relationship.required is True
