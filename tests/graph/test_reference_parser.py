from compliance_scanner.graph.reference_parser import ReferenceParser


def make_parser() -> ReferenceParser:
    return ReferenceParser()


def test_parse_reference_without_attribute():

    parser = make_parser()

    assert parser.parse_references(
        "aws_subnet.private",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_name_attribute():

    parser = make_parser()

    assert parser.parse_references(
        "aws_iam_role.lambda.name",
    ) == [
        (
            "aws_iam_role",
            "lambda",
        )
    ]


def test_parse_reference_with_arn_attribute():

    parser = make_parser()

    assert parser.parse_references(
        "aws_lb.main.arn",
    ) == [
        (
            "aws_lb",
            "main",
        )
    ]


def test_parse_reference_with_index():

    parser = make_parser()

    assert parser.parse_references(
        "aws_subnet.private[0].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_splat():

    parser = make_parser()

    assert parser.parse_references(
        "aws_subnet.private[*].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_count_index():

    parser = make_parser()

    assert parser.parse_references(
        "aws_subnet.private[count.index].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_reference_with_each_key():

    parser = make_parser()

    assert parser.parse_references(
        "aws_subnet.private[each.key].id",
    ) == [
        (
            "aws_subnet",
            "private",
        )
    ]


def test_parse_nested_lists():

    parser = make_parser()

    assert parser.parse_references(
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

    parser = make_parser()

    assert parser.parse_references(
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

    parser = make_parser()

    assert parser.parse_references(
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
