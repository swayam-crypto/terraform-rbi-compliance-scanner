from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Expression:
    pass


@dataclass(frozen=True)
class VariableReference(Expression):
    name: str


@dataclass(frozen=True)
class LocalReference(Expression):
    name: str


@dataclass(frozen=True)
class ModuleReference(Expression):
    module: str
    output: str


@dataclass(frozen=True)
class LiteralExpression(Expression):
    value: Any
