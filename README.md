# ssp-airplane-sysml

Standalone SysML utilities extracted from the `ssp_airplane` repository.

## Install

From the repository root:

```bash
pip install -e ./sysml
```

Or from a cloned standalone module repo later:

```bash
pip install .
```

## Development

Run package-local tests:

```bash
pytest -q sysml/tests
```

## Provided API

- `sysml.parse_sysml_folder`
- `sysml.SysMLFolderParser`
- `sysml.load_architecture`
- `sysml.component_modelica_map`
- `sysml.parse_literal`
- `sysml.normalize_primitive`
- `sysml.infer_primitive`

## Package layout

- `src/sysml/` - package implementation
- `tests/` - package-local tests
- `examples/` - small usage scripts
- `docs/` - package-specific notes

Package tests use `tests/fixtures/aircraft_subset/`, a compact subset extracted
from the main project architecture so validation is self-contained.
