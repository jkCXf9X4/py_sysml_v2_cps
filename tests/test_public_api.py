import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from sysml import (
    load_architecture,
)


FIXTURE_ARCH_DIR = Path(__file__).resolve().parent / "fixtures" / "aircraft_subset"
FIXTURE_REFERENCE_JSON = FIXTURE_ARCH_DIR / "architecture_reference.json"


def _to_jsonable(value):
    if is_dataclass(value):
        return {
            field.name: _to_jsonable(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, dict):
        return {str(key): _to_jsonable(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def test_architecture_loader_from_fixture_directory():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    composition = architecture.parts["AircraftComposition"]
    assert architecture.package == "Aircraft"
    assert set(architecture.parts) == {
        "AutopilotModule",
        "MissionComputer",
        "Environment",
        "AircraftComposition",
    }
    assert set(architecture._port_definitions) == {
        "PilotCommand",
        "OrientationEuler",
        "PositionXYZ",
        "FlightStatusPacket",
        "MissionStatus",
    }
    assert len(composition.connections) == 5
    assert len(architecture.requirements) == 2

    # Keep a checked-in JSON snapshot of the parsed fixture for easy diffing.
    snapshot = json.dumps(_to_jsonable(architecture), indent=2, sort_keys=True) + "\n"
    FIXTURE_REFERENCE_JSON.write_text(snapshot)


def test_architecture_loader_from_fixture_file():
    arch_file = FIXTURE_ARCH_DIR / "part_definitions.sysml"
    architecture = load_architecture(arch_file)
    assert architecture.package == "Aircraft"
    assert "AutopilotModule" in architecture.parts


def test_ports_are_linked_to_payload_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    autopilot = architecture.parts["AutopilotModule"]
    by_name = autopilot.ports
    assert by_name["autopilotCmd"].payload == "PilotCommand"
    assert by_name["autopilotCmd"].payload_def is not None
    assert by_name["autopilotCmd"].payload_def.name == "PilotCommand"
    assert by_name["feedbackBus"].payload_def is not None
    assert by_name["feedbackBus"].payload_def.name == "FlightStatusPacket"


def test_extracted_attribute_literals_are_parseable():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    waypoint_attr = architecture.parts["AutopilotModule"].attributes["waypointX_km"]
    assert waypoint_attr.value == [0.0, 10.0, 20.0]
    assert architecture.parts["AutopilotModule"].attributes["waypointCount"].value == 10


def test_subparts_are_linked_to_part_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    aircraft = architecture.parts["AircraftComposition"]
    by_name = aircraft.parts

    assert by_name["autopilot"].target == "AutopilotModule"
    assert by_name["autopilot"].target_def is not None
    assert by_name["autopilot"].target_def.name == "AutopilotModule"

    assert by_name["missionComputer"].target_def is not None
    assert by_name["missionComputer"].target_def.name == "MissionComputer"

    assert by_name["environment"].target_def is not None
    assert by_name["environment"].target_def.name == "Environment"


def test_connections_are_linked_to_part_and__port_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    composition = architecture.parts["AircraftComposition"]

    first = composition.connections[0]
    assert first.src_component == "autopilot"
    assert first.src_port == "autopilotCmd"
    assert first.dst_component == "missionComputer"
    assert first.dst_port == "autopilotInput"

    assert first.src_part_def is not None
    assert first.src_part_def.name == "AutopilotModule"
    assert first.dst_part_def is not None
    assert first.dst_part_def.name == "MissionComputer"

    assert first.src_port_def is not None
    assert first.src_port_def.name == "autopilotCmd"
    assert first.src_port_def.payload_def is not None
    assert first.src_port_def.payload_def.name == "PilotCommand"

    assert first.dst_port_def is not None
    assert first.dst_port_def.name == "autopilotInput"
    assert first.dst_port_def.payload_def is not None
    assert first.dst_port_def.payload_def.name == "PilotCommand"
