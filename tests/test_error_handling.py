from pathlib import Path

import pytest

from pycps_sysmlv2 import load_architecture, load_system


def _write(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n")


def test_load_system_raises_key_error_for_missing_part(tmp_path: Path):
    _write(
        tmp_path / "model.sysml",
        """
        package Example {
          part def Present {}
        }
        """,
    )

    with pytest.raises(KeyError, match="Part not found: Missing"):
        load_system(tmp_path, "Missing")


def test_missing_port_definition_fails_with_context(tmp_path: Path):
    _write(
        tmp_path / "model.sysml",
        """
        package Example {
          part def A {
            out port x : MissingPortType;
          }
        }
        """,
    )

    with pytest.raises(ValueError, match="Port definition not found for A.x"):
        load_architecture(tmp_path)


def test_connection_to_unknown_part_definition_fails_with_context(tmp_path: Path):
    _write(
        tmp_path / "model.sysml",
        """
        package Example {
          port def Signal {}

          part def KnownPart {
            out port out_signal : Signal;
          }

          part def System {
            part known : KnownPart;
            part unknown : UnknownPart;
            connect known.out_signal to unknown.in_signal;
          }
        }
        """,
    )

    with pytest.raises(
        ValueError, match="Part definition not found for subpart System.unknown"
    ):
        load_architecture(tmp_path)
