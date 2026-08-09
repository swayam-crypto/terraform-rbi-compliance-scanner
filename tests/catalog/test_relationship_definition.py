from compliance_scanner.catalog.relationships import RelationshipDefinition
from compliance_scanner.graph.relationship import RelationshipType


def test_relationship_definition():

    relationship = RelationshipDefinition(
        type=RelationshipType.SUBNET,
    )

    assert relationship.type is RelationshipType.SUBNET

    assert relationship.required is False


def test_required_relationship():

    relationship = RelationshipDefinition(
        type=RelationshipType.KMS_KEY,
        required=True,
    )

    assert relationship.required is True
