from __future__ import annotations

import math
import random
from datetime import datetime
from typing import Any

from runtime import JSDate, NativeFunction, is_truthy, js_to_string, js_type_number


def create_global_builtins() -> dict[str, Any]:
    return {
        "console": {"log": NativeFunction(console_log, "console.log")},
        "Math": {
            "floor": NativeFunction(lambda x=0: math.floor(js_type_number(x)), "Math.floor"),
            "ceil": NativeFunction(lambda x=0: math.ceil(js_type_number(x)), "Math.ceil"),
            "round": NativeFunction(lambda x=0: math.floor(js_type_number(x) + 0.5), "Math.round"),
            "abs": NativeFunction(lambda x=0: abs(js_type_number(x)), "Math.abs"),
            "max": NativeFunction(lambda *xs: max(js_type_number(x) for x in xs), "Math.max"),
            "min": NativeFunction(lambda *xs: min(js_type_number(x) for x in xs), "Math.min"),
            "random": NativeFunction(lambda: random.random(), "Math.random"),
        },
        "Date": {
            "__constructor__": NativeFunction(lambda: JSDate(datetime.now()), "Date"),
            "now": NativeFunction(lambda: int(datetime.now().timestamp() * 1000), "Date.now"),
        },
        "Number": NativeFunction(lambda value=None: js_type_number(value), "Number"),
        "String": NativeFunction(lambda value=None: js_to_string(value), "String"),
        "Boolean": NativeFunction(lambda value=None: is_truthy(value), "Boolean"),
        "parseInt": NativeFunction(parse_int, "parseInt"),
        "parseFloat": NativeFunction(parse_float, "parseFloat"),
    }


def console_log(*values: Any) -> None:
    print(" ".join(js_to_string(value) for value in values))
    return None


def parse_int(value: Any = "", radix: Any = 10) -> Any:
    text = js_to_string(value).strip()
    sign = -1 if text.startswith("-") else 1
    if text.startswith(("+", "-")):
        text = text[1:]
    digits = []
    for char in text:
        if char.isdigit():
            digits.append(char)
        else:
            break
    return sign * int("".join(digits), int(radix or 10)) if digits else math.nan


def parse_float(value: Any = "") -> Any:
    text = js_to_string(value).strip()
    chars = []
    dot_seen = False
    for index, char in enumerate(text):
        if char in "+-" and index == 0:
            chars.append(char)
        elif char.isdigit():
            chars.append(char)
        elif char == "." and not dot_seen:
            dot_seen = True
            chars.append(char)
        else:
            break
    try:
        return float("".join(chars))
    except ValueError:
        return math.nan
