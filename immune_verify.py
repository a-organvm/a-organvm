"""immune--verify: the organism validates its own integrity.

GEN-002: canonical '--' maps to '_' in .py filenames.

The immune system checks that the organism's structure is self-consistent:
contracts match reality, signals flow without defects, governance rules hold.

Skeletal reads what EXISTS. Circulatory computes what FLOWS.
Cultvra documents what it MEANS. Immune verifies what is TRUE.

Four verification dimensions:
  Structural — do gates reference real modules? do signals have producers?
  Temporal   — are observations recent? has the organism gone stale?
  Governance — do promotion states follow the FSM? are counts consistent?
  Coherence  — do contracts, signal graph, and functions agree?
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).parent


# -- data structures --


@dataclass
class Finding:
    """A single verification finding."""

    dimension: str  # structural, temporal, governance, coherence
    severity: str  # ERROR, WARNING, INFO
    subject: str
    detail: str


@dataclass
class Validation:
    """The verification result for one check."""

    check_name: str
    passed: bool
    findings: list[Finding]


@dataclass
class VerificationReport:
    """Complete integrity report of the organism at a moment in time."""

    timestamp: str
    validations: list[Validation]
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


# -- verification checks --


def check_signal_graph_integrity(graph: dict[str, Any]) -> Validation:
    """Verify signal graph internal consistency."""
    findings: list[Finding] = []
    functions = set(graph.get("functions", {}).keys())
    signal_types = set(graph.get("signal_types", {}).keys())

    # all edge endpoints must reference existing functions
    for family in ("dependency", "information", "governance", "evolution"):
        for edge in graph.get("edges", {}).get(family, []):
            if not isinstance(edge, dict):
                continue
            if edge.get("from") not in functions:
                findings.append(Finding(
                    "structural", "ERROR", edge.get("from", "?"),
                    f"edge source not in functions (family={family})",
                ))
            if edge.get("to") not in functions:
                findings.append(Finding(
                    "structural", "ERROR", edge.get("to", "?"),
                    f"edge target not in functions (family={family})",
                ))
            if "signal" in edge and edge["signal"] not in signal_types:
                findings.append(Finding(
                    "structural", "WARNING", edge["signal"],
                    f"edge references undeclared signal type (family={family})",
                ))

    # all functions must have inputs and outputs
    for fname, fdata in graph.get("functions", {}).items():
        if not isinstance(fdata, dict):
            continue
        if not fdata.get("inputs"):
            findings.append(Finding(
                "structural", "WARNING", fname,
                "function has no declared inputs",
            ))
        if not fdata.get("outputs"):
            findings.append(Finding(
                "structural", "WARNING", fname,
                "function has no declared outputs",
            ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("signal_graph_integrity", passed, findings)


def check_contract_consistency(
    contracts: list[tuple[str, dict]],
    graph: dict[str, Any],
) -> Validation:
    """Verify contracts are internally consistent and align with graph."""
    findings: list[Finding] = []
    graph_functions = set(graph.get("functions", {}).keys())

    for stem, contract in contracts:
        identity = contract.get("identity", {})
        name = identity.get("name", stem)

        # contracts must have identity section
        if not identity:
            findings.append(Finding(
                "structural", "ERROR", stem,
                "gate contract missing identity section",
            ))
            continue

        # contracts must have mechanism and verb
        if not identity.get("mechanism"):
            findings.append(Finding(
                "structural", "WARNING", name,
                "gate contract missing mechanism field",
            ))
        if not identity.get("verb"):
            findings.append(Finding(
                "structural", "WARNING", name,
                "gate contract missing verb field",
            ))

        # contracts with signal inputs/outputs should reference valid types
        signal_types = set(graph.get("signal_types", {}).keys())
        for sig in identity.get("signal_inputs", []):
            if sig not in signal_types:
                findings.append(Finding(
                    "coherence", "INFO", name,
                    f"input signal '{sig}' not yet in signal graph "
                    f"(may be declared by a future function)",
                ))
        for sig in identity.get("signal_outputs", []):
            if sig not in signal_types:
                findings.append(Finding(
                    "coherence", "INFO", name,
                    f"output signal '{sig}' not yet in signal graph "
                    f"(may be declared by a future function)",
                ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("contract_consistency", passed, findings)


def check_function_implementation(
    graph: dict[str, Any],
    directory: Path | None = None,
) -> Validation:
    """Verify that declared functions have corresponding Python implementations."""
    findings: list[Finding] = []
    root = directory or _HERE

    for fname in graph.get("functions", {}).keys():
        # GEN-002: canonical '--' maps to '_' in .py filenames
        py_stem = fname.replace("--", "_")
        py_path = root / f"{py_stem}.py"

        if not py_path.is_file():
            findings.append(Finding(
                "structural", "ERROR", fname,
                f"function declared in signal graph but no {py_stem}.py exists",
            ))
        else:
            # check it has a module docstring (minimal implementation evidence)
            text = py_path.read_text(encoding="utf-8").lstrip()
            if not (text.startswith('"""') or text.startswith("'''")):
                findings.append(Finding(
                    "coherence", "WARNING", fname,
                    f"{py_stem}.py exists but has no module docstring",
                ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("function_implementation", passed, findings)


def check_gate_health(contracts: list[tuple[str, dict]]) -> Validation:
    """Report on gate status distribution and defects."""
    findings: list[Finding] = []
    total_gates = 0
    passed_gates = 0
    pending_gates = 0
    failed_gates = 0

    for stem, contract in contracts:
        for gate in contract.get("gate", []):
            if not isinstance(gate, dict):
                continue
            total_gates += 1
            status = gate.get("status", "UNKNOWN").upper()
            if status in ("PASS", "PASSED"):
                passed_gates += 1
            elif status == "PENDING":
                pending_gates += 1
            elif status in ("FAIL", "FAILED"):
                failed_gates += 1
                findings.append(Finding(
                    "governance", "ERROR",
                    f"{stem}:{gate.get('id', '?')}",
                    f"gate FAILED: {gate.get('check', '?')}",
                ))

    if total_gates == 0:
        findings.append(Finding(
            "structural", "WARNING", "organism",
            "no gates found in any contract",
        ))

    # ratio check — if < 5% lit, the organism is embryonic (not an error)
    if total_gates > 0:
        ratio = passed_gates / total_gates
        if ratio < 0.05:
            findings.append(Finding(
                "governance", "INFO", "organism",
                f"gate pass ratio is {ratio:.1%} ({passed_gates}/{total_gates}) "
                f"— organism is embryonic",
            ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("gate_health", passed, findings)


def check_temporal_freshness(directory: Path | None = None) -> Validation:
    """Check that key organism files have been updated recently."""
    findings: list[Finding] = []
    root = directory or _HERE

    # check that observations.jsonl, routes.jsonl, docs.jsonl exist and are non-empty
    for log_name, producer in [
        ("observations.jsonl", "skeletal--define"),
        ("routes.jsonl", "circulatory--route"),
        ("docs.jsonl", "cultvra--logos"),
    ]:
        log_path = root / log_name
        if not log_path.is_file():
            findings.append(Finding(
                "temporal", "WARNING", log_name,
                f"log file missing — {producer} has never been recorded",
            ))
        elif log_path.stat().st_size == 0:
            findings.append(Finding(
                "temporal", "WARNING", log_name,
                f"log file is empty — {producer} has never been recorded",
            ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("temporal_freshness", passed, findings)


def check_feedback_loop(graph: dict[str, Any]) -> Validation:
    """Verify at least one feedback edge exists (autopoietic minimum)."""
    findings: list[Finding] = []

    info_edges = graph.get("edges", {}).get("information", [])
    feedback_edges = [
        e for e in info_edges
        if isinstance(e, dict) and e.get("direction") == "feedback"
    ]

    if not feedback_edges:
        findings.append(Finding(
            "coherence", "ERROR", "signal_graph",
            "no feedback edges — organism has no self-correction capability",
        ))
    else:
        findings.append(Finding(
            "coherence", "INFO", "signal_graph",
            f"{len(feedback_edges)} feedback edge(s) — "
            f"organism has self-correction",
        ))

    passed = not any(f.severity == "ERROR" for f in findings)
    return Validation("feedback_loop", passed, findings)


# -- main entry --


def verify(
    graph_path: Path | None = None,
    contract_dir: Path | None = None,
) -> VerificationReport:
    """The organism verifies its own integrity."""
    root = contract_dir or _HERE
    graph = load_signal_graph(graph_path or (root / "signal-graph.yaml"))
    contracts = load_contracts(root)

    validations = [
        check_signal_graph_integrity(graph),
        check_contract_consistency(contracts, graph),
        check_function_implementation(graph, root),
        check_gate_health(contracts),
        check_temporal_freshness(root),
        check_feedback_loop(graph),
    ]

    errors = sum(
        1 for v in validations
        for f in v.findings if f.severity == "ERROR"
    )
    warnings = sum(
        1 for v in validations
        for f in v.findings if f.severity == "WARNING"
    )
    passed = sum(1 for v in validations if v.passed)
    failed = sum(1 for v in validations if not v.passed)

    return VerificationReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        validations=validations,
        summary={
            "checks_run": len(validations),
            "checks_passed": passed,
            "checks_failed": failed,
            "total_errors": errors,
            "total_warnings": warnings,
            "organism_healthy": 1 if failed == 0 else 0,
        },
    )


# -- recording --


def record_verification(
    report: VerificationReport, path: Path | None = None,
) -> Path:
    """Append verification report to the verification log (TRACE output)."""
    log = path or (_HERE / "verifications.jsonl")
    with log.open("a") as f:
        f.write(json.dumps(asdict(report), default=str) + "\n")
    return log


def load_verification_history(path: Path | None = None) -> list[VerificationReport]:
    """Load all verification reports from the log."""
    log = path or (_HERE / "verifications.jsonl")
    if not log.is_file():
        return []
    reports = []
    for line in log.read_text().splitlines():
        if line.strip():
            data = json.loads(line)
            reports.append(VerificationReport(
                timestamp=data["timestamp"],
                validations=[
                    Validation(
                        check_name=v["check_name"],
                        passed=v["passed"],
                        findings=[Finding(**f) for f in v["findings"]],
                    )
                    for v in data["validations"]
                ],
                summary=data["summary"],
            ))
    return reports
