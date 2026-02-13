"""Compatibility facade for SysML parsing API.

Definitions are in `sysml.definitions`, parser helpers in `sysml.parser_utils`,
and parsing functions in `sysml.parsing`.
"""

from .definitions import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLConnection,
    SysMLPartDefinition,
    SysMLPartReference,
    SysMLPortDefinition,
    SysMLPortReference,
    SysMLRequirement,
)
from .parsing import SysMLFolderParser, load_architecture

__all__ = [
    "SysMLArchitecture",
    "SysMLAttribute",
    "SysMLConnection",
    "SysMLFolderParser",
    "SysMLPartDefinition",
    "SysMLPartReference",
    "SysMLPortDefinition",
    "SysMLPortReference",
    "SysMLRequirement",
    "load_architecture",
]
