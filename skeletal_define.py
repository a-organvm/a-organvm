"""skeletal--define: the organism reads its own structure.

GEN-002: canonical '--' maps to '_' in .py filenames.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).parent


@dataclass
class Observation:
    timestamp: str
    mechanisms: dict[str, list[dict[str, Any]]]
    signal_types: dict[str, dict[str, list[str]]]
    gates: dict[str, list[dict[str, str]]]
    phases: dict[str, str]
    summary: dict[str, int]


@dataclass
class Variance:
    new_mechanisms: list[str]
    removed_mechanisms: list[str]
    gate_transitions: list[dict[str, str]]
    phase_transitions: list[dict[str, str]]
    signal_changes: dict[str, list[str]] = field(
        default_factory=lambda: {"added": [], "removed": []}
    )
    stasis: list[str] = field(default_factory=list)
    elapsed: str = ""


# -- reading --


def _read_contracts() -> list[tuple[str, dict]]:
    """(stem, parsed_yaml) for every gate contract in the directory."""
    results = []
    for path in sorted(_HERE.glob("*--*.yaml")):
        stem = path.stem
        if "--" not in stem:
            continue
        with path.open() as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            results.append((stem, data))
    return results


def _read_cocoon_map() -> dict[str, Any]:
    cocoon_path = _HERE / "cocoon-map.yaml"
    if not cocoon_path.is_file():
        return {}
    with cocoon_path.open() as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def resolve_mechanism(key: str) -> dict[str, Any] | None:
    """First gate contract whose mechanism matches key, or None."""
    for path in sorted(_HERE.glob(f"{key}--*.yaml")):
        with path.open() as f:
            contract = yaml.safe_load(f)
        if isinstance(contract, dict) and "identity" in contract:
            return contract
    return None


def list_mechanisms() -> list[str]:
    """Mechanism names found in the directory."""
    return sorted({stem.split("--")[0] for stem, _ in _read_contracts()})


def resolve_contract(canonical_name: str) -> dict[str, Any] | None:
    """Gate contract by canonical name, or None."""
    path = _HERE / f"{canonical_name}.yaml"
    if not path.is_file():
        return None
    with path.open() as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else None


# -- signal inventory --


def signal_inventory(
    contracts: list[tuple[str, dict]] | None = None,
    cocoon_map: dict[str, Any] | None = None,
) -> dict[str, dict[str, list[str]]]:
    """Every signal type mapped to who produces and consumes it.

    Gate contracts are the declared authority.
    Cocoon-map entries that aren't also gate contracts are planned topology.
    """
    if contracts is None:
        contracts = _read_contracts()
    if cocoon_map is None:
        cocoon_map = _read_cocoon_map()

    inv: dict[str, dict[str, list[str]]] = {}

    def touch(sig: str) -> dict[str, list[str]]:
        if sig not in inv:
            inv[sig] = {"produced_by": [], "consumed_by": []}
        return inv[sig]

    # gate contracts: declared authority
    contract_names = set()
    for stem, contract in contracts:
        identity = contract.get("identity", {})
        name = identity.get("name", stem)
        contract_names.add(name)
        for sig in identity.get("signal_inputs", []):
            touch(sig)["consumed_by"].append(name)
        for sig in identity.get("signal_outputs", []):
            touch(sig)["produced_by"].append(name)

    # cocoon-map: planned topology (only entries NOT already in gate contracts)
    for cocoon_name, cocoon_data in cocoon_map.items():
        if not isinstance(cocoon_data, dict):
            continue
        if cocoon_name in contract_names:
            continue
        for sig in cocoon_data.get("signal_inputs", []):
            touch(sig)["consumed_by"].append(cocoon_name)
        for sig in cocoon_data.get("signal_outputs", []):
            touch(sig)["produced_by"].append(cocoon_name)

    return inv


# -- observation --


def observe() -> Observation:
    """Look at the organism. Return what you see."""
    contracts = _read_contracts()
    cocoon_map = _read_cocoon_map()

    mechanisms: dict[str, list[dict[str, Any]]] = {}
    gates: dict[str, list[dict[str, str]]] = {}
    total_gates = gates_pending = gates_passed = 0

    for stem, contract in contracts:
        identity = contract.get("identity", {})
        mechanism = identity.get("mechanism", stem.split("--")[0])
        verb = identity.get("verb", stem.split("--")[-1] if "--" in stem else "")
        state = contract.get("state", "UNKNOWN")

        mechanisms.setdefault(mechanism, []).append(
            {"name": identity.get("name", stem), "state": state, "verb": verb}
        )

        contract_gates = []
        for gate in contract.get("gate", []):
            if not isinstance(gate, dict):
                continue
            gs = gate.get("status", "UNKNOWN")
            contract_gates.append({
                "id": gate.get("id", "?"),
                "check": gate.get("check", "?"),
                "status": gs,
            })
            total_gates += 1
            if gs == "PENDING":
                gates_pending += 1
            elif gs in ("PASS", "PASSED"):
                gates_passed += 1
        if contract_gates:
            gates[stem] = contract_gates

    phases = {
        name: data["state"]
        for name, data in cocoon_map.items()
        if isinstance(data, dict) and "state" in data
    }

    sig_types = signal_inventory(contracts=contracts, cocoon_map=cocoon_map)

    return Observation(
        timestamp=datetime.now(timezone.utc).isoformat(),
        mechanisms=mechanisms,
        signal_types=sig_types,
        gates=gates,
        phases=phases,
        summary={
            "total_mechanisms": len(mechanisms),
            "total_contracts": sum(len(v) for v in mechanisms.values()),
            "total_gates": total_gates,
            "gates_pending": gates_pending,
            "gates_passed": gates_passed,
            "signal_types": len(sig_types),
        },
    )


# -- recording --


def record_observation(obs: Observation, path: Path | None = None) -> Path:
    """Append one line to the fossil record."""
    log_path = path or (_HERE / "observations.jsonl")
    with log_path.open("a") as f:
        f.write(json.dumps(asdict(obs), default=str) + "\n")
    return log_path


def load_observations(path: Path | None = None) -> list[Observation]:
    """Read back the fossil record."""
    log_path = path or (_HERE / "observations.jsonl")
    if not log_path.is_file():
        return []
    observations = []
    with log_path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                observations.append(Observation(**json.loads(line)))
    return observations


# -- variance --


def detect_variance(current: Observation, previous: Observation) -> Variance:
    """What changed. What didn't. What decayed."""
    cur_mechs = set(current.mechanisms)
    prev_mechs = set(previous.mechanisms)

    gate_transitions = []
    stasis_contracts = []
    for contract in sorted(set(current.gates) | set(previous.gates)):
        cur_g = {g["id"]: g["status"] for g in current.gates.get(contract, [])}
        prev_g = {g["id"]: g["status"] for g in previous.gates.get(contract, [])}
        changed = False
        for gid in set(cur_g) | set(prev_g):
            old, new = prev_g.get(gid, "ABSENT"), cur_g.get(gid, "ABSENT")
            if old != new:
                gate_transitions.append(
                    {"contract": contract, "gate": gid, "old": old, "new": new}
                )
                changed = True
        if not changed and contract in current.gates:
            stasis_contracts.append(contract)

    phase_transitions = []
    for cocoon in sorted(set(current.phases) | set(previous.phases)):
        old = previous.phases.get(cocoon, "ABSENT")
        new = current.phases.get(cocoon, "ABSENT")
        if old != new:
            phase_transitions.append({"cocoon": cocoon, "old": old, "new": new})

    cur_sigs = set(current.signal_types)
    prev_sigs = set(previous.signal_types)

    try:
        delta = datetime.fromisoformat(current.timestamp) - datetime.fromisoformat(
            previous.timestamp
        )
        elapsed = str(delta)
    except (ValueError, TypeError):
        elapsed = "unknown"

    return Variance(
        new_mechanisms=sorted(cur_mechs - prev_mechs),
        removed_mechanisms=sorted(prev_mechs - cur_mechs),
        gate_transitions=gate_transitions,
        phase_transitions=phase_transitions,
        signal_changes={"added": sorted(cur_sigs - prev_sigs), "removed": sorted(prev_sigs - cur_sigs)},
        stasis=stasis_contracts,
        elapsed=elapsed,
    )


