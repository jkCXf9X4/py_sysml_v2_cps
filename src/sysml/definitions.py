"""Data model definitions for lightweight SysML parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .parser_utils import json_dumps


@dataclass
class SysMLAttribute:
    name: str
    type: Optional[str] = None
    value: Optional[Any] = None
    doc: Optional[str] = None

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLPartReference:
    name: str
    target: str
    doc: Optional[str] = None
    target_def: Optional["SysMLPartDefinition"] = None

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
class SysMLPortReference:
    name: str
    direction: str  # "in" or "out"
    payload: str
    doc: Optional[str] = None
    payload_def: Optional[SysMLPortDefinition] = None

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
class SysMLPartDefinition:
    name: str
    doc: Optional[str] = None
    attributes: Dict[str, SysMLAttribute] = field(default_factory=dict)
    ports: Dict[str, SysMLPortReference] = field(default_factory=dict)
    parts: Dict[str, SysMLPartReference] = field(default_factory=dict)
    connections: List[SysMLConnection] = field(default_factory=list)

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLRequirement:
    identifier: str
    text: str

    def __str__(self) -> str:
        return json_dumps(self)


@dataclass
class SysMLArchitecture:
    package: str
    parts: Dict[str, SysMLPartDefinition]
    _port_definitions: Dict[str, SysMLPortDefinition]
    requirements: List[SysMLRequirement]

    def __str__(self) -> str:
        return json_dumps(self)
