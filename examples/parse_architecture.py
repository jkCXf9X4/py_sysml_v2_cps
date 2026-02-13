from pathlib import Path

from sysml import load_architecture


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    architecture = load_architecture(repo_root / "tests" / "fixtures" / "aircraft_subset")
    aircraft = architecture.parts["AircraftComposition"]
    print(f"package={architecture.package}")
    print(f"parts={len(architecture.parts)}")
    print(f"connections={len(aircraft.connections)}")
    print("subparts:")
    for subpart in aircraft.parts.values():
        target_name = subpart.target_def.name if subpart.target_def else "<unresolved>"
        print(f"  - {subpart.name}: {target_name}")

    print("connections:")
    for connection in aircraft.connections:
        src_part = connection.src_part_def.name if connection.src_part_def else "<unresolved>"
        dst_part = connection.dst_part_def.name if connection.dst_part_def else "<unresolved>"
        src_port = connection.src_port_def.name if connection.src_port_def else "<unresolved>"
        dst_port = connection.dst_port_def.name if connection.dst_port_def else "<unresolved>"
        print(f"  - {src_part}.{src_port} -> {dst_part}.{dst_port}")


if __name__ == "__main__":
    main()
