from compliance_scanner.catalog.relationship_types import RelationshipType


def test_relationship_type_values():

    assert RelationshipType.VPC == "vpc"

    assert RelationshipType.SUBNET == "subnet"

    assert RelationshipType.SECURITY_GROUP == "security_group"


def test_relationship_type_lookup():

    assert RelationshipType("vpc") is RelationshipType.VPC

    assert RelationshipType("database") is RelationshipType.DATABASE
