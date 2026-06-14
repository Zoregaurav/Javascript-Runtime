from __future__ import annotations

import math
import importlib.util
from pathlib import Path
from typing import Any

from ast_nodes import (
    ArrayExpression,
    ArrowFunctionExpression,
    AssignmentExpression,
    BinaryExpression,
    BlockStatement,
    BreakStatement,
    CallExpression,
    ConditionalExpression,
    ContinueStatement,
    ExpressionStatement,
    ForStatement,
    FunctionDeclaration,
    FunctionExpression,
    Identifier,
    IfStatement,
    Literal,
    LogicalExpression,
    MemberExpression,
    NewExpression,
    ObjectExpression,
    Program,
    ReturnStatement,
    SpreadElement,
    UnaryExpression,
    UpdateExpression,
    VariableDeclaration,
    WhileStatement,
)
from environment import Environment
from runtime import (
    BoundMethod,
    BreakSignal,
    ContinueSignal,
    JSDate,
    JSFunction,
    JSRuntimeError,
    NativeFunction,
    ReturnSignal,
    is_truthy,
    js_equal,
    js_to_string,
    js_type_number,
)

_BUILTINS_SPEC = importlib.util.spec_from_file_location("_thunder_js_builtins", Path(__file__).with_name("builtins.py"))
if _BUILTINS_SPEC is None or _BUILTINS_SPEC.loader is None:
    raise ImportError("Unable to load local builtins.py")
_BUILTINS_MODULE = importlib.util.module_from_spec(_BUILTINS_SPEC)
_BUILTINS_SPEC.loader.exec_module(_BUILTINS_MODULE)
create_global_builtins = _BUILTINS_MODULE.create_global_builtins


