"""Parsing logic for lightweight SysML v2 folder parsing."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, Iterator, List, Optional, Tuple

from .definitions import (
    SysMLArchitecture,
    SysMLType,
    SysMLAttribute,
    SysMLConnection,
    SysMLPartDefinition,
    SysMLPartReference,
    SysMLPortDefinition,
    SysMLPortReference,
    SysMLRequirement,
)
from .parser_utils import collect_block, normalize_doc, strip_inline_comment


class SysMLFolderParser:
    """Parse and merge all `.sysml` files within a directory."""

    def __init__(self, folder: Path | str):
        self.folder = Path(folder)
        if not self.folder.is_dir():
            raise FileNotFoundError(f"SysML folder not found: {self.folder}")

    def parse(self) -> SysMLArchitecture:
        files = sorted(self.folder.glob("*.sysml"))
        if not files:
            raise FileNotFoundError(f"No .sysml files found under {self.folder}")

        part_defs: Dict[str, SysMLPartDefinition] = {}
        port_defs: Dict[str, SysMLPortDefinition] = {}
        requirements: List[SysMLRequirement] = []
        package_name: Optional[str] = None

        for path in files:
            text = path.read_text()
            pkg, body = _extract_package_body(text, path)
            if package_name is None:
                package_name = pkg
            elif pkg != package_name:
                raise ValueError(
                    f"Mismatched package names: {package_name} vs {pkg} in {path}"
                )

            for name, block in _extract_named_blocks(body, "part def"):
                if name in part_defs:
                    raise ValueError(f"Duplicate part definition for {name} in {path}")
                part_defs[name] = _parse_part_block(name, block)

            for name, block in _extract_named_blocks(body, "port def"):
                if name in port_defs:
                    raise ValueError(f"Duplicate port definition for {name} in {path}")
                port_defs[name] = _parse_port_block(name, block)

            requirements.extend(_parse_requirements(body))

        _attach_port_definitions(part_defs, port_defs)
        _attach_part_definitions(part_defs)

        _attach_connection_definitions(part_defs, port_defs)
        return SysMLArchitecture(
            package=package_name or "Package",
            part_definitions=part_defs,
            port_definitions=port_defs,
            requirements=requirements,
        )


def load_architecture(folder: Path | str) -> SysMLArchitecture:
    path = Path(folder)
    if path.is_file():
        path = path.parent
    return SysMLFolderParser(path).parse()


def load_system(folder: Path | str, system_part: str):
    a = load_architecture(folder)
    if system_part not in a.part_definitions:
        raise Exception("Part not found")
    return a.part_definitions[system_part]


_PACKAGE_RE = re.compile(r"package\s+([A-Za-z0-9_]+)\s*\{", re.MULTILINE)
_CONNECTION_RE = re.compile(
    r"connect\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s+to\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s*;"
)


def _extract_package_body(text: str, path: Path) -> Tuple[str, str]:
    match = _PACKAGE_RE.search(text)
    if not match:
        raise ValueError(f"No package declaration found in {path}")
    pkg_name = match.group(1)
    brace_start = match.end() - 1
    body, _ = collect_block(text, brace_start)
    return pkg_name, body


def _extract_named_blocks(body: str, keyword: str) -> List[Tuple[str, str]]:
    pattern = re.compile(rf"{keyword}\s+([A-Za-z0-9_]+)\s*\{{", re.MULTILINE)
    blocks: List[Tuple[str, str]] = []
    idx = 0
    while True:
        match = pattern.search(body, idx)
        if not match:
            break
        name = match.group(1)
        brace_start = match.end() - 1
        block, new_idx = collect_block(body, brace_start)
        blocks.append((name, block))
        idx = new_idx
    return blocks


def _parse_part_block(name: str, block: str) -> SysMLPartDefinition:
    attributes: Dict[str, SysMLAttribute] = {}
    ports: Dict[str, SysMLPortReference] = {}
    parts: Dict[str, SysMLPartReference] = {}
    connections: List[SysMLConnection] = []
    pending_doc: Optional[str] = None
    part_doc: Optional[str] = None

    for kind, payload in _iter_block_items(block):
        if kind == "doc":
            if part_doc is None and not attributes and not ports and not parts:
                part_doc = payload
            else:
                pending_doc = payload
            continue

        line = strip_inline_comment(payload)
        if not line:
            continue

        if line.startswith("attribute "):
            attr = _parse_attribute(line, pending_doc)
            attributes[attr.name] = attr
        elif line.startswith("in port "):
            port = _parse_port_endpoint("in", line, pending_doc)
            ports[port.name] = port
        elif line.startswith("out port "):
            port = _parse_port_endpoint("out", line, pending_doc)
            ports[port.name] = port
        elif line.startswith("part "):
            part = _parse_part_reference(line, pending_doc)
            parts[part.name] = part
        elif line.startswith("connect "):
            connections.append(_parse_connection(line))

        pending_doc = None

    return SysMLPartDefinition(
        name=name,
        doc=part_doc,
        attributes=attributes,
        ports=ports,
        parts=parts,
        connections=connections,
    )


def _parse_port_block(name: str, block: str) -> SysMLPortDefinition:
    attributes: Dict[str, SysMLAttribute] = {}
    port_doc: Optional[str] = None
    pending_doc: Optional[str] = None

    for kind, payload in _iter_block_items(block):
        if kind == "doc":
            if port_doc is None and not attributes:
                port_doc = payload
            else:
                pending_doc = payload
            continue

        line = strip_inline_comment(payload)
        if not line:
            continue
        if line.startswith("attribute "):
            attr = _parse_attribute(line, pending_doc)
            attributes[attr.name] = attr
        pending_doc = None

    return SysMLPortDefinition(name=name, doc=port_doc, attributes=attributes)


def _parse_attribute(line: str, doc: Optional[str]) -> SysMLAttribute:
    content = line[len("attribute ") :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()

    attr_type: Optional[str] = None
    value: Optional[str] = None
    if "=" in content:
        name, value = content.split("=", 1)
        name = name.strip()
        value = SysMLAttribute._parse_literal(value)
        attr_type = SysMLType.from_value(value)
    elif ":" in content:
        name, attr_type = content.split(":", 1)
        name = name.strip()
        attr_type = SysMLType.from_string(attr_type.strip())
    else:
        name = content.strip()
    return SysMLAttribute(name=name, type=attr_type, value=value, doc=doc)


def _normalize_port_name(name: str) -> str:
    name = name.strip()
    if name.startswith("port "):
        return name[len("port ") :].strip()
    return name


def _parse_port_endpoint(
    direction: str, line: str, doc: Optional[str]
) -> SysMLPortReference:
    content = line[len(direction) :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()
    if ":" not in content:
        raise ValueError(f"Malformed port declaration: {line}")
    name, payload = content.split(":", 1)
    return SysMLPortReference(
        direction=direction,
        name=_normalize_port_name(name),
        port_name=payload.strip(),
        doc=doc,
    )


def _parse_part_reference(line: str, doc: Optional[str]) -> SysMLPartReference:
    content = line[len("part ") :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()
    if ":" not in content:
        raise ValueError(f"Malformed part reference: {line}")
    name, target = content.split(":", 1)
    return SysMLPartReference(name=name.strip(), part_name=target.strip(), doc=doc)


def _parse_connection(line: str) -> SysMLConnection:
    match = _CONNECTION_RE.fullmatch(line.strip())
    if match is None:
        raise ValueError(f"Malformed connection declaration: {line}")
    return SysMLConnection(
        src_component=match.group(1),
        src_port=match.group(2),
        dst_component=match.group(3),
        dst_port=match.group(4),
    )


def _attach_port_definitions(
    parts: Dict[str, SysMLPartDefinition], port_defs: Dict[str, SysMLPortDefinition]
) -> None:
    for part in parts.values():
        for port in part.ports.values():
            port.port_def = port_defs.get(port.port_name)


def _attach_part_definitions(parts: Dict[str, SysMLPartDefinition]) -> None:
    for part in parts.values():
        for subpart in part.parts.values():
            subpart.part_def = parts.get(subpart.part_name)


def _attach_connection_definitions(parts: Dict[str, SysMLPartDefinition], ports: Dict[str, SysMLPortDefinition]) -> None:

    for part in parts.values():
        for c in part.connections:
            if c.src_component not in part.parts:
                raise Exception(f"Subpart not found for connection, {part.name}:{c.src_component}")
            if c.dst_component not in part.parts:
                raise Exception(f"Subpart not found for connection, {part.name}:{c.dst_component}")

            c.src_part_def = part.parts[c.src_component].part_def
            c.dst_part_def = part.parts[c.dst_component].part_def

            if c.src_port not in c.src_part_def.ports:
                raise Exception(f"Port not found for connection, {c.src_part_def.name}:{c.src_port}")
            if c.dst_port not in c.dst_part_def.ports:
                raise Exception(f"Port not found for connection, {c.dst_part_def.name}:{c.dst_port}")

            c.src_port_def = c.src_part_def.ports[c.src_port].port_def
            c.dst_port_def = c.dst_part_def.ports[c.dst_port].port_def

def _iter_block_items(block: str) -> Iterator[Tuple[str, str]]:
    lines = block.splitlines()
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        idx += 1
        if not stripped:
            continue
        if stripped.startswith("doc"):
            doc_lines = [stripped]
            while "*/" not in stripped:
                if idx >= len(lines):
                    raise ValueError("Unterminated doc comment in SysML block")
                stripped = lines[idx].strip()
                doc_lines.append(stripped)
                idx += 1
            yield ("doc", normalize_doc(" ".join(doc_lines)))
        else:
            yield ("stmt", stripped)


def _parse_requirements(body: str) -> List[SysMLRequirement]:
    reqs: List[SysMLRequirement] = []
    pattern = re.compile(r"comment\s+([A-Za-z0-9_]+)\s*/\*\s*(.*?)\s*\*/", re.DOTALL)
    for match in pattern.finditer(body):
        identifier = match.group(1)
        text = re.sub(r"\s+", " ", match.group(2).strip())
        reqs.append(SysMLRequirement(identifier=identifier, text=text))
    return reqs
