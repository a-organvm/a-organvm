"""cultvra--logos: the organism documents itself.

GEN-002: canonical '--' maps to '_' in .py filenames.

The cultvra system records, critiques, and narrates the organism's state.
Skeletal reads what EXISTS. Circulatory computes what FLOWS. Cultvra
describes what it all MEANS — documentation as the fourth rendering language.

Three rendering languages already exist:
  Logic  (YAML / gate contracts)  — qualification proofs
  Math   (JSONL / measurements)   — numerical evidence
  Biology (Python / functions)    — algorithmic embodiment

Cultvra adds the fourth:
  Logos  (Markdown / documentation) — natural-language discourse
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).parent


# -- data structures --


@dataclass
class DocumentationEntry:
    """One element's documentation state."""

    element_name: str
    element_type: str  # function, signal_type, mechanism, gate_contract
    documented: bool
    documentation_source: str  # path or description if documented, empty if not
    staleness: str  # current, stale, missing


@dataclass
class Query:
    """A QUERY signal — a documentation gap that feeds back to skeletal."""

    gap_type: str  # undocumented, stale, structural
    element_name: str
    element_type: str
    detail: str


@dataclass
class DocumentationState:
    """Full documentation inventory of the organism at a moment in time."""

    timestamp: str
    entries: list[DocumentationEntry]
    queries: list[Query]
    summary: dict[str, int]


# -- reading --


def load_signal_graph(path: Path | None = None) -> dict[str, Any]:
    """Read the organism's wiring diagram."""
    sg = path or (_HERE / "signal-graph.yaml")
    if not sg.is_file():
        return {}
    with sg.open() as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_contracts(directory: Path | None = None) -> list[tuple[str, dict]]:
    """Read all gate contracts from the organism directory."""
    root = directory or _HERE
    results = []
    for p in sorted(root.glob("*--*.yaml")):
        if "--" not in p.stem:
            continue
        with p.open() as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            results.append((p.stem, data))
    return results


def _list_md_files(directory: Path | None = None) -> dict[str, Path]:
    """Map lowercased stem → path for all .md files in the directory."""
    root = directory or _HERE
    return {
        p.stem.lower(): p
        for p in sorted(root.glob("*.md"))
        if p.is_file()
    }


def _list_py_files(directory: Path | None = None) -> dict[str, Path]:
    """Map stem → path for all non-test .py files in the directory."""
    root = directory or _HERE
    return {
        p.stem: p
        for p in sorted(root.glob("*.py"))
        if p.is_file() and not p.stem.startswith("test_")
    }


def _has_docstring(py_path: Path) -> bool:
    """Check whether a Python file has a module-level docstring."""
    try:
        text = py_path.read_text(encoding="utf-8")
        stripped = text.lstrip()
        return stripped.startswith('"""') or stripped.startswith("'''")
    except (OSError, UnicodeDecodeError):
        return False


def _file_mtime_iso(path: Path) -> str:
    """ISO timestamp of a file's last modification."""
    try:
        return datetime.fromtimestamp(
            os.path.getmtime(path), tz=timezone.utc
        ).isoformat()
    except OSError:
        return ""


# -- documentation inventory --