class Interpreter:
    def create_global_environment(self) -> Environment:
        env = Environment(is_function_scope=True)
        for name, value in create_global_builtins().items():
            env.declare(name, value, "const")
        return env

    def run(self, program: Program) -> Any:
        return self.evaluate(program, self.create_global_environment())

    def evaluate(self, node: Any, env: Environment) -> Any:
        method = getattr(self, f"eval_{type(node).__name__}", None)
        if method is None:
            raise JSRuntimeError(f"No evaluator for {type(node).__name__}")
        return method(node, env)

    def eval_Program(self, node: Program, env: Environment) -> Any:
        result = None
        for statement in node.body:
            result = self.evaluate(statement, env)
        return result

    def eval_BlockStatement(self, node: BlockStatement, env: Environment) -> Any:
        return self.evaluate_block(node, env)

    def evaluate_block(self, node: BlockStatement, env: Environment, create_scope: bool = True) -> Any:
        scope = Environment(parent=env) if create_scope else env
        result = None
        for statement in node.body:
            result = self.evaluate(statement, scope)
        return result

    def eval_ExpressionStatement(self, node: ExpressionStatement, env: Environment) -> Any:
        return self.evaluate(node.expression, env)

    def eval_VariableDeclaration(self, node: VariableDeclaration, env: Environment) -> Any:
        value = None
        for declaration in node.declarations:
            value = self.evaluate(declaration.initializer, env) if declaration.initializer is not None else None
            env.declare(declaration.identifier.name, value, node.kind)
        return value

    def eval_FunctionDeclaration(self, node: FunctionDeclaration, env: Environment) -> Any:
        function = JSFunction(node.params, node.body, env, self, node.name.name)
        env.declare(node.name.name, function, "var")
        return function

    def eval_ReturnStatement(self, node: ReturnStatement, env: Environment) -> Any:
        raise ReturnSignal(self.evaluate(node.argument, env) if node.argument is not None else None)

    def eval_IfStatement(self, node: IfStatement, env: Environment) -> Any:
        if is_truthy(self.evaluate(node.test, env)):
            return self.evaluate(node.consequent, env)
        if node.alternate is not None:
            return self.evaluate(node.alternate, env)
        return None

    def eval_WhileStatement(self, node: WhileStatement, env: Environment) -> Any:
        result = None
        while is_truthy(self.evaluate(node.test, env)):
            try:
                result = self.evaluate(node.body, env)
            except ContinueSignal:
                continue
            except BreakSignal:
                break
        return result

    def eval_ForStatement(self, node: ForStatement, env: Environment) -> Any:
        loop_env = Environment(parent=env)
        if node.init is not None:
            self.evaluate(node.init, loop_env)
        result = None
        while node.test is None or is_truthy(self.evaluate(node.test, loop_env)):
            try:
                result = self.evaluate(node.body, loop_env)
            except ContinueSignal:
                pass
            except BreakSignal:
                break
            if node.update is not None:
                self.evaluate(node.update, loop_env)
        return result

    def eval_BreakStatement(self, node: BreakStatement, env: Environment) -> Any:
        raise BreakSignal()

    def eval_ContinueStatement(self, node: ContinueStatement, env: Environment) -> Any:
        raise ContinueSignal()

    def eval_Identifier(self, node: Identifier, env: Environment) -> Any:
        return env.get(node.name)

    def eval_Literal(self, node: Literal, env: Environment) -> Any:
        return node.value

    def eval_ArrayExpression(self, node: ArrayExpression, env: Environment) -> Any:
        values = []
        for element in node.elements:
            if isinstance(element, SpreadElement):
                spread = self.evaluate(element.argument, env)
                if not isinstance(spread, list):
                    raise JSRuntimeError("Array spread value is not iterable")
                values.extend(spread)
            else:
                values.append(self.evaluate(element, env))
        return values

    def eval_ObjectExpression(self, node: ObjectExpression, env: Environment) -> Any:
        obj: dict[str, Any] = {}
        for prop in node.properties:
            if isinstance(prop, SpreadElement):
                value = self.evaluate(prop.argument, env)
                if not isinstance(value, dict):
                    raise JSRuntimeError("Object spread value must be an object")
                obj.update(value)
            else:
                obj[str(prop.key)] = self.evaluate(prop.value, env)
        return obj

    def eval_SpreadElement(self, node: SpreadElement, env: Environment) -> Any:
        return self.evaluate(node.argument, env)

    def eval_UnaryExpression(self, node: UnaryExpression, env: Environment) -> Any:
        value = self.evaluate(node.argument, env)
        if node.operator == "!":
            return not is_truthy(value)
        if node.operator == "-":
            return -js_type_number(value)
        if node.operator == "+":
            return js_type_number(value)
        raise JSRuntimeError(f"Unsupported unary operator {node.operator}")

    def eval_UpdateExpression(self, node: UpdateExpression, env: Environment) -> Any:
        old_value = self._read_reference(node.argument, env)
        new_value = js_type_number(old_value) + (1 if node.operator == "++" else -1)
        if isinstance(new_value, float) and new_value.is_integer():
            new_value = int(new_value)
        self._write_reference(node.argument, env, new_value)
        return new_value if node.prefix else old_value

    def eval_BinaryExpression(self, node: BinaryExpression, env: Environment) -> Any:
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)
        op = node.operator
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return js_to_string(left) + js_to_string(right)
            return self._normalize_number(js_type_number(left) + js_type_number(right))
        if op == "-":
            return self._normalize_number(js_type_number(left) - js_type_number(right))
        if op == "*":
            return self._normalize_number(js_type_number(left) * js_type_number(right))
        if op == "/":
            return js_type_number(left) / js_type_number(right)
        if op == "%":
            return self._normalize_number(js_type_number(left) % js_type_number(right))
        if op == "**":
            return self._normalize_number(js_type_number(left) ** js_type_number(right))
        if op == "==":
            return js_equal(left, right)
        if op == "===":
            return js_equal(left, right, strict=True)
        if op == "!=":
            return not js_equal(left, right)
        if op == "!==":
            return not js_equal(left, right, strict=True)
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        raise JSRuntimeError(f"Unsupported binary operator {op}")

    def eval_LogicalExpression(self, node: LogicalExpression, env: Environment) -> Any:
        left = self.evaluate(node.left, env)
        if node.operator == "&&":
            return self.evaluate(node.right, env) if is_truthy(left) else left
        if node.operator == "||":
            return left if is_truthy(left) else self.evaluate(node.right, env)
        raise JSRuntimeError(f"Unsupported logical operator {node.operator}")

    def eval_ConditionalExpression(self, node: ConditionalExpression, env: Environment) -> Any:
        branch = node.consequent if is_truthy(self.evaluate(node.test, env)) else node.alternate
        return self.evaluate(branch, env)

    def eval_AssignmentExpression(self, node: AssignmentExpression, env: Environment) -> Any:
        if node.operator == "=":
            value = self.evaluate(node.right, env)
        else:
            current = self._read_reference(node.left, env)
            right = self.evaluate(node.right, env)
            value = self._compound_assign(current, node.operator, right)
        return self._write_reference(node.left, env, value)

    def eval_MemberExpression(self, node: MemberExpression, env: Environment) -> Any:
        obj = self.evaluate(node.object, env)
        prop = self.evaluate(node.property, env) if node.computed else node.property.name
        return self._get_member(obj, prop)

    def eval_CallExpression(self, node: CallExpression, env: Environment) -> Any:
        callee = self.evaluate(node.callee, env)
        args = self._evaluate_arguments(node.arguments, env)
        return self._call(callee, args)

    def eval_NewExpression(self, node: NewExpression, env: Environment) -> Any:
        callee = self.evaluate(node.callee, env)
        args = self._evaluate_arguments(node.arguments, env)
        if isinstance(callee, dict) and "__constructor__" in callee:
            return self._call(callee["__constructor__"], args)
        return self._call(callee, args)

    def eval_FunctionExpression(self, node: FunctionExpression, env: Environment) -> Any:
        return JSFunction(node.params, node.body, env, self, node.name.name if node.name else None)

    def eval_ArrowFunctionExpression(self, node: ArrowFunctionExpression, env: Environment) -> Any:
        expression_body = not isinstance(node.body, BlockStatement)
        return JSFunction(node.params, node.body, env, self, "<arrow>", expression_body)

    def _evaluate_arguments(self, arguments: list[Any], env: Environment) -> list[Any]:
        values = []
        for arg in arguments:
            if isinstance(arg, SpreadElement):
                value = self.evaluate(arg.argument, env)
                if not isinstance(value, list):
                    raise JSRuntimeError("Spread argument must be an array")
                values.extend(value)
            else:
                values.append(self.evaluate(arg, env))
        return values

    def _call(self, callee: Any, args: list[Any]) -> Any:
        if isinstance(callee, (JSFunction, NativeFunction, BoundMethod)):
            return callee.call(args)
        raise JSRuntimeError(f"{js_to_string(callee)} is not callable")

    def _read_reference(self, target: Any, env: Environment) -> Any:
        if isinstance(target, Identifier):
            return env.get(target.name)
        if isinstance(target, MemberExpression):
            obj = self.evaluate(target.object, env)
            prop = self.evaluate(target.property, env) if target.computed else target.property.name
            return self._get_member(obj, prop)
        raise JSRuntimeError("Invalid assignment target")

    def _write_reference(self, target: Any, env: Environment, value: Any) -> Any:
        if isinstance(target, Identifier):
            return env.assign(target.name, value)
        if isinstance(target, MemberExpression):
            obj = self.evaluate(target.object, env)
            prop = self.evaluate(target.property, env) if target.computed else target.property.name
            return self._set_member(obj, prop, value)
        raise JSRuntimeError("Invalid assignment target")

    def _get_member(self, obj: Any, prop: Any) -> Any:
        if isinstance(obj, dict):
            return obj.get(str(prop))
        if isinstance(obj, list):
            if prop == "length":
                return len(obj)
            if isinstance(prop, (int, float)) or str(prop).isdigit():
                index = int(prop)
                return obj[index] if 0 <= index < len(obj) else None
            if str(prop) in ARRAY_METHODS:
                return BoundMethod(obj, str(prop), ARRAY_METHODS[str(prop)])
        if isinstance(obj, str):
            if prop == "length":
                return len(obj)
            if isinstance(prop, (int, float)) or str(prop).isdigit():
                index = int(prop)
                return obj[index] if 0 <= index < len(obj) else None
            if str(prop) in STRING_METHODS:
                return BoundMethod(obj, str(prop), STRING_METHODS[str(prop)])
        if isinstance(obj, JSDate):
            if prop == "toString":
                return BoundMethod(obj, "toString", lambda receiver, args: js_to_string(receiver))
        return None

    def _set_member(self, obj: Any, prop: Any, value: Any) -> Any:
        if isinstance(obj, dict):
            obj[str(prop)] = value
            return value
        if isinstance(obj, list):
            index = int(prop)
            while index >= len(obj):
                obj.append(None)
            obj[index] = value
            return value
        raise JSRuntimeError("Cannot set property on this value")

    def _compound_assign(self, current: Any, operator: str, right: Any) -> Any:
        if operator == "+=":
            return js_to_string(current) + js_to_string(right) if isinstance(current, str) or isinstance(right, str) else self._normalize_number(js_type_number(current) + js_type_number(right))
        if operator == "-=":
            return self._normalize_number(js_type_number(current) - js_type_number(right))
        if operator == "*=":
            return self._normalize_number(js_type_number(current) * js_type_number(right))
        if operator == "/=":
            return js_type_number(current) / js_type_number(right)
        if operator == "%=":
            return self._normalize_number(js_type_number(current) % js_type_number(right))
        raise JSRuntimeError(f"Unsupported assignment operator {operator}")

    @staticmethod
    def _normalize_number(value: Any) -> Any:
        return int(value) if isinstance(value, float) and math.isfinite(value) and value.is_integer() else value


