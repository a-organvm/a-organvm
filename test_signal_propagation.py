"""Signal propagation integration test — proves the organism is alive.

This test lights the full signal graph. It runs all five functions in
sequence and verifies that signals flow between them:

  skeletal (KNOWLEDGE) → circulatory (STATE) → cultvra (QUERY) → skeletal (feedback)
  skeletal (KNOWLEDGE) → immune (REPORT) → skeletal (feedback)
  skeletal (KNOWLEDGE) → respiratory (SOURCE) → circulatory (feedback via routing)
  respiratory (KNOWLEDGE) → skeletal (feedback)

Three feedback loops complete the autopoietic circuit:
  1. cultvra → skeletal via QUERY (documentation gaps become structural queries)
  2. immune → skeletal via REPORT (verification findings become structural queries)
  3. respiratory → skeletal via KNOWLEDGE (ingestion discoveries enrich structure)

Two governance edges enforce correctness:
  immune → skeletal via VALIDATION
  immune → circulatory via VALIDATION
"""

from pathlib import Path

import circulatory_route
import cultvra_logos
import immune_verify
import respiratory_ingest
import skeletal_define

_HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. Signal chain: skeletal → circulatory → cultvra → immune → respiratory
# ---------------------------------------------------------------------------


class TestSignalChain:
    """End-to-end signal propagation through the organism."""

    def test_skeletal_produces_knowledge(self):
        """skeletal--define emits KNOWLEDGE: mechanisms and gates."""
        obs = skeletal_define.observe()
        assert len(obs.mechanisms) > 0, "no mechanisms observed"
        assert obs.summary["total_gates"] > 0, "no gates observed"
        assert obs.summary["signal_types"] > 0, "no signal types observed"

    def test_circulatory_consumes_knowledge_produces_state(self):
        """circulatory--route reads signal-graph (KNOWLEDGE) and produces STATE."""
        table = circulatory_route.route(
            graph_path=_HERE / "signal-graph.yaml",
            contract_dir=_HERE,
        )
        assert table.summary["functions_in_graph"] >= 5, (
            f"expected ≥5 functions in graph, got {table.summary['functions_in_graph']}"
        )
        assert table.summary["total_routes"] > 0, "no routes computed"
        assert table.summary["signal_types_in_graph"] >= 9, (
            f"expected ≥9 signal types, got {table.summary['signal_types_in_graph']}"
        )

    def test_cultvra_consumes_state_produces_queries(self):
        """cultvra--logos reads structure and produces QUERY signals."""
        state = cultvra_logos.document(
            graph_path=_HERE / "signal-graph.yaml",
            contract_dir=_HERE,
        )
        assert state.summary["total_elements"] > 0, "no elements inventoried"

    def test_immune_consumes_knowledge_produces_validation(self):
        """immune--verify reads structure and produces REPORT + VALIDATION."""
        report = immune_verify.verify()
        assert report.summary["checks_run"] >= 6, "fewer than 6 checks"
        assert report.summary["organism_healthy"] == 1, (
            "organism is not healthy — immune--verify found failures"
        )

    def test_respiratory_consumes_source_produces_knowledge(self):
        """respiratory--ingest discovers sources and produces SOURCE + KNOWLEDGE."""
        report = respiratory_ingest.ingest()
        assert report.summary["total_sources"] > 0, "no sources discovered"
        assert report.summary["migrations_tracked"] > 0, "no migrations tracked"
        assert report.summary["channels_total"] == 4, "expected 4 pipeline channels"

    def test_full_chain_signals_flow(self):
        """The complete chain: observe → route → document → verify → ingest."""
        # 1. KNOWLEDGE: skeletal reads structure (proves observation works)
        skeletal_define.observe()

        # 2. STATE: circulatory computes routing from the same signal graph
        table = circulatory_route.route(
            graph_path=_HERE / "signal-graph.yaml",
            contract_dir=_HERE,
        )

        # 3. QUERY: cultvra documents everything and emits gap queries
        doc = cultvra_logos.document(
            graph_path=_HERE / "signal-graph.yaml",
            contract_dir=_HERE,
        )

        # 4. REPORT + VALIDATION: immune verifies integrity
        verification = immune_verify.verify()

        # 5. SOURCE + KNOWLEDGE: respiratory discovers external material
        ingestion = respiratory_ingest.ingest()

        # --- signal propagation assertions ---

        # KNOWLEDGE → STATE: routes reference functions from signal graph
        graph_functions = set(circulatory_route.load_signal_graph(
            _HERE / "signal-graph.yaml"
        ).get("functions", {}).keys())
        assert len(graph_functions) >= 5, "signal graph should have ≥5 functions"
        assert len(table.routes) > 0, "routing table should have routes"

        # STATE → QUERY: documentation entries exist for all graph functions
        documented_elements = {e.element_name for e in doc.entries}
        for func in graph_functions:
            assert func in documented_elements, (
                f"function '{func}' is in signal graph but not in documentation inventory"
            )

        # QUERY → KNOWLEDGE (feedback): queries reference resolvable types
        resolvable_types = {"function", "signal_type", "mechanism", "gate_contract",
                            "organism"}
        for query in doc.queries:
            assert query.element_type in resolvable_types, (
                f"query element_type '{query.element_type}' is not resolvable"
            )

        # REPORT → KNOWLEDGE (feedback): verification produces structured findings
        assert verification.summary["checks_run"] >= 6

        # SOURCE → KNOWLEDGE (feedback): ingestion finds sources from gate contracts
        assert ingestion.summary["total_sources"] > 0
        # ingested sources should reference known gate contracts
        contract_stems = {stem for stem, _ in respiratory_ingest.load_contracts()}
        for src in ingestion.sources:
            assert src.channel in contract_stems, (
                f"source channel '{src.channel}' is not a known gate contract"
            )


