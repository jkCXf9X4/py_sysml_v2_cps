import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from pycps_sysmlv2 import (
    load_architecture,
)
from pycps_sysmlv2.definitions import PrimitiveType, SysMLType


FIXTURE_ARCH_DIR = Path(__file__).resolve().parent / "fixtures" / "aircraft_subset"
FIXTURE_REFERENCE_JSON = FIXTURE_ARCH_DIR / "architecture_reference.json"


def test_architecture_loader_from_fixture_directory():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    composition = architecture.part_definitions["AircraftComposition"]
    assert architecture.package == "Aircraft"
    assert set(architecture.part_definitions) == {
        "AutopilotModule",
        "MissionComputer",
        "Environment",
        "AircraftComposition",
    }
    assert set(architecture.port_definitions) == {
        "PilotCommand",
        "OrientationEuler",
        "PositionXYZ",
        "FlightStatusPacket",
        "MissionStatus",
    }
    assert len(composition.connections) == 5
    assert len(architecture.requirements) == 2

    # Keep a checked-in JSON snapshot of the parsed fixture for easy diffing.
    FIXTURE_REFERENCE_JSON.write_text(str(architecture))


def test_architecture_loader_from_fixture_file():
    arch_file = FIXTURE_ARCH_DIR / "part_definitions.sysml"
    architecture = load_architecture(arch_file)
    assert architecture.package == "Aircraft"
    assert "AutopilotModule" in architecture.part_definitions


def test_ports_are_linked_to_payload_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    autopilot = architecture.part_definitions["AutopilotModule"]
    by_name = autopilot.ports
    assert by_name["autopilotCmd"].port_name == "PilotCommand"
    assert by_name["autopilotCmd"].port_def is not None
    assert by_name["autopilotCmd"].port_def.name == "PilotCommand"
    assert by_name["feedbackBus"].port_def is not None
    assert by_name["feedbackBus"].port_def.name == "FlightStatusPacket"


def test_extracted_attribute_literals_are_parseable():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    waypoint_attr = architecture.part_definitions["AutopilotModule"].attributes["waypointX_km"]
    assert waypoint_attr.value == [0.0, 10.0, 20.0]
    assert isinstance(waypoint_attr.type, SysMLType)
    assert waypoint_attr.type.primitive_type() == PrimitiveType.Real
    assert architecture.part_definitions["AutopilotModule"].attributes["waypointCount"].value == 10


def test_subparts_are_linked_to_part_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    aircraft = architecture.part_definitions["AircraftComposition"]
    by_name = aircraft.parts

    assert by_name["autopilot"].part_name == "AutopilotModule"
    assert by_name["autopilot"].part_def is not None
    assert by_name["autopilot"].part_def.name == "AutopilotModule"

    assert by_name["missionComputer"].part_def is not None
    assert by_name["missionComputer"].part_def.name == "MissionComputer"

    assert by_name["environment"].part_def is not None
    assert by_name["environment"].part_def.name == "Environment"


def test_connections_are_linked_to_part_and_port_definitions():
    architecture = load_architecture(FIXTURE_ARCH_DIR)
    composition = architecture.part_definitions["AircraftComposition"]

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
    assert first.src_port_def.port_def is not None
    assert first.src_port_def.port_def.name == "PilotCommand"

    assert first.dst_port_def is not None
    assert first.dst_port_def.name == "autopilotInput"
    assert first.dst_port_def.port_def is not None
    assert first.dst_port_def.port_def.name == "PilotCommand"