def inventory(
    graph: dict[str, Any] | None = None,
    contracts: list[tuple[str, dict]] | None = None,
    directory: Path | None = None,
) -> list[DocumentationEntry]:
    """Build a documentation inventory for every organism element."""
    root = directory or _HERE
    if graph is None:
        graph = load_signal_graph(root / "signal-graph.yaml")
    if contracts is None:
        contracts = load_contracts(root)

    md_files = _list_md_files(root)
    py_files = _list_py_files(root)
    entries: list[DocumentationEntry] = []

    # -- functions (from signal graph) --
    for fname, fdata in graph.get("functions", {}).items():
        if not isinstance(fdata, dict):
            continue
        # a function is "documented" if its .py file has a module docstring
        py_stem = fname.replace("--", "_")
        py_path = py_files.get(py_stem)
        has_doc = py_path is not None and _has_docstring(py_path)
        entries.append(DocumentationEntry(
            element_name=fname,
            element_type="function",
            documented=has_doc,
            documentation_source=str(py_path) if has_doc else "",
            staleness="current" if has_doc else "missing",
        ))

    # -- signal types --
    for stype, sdata in graph.get("signal_types", {}).items():
        desc = sdata.get("description", "") if isinstance(sdata, dict) else ""
        has_desc = bool(desc.strip())
        entries.append(DocumentationEntry(
            element_name=stype,
            element_type="signal_type",
            documented=has_desc,
            documentation_source="signal-graph.yaml" if has_desc else "",
            staleness="current" if has_desc else "missing",
        ))

    # -- mechanisms (derived from contracts + signal graph) --
    mechanisms: set[str] = set()
    for stem, contract in contracts:
        identity = contract.get("identity", {})
        mech = identity.get("mechanism", stem.split("--")[0])
        mechanisms.add(mech)
    for fname, fdata in graph.get("functions", {}).items():
        if isinstance(fdata, dict) and "mechanism" in fdata:
            mechanisms.add(fdata["mechanism"])

    for mech in sorted(mechanisms):
        # a mechanism is "documented" if a matching .md file exists
        has_md = mech.lower() in md_files or f"cultvra--{mech}" in md_files
        md_path = md_files.get(mech.lower(), md_files.get(f"cultvra--{mech}"))
        entries.append(DocumentationEntry(
            element_name=mech,
            element_type="mechanism",
            documented=has_md,
            documentation_source=str(md_path) if has_md else "",
            staleness="current" if has_md else "missing",
        ))

    # -- gate contracts --
    for stem, contract in contracts:
        identity = contract.get("identity", {})
        has_dna = bool(contract.get("dna"))
        has_defect = "defect" in contract
        complete = has_dna and has_defect and "gate" in contract
        entries.append(DocumentationEntry(
            element_name=stem,
            element_type="gate_contract",
            documented=complete,
            documentation_source=f"{stem}.yaml" if complete else "",
            staleness="current" if complete else "stale",
        ))

    # -- organism-level documentation --
    readme_exists = "readme" in md_files
    entries.append(DocumentationEntry(
        element_name="organism",
        element_type="organism",
        documented=readme_exists,
        documentation_source=str(md_files["readme"]) if readme_exists else "",
        staleness="current" if readme_exists else "missing",
    ))

    return entries


# -- query emission --


def emit_queries(entries: list[DocumentationEntry]) -> list[Query]:
    """Produce QUERY signals from documentation gaps."""
    queries: list[Query] = []
    for entry in entries:
        if entry.staleness == "missing":
            queries.append(Query(
                gap_type="undocumented",
                element_name=entry.element_name,
                element_type=entry.element_type,
                detail=(
                    f"{entry.element_type} '{entry.element_name}'"
                    " has no documentation counterpart"
                ),
            ))
        elif entry.staleness == "stale":
            queries.append(Query(
                gap_type="stale",
                element_name=entry.element_name,
                element_type=entry.element_type,
                detail=f"{entry.element_type} '{entry.element_name}' has incomplete documentation",
            ))
    return queries


# -- main operation --


def document(
    graph_path: Path | None = None,
    contract_dir: Path | None = None,
) -> DocumentationState:
    """The organism documents itself."""
    root = contract_dir or _HERE
    graph = load_signal_graph(graph_path or (root / "signal-graph.yaml"))
    contracts = load_contracts(root)

    entries = inventory(graph=graph, contracts=contracts, directory=root)
    queries = emit_queries(entries)

    documented = sum(1 for e in entries if e.documented)
    missing = sum(1 for e in entries if e.staleness == "missing")
    stale = sum(1 for e in entries if e.staleness == "stale")

    return DocumentationState(
        timestamp=datetime.now(timezone.utc).isoformat(),
        entries=entries,
        queries=queries,
        summary={
            "total_elements": len(entries),
            "documented": documented,
            "missing": missing,
            "stale": stale,
            "queries_emitted": len(queries),
            "coverage_pct": round(documented / len(entries) * 100) if entries else 0,
        },
    )


# -- recording --


def record_documentation(state: DocumentationState, path: Path | None = None) -> Path:
    """Append documentation state to the documentation log (TRACE output)."""
    log = path or (_HERE / "docs.jsonl")
    with log.open("a") as f:
        f.write(json.dumps(asdict(state), default=str) + "\n")
    return log


def load_documentation_history(path: Path | None = None) -> list[DocumentationState]:
    """Read back the documentation log."""
    log = path or (_HERE / "docs.jsonl")
    if not log.is_file():
        return []
    states: list[DocumentationState] = []
    with log.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            states.append(DocumentationState(
                timestamp=raw["timestamp"],
                entries=[DocumentationEntry(**e) for e in raw.get("entries", [])],
                queries=[Query(**q) for q in raw.get("queries", [])],
                summary=raw.get("summary", {}),
            ))
    return states


# -- entry point --


if __name__ == "__main__":
    state = document()
    s = state.summary
    print(
        f"{s['total_elements']} elements · "
        f"{s['documented']} documented · "
        f"{s['missing']} missing · "
        f"{s['stale']} stale · "
        f"{s['coverage_pct']}% coverage"
    )

    log = record_documentation(state)
    print(f"recorded → {log.name}")

    if state.queries:
        print(f"\nQueries ({len(state.queries)}):")
        for q in state.queries:
            print(f"  [{q.gap_type.upper()}] {q.element_name}: {q.detail}")
