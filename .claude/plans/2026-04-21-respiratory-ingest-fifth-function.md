# Plan: Fifth Function — respiratory--ingest

## Context

**Repo:** `/Users/4jp/Workspace/organvm/sovereign--ground/holds--same/a-organvm`

The a-organvm computational organism has 4 functions (skeletal--define, circulatory--route, cultvra--logos, immune--verify), 112 tests, 7 signal types, and 7 information edges. RELAY.md (S58b) identifies the fifth function as the next deliverable.

Three candidates were evaluated:
- `nervous--orchestrate`: 1/6 gates PASS → not ready
- `digestive--measure`: 0/4 gates PASS, 21K lines must split → not ready
- **`respiratory--ingest`: 3/3 gates PASS, CONVERGING state, 3,053 lines → ready**

This is the first function that reaches outward — it absorbs external material. The predecessor is `meta-organvm/alchemia-ingestvm` (intake→absorb→alchemize pipeline).

---

## 1. Discover two new signal types

SOURCE and MIGRATION don't exist in signal-graph.yaml yet. Define them:

- **SOURCE**: external material available for ingestion — files, URLs, documents, repo artifacts. Qualitatively distinct from KNOWLEDGE (which is structural metadata about the organism itself). SOURCE is _stuff from outside_.
- **MIGRATION**: a directive describing material movement — what moves, from where, to where, and the migration law that governs it (SEED §II Procedure 4: extractive/methodic/structural/pedagogical/archival).

Add to `signal-graph.yaml` `signal_types:` block.

## 2. Implement `respiratory_ingest.py`

**Pattern:** follows immune_verify.py / skeletal_define.py structure:
- Module docstring explaining the biological metaphor
- `from __future__ import annotations` + dataclasses + yaml + json + pathlib
- `_HERE = Path(__file__).parent`
- Data structures → reading functions → core logic → recording → `__main__`

**Data structures:**
```python
@dataclass
class SourceMaterial:
    """A unit of external material available for ingestion."""
    name: str
    origin: str          # repo, URL, filesystem path
    channel: str         # which alchemia channel (intake, gdocs, bookmarks, etc.)
    state: str           # AVAILABLE, INGESTED, STALE, UNREACHABLE
    size_hint: int       # approximate lines or bytes

@dataclass
class MigrationDirective:
    """A migration law application — what moved and why."""
    subject: str
    migration_type: str  # extractive, methodic, structural, pedagogical, archival
    from_location: str
    to_location: str
    law_ref: str         # SEED §II Procedure 4 reference

@dataclass
class IngestionReport:
    """Complete ingestion state at a moment in time."""
    timestamp: str
    sources: list[SourceMaterial]
    migrations: list[MigrationDirective]
    channels: dict[str, dict]   # channel name → {available, ingested, stale}
    pipeline_phases: dict[str, str]  # intake/absorb/alchemize → status
    summary: dict[str, int]
```

**Core operations (what `ingest()` does):**

1. **Discover sources** — read gate contracts that declare `sources:` sections. Each source entry is a SourceMaterial. Check if the referenced repo/module exists locally.
2. **Enumerate channels** — read the alchemia-ingestvm predecessor's channel structure (intake/, absorb/, alchemize/, channels/). Report channel availability.
3. **Assess pipeline** — for each of the three alchemia phases, determine if the phase is reachable (does the predecessor repo exist? do imports resolve?).
4. **Track migrations** — read cocoon-map.yaml for entries with state transitions (PLANNED→ERECTED→MOLTING→EMERGED). Each transition that consumed a source is a MigrationDirective.
5. **Emit signals** — SOURCE (list of available materials) + KNOWLEDGE (metadata about ingestion state).
6. **Record** — append to `ingestions.jsonl` (gitignored temporal artifact).

**Key files to read during implementation:**
- `respiratory--ingest.yaml` — gate contract (sources, dna, defects)
- `cocoon-map.yaml` — absorption blueprint (phase states)
- All `*--*.yaml` gate contracts (each has a `sources:` section)
- `signal-graph.yaml` — for structural context

