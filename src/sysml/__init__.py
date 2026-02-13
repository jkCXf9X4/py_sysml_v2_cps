"""Standalone SysML utilities package for architecture parsing and generation tooling."""

__version__ = "0.1.0"

from .parsing import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLConnection,
    SysMLFolderParser,
    SysMLPartDefinition,
    SysMLPartReference,
    SysMLPortDefinition,
    SysMLPortReference,
    SysMLRequirement,
    load_architecture,
)

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
