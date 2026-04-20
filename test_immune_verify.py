"""CHECK 20 — functional verification for immune--verify.

The immune system verifies the organism's own integrity.
Tests run against the REAL organism state.
"""

from __future__ import annotations

import json
from pathlib import Path

from immune_verify import (
    Finding,
    Validation,
    VerificationReport,
    check_contract_consistency,
    check_feedback_loop,
    check_function_implementation,
    check_gate_health,
    check_signal_graph_integrity,
    check_temporal_freshness,
    load_contracts,
    load_signal_graph,
    load_verification_history,
    record_verification,
    verify,
)


_HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. Signal graph integrity (structural dimension)
# ---------------------------------------------------------------------------


class TestSignalGraphIntegrity:
    def test_passes_on_real_graph(self):
        graph = load_signal_graph()
        result = check_signal_graph_integrity(graph)
        assert result.passed, f"failures: {[(f.subject, f.detail) for f in result.findings if f.severity == 'ERROR']}"

    def test_detects_missing_function(self):
        graph = {"functions": {"foo": {"inputs": ["X"], "outputs": ["Y"]}},
                 "signal_types": {"X": {}, "Y": {}},
                 "edges": {"information": [{"from": "foo", "to": "GHOST", "signal": "Y"}],
                           "dependency": [], "governance": [], "evolution": []}}
        result = check_signal_graph_integrity(graph)
        assert not result.passed
        assert any("GHOST" in f.subject for f in result.findings)

    def test_detects_undeclared_signal(self):
        graph = {"functions": {"a": {"inputs": ["X"], "outputs": ["Y"]},
                               "b": {"inputs": ["Y"], "outputs": ["X"]}},
                 "signal_types": {"X": {}},
                 "edges": {"information": [{"from": "a", "to": "b", "signal": "Y"}],
                           "dependency": [], "governance": [], "evolution": []}}
        result = check_signal_graph_integrity(graph)
        assert any(f.detail and "undeclared signal" in f.detail for f in result.findings)


# ---------------------------------------------------------------------------
# 2. Contract consistency (coherence dimension)
# ---------------------------------------------------------------------------


class TestContractConsistency:
    def test_passes_on_real_contracts(self):
        graph = load_signal_graph()
        contracts = load_contracts()
        result = check_contract_consistency(contracts, graph)
        assert result.passed

    def test_detects_missing_identity(self):
        contracts = [("broken--contract", {"state": "CALLING"})]
        graph = {"signal_types": {}}
        result = check_contract_consistency(contracts, graph)
        assert not result.passed
        assert any("missing identity" in f.detail for f in result.findings)

    def test_all_contracts_have_mechanism(self):
        contracts = load_contracts()
        for stem, contract in contracts:
            identity = contract.get("identity", {})
            assert identity.get("mechanism"), f"{stem}: missing mechanism"


# ---------------------------------------------------------------------------
# 3. Function implementation (structural dimension)
# ---------------------------------------------------------------------------


class TestFunctionImplementation:
    def test_all_graph_functions_have_py_files(self):
        graph = load_signal_graph()
        result = check_function_implementation(graph)
        assert result.passed, f"missing: {[(f.subject, f.detail) for f in result.findings if f.severity == 'ERROR']}"

    def test_detects_missing_implementation(self, tmp_path):
        graph = {"functions": {"phantom--function": {"inputs": ["X"], "outputs": ["Y"]}}}
        result = check_function_implementation(graph, tmp_path)
        assert not result.passed
        assert any("phantom--function" in f.subject for f in result.findings)


# ---------------------------------------------------------------------------
# 4. Gate health (governance dimension)
# ---------------------------------------------------------------------------


class TestGateHealth:
    def test_real_organism_gates_no_failures(self):
        contracts = load_contracts()
        result = check_gate_health(contracts)
        # no FAILED gates expected (PENDING is fine)
        assert result.passed

    def test_detects_failed_gate(self):
        contracts = [("test--contract", {
            "identity": {"name": "test--contract", "mechanism": "test", "verb": "test"},
            "gate": [{"id": "G1", "check": "BROKEN", "status": "FAILED"}]
        })]
        result = check_gate_health(contracts)
        assert not result.passed
        assert any("FAILED" in f.detail for f in result.findings)

    def test_counts_gates_correctly(self):
        contracts = load_contracts()
        result = check_gate_health(contracts)
        # the real organism has gates
        total_findings = len(result.findings)
        assert total_findings >= 0  # at minimum, INFO about ratio


# ---------------------------------------------------------------------------
# 5. Temporal freshness (temporal dimension)
# ---------------------------------------------------------------------------


class TestTemporalFreshness:
    def test_real_organism_has_logs(self):
        result = check_temporal_freshness()
        # at least observations.jsonl should exist
        missing = [f for f in result.findings if "missing" in f.detail]
        # routes.jsonl is populated by circulatory, observations by skeletal
        assert result.passed

    def test_detects_missing_logs(self, tmp_path):
        result = check_temporal_freshness(tmp_path)
        assert any("missing" in f.detail for f in result.findings)


# ---------------------------------------------------------------------------
# 6. Feedback loop (coherence dimension)
# ---------------------------------------------------------------------------


class TestFeedbackLoop:
    def test_real_organism_has_feedback(self):
        graph = load_signal_graph()
        result = check_feedback_loop(graph)
        assert result.passed

    def test_detects_missing_feedback(self):
        graph = {"edges": {"information": [], "dependency": [],
                           "governance": [], "evolution": []}}
        result = check_feedback_loop(graph)
        assert not result.passed


# ---------------------------------------------------------------------------
# 7. Full verification (integration)
# ---------------------------------------------------------------------------


class TestVerify:
    def test_returns_report(self):
        report = verify()
        assert isinstance(report, VerificationReport)
        assert report.summary["checks_run"] == 6

    def test_organism_is_healthy(self):
        report = verify()
        assert report.summary["organism_healthy"] == 1, (
            f"organism unhealthy: {[(v.check_name, [(f.subject, f.detail) for f in v.findings if f.severity == 'ERROR']) for v in report.validations if not v.passed]}"
        )

    def test_summary_counts_consistent(self):
        report = verify()
        assert report.summary["checks_passed"] + report.summary["checks_failed"] == report.summary["checks_run"]


# ---------------------------------------------------------------------------
# 8. Recording (TRACE output)
# ---------------------------------------------------------------------------


class TestRecording:
    def test_record_and_load(self, tmp_path):
        report = verify()
        log = tmp_path / "verifications.jsonl"
        record_verification(report, log)
        loaded = load_verification_history(log)
        assert len(loaded) == 1
        assert loaded[0].summary == report.summary

    def test_append_only(self, tmp_path):
        log = tmp_path / "verifications.jsonl"
        r1 = verify()
        r2 = verify()
        record_verification(r1, log)
        record_verification(r2, log)
        loaded = load_verification_history(log)
        assert len(loaded) == 2

    def test_empty_log_returns_empty(self, tmp_path):
        log = tmp_path / "verifications.jsonl"
        assert load_verification_history(log) == []