**NOT copying code from alchemia-ingestvm.** The function reads the predecessor's structure through gate contracts and assesses ingestion readiness. It calls through gates, not inheritance.

## 3. Wire edges in `signal-graph.yaml`

New edges in `edges.information`:

| From | To | Signal | Direction | Rationale |
|------|----|--------|-----------|-----------|
| skeletal--define | respiratory--ingest | KNOWLEDGE | feedfront | ingestor reads organism structure to know what to ingest |
| respiratory--ingest | circulatory--route | SOURCE | feedfront | ingested material flows to routing for distribution |
| respiratory--ingest | skeletal--define | KNOWLEDGE | feedback | ingestion discoveries become structural knowledge (third feedback loop) |

New entry in `functions:` for respiratory--ingest.

New entries in `boundary_signals:` — SOURCE from external world (files, repos, URLs).

## 4. Write `test_respiratory_ingest.py`

Follow test_immune_verify.py pattern (CHECK 21 → ~20-25 tests):

**Test classes:**
1. `TestSourceDiscovery` (4-5 tests)
   - discovers sources from real gate contracts
   - handles missing repos gracefully
   - counts available vs unreachable
   - detects new sources in contracts

2. `TestChannelEnumeration` (3-4 tests)
   - enumerates alchemia channels
   - handles missing predecessor gracefully
   - reports channel state

3. `TestPipelineAssessment` (3-4 tests)
   - assesses three-phase pipeline
   - reports phase reachability
   - detects stale pipeline state

4. `TestMigrationTracking` (3-4 tests)
   - reads cocoon-map transitions
   - classifies migration types (extractive/methodic/etc.)
   - tracks migration history

5. `TestIngestionIntegration` (3-4 tests)
   - full ingest() call against real data
   - produces SourceMaterial and MigrationDirective
   - records to ingestions.jsonl
   - emits correct signal types

6. `TestRecording` (2-3 tests)
   - append/load cycle for ingestions.jsonl
   - handles empty log

Tests run against REAL organism state (no mocks).

## 5. Fill governance edges (secondary)

`signal-graph.yaml` `edges.governance` is empty. immune--verify naturally provides governance:

```yaml
governance:
  - from: immune--verify
    to: skeletal--define
    signal: VALIDATION
    rationale: "verification pass/fail governs structural reads"
  - from: immune--verify
    to: circulatory--route
    signal: VALIDATION
    rationale: "verification governs routing computation"
```

`edges.evolution` remains empty — no evolution events have occurred yet (no function has been replaced or dissolved).

## 6. Update respiratory--ingest.yaml gate contract state

Change `state: CALLING` → `state: EMERGED` (or appropriate next state per cocoon lifecycle).

## 7. Update RELAY.md

Session handoff: document what was built, organism vitals at close, next steps.

---

## Verification

1. `python3 -m pytest -v` — all tests pass (target: ~135 total = 112 existing + ~23 new)
2. `ruff check .` — no lint errors
3. `python3 respiratory_ingest.py` — runs successfully, produces ingestions.jsonl
4. `python3 immune_verify.py` — organism still HEALTHY (6/6 checks pass) with the new function wired
5. `python3 skeletal_define.py` — new mechanism (respiratory) appears in observation
6. Signal graph consistency: new function's signals have both emitters and receivers

---

## Files to modify

| File | Action |
|------|--------|
| `respiratory_ingest.py` | **CREATE** — fifth function |
| `test_respiratory_ingest.py` | **CREATE** — verification tests |
| `signal-graph.yaml` | **EDIT** — add function, signal types, edges, boundary signals |
| `respiratory--ingest.yaml` | **EDIT** — update state field |
| `RELAY.md` | **EDIT** — session handoff |

## Files to read (reference only)

| File | Why |
|------|-----|
| `immune_verify.py` | Implementation pattern (most recent function) |
| `skeletal_define.py` | Implementation pattern + reading functions |
| `cultvra_logos.py` | Implementation pattern |
| `cocoon-map.yaml` | Absorption blueprint for migration tracking |
| `respiratory--ingest.yaml` | Gate contract (sources, DNA, defects) |
| `SEED.md` | Growth procedure (§II Procedure 1, step 5-7) |
