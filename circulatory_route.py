"""circulatory--route: the organism routes signals between its parts.

GEN-002: canonical '--' maps to '_' in .py filenames.

The circulatory system moves information around the organism. It reads
what the skeletal system defined (the structure) and computes what flows
(the routes), what could flow (attractions), and what is broken (defects).

Skeletal reads what EXISTS. Circulatory computes what FLOWS.
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
class Route:
    """A signal path from producer to consumer."""

    signal_type: str
    producer: str
    consumer: str
    edge_family: str  # dependency, information, governance, evolution


@dataclass
class Attraction:
    """A candidate connection discovered by signal type overlap.

    SEED §II Step 5: "what else in the organism shares my signal types?"
    """

    function_a: str
    function_b: str
    shared_signals: list[str]
    direction: str  # "a → b", "b → a", or "bidirectional"


@dataclass
class RoutingDefect:
    """A structural problem in the organism's signal flow."""

    kind: str  # DEAD_SIGNAL, STARVED_CONSUMER, ORPHANED_FUNCTION
    subject: str
    detail: str


@dataclass
class RoutingTable:
    """The complete routing state of the organism at a moment in time."""

    timestamp: str
    routes: list[Route]
    attractions: list[Attraction]
    defects: list[RoutingDefect]
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


# -- signal profiles --


def _build_profiles(
    graph: dict[str, Any],
    contracts: list[tuple[str, dict]],
) -> dict[str, dict[str, set[str]]]:
    """Build signal profiles: name → {inputs: set, outputs: set}.

    Sources: graph functions (living) + gate contracts (declared).
    Graph functions take priority — they are the ratified wiring.
    """
    profiles: dict[str, dict[str, set[str]]] = {}

    # living functions from signal graph
    for fname, fdata in graph.get("functions", {}).items():
        if isinstance(fdata, dict):
            profiles[fname] = {
                "inputs": set(fdata.get("inputs", [])),
                "outputs": set(fdata.get("outputs", [])),
            }

    # declared contracts (only if not already in graph)
    for stem, contract in contracts:
        identity = contract.get("identity", {})
        name = identity.get("name", stem)
        if name not in profiles:
            profiles[name] = {
                "inputs": set(identity.get("signal_inputs", [])),
                "outputs": set(identity.get("signal_outputs", [])),
            }

    return profiles


# -- routing --


def compute_routes(graph: dict[str, Any]) -> list[Route]:
    """Trace all signal paths from the signal graph.

    Two sources of routes:
    1. Declared edges in graph.edges (explicit wiring)
    2. Implicit routes from signal type matching between functions
       (producer output type == consumer input type)
    """
    functions = graph.get("functions", {})
    routes: list[Route] = []

    # 1. declared edges
    for family in ("dependency", "information", "governance", "evolution"):
        for edge in graph.get("edges", {}).get(family, []):
            if isinstance(edge, dict):
                routes.append(Route(
                    signal_type=edge.get("signal", ""),
                    producer=edge.get("from", ""),
                    consumer=edge.get("to", ""),
                    edge_family=family,
                ))

    # 2. implicit routes from signal type matching between graph functions
    producers: dict[str, list[str]] = {}
    consumers: dict[str, list[str]] = {}
    for fname, fdata in functions.items():
        if not isinstance(fdata, dict):
            continue
        for sig in fdata.get("outputs", []):
            producers.setdefault(sig, []).append(fname)
        for sig in fdata.get("inputs", []):
            consumers.setdefault(sig, []).append(fname)

    declared = {(r.producer, r.consumer, r.signal_type) for r in routes}
    for sig_type in sorted(set(producers) & set(consumers)):
        for prod in producers[sig_type]:
            for cons in consumers[sig_type]:
                if prod != cons and (prod, cons, sig_type) not in declared:
                    routes.append(Route(
                        signal_type=sig_type,
                        producer=prod,
                        consumer=cons,
                        edge_family="information",
                    ))

    return routes


def compute_attractions(
    graph: dict[str, Any],
    contracts: list[tuple[str, dict]],
) -> list[Attraction]:
    """Signal attraction: what functions share signal types?

    For each pair of functions/contracts, check if one's outputs
    intersect the other's inputs. These are CANDIDATES, not connections.
    The organism sees its potential wiring.
    """
    profiles = _build_profiles(graph, contracts)
    attractions: list[Attraction] = []
    names = sorted(profiles)

    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            pa, pb = profiles[a], profiles[b]
            a_feeds_b = pa["outputs"] & pb["inputs"]
            b_feeds_a = pb["outputs"] & pa["inputs"]
            shared = a_feeds_b | b_feeds_a
            if not shared:
                continue

            if a_feeds_b and b_feeds_a:
                direction = "bidirectional"
            elif a_feeds_b:
                direction = f"{a} → {b}"
            else:
                direction = f"{b} → {a}"

            attractions.append(Attraction(
                function_a=a,
                function_b=b,
                shared_signals=sorted(shared),
                direction=direction,
            ))

    return attractions


