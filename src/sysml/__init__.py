"""Standalone SysML utilities package for architecture parsing and generation tooling."""

__version__ = "0.1.0"

from .helpers import component_modelica_map, load_architecture
from .parser import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLConnection,
    SysMLFolderParser,
    SysMLPartDefinition,
    SysMLPartReference,
    SysMLPortDefinition,
    SysMLPortEndpoint,
    SysMLRequirement,
    parse_sysml_folder,
)
from .type_utils import (
    infer_primitive,
    modelica_connector_type,
    normalize_primitive,
    optional_primitive,
    primitive_from_value,
)
from .values import parse_literal

__all__ = [
    "SysMLArchitecture",
    "SysMLAttribute",
    "SysMLConnection",
    "SysMLFolderParser",
    "SysMLPartDefinition",
    "SysMLPartReference",
    "SysMLPortDefinition",
    "SysMLPortEndpoint",
    "SysMLRequirement",
    "component_modelica_map",
    "infer_primitive",
    "load_architecture",
    "modelica_connector_type",
    "normalize_primitive",
    "optional_primitive",
    "parse_literal",
    "parse_sysml_folder",
    "primitive_from_value",
]
