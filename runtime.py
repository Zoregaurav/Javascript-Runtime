from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Optional


JS_NULL = None


class JSRuntimeError(RuntimeError):
    pass


class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


@dataclass
class JSFunction:
    params: list[Any]
    body: Any
    closure: Any
    interpreter: Any
    name: Optional[str] = None
    expression_body: bool = False

    def call(self, args: list[Any]) -> Any:
        from environment import Environment

        local = Environment(parent=self.closure, is_function_scope=True)
        for index, param in enumerate(self.params):
            local.declare(param.name, args[index] if index < len(args) else JS_NULL, "let")
        try:
            if self.expression_body:
                return self.interpreter.evaluate(self.body, local)
            self.interpreter.evaluate_block(self.body, local, create_scope=False)
        except ReturnSignal as signal:
            return signal.value
        return JS_NULL


@dataclass
class NativeFunction:
    func: Callable[..., Any]
    name: str = "<native>"

    def call(self, args: list[Any]) -> Any:
        return self.func(*args)


@dataclass
class JSDate:
    value: datetime


@dataclass
class BoundMethod:
    receiver: Any
    name: str
    func: Callable[[Any, list[Any]], Any]

    def call(self, args: list[Any]) -> Any:
        return self.func(self.receiver, args)


def is_truthy(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, (int, float)) and value == 0:
        return False
    if isinstance(value, str) and value == "":
        return False
    return True


def js_type_number(value: Any) -> float:
    if value is None:
        return 0
    if value is True:
        return 1
    if value is False:
        return 0
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            return 0
        try:
            return float(stripped)
        except ValueError:
            return float("nan")
    return float("nan")


def js_to_string(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, list):
        return "[" + ", ".join(js_to_string(item) for item in value) + "]"
    if isinstance(value, dict):
        pairs = ", ".join(f"{key}: {js_to_string(val)}" for key, val in value.items())
        return "{" + pairs + "}"
    if isinstance(value, JSDate):
        return value.value.strftime("%a %b %d %Y %H:%M:%S")
    return str(value)


def js_equal(left: Any, right: Any, strict: bool = False) -> bool:
    if strict:
        return type(left) is type(right) and left == right
    if left is None and right is None:
        return True
    if isinstance(left, (int, float, bool)) or isinstance(right, (int, float, bool)):
        return js_type_number(left) == js_type_number(right)
    return left == right
