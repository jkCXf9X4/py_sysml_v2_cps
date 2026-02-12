# py-sysml-v2-cps

Standalone python SysML V" utilities for working with cps architecture

## Install

From the repository root:

```bash
pip install -e .
```

Or as a regular package install:

```bash
pip install .
```

Install directly from GitHub (no separate manual build step):

```bash
pip install "git+https://github.com/jkCXf9X4/py_sysml_v2_cps.git"
```

Pin to a branch or tag:

```bash
pip install "git+https://github.com/jkCXf9X4/py_sysml_v2_cps.git@main"
pip install "git+https://github.com/jkCXf9X4/py_sysml_v2_cps.git@v0.1.0"
```

## Development

Run package-local tests:

```bash
pytest -q
```

Build distributable artifacts:

```bash
python -m build
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
from the original project architecture so validation is self-contained.