# -- instrument: topology scope --


def _hue(name: str) -> float:
    return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16) % 360


def render(obs: Observation) -> str:
    """Topology scope. Mechanisms, signal flow, gate state. SVG."""
    mechanisms = sorted(obs.mechanisms.keys())
    n = len(mechanisms)
    if n == 0:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"/>'

    cx, cy, radius = 400, 400, 300
    w, h = 800, 800
    pos: dict[str, tuple[float, float]] = {}
    for i, mech in enumerate(mechanisms):
        a = 2 * math.pi * i / n - math.pi / 2
        pos[mech] = (cx + radius * math.cos(a), cy + radius * math.sin(a))

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" style="background:#0a0a0f">'
    )
    p.append('<defs><style>'
        'text{font-family:monospace;fill:#ccc;font-size:10px;text-anchor:middle}'
        '.label{font-size:11px;fill:#eee}'
        '.stat{font-size:9px;fill:#888}'
        '.dim{fill:#555}'
        '</style></defs>')

    # signal flow edges
    drawn: set[tuple[str, str, str]] = set()
    for sig_type, edges in obs.signal_types.items():
        hu = _hue(sig_type)
        for prod in edges.get("produced_by", []):
            pm = prod.split("--")[0] if "--" in prod else prod
            for cons in edges.get("consumed_by", []):
                cm = cons.split("--")[0] if "--" in cons else cons
                if pm == cm or pm not in pos or cm not in pos:
                    continue
                key = (min(pm, cm), max(pm, cm), sig_type)
                if key in drawn:
                    continue
                drawn.add(key)
                x1, y1 = pos[pm]
                x2, y2 = pos[cm]
                qx = (x1 + x2) / 2 + (y2 - y1) * 0.08
                qy = (y1 + y2) / 2 - (x2 - x1) * 0.08
                p.append(
                    f'<path d="M {x1:.1f} {y1:.1f} Q {qx:.1f} {qy:.1f} {x2:.1f} {y2:.1f}" '
                    f'fill="none" stroke="hsl({hu}, 60%, 40%)" stroke-width="0.7" opacity="0.3"/>'
                )

    # mechanism nodes
    for mech in mechanisms:
        mx, my = pos[mech]
        contracts = obs.mechanisms[mech]
        nr = 18 + len(contracts) * 4
        mg = mp = 0
        for c in contracts:
            for g in obs.gates.get(c.get("name", ""), []):
                mg += 1
                if g["status"] in ("PASS", "PASSED"):
                    mp += 1
        ratio = mp / mg if mg > 0 else 0
        hu = _hue(mech)

        p.append(
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{nr}" '
            f'fill="hsl({hu}, 40%, 12%)" stroke="hsl({hu}, 50%, 25%)" stroke-width="1.5"/>'
        )
        if ratio >= 1.0:
            p.append(
                f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{nr - 2}" '
                f'fill="hsl({hu}, 70%, 45%)" opacity="0.6"/>'
            )
        elif ratio > 0:
            ar = nr - 2
            sa = -math.pi / 2
            ea = 2 * math.pi * ratio + sa
            sx, sy = mx + ar * math.cos(sa), my + ar * math.sin(sa)
            ex, ey = mx + ar * math.cos(ea), my + ar * math.sin(ea)
            lg = 1 if ratio > 0.5 else 0
            p.append(
                f'<path d="M {mx:.1f} {my:.1f} L {sx:.1f} {sy:.1f} '
                f'A {ar} {ar} 0 {lg} 1 {ex:.1f} {ey:.1f} Z" '
                f'fill="hsl({hu}, 70%, 45%)" opacity="0.6"/>'
            )

        p.append(f'<text x="{mx:.1f}" y="{my + nr + 14:.1f}" class="label">{mech}</text>')
        p.append(f'<text x="{mx:.1f}" y="{my + nr + 24:.1f}" class="stat">{mp}/{mg}</text>')

    # summary
    s = obs.summary
    p.append(
        f'<text x="{cx}" y="28" class="label" style="font-size:12px">'
        f'{s["total_mechanisms"]} mechanisms · {s["total_gates"]} gates '
        f'({s["gates_passed"]} lit / {s["gates_pending"]} dim) · '
        f'{s["signal_types"]} signal types</text>'
    )
    p.append(f'<text x="{cx}" y="44" class="stat">{obs.timestamp}</text>')
    p.append('</svg>')
    return "\n".join(p)


