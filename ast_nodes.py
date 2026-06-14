from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Program:
    body: list[Any]


@dataclass
class BlockStatement:
    body: list[Any]


@dataclass
class ExpressionStatement:
    expression: Any


@dataclass
class VariableDeclarator:
    identifier: "Identifier"
    initializer: Optional[Any]


@dataclass
class VariableDeclaration:
    kind: str
    declarations: list[VariableDeclarator]


@dataclass
class FunctionDeclaration:
    name: "Identifier"
    params: list["Identifier"]
    body: BlockStatement


@dataclass
class ReturnStatement:
    argument: Optional[Any]


@dataclass
class IfStatement:
    test: Any
    consequent: Any
    alternate: Optional[Any]


@dataclass
class WhileStatement:
    test: Any
    body: Any


@dataclass
class ForStatement:
    init: Optional[Any]
    test: Optional[Any]
    update: Optional[Any]
    body: Any


@dataclass
class BreakStatement:
    pass


@dataclass
class ContinueStatement:
    pass


@dataclass
class Identifier:
    name: str


@dataclass
class Literal:
    value: Any


@dataclass
class ArrayExpression:
    elements: list[Any]


@dataclass
class SpreadElement:
    argument: Any


@dataclass
class ObjectProperty:
    key: Any
    value: Any


@dataclass
class ObjectExpression:
    properties: list[ObjectProperty | SpreadElement]


@dataclass
class UnaryExpression:
    operator: str
    argument: Any


@dataclass
class UpdateExpression:
    operator: str
    argument: Any
    prefix: bool


@dataclass
class BinaryExpression:
    left: Any
    operator: str
    right: Any


@dataclass
class LogicalExpression:
    left: Any
    operator: str
    right: Any


@dataclass
class ConditionalExpression:
    test: Any
    consequent: Any
    alternate: Any


@dataclass
class AssignmentExpression:
    left: Any
    operator: str
    right: Any


@dataclass
class MemberExpression:
    object: Any
    property: Any
    computed: bool = False


@dataclass
class CallExpression:
    callee: Any
    arguments: list[Any]


@dataclass
class NewExpression:
    callee: Any
    arguments: list[Any]


@dataclass
class FunctionExpression:
    params: list[Identifier]
    body: BlockStatement
    name: Optional[Identifier] = None


@dataclass
class ArrowFunctionExpression:
    params: list[Identifier]
    body: Any
