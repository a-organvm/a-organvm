"""CHECK 22 — functional verification for respiratory--ingest.

The respiratory system absorbs external material.
Tests run against the REAL organism state.
"""

from respiratory_ingest import (
    IngestionReport,
    discover_sources,
    enumerate_channels,
    ingest,
    load_ingestion_history,
    record_ingestion,
    track_migrations,
)

# ---------------------------------------------------------------------------
# 1. Source discovery
# ---------------------------------------------------------------------------


class TestSourceDiscovery:
    def test_discovers_sources_from_real_contracts(self):
        sources = discover_sources()
        assert len(sources) > 0, "no sources found in gate contracts"

    def test_every_source_has_origin(self):
        sources = discover_sources()
        for s in sources:
            assert s.origin, f"source {s.name} has no origin"

    def test_every_source_has_channel(self):
        sources = discover_sources()
        for s in sources:
            assert s.channel, f"source {s.name} has no channel"
            assert "--" in s.channel, f"channel {s.channel} not a gate contract name"

    def test_state_is_valid(self):
        sources = discover_sources()
        valid_states = {"AVAILABLE", "UNREACHABLE", "ABSORBED"}
        for s in sources:
            assert s.state in valid_states, f"source {s.name} has invalid state: {s.state}"

    def test_respiratory_ingest_contract_sources_absorbed(self):
        """The respiratory--ingest gate contract has all gates PASS → its sources are ABSORBED."""
        sources = discover_sources()
        resp_sources = [s for s in sources if s.channel == "respiratory--ingest"]
        assert len(resp_sources) > 0, "no sources found for respiratory--ingest"
        for s in resp_sources:
            assert s.state == "ABSORBED", (
                f"respiratory--ingest source {s.name} should be ABSORBED "
                f"(all gates PASS) but is {s.state}"
            )


# ---------------------------------------------------------------------------
# 2. Channel enumeration
# ---------------------------------------------------------------------------


class TestChannelEnumeration:
    def test_enumerates_four_phases(self):
        channels = enumerate_channels()
        assert len(channels) == 4
        names = {c.name for c in channels}
        assert names == {"intake", "absorb", "alchemize", "channels"}

    def test_channel_state_type(self):
        channels = enumerate_channels()
        for c in channels:
            assert isinstance(c.reachable, bool)
            assert isinstance(c.name, str)

    def test_reachable_channels_have_path(self):
        channels = enumerate_channels()
        for c in channels:
            if c.reachable:
                assert c.path, f"reachable channel {c.name} has no path"

    def test_handles_missing_predecessor(self):
        """With no contracts, all channels report unreachable."""
        channels = enumerate_channels(contracts=[])
        for c in channels:
            assert not c.reachable


# ---------------------------------------------------------------------------
# 3. Pipeline assessment (via source + channel integration)
# ---------------------------------------------------------------------------


class TestPipelineAssessment:
    def test_sources_cover_multiple_contracts(self):
        """Sources should come from more than one gate contract."""
        sources = discover_sources()
        channels = {s.channel for s in sources}
        assert len(channels) > 1, "sources come from only one contract"

    def test_total_lines_is_positive(self):
        """Gate contracts declare non-zero line counts."""
        sources = discover_sources()
        total = sum(s.size_hint for s in sources)
        assert total > 0, "no lines declared across all sources"

    def test_at_least_one_available_source(self):
        """At least one source should be locally available."""
        sources = discover_sources()
        available = [s for s in sources if s.state in ("AVAILABLE", "ABSORBED")]
        assert len(available) > 0, "no sources are locally available"


# ---------------------------------------------------------------------------
# 4. Migration tracking
# ---------------------------------------------------------------------------


class TestMigrationTracking:
    def test_tracks_migrations_from_cocoon_map(self):
        migrations = track_migrations()
        assert len(migrations) > 0, "no migrations found in cocoon-map"

    def test_migration_has_required_fields(self):
        migrations = track_migrations()
        for m in migrations:
            assert m.subject, "migration has no subject"
            assert m.migration_type, "migration has no type"
            assert m.from_location, "migration has no from_location"

    def test_migration_types_are_cocoon_states(self):
        valid_states = {"PLANNED", "ERECTED", "MOLTING", "EMERGED", "UNKNOWN"}
        migrations = track_migrations()
        for m in migrations:
            assert m.migration_type in valid_states, (
                f"migration {m.subject} has unexpected type: {m.migration_type}"
            )

    def test_respiratory_ingest_migration_exists(self):
        """The cocoon-map should have an entry for respiratory--ingest."""
        migrations = track_migrations()
        resp = [m for m in migrations if m.subject == "respiratory--ingest"]
        assert len(resp) > 0, "no migration for respiratory--ingest in cocoon-map"


# ---------------------------------------------------------------------------
# 5. Full ingestion integration
# ---------------------------------------------------------------------------


class TestIngestionIntegration:
    def test_ingest_returns_report(self):
        report = ingest()
        assert isinstance(report, IngestionReport)
        assert report.timestamp
        assert isinstance(report.sources, list)
        assert isinstance(report.migrations, list)
        assert isinstance(report.channels, list)

    def test_report_summary_keys(self):
        report = ingest()
        expected_keys = {
            "total_sources", "available", "unreachable", "absorbed",
            "total_lines_declared", "channels_reachable", "channels_total",
            "migrations_tracked",
        }
        assert expected_keys <= set(report.summary.keys())

    def test_summary_counts_are_consistent(self):
        report = ingest()
        s = report.summary
        assert s["total_sources"] == s["available"] + s["unreachable"] + s["absorbed"]
        assert s["channels_total"] == len(report.channels)
        assert s["migrations_tracked"] == len(report.migrations)

    def test_signal_types_present(self):
        """The function should produce SOURCE and KNOWLEDGE signals.

        SOURCE is represented by the sources list.
        KNOWLEDGE is represented by the summary and channel metadata.
        """
        report = ingest()
        assert len(report.sources) > 0, "no SOURCE signals emitted"
        assert report.summary, "no KNOWLEDGE signal (summary) emitted"


# ---------------------------------------------------------------------------
# 6. Recording
# ---------------------------------------------------------------------------


class TestRecording:
    def test_record_and_load_cycle(self, tmp_path):
        report = ingest()
        log = tmp_path / "ingestions.jsonl"
        record_ingestion(report, path=log)
        assert log.is_file()

        history = load_ingestion_history(path=log)
        assert len(history) == 1
        assert history[0].timestamp == report.timestamp
        assert len(history[0].sources) == len(report.sources)

    def test_append_multiple(self, tmp_path):
        log = tmp_path / "ingestions.jsonl"
        r1 = ingest()
        record_ingestion(r1, path=log)
        r2 = ingest()
        record_ingestion(r2, path=log)

        history = load_ingestion_history(path=log)
        assert len(history) == 2

    def test_load_empty_returns_empty(self, tmp_path):
        log = tmp_path / "ingestions.jsonl"
        assert load_ingestion_history(path=log) == []