def _array_push(receiver: list[Any], args: list[Any]) -> Any:
    receiver.extend(args)
    return len(receiver)


def _array_pop(receiver: list[Any], args: list[Any]) -> Any:
    return receiver.pop() if receiver else None


def _array_shift(receiver: list[Any], args: list[Any]) -> Any:
    return receiver.pop(0) if receiver else None


def _array_unshift(receiver: list[Any], args: list[Any]) -> Any:
    receiver[0:0] = args
    return len(receiver)


def _array_reverse(receiver: list[Any], args: list[Any]) -> Any:
    receiver.reverse()
    return receiver


def _array_join(receiver: list[Any], args: list[Any]) -> Any:
    sep = js_to_string(args[0]) if args else ","
    return sep.join("" if item is None else js_to_string(item) for item in receiver)


def _array_slice(receiver: list[Any], args: list[Any]) -> Any:
    start = int(js_type_number(args[0])) if args else 0
    end = int(js_type_number(args[1])) if len(args) > 1 and args[1] is not None else len(receiver)
    return receiver[start:end]


def _array_map(receiver: list[Any], args: list[Any]) -> Any:
    callback = args[0]
    return [callback.call([value, index, receiver]) for index, value in enumerate(receiver)]


def _array_filter(receiver: list[Any], args: list[Any]) -> Any:
    callback = args[0]
    return [value for index, value in enumerate(receiver) if is_truthy(callback.call([value, index, receiver]))]


