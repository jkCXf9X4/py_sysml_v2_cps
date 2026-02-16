# pycps_sysmlv2

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

[Example](examples/parse_architecture.py)

```python
from pycps_sysmlv2 import load_architecture

architecture = load_architecture("tests/fixtures/aircraft_subset")
aircraft = architecture.part_definitions["AircraftComposition"]

# Connections belong to the part definition, not SysMLArchitecture.
for connection in aircraft.connections:
    print(
        connection.src_part_def.name,
        connection.src_port_def.name,
        "->",
        connection.dst_part_def.name,
        connection.dst_port_def.name,
    )
```

Run the bundled example from this repository root:

```bash
PYTHONPATH=src python3 examples/parse_architecture.py
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

- `src/pycps_sysmlv2/` - package implementation
- `tests/` - package-local tests
- `examples/` - small usage scripts
- `docs/` - package-specific notes

Package tests use `tests/fixtures/aircraft_subset/`, a compact subset extracted
from the original project architecture so validation is self-contained.
