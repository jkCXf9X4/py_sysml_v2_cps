"""Helpers for normalizing SysML primitive type names."""
from __future__ import annotations

import ast
from typing import Any, Optional

PRIMITIVE_TYPE_MAP = {
    "real": "Real",
    "float": "Real",
    "float32": "Real",
    "float64": "Real",
    "double": "Real",
    "integer": "Integer",
    "int": "Integer",
    "int8": "Integer",
    "int32": "Integer",
    "uint8": "Integer",
    "uint32": "Integer",
    "boolean": "Boolean",
    "bool": "Boolean",
    "string": "String",
}


def normalize_primitive(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical primitive name (Real/Integer/Boolean/String) for SysML types."""
    if not type_name:
        return default
    key = type_name.strip().lower()
    return PRIMITIVE_TYPE_MAP.get(key, default)


def optional_primitive(type_name: Optional[str]) -> Optional[str]:
    """Return the canonical primitive name or None if the type is unset/unknown."""
    if not type_name:
        return None
    key = type_name.strip().lower()
    return PRIMITIVE_TYPE_MAP.get(key)


def modelica_connector_type(type_name: Optional[str]) -> str:
    """Map SysML types to Modelica connector primitives, preserving custom names."""
    if not type_name:
        return "Real"
    key = type_name.strip().lower()
    return PRIMITIVE_TYPE_MAP.get(key, type_name)


def primitive_from_value(value: Optional[object]) -> Optional[str]:
    """Infer a primitive type from a literal value."""
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, float):
        return "Real"
    if isinstance(value, str):
        return "String"
    return None


def infer_primitive(attr_type: Optional[str], sample: Optional[object], default: str = "Real") -> str:
    """Infer primitive from an explicit type hint or fallback sample value."""
    normalized = optional_primitive(attr_type)
    if normalized:
        return normalized
    inferred = primitive_from_value(sample)
    if inferred:
        return inferred
    return default



def parse_literal(value: Optional[str]) -> Optional[Any]:
    """Decode a SysML attribute string literal into a Python primitive/list."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if any(ch in text for ch in (".", "e", "E")):
            return float(text)
        return int(text)
    except ValueError:
        return text
