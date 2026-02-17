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

from .type_utils import (
    evaluate_type,
    is_list,
    get_primitive_type,
    value_iterator, 
    get_item,
    parse_literal
)