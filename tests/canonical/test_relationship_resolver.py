from compliance_scanner.canonical.relationship_resolver import RelationshipResolver


def test_parse_reference_without_attribute():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_subnet.private",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_name_attribute():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_iam_role.lambda.name",
    ) == [
        (
            "aws_iam_role",
            "lambda",
        )
    ]


def test_parse_reference_with_arn_attribute():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_lb.main.arn",
    ) == [
        (
            "aws_lb",
            "main",
        )
    ]


def test_parse_reference_with_index():
    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_subnet.private[0].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_splat():
    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_subnet.private[*].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_count_index():
    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_subnet.private[count.index].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_each_key():
    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        "aws_subnet.private[each.key].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_nested_lists():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        [
            [
                "aws_subnet.private.id",
            ],
            [
                "aws_subnet.public.id",
            ],
        ]
    ) == [
        (
            "aws_subnet",
            "private",
        ),
        (
            "aws_subnet",
            "public",
        ),
    ]


def test_parse_mixed_nested_collection():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        [
            "aws_subnet.private.id",
            (
                "aws_security_group.web.id",
                [
                    "aws_security_group.db.id",
                ],
            ),
        ]
    ) == [
        (
            "aws_subnet",
            "private",
        ),
        (
            "aws_security_group",
            "web",
        ),
        (
            "aws_security_group",
            "db",
        ),
    ]


def test_parse_tuple():

    resolver = RelationshipResolver(None)

    assert resolver._parse_references(
        (
            "aws_subnet.private.id",
            "aws_subnet.public.id",
        )
    ) == [
        (
            "aws_subnet",
            "private",
        ),
        (
            "aws_subnet",
            "public",
        ),
    ]
