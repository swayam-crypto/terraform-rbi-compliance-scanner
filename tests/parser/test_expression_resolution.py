from compliance_scanner.parser.expression import (
    VariableReference,
    LocalReference,
    ModuleReference,
    LiteralExpression,
)
from compliance_scanner.parser.resolver import resolve_value


def test_literal_expression():

    expression = LiteralExpression("hello")

    assert expression.value == "hello"


def test_variable_reference():

    expression = VariableReference("vpc_id")

    assert expression.name == "vpc_id"


def test_local_reference():

    expression = LocalReference("subnet")

    assert expression.name == "subnet"


def test_module_reference():

    expression = ModuleReference(
        module="network",
        output="private_subnet",
    )

    assert expression.module == "network"

    assert expression.output == "private_subnet"