def _array_reduce(receiver: list[Any], args: list[Any]) -> Any:
    callback = args[0]
    if len(args) > 1:
        acc = args[1]
        iterable = receiver
    else:
        if not receiver:
            raise JSRuntimeError("Reduce of empty array with no initial value")
        acc = receiver[0]
        iterable = receiver[1:]
    for index, value in enumerate(iterable):
        acc = callback.call([acc, value, index, receiver])
    return acc


def _array_for_each(receiver: list[Any], args: list[Any]) -> Any:
    callback = args[0]
    for index, value in enumerate(receiver):
        callback.call([value, index, receiver])
    return None


def _string_split(receiver: str, args: list[Any]) -> Any:
    if not args:
        return [receiver]
    sep = js_to_string(args[0])
    return list(receiver) if sep == "" else receiver.split(sep)


def _string_substring(receiver: str, args: list[Any]) -> Any:
    start = max(0, int(js_type_number(args[0])) if args else 0)
    end = max(0, int(js_type_number(args[1])) if len(args) > 1 else len(receiver))
    if start > end:
        start, end = end, start
    return receiver[start:end]


def _string_slice(receiver: str, args: list[Any]) -> Any:
    start = int(js_type_number(args[0])) if args else 0
    end = int(js_type_number(args[1])) if len(args) > 1 else len(receiver)
    return receiver[start:end]


ARRAY_METHODS = {
    "push": _array_push,
    "pop": _array_pop,
    "shift": _array_shift,
    "unshift": _array_unshift,
    "reverse": _array_reverse,
    "join": _array_join,
    "slice": _array_slice,
    "map": _array_map,
    "filter": _array_filter,
    "reduce": _array_reduce,
    "forEach": _array_for_each,
}


STRING_METHODS = {
    "split": _string_split,
    "substring": _string_substring,
    "slice": _string_slice,
    "includes": lambda receiver, args: js_to_string(args[0]) in receiver,
    "startsWith": lambda receiver, args: receiver.startswith(js_to_string(args[0])),
    "endsWith": lambda receiver, args: receiver.endswith(js_to_string(args[0])),
    "toUpperCase": lambda receiver, args: receiver.upper(),
    "toLowerCase": lambda receiver, args: receiver.lower(),
    "trim": lambda receiver, args: receiver.strip(),
    "replace": lambda receiver, args: receiver.replace(js_to_string(args[0]), js_to_string(args[1]), 1),
}
