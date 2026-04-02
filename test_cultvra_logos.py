"""CHECK 16 — functional verification for cultvra--logos.

Tests run against the REAL signal graph and gate contracts.
The function's job IS to document the organism's own state.
"""

from __future__ import annotations

from pathlib import Path

from cultvra_logos import (
    DocumentationEntry,
    DocumentationState,
    Query,
    document,
    emit_queries,
    inventory,
    load_contracts,
    load_documentation_history,
    load_signal_graph,
    record_documentation,
)

# ---------------------------------------------------------------------------
# 1. Reading (KNOWLEDGE + STATE input)
# ---------------------------------------------------------------------------


class TestLoadSignalGraph:
    def test_loads_real_graph(self):
        graph = load_signal_graph()
        assert isinstance(graph, dict)
        assert "functions" in graph
        assert "signal_types" in graph

    def test_missing_file_returns_empty(self, tmp_path: Path):
        graph = load_signal_graph(tmp_path / "nonexistent.yaml")
        assert graph == {}


class TestLoadContracts:
    def test_loads_real_contracts(self):
        contracts = load_contracts()
        assert len(contracts) >= 10
        names = [stem for stem, _ in contracts]
        assert "cultvra--logos" in names

    def test_empty_directory_returns_empty(self, tmp_path: Path):
        contracts = load_contracts(tmp_path)
        assert contracts == []


# ---------------------------------------------------------------------------
# 2. Documentation inventory (KNOWLEDGE output)
# ---------------------------------------------------------------------------


class TestInventory:
    def test_all_functions_have_entries(self):
        graph = load_signal_graph()
        entries = inventory(graph=graph)
        fn_names = {e.element_name for e in entries if e.element_type == "function"}
        for fname in graph.get("functions", {}):
            assert fname in fn_names, f"function {fname} missing from inventory"

    def test_all_signal_types_have_entries(self):
        graph = load_signal_graph()
        entries = inventory(graph=graph)
        st_names = {e.element_name for e in entries if e.element_type == "signal_type"}
        for stype in graph.get("signal_types", {}):
            assert stype in st_names, f"signal type {stype} missing from inventory"

    def test_all_mechanisms_have_entries(self):
        entries = inventory()
        mech_names = {e.element_name for e in entries if e.element_type == "mechanism"}
        # at least skeletal, circulatory, cultvra should be present
        assert "skeletal" in mech_names
        assert "circulatory" in mech_names
        assert "cultvra" in mech_names

    def test_entry_staleness_computed(self):
        entries = inventory()
        for e in entries:
            assert e.staleness in ("current", "stale", "missing"), (
                f"{e.element_name} has invalid staleness: {e.staleness}"
            )

    def test_organism_entry_exists(self):
        entries = inventory()
        org = [e for e in entries if e.element_type == "organism"]
        assert len(org) == 1

    def test_gate_contracts_inventoried(self):
        entries = inventory()
        gc_entries = [e for e in entries if e.element_type == "gate_contract"]
        assert len(gc_entries) >= 10

    def test_functions_with_docstrings_are_documented(self):
        entries = inventory()
        fn_entries = {e.element_name: e for e in entries if e.element_type == "function"}
        # skeletal--define and circulatory--route both have docstrings
        assert fn_entries["skeletal--define"].documented is True
        assert fn_entries["circulatory--route"].documented is True
        assert fn_entries["cultvra--logos"].documented is True

    def test_signal_types_with_descriptions_are_documented(self):
        entries = inventory()
        st_entries = {e.element_name: e for e in entries if e.element_type == "signal_type"}
        # all 5 signal types have descriptions in signal-graph.yaml
        for stype in ("QUERY", "KNOWLEDGE", "TRACE", "CONTRACT", "STATE"):
            assert st_entries[stype].documented is True, f"{stype} should be documented"


# ---------------------------------------------------------------------------
# 3. Query emission (QUERY output)
# ---------------------------------------------------------------------------


class TestQueryEmission:
    def test_queries_produced_for_missing(self):
        entries = [
            DocumentationEntry("test-mech", "mechanism", False, "", "missing"),
        ]
        queries = emit_queries(entries)
        assert len(queries) == 1
        assert queries[0].gap_type == "undocumented"
        assert queries[0].element_name == "test-mech"

    def test_queries_produced_for_stale(self):
        entries = [
            DocumentationEntry("test-gc", "gate_contract", True, "test.yaml", "stale"),
        ]
        queries = emit_queries(entries)
        assert len(queries) == 1
        assert queries[0].gap_type == "stale"

    def test_no_queries_for_documented(self):
        entries = [
            DocumentationEntry("ok-fn", "function", True, "ok.py", "current"),
        ]
        queries = emit_queries(entries)
        assert queries == []

    def test_real_organism_emits_queries(self):
        entries = inventory()
        queries = emit_queries(entries)
        # the organism has undocumented mechanisms — queries must exist
        assert len(queries) > 0

    def test_query_format(self):
        entries = inventory()
        queries = emit_queries(entries)
        for q in queries:
            assert isinstance(q, Query)
            assert q.gap_type in ("undocumented", "stale", "structural")
            assert q.element_name
            assert q.element_type
            assert q.detail


