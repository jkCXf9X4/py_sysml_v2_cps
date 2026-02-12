from pathlib import Path

from sysml import (
    component_modelica_map,
    load_architecture,
    parse_literal,
    parse_sysml_folder,
)


FIXTURE_ARCH_DIR = Path(__file__).resolve().parent / "fixtures" / "aircraft_subset"


def test_literal_parser_handles_primitives():
    assert parse_literal("true") is True
    assert parse_literal("3.5") == 3.5
    assert parse_literal("\"abc\"") == "abc"
    assert parse_literal("[1.0, 2.0]") == [1.0, 2.0]


def test_architecture_loader_from_fixture_directory():
    architecture = parse_sysml_folder(FIXTURE_ARCH_DIR)
    assert architecture.package == "Aircraft"
    assert set(architecture.parts) == {"AutopilotModule", "MissionComputer", "Environment"}
    assert set(architecture.port_definitions) == {
        "PilotCommand",
        "OrientationEuler",
        "PositionXYZ",
        "FlightStatusPacket",
        "MissionStatus",
    }
    assert len(architecture.connections) == 5
    assert len(architecture.requirements) == 2


def test_architecture_loader_from_fixture_file():
    arch_file = FIXTURE_ARCH_DIR / "architecture.sysml"
    architecture = load_architecture(arch_file)
    assert architecture.package == "Aircraft"
    assert "AutopilotModule" in architecture.parts


def test_ports_are_linked_to_payload_definitions():
    architecture = parse_sysml_folder(FIXTURE_ARCH_DIR)
    autopilot = architecture.part("AutopilotModule")
    by_name = {port.name: port for port in autopilot.ports}
    assert by_name["autopilotCmd"].payload == "PilotCommand"
    assert by_name["autopilotCmd"].payload_def is not None
    assert by_name["autopilotCmd"].payload_def.name == "PilotCommand"
    assert by_name["feedbackBus"].payload_def is not None
    assert by_name["feedbackBus"].payload_def.name == "FlightStatusPacket"


def test_extracted_attribute_literals_are_parseable():
    architecture = parse_sysml_folder(FIXTURE_ARCH_DIR)
    waypoint_attr = architecture.part("AutopilotModule").attributes["waypointX_km"]
    assert parse_literal(waypoint_attr.value) == [0.0, 10.0, 20.0]
    assert parse_literal(architecture.part("AutopilotModule").attributes["waypointCount"].value) == 10


def test_component_modelica_map_uses_package_name():
    architecture = parse_sysml_folder(FIXTURE_ARCH_DIR)
    model_map = component_modelica_map(architecture)
    assert model_map["AutopilotModule"] == "Aircraft.AutopilotModule"
    assert model_map["MissionComputer"] == "Aircraft.MissionComputer"