def render_variance(current: Observation, previous: Observation) -> str:
    """Diff scope. What moved between two observations. SVG."""
    v = detect_variance(current, previous)
    mechanisms = sorted(set(current.mechanisms) | set(previous.mechanisms))
    n = len(mechanisms)
    if n == 0:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"/>'

    cx, cy, radius = 400, 400, 300
    w, h = 800, 800
    pos: dict[str, tuple[float, float]] = {}
    for i, mech in enumerate(mechanisms):
        a = 2 * math.pi * i / n - math.pi / 2
        pos[mech] = (cx + radius * math.cos(a), cy + radius * math.sin(a))

    new_set = set(v.new_mechanisms)
    removed_set = set(v.removed_mechanisms)
    stasis_set = set(v.stasis)
    transitioned_contracts = {t["contract"] for t in v.gate_transitions}

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" style="background:#0a0a0f">'
    )
    p.append('<defs><style>'
        'text{font-family:monospace;fill:#ccc;font-size:10px;text-anchor:middle}'
        '.label{font-size:11px;fill:#eee}'
        '.stat{font-size:9px;fill:#888}'
        '.new{fill:#4f8}'
        '.gone{fill:#f44}'
        '.moved{fill:#ff8}'
        '.still{fill:#555}'
        '</style></defs>')

    for mech in mechanisms:
        mx, my = pos[mech]
        hu = _hue(mech)
        nr = 22

        if mech in new_set:
            stroke, label_cls = "#4f8", "new"
        elif mech in removed_set:
            stroke, label_cls = "#f44", "gone"
        else:
            # check if any of this mechanism's contracts had gate transitions
            contracts = current.mechanisms.get(mech, [])
            has_movement = any(
                c.get("name", "") in transitioned_contracts for c in contracts
            )
            if has_movement:
                stroke, label_cls = "#ff8", "moved"
            else:
                stroke, label_cls = "hsl({}, 50%, 20%)".format(hu), "still"

        p.append(
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{nr}" '
            f'fill="hsl({hu}, 40%, 8%)" stroke="{stroke}" stroke-width="2"/>'
        )
        p.append(f'<text x="{mx:.1f}" y="{my + nr + 14:.1f}" class="{label_cls}">{mech}</text>')

    # gate transitions as annotations
    for i, t in enumerate(v.gate_transitions[:12]):
        y = 60 + i * 14
        p.append(
            f'<text x="60" y="{y}" class="stat" style="text-anchor:start">'
            f'{t["contract"]} {t["gate"]}: {t["old"]} → {t["new"]}</text>'
        )

    # phase transitions
    for i, pt in enumerate(v.phase_transitions[:8]):
        y = 60 + i * 14
        p.append(
            f'<text x="740" y="{y}" class="stat" style="text-anchor:end">'
            f'{pt["cocoon"]}: {pt["old"]} → {pt["new"]}</text>'
        )

    # summary
    p.append(
        f'<text x="{cx}" y="28" class="label" style="font-size:12px">'
        f'Δ {len(v.gate_transitions)} gates · {len(v.phase_transitions)} phases · '
        f'{len(v.new_mechanisms)} new · {len(v.removed_mechanisms)} gone · '
        f'{len(v.stasis)} still · {v.elapsed}</text>'
    )
    p.append('</svg>')
    return "\n".join(p)


# -- entry point --


if __name__ == "__main__":
    obs = observe()
    path = record_observation(obs)
    svg_path = _HERE / "scope-topology.svg"
    svg_path.write_text(render(obs))

    s = obs.summary
    print(
        f"{s['total_mechanisms']} mechanisms · "
        f"{s['total_gates']} gates ({s['gates_passed']} lit / {s['gates_pending']} dim) · "
        f"{s['signal_types']} signal types"
    )
    print(f"recorded → {path.name}")
    print(f"rendered → {svg_path.name}")

    # if prior observations exist, show variance
    history = load_observations(path)
    if len(history) >= 2:
        v = detect_variance(history[-1], history[-2])
        diff_path = _HERE / "scope-variance.svg"
        diff_path.write_text(render_variance(history[-1], history[-2]))
        print(
            f"Δ {len(v.gate_transitions)} gates · {len(v.stasis)} still · "
            f"{v.elapsed} elapsed → {diff_path.name}"
        )
