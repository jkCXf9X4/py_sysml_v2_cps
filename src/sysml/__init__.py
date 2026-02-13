"""Standalone SysML utilities package for architecture parsing and generation tooling."""

__version__ = "0.1.0"

from .parser import (
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
from .type_utils import (
    infer_primitive,
    modelica_connector_type,
    normalize_primitive,
    optional_primitive,
    parse_literal,
    primitive_from_value,
)

# Backward-compatible name used in older examples/docs.
parse_sysml_folder = load_architecture

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
    "infer_primitive",
    "load_architecture",
    "modelica_connector_type",
    "normalize_primitive",
    "optional_primitive",
    "parse_literal",
    "parse_sysml_folder",
    "primitive_from_value",
]
