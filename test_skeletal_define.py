"""CHECK 16 — functional verification for skeletal--define.

At least one verifiable example per capability:
given this input, it produces this output.

Tests run against the REAL gate contracts in the organism directory.
The function's job IS to read the organism's own structure.
"""

from __future__ import annotations

import copy
from pathlib import Path

from skeletal_define import (
    Observation,
    Variance,
    detect_variance,
    list_mechanisms,
    load_observations,
    observe,
    record_observation,
    render,
    render_variance,
    resolve_contract,
    resolve_mechanism,
    signal_inventory,
)


# ---------------------------------------------------------------------------
# 1. Structure reading (KNOWLEDGE)
# ---------------------------------------------------------------------------


class TestResolveMechanism:
    def test_skeletal_returns_contract(self):
        result = resolve_mechanism("skeletal")
        assert result is not None
        assert "identity" in result
        assert result["identity"]["mechanism"] == "skeletal"

    def test_unknown_mechanism_returns_none(self):
        result = resolve_mechanism("nonexistent")
        assert result is None


class TestListMechanisms:
    def test_includes_skeletal(self):
        mechs = list_mechanisms()
        assert "skeletal" in mechs
        assert isinstance(mechs, list)
        assert mechs == sorted(mechs)

    def test_discovers_multiple(self):
        mechs = list_mechanisms()
        # 35 gate contracts across ~15 unique mechanisms
        assert len(mechs) >= 5


class TestResolveContract:
    def test_by_canonical_name(self):
        result = resolve_contract("skeletal--define")
        assert result is not None
        assert result["identity"]["name"] == "skeletal--define"
        assert result["identity"]["verb"] == "define"

    def test_missing_returns_none(self):
        result = resolve_contract("nonexistent--function")
        assert result is None


# ---------------------------------------------------------------------------
# 2. Signal inventory (KNOWLEDGE)
# ---------------------------------------------------------------------------


class TestSignalInventory:
    def test_returns_known_types(self):
        inv = signal_inventory()
        # TRACE, KNOWLEDGE, STATE are used across many cocoons
        assert "TRACE" in inv
        assert "STATE" in inv

    def test_trace_consumed_by_nervous_govern(self):
        inv = signal_inventory()
        assert "nervous--govern" in inv["TRACE"]["consumed_by"]

    def test_every_type_has_participants(self):
        inv = signal_inventory()
        for sig_type, edges in inv.items():
            has_producer = len(edges["produced_by"]) > 0
            has_consumer = len(edges["consumed_by"]) > 0
            assert has_producer or has_consumer, (
                f"Signal type {sig_type} has no producers or consumers"
            )


# ---------------------------------------------------------------------------
# 3. Observation (TRACE)
# ---------------------------------------------------------------------------


class TestObserve:
    def test_returns_observation_with_timestamp(self):
        obs = observe()
        assert isinstance(obs, Observation)
        assert obs.timestamp  # non-empty ISO 8601

    def test_mechanisms_discovered(self):
        obs = observe()
        assert obs.summary["total_mechanisms"] >= 5

    def test_gates_have_pending_status(self):
        obs = observe()
        has_pending = any(
            gate["status"] == "PENDING"
            for contract_gates in obs.gates.values()
            for gate in contract_gates
        )
        assert has_pending, "Expected at least one PENDING gate"

    def test_phases_from_cocoon_map(self):
        obs = observe()
        assert len(obs.phases) > 0
        # cocoon-map.yaml declares PLANNED as the initial state
        assert "PLANNED" in obs.phases.values()


# ---------------------------------------------------------------------------
# 4. Temporal recording (TRACE persistence)
# ---------------------------------------------------------------------------


class TestTemporalRecording:
    def test_record_and_load(self, tmp_path: Path):
        log = tmp_path / "observations.jsonl"
        obs = observe()
        record_observation(obs, path=log)
        loaded = load_observations(path=log)
        assert len(loaded) == 1
        assert loaded[0].timestamp == obs.timestamp

    def test_append_only(self, tmp_path: Path):
        log = tmp_path / "observations.jsonl"
        obs1 = observe()
        obs2 = observe()
        record_observation(obs1, path=log)
        record_observation(obs2, path=log)
        loaded = load_observations(path=log)
        assert len(loaded) == 2

    def test_empty_log_returns_empty_list(self, tmp_path: Path):
        log = tmp_path / "observations.jsonl"
        loaded = load_observations(path=log)
        assert loaded == []


# ---------------------------------------------------------------------------
# 5. Variance detection (TRACE analysis — shape of change and decay)
# ---------------------------------------------------------------------------


class TestVarianceDetection:
    def test_identical_observations_show_stasis(self):
        obs = observe()
        variance = detect_variance(obs, obs)
        assert isinstance(variance, Variance)
        assert variance.new_mechanisms == []
        assert variance.removed_mechanisms == []
        assert variance.gate_transitions == []
        assert variance.phase_transitions == []
        # Stasis: all contracts appear unchanged
        assert len(variance.stasis) > 0

    def test_gate_status_change_detected(self):
        obs1 = observe()
        obs2 = copy.deepcopy(obs1)
        # Find any gate and flip its status to a synthetic value
        target_contract = None
        original_status = None
        for contract, gates in obs2.gates.items():
            if gates:
                target_contract = contract
                original_status = gates[0]["status"]
                gates[0]["status"] = "SYNTHETIC_TEST_VALUE"
                break
        assert target_contract is not None, "Expected at least one contract with gates"

        variance = detect_variance(obs2, obs1)
        assert len(variance.gate_transitions) >= 1
        transition = variance.gate_transitions[0]
        assert transition["contract"] == target_contract
        assert transition["old"] == original_status
        assert transition["new"] == "SYNTHETIC_TEST_VALUE"


# ---------------------------------------------------------------------------
# Instrument: topology scope
# ---------------------------------------------------------------------------


class TestRender:
    def test_produces_valid_svg(self):
        obs = observe()
        svg = render(obs)
        assert svg.startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_deterministic(self):
        obs = observe()
        assert render(obs) == render(obs)

    def test_contains_mechanism_labels(self):
        obs = observe()
        svg = render(obs)
        assert "skeletal" in svg
        assert "nervous" in svg

    def test_variance_scope_produces_svg(self):
        obs = observe()
        svg = render_variance(obs, obs)
        assert svg.startswith("<svg")
        assert "still" in svg  # stasis class appears
