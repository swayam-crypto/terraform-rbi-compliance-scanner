from compliance_scanner.parser.relationship_extractor import RelationshipExtractor


def test_parse_reference():
    extractor = RelationshipExtractor()

    reference = extractor._parse_reference("aws_subnet.private.id")

    assert reference == (
        "aws_subnet",
        "private",
    )


def test_parse_reference_returns_none_for_non_reference():
    extractor = RelationshipExtractor()

    assert extractor._parse_reference("subnet-123456") is None


def test_parse_reference_returns_none_for_non_string():
    extractor = RelationshipExtractor()

    assert extractor._parse_reference(None) is None