# ---------------------------------------------------------------------------
# 2. Signal graph structural integrity
# ---------------------------------------------------------------------------


class TestSignalGraphIntegrity:
    """The wiring diagram is internally consistent."""

    def test_all_functions_have_io(self):
        """Every function in signal-graph.yaml declares inputs and outputs."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        for fname, fdata in graph.get("functions", {}).items():
            assert isinstance(fdata, dict), f"{fname}: function data is not a dict"
            assert len(fdata.get("inputs", [])) > 0, f"{fname}: no inputs declared"
            assert len(fdata.get("outputs", [])) > 0, f"{fname}: no outputs declared"

    def test_edges_reference_existing_functions(self):
        """All edge endpoints exist as declared functions."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        functions = set(graph.get("functions", {}).keys())
        for family in ("dependency", "information", "governance", "evolution"):
            for edge in graph.get("edges", {}).get(family, []):
                if isinstance(edge, dict):
                    assert edge["from"] in functions, (
                        f"edge from '{edge['from']}' not in functions ({family})"
                    )
                    assert edge["to"] in functions, (
                        f"edge to '{edge['to']}' not in functions ({family})"
                    )

    def test_edges_reference_valid_signals(self):
        """All edge signal types are declared in signal_types."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        signal_types = set(graph.get("signal_types", {}).keys())
        for family in ("dependency", "information", "governance", "evolution"):
            for edge in graph.get("edges", {}).get(family, []):
                if isinstance(edge, dict) and "signal" in edge:
                    assert edge["signal"] in signal_types, (
                        f"edge signal '{edge['signal']}' not in signal_types ({family})"
                    )

    def test_no_routing_defects_in_live_functions(self):
        """No structural routing defects in the five live functions."""
        table = circulatory_route.route(
            graph_path=_HERE / "signal-graph.yaml",
            contract_dir=_HERE,
        )
        live_functions = {
            "skeletal--define", "circulatory--route", "cultvra--logos",
            "immune--verify", "respiratory--ingest",
        }
        function_defects = [
            d for d in table.defects
            if d.subject in live_functions
        ]
        assert len(function_defects) == 0, (
            f"routing defects in live functions: "
            f"{[(d.kind, d.subject, d.detail) for d in function_defects]}"
        )

    def test_three_feedback_loops_exist(self):
        """Three feedback edges exist (cultvra, immune, respiratory → skeletal)."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        info_edges = graph.get("edges", {}).get("information", [])
        feedback = [
            e for e in info_edges
            if isinstance(e, dict) and e.get("direction") == "feedback"
        ]
        assert len(feedback) >= 3, (
            f"expected ≥3 feedback loops, found {len(feedback)}"
        )
        # verify each specific feedback loop
        feedback_pairs = {(e["from"], e["to"]) for e in feedback}
        assert ("cultvra--logos", "skeletal--define") in feedback_pairs, (
            "missing cultvra→skeletal QUERY feedback"
        )
        assert ("immune--verify", "skeletal--define") in feedback_pairs, (
            "missing immune→skeletal REPORT feedback"
        )
        assert ("respiratory--ingest", "skeletal--define") in feedback_pairs, (
            "missing respiratory→skeletal KNOWLEDGE feedback"
        )

    def test_governance_edges_exist(self):
        """Governance edges from immune--verify to skeletal and circulatory."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        gov_edges = graph.get("edges", {}).get("governance", [])
        assert len(gov_edges) >= 2, (
            f"expected ≥2 governance edges, found {len(gov_edges)}"
        )
        gov_pairs = {(e["from"], e["to"]) for e in gov_edges if isinstance(e, dict)}
        assert ("immune--verify", "skeletal--define") in gov_pairs, (
            "missing immune→skeletal governance edge"
        )
        assert ("immune--verify", "circulatory--route") in gov_pairs, (
            "missing immune→circulatory governance edge"
        )

    def test_nine_signal_types_declared(self):
        """The signal graph declares all 9 discovered signal types."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        signal_types = set(graph.get("signal_types", {}).keys())
        expected = {
            "QUERY", "KNOWLEDGE", "TRACE", "CONTRACT", "STATE",
            "REPORT", "VALIDATION", "SOURCE", "MIGRATION",
        }
        assert expected <= signal_types, (
            f"missing signal types: {expected - signal_types}"
        )

    def test_five_functions_declared(self):
        """The signal graph declares all 5 embodied functions."""
        graph = circulatory_route.load_signal_graph(_HERE / "signal-graph.yaml")
        functions = set(graph.get("functions", {}).keys())
        expected = {
            "skeletal--define", "circulatory--route", "cultvra--logos",
            "immune--verify", "respiratory--ingest",
        }
        assert expected <= functions, (
            f"missing functions: {expected - functions}"
        )
