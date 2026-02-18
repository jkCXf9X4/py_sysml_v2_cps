"""Data model definitions for lightweight SysML parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .parser_utils import json_dumps
from .utils import obj_base

from enum import StrEnum, auto

import ast
#  Definitions


class PrimitiveType(StrEnum):
    Boolean = "Boolean"
    Integer = "Integer"
    Real = "Real"
    String = "String"
    Null = "Null"
    Unknown = auto()


SYSML_TYPE_MAP = {
    "real": PrimitiveType.Real,
    "float": PrimitiveType.Real,
    "float32": PrimitiveType.Real,
    "float64": PrimitiveType.Real,
    "double": PrimitiveType.Real,
    "integer": PrimitiveType.Integer,
    "int": PrimitiveType.Integer,
    "int8": PrimitiveType.Integer,
    "int32": PrimitiveType.Integer,
    "uint8": PrimitiveType.Integer,
    "uint32": PrimitiveType.Integer,
    "boolean": PrimitiveType.Boolean,
    "bool": PrimitiveType.Boolean,
    "string": PrimitiveType.String,
}


class SysMLType:
    def __init__(self, type: PrimitiveType, string_definition: Optional[str] = None):
        self.type = type
        self.string_definition = string_definition

    def is_unknown(self):
        return self.type == PrimitiveType.Unknown

    def primitive_type(self):
        return obj_base(self.type)
    
    def primitive_type_str(self):
        return self._as_string(obj_base(self.type))

    def as_string(self):
        return self._as_string(self.type)

    # Static methods

    @staticmethod
    def _as_string(type):
        if isinstance(type, (list, tuple)):
            if len(type) == 0:
                return "List[]"
            else:
                return f"List[{SysMLType._as_string(type[0])}]"
        return str(type)

    @staticmethod
    def from_value(value):
        return SysMLType(SysMLType._from_value(value))

    @staticmethod
    def _from_value(value):
        if value is None:
            return PrimitiveType.Null
        if isinstance(value, bool):
            return PrimitiveType.Boolean
        if isinstance(value, int):
            return PrimitiveType.Integer
        if isinstance(value, float):
            return PrimitiveType.Real
        if isinstance(value, str):
            return PrimitiveType.String
        if isinstance(value, (list, tuple)):
            if len(value) == 0:
                return list()
            else:
                return [SysMLType._from_value(value[0])]

    @staticmethod
    def from_string(string: str) -> "SysMLType":
        # List types are not supported
        striped = string.strip().lower()
        if striped in SYSML_TYPE_MAP:
            return SysMLType(SYSML_TYPE_MAP[striped])
        return SysMLType(PrimitiveType.Unknown, string)

    def __str__(self) -> str:
        return json_dumps(self)


class SysMLAttribute:
    def __init__(
        self,
        name: str,
        type: Optional[SysMLType],
        value: Optional[Any],
        doc: Optional[str],
    ):
        self.name = name
        self.type = type
        self.value = value
        self.doc = doc

    def is_list(self):
        return isinstance(self.value, (list, tuple))

    @staticmethod
    def from_literal(name, value: Optional[str], doc: Optional[str]):
        value = SysMLAttribute._parse_literal(value)
        type = SysMLType.from_value(value)
        return SysMLAttribute(name=name, type=type, value=value, doc=doc)

    @staticmethod
    def _parse_literal(value: Optional[str]) -> Any:
        if value is None:
            return None

        text = value.strip()
        if not text:
            return None

        lowered = text.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"

        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            pass

        return text

    def _get_item(item: Any):
        if isinstance(item, (list, tuple)):
            return next((i for i in item if i is not None), None)
        else:
            return item

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLRequirement:
    identifier: str
    text: str

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLConnection:
    src_component: str
    src_port: str
    dst_component: str
    dst_port: str
    src_part_def: Optional["SysMLPartDefinition"] = None
    dst_part_def: Optional["SysMLPartDefinition"] = None
    src_port_def: Optional["SysMLPortReference"] = None
    dst_port_def: Optional["SysMLPortReference"] = None

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLPortDefinition:
    name: str
    doc: Optional[str] = None
    attributes: Dict[str, SysMLAttribute] = field(default_factory=dict)

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLPartDefinition:
    name: str
    doc: Optional[str] = None
    attributes: Dict[str, SysMLAttribute] = field(default_factory=dict)
    ports: Dict[str, SysMLPortReference] = field(default_factory=dict)
    parts: Dict[str, SysMLPartReference] = field(default_factory=dict)
    connections: List[SysMLConnection] = field(default_factory=list)

    def get_all_port_attributes(
        self,
    ) -> List[Tuple[SysMLPortReference, SysMLPortDefinition, SysMLAttribute]]:
        attributes = []
        for port in self.ports.values():
            port_def = port.port_def
            for attr in port_def.attributes.values():
                s = (
                    port,
                    port_def,
                    attr,
                )
                attributes.append(s)
        return attributes

    def get_all_attributes(
        self,
    ) -> List[Tuple[str, str, SysMLAttribute]]:
        attributes = []

        for part_name, part in self.parts.items():
            for attr_name, attr in part.part_def.attributes.items():
                attributes.append((part_name, attr_name, attr))

        return attributes

    def __str__(self) -> str:
        return json_dumps(self)


#  References


@dataclass
class SysMLPartReference:
    name: str
    part_name: str
    doc: Optional[str] = None
    part_def: Optional["SysMLPartDefinition"] = None

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLPortReference:
    name: str
    direction: str  # "in" or "out"
    port_name: str
    doc: Optional[str] = None
    port_def: Optional[SysMLPortDefinition] = None

    def __str__(self) -> str:
        return json_dumps(self)


#  Architecture


@dataclass
class SysMLArchitecture:
    package: str
    part_definitions: Dict[str, SysMLPartDefinition]
    port_definitions: Dict[str, SysMLPortDefinition]
    requirements: List[SysMLRequirement]

    def __str__(self) -> str:
        return json_dumps(self)
