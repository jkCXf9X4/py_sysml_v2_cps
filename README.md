# py-sysml-v2-cps

Standalone Python SysML v2 parsing and helper utilities for CPS development.

## Requirements

- Python 3.10 or newer

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

## Quickstart

```python
from sysml import parse_literal, parse_sysml_folder

architecture = parse_sysml_folder("path/to/sysml_folder")
print(architecture.package)
print(sorted(architecture.parts))

```

## Development

Run package-local tests:

```bash
python -m pytest -q
```

Build distributable artifacts:

```bash
python -m build
```

## Package layout

- `src/sysml/` - package implementation
- `tests/` - package-local tests
- `examples/` - small usage scripts
- `docs/` - package-specific notes

Package tests use `tests/fixtures/aircraft_subset/`, a compact subset extracted
from the original project architecture so validation is self-contained.