def detect_defects(
    graph: dict[str, Any],
    contracts: list[tuple[str, dict]],
    routes: list[Route],
) -> list[RoutingDefect]:
    """Find structural routing problems.

    Three categories:
    - DEAD_SIGNAL: produced but never consumed (energy lost)
    - STARVED_CONSUMER: consumed but never produced (dependency unmet)
    - ORPHANED_FUNCTION: in the signal graph but participates in no routes
    """
    defects: list[RoutingDefect] = []
    profiles = _build_profiles(graph, contracts)

    # aggregate all producers and consumers
    all_prod: dict[str, set[str]] = {}
    all_cons: dict[str, set[str]] = {}
    for name, profile in profiles.items():
        for sig in profile["outputs"]:
            all_prod.setdefault(sig, set()).add(name)
        for sig in profile["inputs"]:
            all_cons.setdefault(sig, set()).add(name)

    for sig in sorted(all_prod):
        if sig not in all_cons:
            defects.append(RoutingDefect(
                kind="DEAD_SIGNAL",
                subject=sig,
                detail=f"produced by {sorted(all_prod[sig])} but consumed by nobody",
            ))

    for sig in sorted(all_cons):
        if sig not in all_prod:
            defects.append(RoutingDefect(
                kind="STARVED_CONSUMER",
                subject=sig,
                detail=f"consumed by {sorted(all_cons[sig])} but produced by nobody",
            ))

    # orphaned functions (only meaningful with 2+ functions in graph)
    functions = graph.get("functions", {})
    if len(functions) >= 2:
        routed = set()
        for r in routes:
            routed.add(r.producer)
            routed.add(r.consumer)
        for fname in sorted(functions):
            if fname not in routed:
                defects.append(RoutingDefect(
                    kind="ORPHANED_FUNCTION",
                    subject=fname,
                    detail="in signal graph but participates in no routes",
                ))

    return defects


# -- main operation --


def route(
    graph_path: Path | None = None,
    contract_dir: Path | None = None,
) -> RoutingTable:
    """The organism routes signals between its parts."""
    graph = load_signal_graph(graph_path)
    contracts = load_contracts(contract_dir)

    routes = compute_routes(graph)
    attractions = compute_attractions(graph, contracts)
    defects = detect_defects(graph, contracts, routes)

    return RoutingTable(
        timestamp=datetime.now(timezone.utc).isoformat(),
        routes=routes,
        attractions=attractions,
        defects=defects,
        summary={
            "functions_in_graph": len(graph.get("functions", {})),
            "signal_types_in_graph": len(graph.get("signal_types", {})),
            "total_routes": len(routes),
            "total_attractions": len(attractions),
            "total_defects": len(defects),
            "contracts_scanned": len(contracts),
        },
    )


# -- recording --


def record_routing(table: RoutingTable, path: Path | None = None) -> Path:
    """Append routing snapshot to the routing log (TRACE output)."""
    log = path or (_HERE / "routes.jsonl")
    with log.open("a") as f:
        f.write(json.dumps(asdict(table), default=str) + "\n")
    return log


def load_routing_history(path: Path | None = None) -> list[RoutingTable]:
    """Read back the routing log."""
    log = path or (_HERE / "routes.jsonl")
    if not log.is_file():
        return []
    tables: list[RoutingTable] = []
    with log.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            tables.append(RoutingTable(
                timestamp=raw["timestamp"],
                routes=[Route(**r) for r in raw.get("routes", [])],
                attractions=[Attraction(**a) for a in raw.get("attractions", [])],
                defects=[RoutingDefect(**d) for d in raw.get("defects", [])],
                summary=raw.get("summary", {}),
            ))
    return tables


# -- entry point --


if __name__ == "__main__":
    table = route()
    s = table.summary
    print(
        f"{s['functions_in_graph']} functions · "
        f"{s['total_routes']} routes · "
        f"{s['total_attractions']} attractions · "
        f"{s['total_defects']} defects"
    )

    log = record_routing(table)
    print(f"recorded → {log.name}")

    if table.routes:
        print("\nRoutes:")
        for r in table.routes:
            print(f"  {r.producer} →[{r.signal_type}]→ {r.consumer} ({r.edge_family})")

    if table.attractions[:10]:
        print(f"\nAttractions ({len(table.attractions)} total, showing first 10):")
        for a in table.attractions[:10]:
            print(f"  {a.function_a} ⇔ {a.function_b}: {a.shared_signals} ({a.direction})")

    if table.defects:
        print(f"\nDefects ({len(table.defects)}):")
        for d in table.defects:
            print(f"  [{d.kind}] {d.subject}: {d.detail}")
