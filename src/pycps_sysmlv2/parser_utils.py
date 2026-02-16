"""Utility helpers shared across SysML parser modules."""

from __future__ import annotations

import json
import re
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Tuple


def to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {
            field_name: to_jsonable(getattr(value, field_name))
            for field_name in value.__dataclass_fields__
        }
    if isinstance(value, dict):
        return {str(key): to_jsonable(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def json_dumps(value: Any) -> str:
    return json.dumps(to_jsonable(value), indent=2, sort_keys=True)


def collect_block(text: str, brace_start: int) -> Tuple[str, int]:
    """Return the substring inside the curly braces starting at brace_start."""
    depth = 0
    body_start = brace_start + 1
    idx = brace_start
    while idx < len(text):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[body_start:idx], idx + 1
        idx += 1
    raise ValueError("Unterminated block while parsing SysML text")


def strip_inline_comment(line: str) -> str:
    result = line
    while "/*" in result and "*/" in result:
        start = result.find("/*")
        end = result.find("*/", start + 2)
        if end == -1:
            break
        result = (result[:start] + result[end + 2 :]).strip()
    return result.strip()


def normalize_doc(text: str) -> str:
    start = text.find("/*")
    end = text.rfind("*/")
    slice_ = text[start + 2 : end] if start != -1 and end != -1 else text
    return re.sub(r"\s+", " ", slice_.strip())
