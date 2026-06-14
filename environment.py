from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


class EnvironmentError(RuntimeError):
    pass


@dataclass
class Binding:
    value: Any
    mutable: bool
    kind: str


class Environment:
    def __init__(self, parent: Optional["Environment"] = None, is_function_scope: bool = False):
        self.parent = parent
        self.is_function_scope = is_function_scope
        self.bindings: dict[str, Binding] = {}

    def declare(self, name: str, value: Any, kind: str = "let") -> Any:
        target = self._var_target() if kind == "var" else self
        if name in target.bindings:
            raise EnvironmentError(f"Identifier '{name}' has already been declared")
        target.bindings[name] = Binding(value=value, mutable=(kind != "const"), kind=kind)
        return value

    def get(self, name: str) -> Any:
        env = self._resolve(name)
        if env is None:
            raise EnvironmentError(f"{name} is not defined")
        return env.bindings[name].value

    def assign(self, name: str, value: Any) -> Any:
        env = self._resolve(name)
        if env is None:
            raise EnvironmentError(f"{name} is not defined")
        binding = env.bindings[name]
        if not binding.mutable:
            raise EnvironmentError(f"Assignment to constant variable '{name}'")
        binding.value = value
        return value

    def _resolve(self, name: str) -> Optional["Environment"]:
        if name in self.bindings:
            return self
        return self.parent._resolve(name) if self.parent else None

    def _var_target(self) -> "Environment":
        env: Environment = self
        while env.parent is not None and not env.is_function_scope:
            env = env.parent
        return env
