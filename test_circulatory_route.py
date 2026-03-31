"""CHECK 16 — functional verification for circulatory--route.

Tests run against the REAL signal graph and gate contracts.
The function's job IS to compute the organism's signal flow.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from circulatory_route import (
    Attraction,
    Route,
    RoutingDefect,
    RoutingTable,
    compute_attractions,
    compute_routes,
    detect_defects,
    load_contracts,
    load_routing_history,
    load_signal_graph,
    record_routing,
    route,
)


# ---------------------------------------------------------------------------
# 1. Reading (CONTRACT input)
# ---------------------------------------------------------------------------


class TestLoadSignalGraph:
    def test_loads_real_graph(self):
        graph = load_signal_graph()
        assert isinstance(graph, dict)
        assert "functions" in graph
        assert "signal_types" in graph
        assert "edges" in graph

    def test_missing_file_returns_empty(self, tmp_path: Path):
        graph = load_signal_graph(tmp_path / "nonexistent.yaml")
        assert graph == {}


class TestLoadContracts:
    def test_loads_real_contracts(self):
        contracts = load_contracts()
        assert len(contracts) >= 10  # 35 gate contracts exist
        names = [stem for stem, _ in contracts]
        assert "skeletal--define" in names
        assert "circulatory--route" in names

    def test_empty_directory_returns_empty(self, tmp_path: Path):
        contracts = load_contracts(tmp_path)
        assert contracts == []

    def test_all_contracts_have_identity(self):
        contracts = load_contracts()
        for stem, contract in contracts:
            assert "identity" in contract, f"{stem} missing identity"


# ---------------------------------------------------------------------------
# 2. Route computation (INFORMATION flow)
# ---------------------------------------------------------------------------


class TestComputeRoutes:
    def test_returns_list_of_routes(self):
        graph = load_signal_graph()
        routes = compute_routes(graph)
        assert isinstance(routes, list)
        for r in routes:
            assert isinstance(r, Route)

    def test_declared_edges_become_routes(self):
        graph = {
            "functions": {
                "a--do": {"inputs": ["X"], "outputs": ["Y"]},
                "b--act": {"inputs": ["Y"], "outputs": ["Z"]},
            },
            "edges": {
                "information": [{"from": "a--do", "to": "b--act", "signal": "Y"}],
                "dependency": [],
                "governance": [],
                "evolution": [],
            },
        }
        routes = compute_routes(graph)
        declared = [r for r in routes if r.producer == "a--do" and r.consumer == "b--act"]
        assert len(declared) >= 1
        assert declared[0].signal_type == "Y"
        assert declared[0].edge_family == "information"

    def test_implicit_routes_from_type_matching(self):
        graph = {
            "functions": {
                "a--do": {"inputs": [], "outputs": ["SHARED"]},
                "b--act": {"inputs": ["SHARED"], "outputs": []},
            },
            "edges": {"dependency": [], "information": [], "governance": [], "evolution": []},
        }
        routes = compute_routes(graph)
        implicit = [
            r
            for r in routes
            if r.producer == "a--do" and r.consumer == "b--act" and r.signal_type == "SHARED"
        ]
        assert len(implicit) == 1

    def test_no_self_routes(self):
        graph = {
            "functions": {
                "a--do": {"inputs": ["X"], "outputs": ["X"]},
            },
            "edges": {"dependency": [], "information": [], "governance": [], "evolution": []},
        }
        routes = compute_routes(graph)
        self_routes = [r for r in routes if r.producer == r.consumer]
        assert self_routes == []

    def test_no_duplicate_routes(self):
        graph = {
            "functions": {
                "a--do": {"inputs": [], "outputs": ["Y"]},
                "b--act": {"inputs": ["Y"], "outputs": []},
            },
            "edges": {
                "information": [{"from": "a--do", "to": "b--act", "signal": "Y"}],
                "dependency": [],
                "governance": [],
                "evolution": [],
            },
        }
        routes = compute_routes(graph)
        a_to_b = [r for r in routes if r.producer == "a--do" and r.consumer == "b--act"]
        assert len(a_to_b) == 1  # declared + implicit should not double


# ---------------------------------------------------------------------------
# 3. Signal attraction (CANDIDATE connections)
# ---------------------------------------------------------------------------


class TestComputeAttractions:
    def test_detects_shared_signals(self):
        graph = {"functions": {}}
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": [], "signal_outputs": ["X"]}}),
            ("b--act", {"identity": {"name": "b--act", "signal_inputs": ["X"], "signal_outputs": []}}),
        ]
        attractions = compute_attractions(graph, contracts)
        assert len(attractions) == 1
        assert attractions[0].shared_signals == ["X"]
        assert "a--do" in attractions[0].direction

    def test_bidirectional_attraction(self):
        graph = {"functions": {}}
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": ["Y"], "signal_outputs": ["X"]}}),
            ("b--act", {"identity": {"name": "b--act", "signal_inputs": ["X"], "signal_outputs": ["Y"]}}),
        ]
        attractions = compute_attractions(graph, contracts)
        assert len(attractions) == 1
        assert attractions[0].direction == "bidirectional"

    def test_no_attraction_without_overlap(self):
        graph = {"functions": {}}
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": ["A"], "signal_outputs": ["B"]}}),
            ("b--act", {"identity": {"name": "b--act", "signal_inputs": ["C"], "signal_outputs": ["D"]}}),
        ]
        attractions = compute_attractions(graph, contracts)
        assert attractions == []

    def test_real_organism_has_attractions(self):
        graph = load_signal_graph()
        contracts = load_contracts()
        attractions = compute_attractions(graph, contracts)
        # 35 contracts sharing signal types — many attractions expected
        assert len(attractions) > 10

    def test_graph_functions_take_priority(self):
        graph = {
            "functions": {
                "a--do": {"inputs": ["Q"], "outputs": ["K"]},
            },
        }
        # contract with DIFFERENT signals for the same name
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": ["Z"], "signal_outputs": ["W"]}}),
            ("b--act", {"identity": {"name": "b--act", "signal_inputs": ["K"], "signal_outputs": []}}),
        ]
        attractions = compute_attractions(graph, contracts)
        # should use graph's K output, not contract's W
        shared = [a for a in attractions if "K" in a.shared_signals]
        assert len(shared) == 1


# ---------------------------------------------------------------------------
# 4. Defect detection (structural problems)
# ---------------------------------------------------------------------------


class TestDetectDefects:
    def test_dead_signal(self):
        graph = {"functions": {}}
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": [], "signal_outputs": ["ORPHAN"]}}),
        ]
        defects = detect_defects(graph, contracts, routes=[])
        dead = [d for d in defects if d.kind == "DEAD_SIGNAL" and d.subject == "ORPHAN"]
        assert len(dead) == 1

    def test_starved_consumer(self):
        graph = {"functions": {}}
        contracts = [
            ("a--do", {"identity": {"name": "a--do", "signal_inputs": ["MISSING"], "signal_outputs": []}}),
        ]
        defects = detect_defects(graph, contracts, routes=[])
        starved = [d for d in defects if d.kind == "STARVED_CONSUMER" and d.subject == "MISSING"]
        assert len(starved) == 1

    def test_orphaned_function(self):
        graph = {
            "functions": {
                "a--do": {"inputs": ["X"], "outputs": ["Y"]},
                "b--act": {"inputs": ["Z"], "outputs": ["W"]},
            },
        }
        defects = detect_defects(graph, [], routes=[])
        orphaned = [d for d in defects if d.kind == "ORPHANED_FUNCTION"]
        assert len(orphaned) == 2

    def test_no_orphan_check_with_single_function(self):
        graph = {
            "functions": {
                "solo--fn": {"inputs": ["X"], "outputs": ["Y"]},
            },
        }
        defects = detect_defects(graph, [], routes=[])
        orphaned = [d for d in defects if d.kind == "ORPHANED_FUNCTION"]
        assert orphaned == []

    def test_no_false_orphan_when_routed(self):
        graph = {
            "functions": {
                "a--do": {"inputs": [], "outputs": ["Y"]},
                "b--act": {"inputs": ["Y"], "outputs": []},
            },
        }
        routes = [Route("Y", "a--do", "b--act", "information")]
        defects = detect_defects(graph, [], routes=routes)
        orphaned = [d for d in defects if d.kind == "ORPHANED_FUNCTION"]
        assert orphaned == []


# ---------------------------------------------------------------------------
# 5. Full routing table (integration)
# ---------------------------------------------------------------------------


class TestRoute:
    def test_returns_routing_table(self):
        table = route()
        assert isinstance(table, RoutingTable)
        assert table.timestamp
        assert isinstance(table.summary, dict)
        assert "total_routes" in table.summary
        assert "total_attractions" in table.summary
        assert "total_defects" in table.summary

    def test_scans_all_contracts(self):
        table = route()
        assert table.summary["contracts_scanned"] >= 10

    def test_finds_real_attractions(self):
        table = route()
        assert table.summary["total_attractions"] > 0


# ---------------------------------------------------------------------------
# 6. Recording (TRACE persistence)
# ---------------------------------------------------------------------------


class TestRecording:
    def test_record_and_load(self, tmp_path: Path):
        log = tmp_path / "routes.jsonl"
        table = route()
        record_routing(table, path=log)
        loaded = load_routing_history(path=log)
        assert len(loaded) == 1
        assert loaded[0].timestamp == table.timestamp

    def test_append_only(self, tmp_path: Path):
        log = tmp_path / "routes.jsonl"
        t1 = route()
        t2 = route()
        record_routing(t1, path=log)
        record_routing(t2, path=log)
        loaded = load_routing_history(path=log)
        assert len(loaded) == 2

    def test_empty_log_returns_empty(self, tmp_path: Path):
        log = tmp_path / "routes.jsonl"
        loaded = load_routing_history(path=log)
        assert loaded == []

    def test_routes_round_trip(self, tmp_path: Path):
        log = tmp_path / "routes.jsonl"
        table = route()
        record_routing(table, path=log)
        loaded = load_routing_history(path=log)[0]
        assert loaded.summary == table.summary
        assert len(loaded.routes) == len(table.routes)
        assert len(loaded.attractions) == len(table.attractions)
        assert len(loaded.defects) == len(table.defects)
