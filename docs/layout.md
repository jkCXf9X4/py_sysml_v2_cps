# Module Layout

This folder is structured as a standalone Python package project:

- `src/sysml/` - package source code
- `tests/` - package-local tests
- `examples/` - small runnable usage examples
- `pyproject.toml` - build/test metadata for packaging with pip

The repository-level `sysml/__init__.py` is a compatibility shim so existing
imports continue to work before this module is split into a separate repository.