# ---------------------------------------------------------------------------
# 4. Full documentation state (integration)
# ---------------------------------------------------------------------------


class TestDocument:
    def test_returns_documentation_state(self):
        state = document()
        assert isinstance(state, DocumentationState)
        assert state.timestamp
        assert isinstance(state.summary, dict)

    def test_summary_has_required_keys(self):
        state = document()
        for key in ("total_elements", "documented", "missing", "stale",
                     "queries_emitted", "coverage_pct"):
            assert key in state.summary, f"summary missing key: {key}"

    def test_coverage_percentage_valid(self):
        state = document()
        pct = state.summary["coverage_pct"]
        assert 0 <= pct <= 100

    def test_counts_consistent(self):
        state = document()
        s = state.summary
        assert s["documented"] + s["missing"] + s["stale"] == s["total_elements"]
        assert s["queries_emitted"] == len(state.queries)


# ---------------------------------------------------------------------------
# 5. Recording (TRACE persistence)
# ---------------------------------------------------------------------------


class TestRecording:
    def test_record_and_load(self, tmp_path: Path):
        log = tmp_path / "docs.jsonl"
        state = document()
        record_documentation(state, path=log)
        loaded = load_documentation_history(path=log)
        assert len(loaded) == 1
        assert loaded[0].timestamp == state.timestamp

    def test_append_only(self, tmp_path: Path):
        log = tmp_path / "docs.jsonl"
        s1 = document()
        s2 = document()
        record_documentation(s1, path=log)
        record_documentation(s2, path=log)
        loaded = load_documentation_history(path=log)
        assert len(loaded) == 2

    def test_empty_log_returns_empty(self, tmp_path: Path):
        loaded = load_documentation_history(path=tmp_path / "docs.jsonl")
        assert loaded == []

    def test_entries_round_trip(self, tmp_path: Path):
        log = tmp_path / "docs.jsonl"
        state = document()
        record_documentation(state, path=log)
        loaded = load_documentation_history(path=log)[0]
        assert loaded.summary == state.summary
        assert len(loaded.entries) == len(state.entries)
        assert len(loaded.queries) == len(state.queries)


# ---------------------------------------------------------------------------
# 6. Signal graph compliance (CHECK verification)
# ---------------------------------------------------------------------------


class TestSignalGraphCompliance:
    def test_function_in_signal_graph(self):
        graph = load_signal_graph()
        assert "cultvra--logos" in graph.get("functions", {})

    def test_inputs_declared(self):
        graph = load_signal_graph()
        fn = graph["functions"]["cultvra--logos"]
        assert set(fn["inputs"]) == {"KNOWLEDGE", "STATE", "TRACE"}

    def test_outputs_declared(self):
        graph = load_signal_graph()
        fn = graph["functions"]["cultvra--logos"]
        assert set(fn["outputs"]) == {"QUERY", "TRACE"}

    def test_mechanism_is_cultvra(self):
        graph = load_signal_graph()
        fn = graph["functions"]["cultvra--logos"]
        assert fn["mechanism"] == "cultvra"

    def test_information_edges_exist(self):
        graph = load_signal_graph()
        info_edges = graph.get("edges", {}).get("information", [])
        # edges TO cultvra--logos
        to_cultvra = [e for e in info_edges if e.get("to") == "cultvra--logos"]
        assert len(to_cultvra) == 2  # from skeletal + from circulatory

    def test_feedback_edge_exists(self):
        graph = load_signal_graph()
        info_edges = graph.get("edges", {}).get("information", [])
        feedback = [
            e for e in info_edges
            if e.get("from") == "cultvra--logos"
            and e.get("to") == "skeletal--define"
            and e.get("signal") == "QUERY"
        ]
        assert len(feedback) == 1
        assert feedback[0].get("direction") == "feedback"

    def test_cycle_exists(self):
        """CHECK 6: information graph has at least one cycle."""
        graph = load_signal_graph()
        info_edges = graph.get("edges", {}).get("information", [])

        # build adjacency from information edges
        adj: dict[str, set[str]] = {}
        for edge in info_edges:
            src = edge.get("from", "")
            dst = edge.get("to", "")
            if src and dst:
                adj.setdefault(src, set()).add(dst)

        # DFS cycle detection
        def has_cycle(start: str) -> bool:
            visited: set[str] = set()
            stack = [start]
            while stack:
                node = stack.pop()
                if node == start and len(visited) > 0:
                    return True
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in adj.get(node, set()):
                    stack.append(neighbor)
            return False

        functions = list(graph.get("functions", {}).keys())
        assert any(has_cycle(f) for f in functions), "no cycle found in information graph"

    def test_check_19_cycle_path(self):
        """CHECK 19: skeletal → circulatory → cultvra → skeletal."""
        graph = load_signal_graph()
        info_edges = graph.get("edges", {}).get("information", [])

        adj: dict[str, set[str]] = {}
        for edge in info_edges:
            src = edge.get("from", "")
            dst = edge.get("to", "")
            if src and dst:
                adj.setdefault(src, set()).add(dst)

        # verify the specific cycle path
        assert "circulatory--route" in adj.get("skeletal--define", set())
        assert "cultvra--logos" in adj.get("circulatory--route", set())
        assert "skeletal--define" in adj.get("cultvra--logos", set())
