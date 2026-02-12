from pathlib import Path

from sysml import parse_sysml_folder


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    architecture = parse_sysml_folder(repo_root / "architecture")
    print(f"package={architecture.package}")
    print(f"parts={len(architecture.parts)}")
    print(f"connections={len(architecture.connections)}")


if __name__ == "__main__":
    main()
