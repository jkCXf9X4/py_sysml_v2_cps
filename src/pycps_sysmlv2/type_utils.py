"""Helpers for normalizing SysML primitive type names."""

from __future__ import annotations

import ast
from typing import Any, Optional, Tuple


def evaluate_type(value):
    if isinstance(value, bool):
        return value, "Boolean"
    if isinstance(value, int):
        return value, "Integer"
    if isinstance(value, float):
        return value, "Real"
    if isinstance(value, (list, tuple)):
        l = list(value)
        if len(value) == 0:
            return l, "List[]"
        else:
            return l, f"List[{evaluate_type(l[0])[-1]}]"
    if isinstance(value, str):
        return value, "String"


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
