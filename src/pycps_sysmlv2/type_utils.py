"""Helpers for normalizing SysML primitive type names."""

from __future__ import annotations

import ast
from typing import Any, Optional, Tuple


def evaluate_type(value):
    if value is None:
        return None, None
    if isinstance(value, bool):
        return value, "Boolean"
    if isinstance(value, int):
        return value, "Integer"
    if isinstance(value, float):
        return value, "Real"
    if isinstance(value, (list, tuple)):
        l = list(value)
        item, type = evaluate_type(get_item(l))
        if item is None:
            return l, "List[]"
        else:
            return l, f"List[{type}]"
    if isinstance(value, str):
        return value, "String"

def is_list(type: str):
    return "List" in type

def get_primitive_type(type: str):
    if is_list(type):
        return type[5:-1]
    return type

def value_iterator(values):
    if isinstance(values, (list, tuple)):
        for i in values:
            yield i
    else:
        yield values

def get_item(item: Any):
    if isinstance(item, (list, tuple)):
        return next((i for i in item if i is not None), None)
    else:
        return item

def parse_literal(value: Optional[str]) -> Tuple[Optional[Any], Optional[str]]:
    if value is None:
        return None, None

    text = value.strip()
    if not text:
        return None, None

    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true", "Boolean"

    try:
        parsed = ast.literal_eval(text)
        return evaluate_type(parsed)
    except (ValueError, SyntaxError):
        pass

    return text, "String"
