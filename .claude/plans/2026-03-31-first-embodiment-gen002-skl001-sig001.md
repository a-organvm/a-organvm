# Plan: First Embodiment — GEN-002 → SKL-001 → SIG-001

## Context

The a-organvm organism at `/Users/4jp/Workspace/a-organvm/` has 35 YAML gate contracts, a 1,208-line genome (SEED.md), and zero code. S43 produced extensive specification; S44's death cantation imposed a throttle: **embody, don't expand**. No new law, issues, contracts, or checks until the organism has a body.

The critical path is three decisions/acts in strict sequence:
1. **GEN-002** — decide how flat `.py` files import each other
2. **SKL-001** — write the first function, prove it works (CHECK 16)
3. **SIG-001** — create signal-graph.yaml with its first entry

**Temporal mandate:** The organism's first act includes temporal self-awareness. Not just "what am I?" but "how am I changing?" Track and record: input signals, output signals, phase and elemental form variance, shape of change and decay through time.

This plan produces 4 new files and zero modifications to existing files.

---

## Step 1: GEN-002 — The Packaging Spine Decision

**Decision:** Single underscore mapping.

| Layer | Convention | Example |
|-------|-----------|---------|
| Canonical (YAML, signal graph, docs) | `mechanism--verb` | `skeletal--define` |
| Python filename | `mechanism_verb.py` | `skeletal_define.py` |
| Python import | `import mechanism_verb` | `import skeletal_define` |
| Test filename | `test_mechanism_verb.py` | `test_skeletal_define.py` |

**Why single underscore, not double:**
- All mechanisms and verbs are single words — no ambiguity in parsing
- `__` has dunder connotations in Python (cognitive noise)
- Single underscore is standard Python module naming

**Why no __init__.py, no package, no sys.path manipulation:**
- SEED Theorem 1 mandates D=1 (flat namespace)
- pytest adds rootdir to `sys.path` by default — `import skeletal_define` resolves immediately
- No packaging ceremony for a non-distributable organism instance

**Why not importlib:**
- Violates A5 (minimality) — every import becomes ceremony
- IDE autocomplete breaks
- The execution substrate (Python) has its own naming conventions; forcing `--` into Python is structural waste

This rule is documented once: in the first `.py` file's module docstring and as a note in `signal-graph.yaml`.

---

## Step 2: SKL-001 — The First Function (with Temporal Awareness)

**File:** `/Users/4jp/Workspace/a-organvm/skeletal_define.py`

Following SEED Procedure 1, Steps 1-7:

### SEED Step 1 — Signal signature
```
skeletal--define : QUERY → (KNOWLEDGE, TRACE) @ on-demand
```

The function reads the organism's own YAML gate contracts (siblings in the flat directory) and returns structured metadata **including temporal observations**. This is the organism's first act of self-perception AND temporal self-awareness.

**Why TRACE as an output signal:** TRACE is the organism's most demanded signal — consumed by **10 of 15 cocoons** (nervous, circulatory, digestive, endocrine, immune, muscular ×2, memory, orchestrate, smith). By producing TRACE from the first function, the organism immediately wires into the widest consumption base. TRACE records "what happened, what changed, what was observed."

**Why mechanism-resolution, not organ-resolution:** The old `organ_config.py` maps Roman numeral organs (I-VII) — the predecessor's categories. The new organism thinks in mechanisms (skeletal, nervous, circulatory). The first function serves the NEW organism's self-knowledge.

### SEED Step 1a — Ontological type
**Capability.** Classification procedure first-match: "Does it authorize a transformation from input to output?" Yes — it transforms a query (mechanism key) into structured knowledge (metadata dict) and a temporal trace (observation snapshot).

### SEED Step 2 — Needs a directory?
**No.** Logic only, no assets. It is a function (file).

### SEED Step 3 — Mechanism
**skeletal.** Characteristic tuple: (QUERY input, KNOWLEDGE + TRACE output, on-demand). Matches the skeletal mechanism from cocoon-map.yaml: "structure, identity, definition."

### SEED Step 4 — Name
Canonical: `skeletal--define`. Python: `skeletal_define.py`.

### SEED Step 6 — Traceability
- **Upward:** "The organism has no way to read its own structure OR observe how that structure changes over time. No existing function resolves mechanism identity, tracks signal inventory, or detects phase/form variance. (A1 + A3 + A4: work requires self-knowledge; persistence requires temporal memory; adaptation requires change detection.)"
- **Downward:** "Produces (1) mechanism metadata dicts (KNOWLEDGE), (2) timestamped observation snapshots (TRACE) persisted to `observations.jsonl`, (3) variance reports comparing current to previous state."

### SEED Step 7 — Evaluation
| Dimension | Assessment |
|-----------|-----------|
| Ontological Legibility | Clear — takes a key or no args, returns metadata + temporal trace |
| Signal Utility | KNOWLEDGE consumed by 5+ cocoons; TRACE consumed by 10 cocoons |
| Boundary Discipline | Reads only YAML siblings + observations.jsonl in the same directory |
| Modulation Safety | Pure reads + append-only writes to observations.jsonl |
| Yield | Produces reusable structural data + temporal log |
| Migration Worthiness | Not yet — too early. Serves G2 (CANONICAL_ORGAN_MAP) in skeletal--define.yaml |

### Implementation — Five capabilities in one file

#### 1. Structure reading (KNOWLEDGE output)
- `resolve_mechanism(key)` → first gate contract for a mechanism
- `list_mechanisms()` → all mechanism names from gate contracts
- `resolve_contract(canonical_name)` → specific contract by canonical name

#### 2. Signal inventory (KNOWLEDGE output)
- `signal_inventory()` → all signal types with their producers and consumers, derived from gate contracts' `signal_inputs` and `signal_outputs` fields
- Returns: `dict[str, {"produced_by": list[str], "consumed_by": list[str]}]`
- This is the organism reading its own signal vocabulary

#### 3. Phase tracking (TRACE output)
- `observe()` → produces a timestamped `Observation` capturing:
  - `timestamp`: ISO 8601
  - `mechanisms`: dict of mechanism → list of (canonical_name, state, verb)
  - `signal_types`: the signal inventory (which types exist, who produces/consumes)
  - `gates`: dict of contract → list of (gate_id, check, status)
  - `phases`: dict of cocoon → phase state (from cocoon-map.yaml: PLANNED/ERECTED/MOLTING/EMERGED)
  - `summary`: counts — total_mechanisms, total_contracts, total_gates, gates_pending, gates_passed

#### 4. Temporal recording (TRACE persistence per A3 + Law 3)
- `record_observation(obs)` → appends observation as one JSON line to `observations.jsonl`
- `load_observations()` → reads all recorded observations from `observations.jsonl`
- Append-only. No overwrites. The temporal log is the organism's fossil record of its own structure.

#### 5. Variance detection (TRACE analysis — shape of change and decay)
- `detect_variance(current, previous)` → returns a `Variance` dict:
  - `new_mechanisms`: mechanisms present now but not before
  - `removed_mechanisms`: mechanisms present before but not now
  - `gate_transitions`: list of (contract, gate_id, old_status → new_status)
  - `phase_transitions`: list of (cocoon, old_phase → new_phase)
  - `signal_changes`: new/removed signal types
  - `stasis`: mechanisms/gates that have NOT changed (potential decay)
  - `elapsed`: timedelta between observations

**Decay detection heuristic:** A gate in PENDING across two or more observations with no other gate transitions in its contract = stasis (the cocoon is not progressing). A cocoon stuck in PLANNED while siblings advance = falling behind. These are surfaced as TRACE-type observations, not governance judgments — the operator decides what to do.

### Data model (Python dataclasses)

```python
@dataclass
class Observation:
    timestamp: str                     # ISO 8601
    mechanisms: dict[str, list[dict]]  # mechanism → [{name, state, verb}]
    signal_types: dict[str, dict]      # type → {produced_by, consumed_by}
    gates: dict[str, list[dict]]       # contract → [{id, check, status}]
    phases: dict[str, str]             # cocoon → phase state
    summary: dict[str, int]            # counts

@dataclass
class Variance:
    new_mechanisms: list[str]
    removed_mechanisms: list[str]
    gate_transitions: list[dict]       # {contract, gate, old, new}
    phase_transitions: list[dict]      # {cocoon, old, new}
    signal_changes: dict[str, list]    # {added: [], removed: []}
    stasis: list[str]                  # contracts with no movement
    elapsed: str                       # human-readable timedelta
```

### Dependency
PyYAML (`pyyaml>=6.0`) — declared in pyproject.toml and as a boundary signal in signal-graph.yaml per SEED §II Step 5f.

### Critical source files for reference
- `/Users/4jp/Workspace/a-organvm/skeletal--define.yaml` — gate contract (structure to read)
- `/Users/4jp/Workspace/a-organvm/cocoon-map.yaml` — mechanism inventory with phase states (35 entries)
- `/Users/4jp/Workspace/a-organvm/SEED.md` lines 112-408 (Procedure 1), 640-646 (A9 lineage), 714-723 (modulation tracking), 752-766 (Law 6 meta-evolution strata)

---

## Step 3: SIG-001 — The Signal Graph

**File:** `/Users/4jp/Workspace/a-organvm/signal-graph.yaml`

Following the exact schema from SEED lines 270-301. Contains:

### Signal types (3, bootstrapped by the first function)
```yaml
signal_types:
  QUERY:
    description: "a request for specific structural information"
    discovered_by: skeletal--define
  KNOWLEDGE:
    description: "structured metadata about the organism's composition"
    discovered_by: skeletal--define
  TRACE:
    description: "temporal observation recording what was found, what changed, what decayed"
    discovered_by: skeletal--define
```

### Function entry
```yaml
functions:
  skeletal--define:
    inputs: [QUERY]
    outputs: [KNOWLEDGE, TRACE]
    mechanism: skeletal
    temporal_mode: on-demand
    ontological_type: Capability
    traceability:
      upward: "A1 + A3 + A4: the organism has no way to read its own structure or observe its change over time"
      downward: "mechanism metadata dicts (KNOWLEDGE) + timestamped observation snapshots (TRACE) persisted to observations.jsonl"
```

### Edges (empty — first function, no connections yet)
### Boundary signals (per Step 5f)
```yaml
boundary_signals:
  - name: pyyaml
    type: EXTERNAL
    source: "PyPI: pyyaml"
    direction: inbound
    consumed_by: skeletal--define
```

### GEN-002 note
```yaml
# Python naming convention (GEN-002): canonical '--' maps to '_' in .py filenames
# skeletal--define → skeletal_define.py
```

Created WITH the first function (same commit), per SEED line 267-268.

---

## Step 4: CHECK 16 — The Test

**File:** `/Users/4jp/Workspace/a-organvm/test_skeletal_define.py`

Tests run against the REAL gate contracts in the organism directory (not fixtures). The function's job IS to read the organism's own structure.

### Structure tests (KNOWLEDGE output)
1. `resolve_mechanism("skeletal")` returns dict with `identity` key, mechanism="skeletal"
2. `resolve_mechanism("nonexistent")` returns None
3. `list_mechanisms()` includes "skeletal", returns sorted list
4. `list_mechanisms()` discovers ≥5 unique mechanisms (35 contracts, ~15 mechanisms)
5. `resolve_contract("skeletal--define")` returns the skeletal gate contract
6. `resolve_contract("nonexistent--function")` returns None

### Signal inventory tests (KNOWLEDGE output)
7. `signal_inventory()` returns dict with known types (TRACE, KNOWLEDGE, STATE, etc.)
8. `signal_inventory()["TRACE"]["consumed_by"]` includes "nervous--govern"
9. Every signal type has at least one producer OR one consumer

### Observation tests (TRACE output)
10. `observe()` returns Observation with timestamp and non-empty mechanisms
11. `observe().summary["total_mechanisms"]` >= 5
12. `observe().gates` contains entries with PENDING status
13. `observe().phases` contains cocoon states from cocoon-map.yaml

### Temporal recording tests (TRACE persistence)
14. `record_observation(obs)` appends to `observations.jsonl` (uses tmp_path fixture)
15. `load_observations()` returns list matching what was recorded
16. Two consecutive observations → `detect_variance()` returns valid Variance

### Variance detection tests
17. Identical observations → stasis list is non-empty, no transitions
18. Observations with a gate status change → `gate_transitions` captures it

---

## Step 5: Infrastructure

**File:** `/Users/4jp/Workspace/a-organvm/pyproject.toml`

Minimal tool configuration (not packaging). Declares:
- `requires-python = ">=3.11"`
- `dependencies = ["pyyaml>=6.0"]`
- `[project.optional-dependencies] dev = ["pytest>=8.0", "ruff>=0.4"]`
- `[tool.pytest.ini_options] testpaths = ["."]`
- `[tool.ruff]` line-length=100, py311

This satisfies CHECK 17 (execution substrate declaration).

---

## Execution Sequence

All 4 files in one atomic commit:

1. Create `pyproject.toml` (infrastructure)
2. Create `skeletal_define.py` (the function — SKL-001, with all 5 capabilities)
3. Create `signal-graph.yaml` (the wiring — SIG-001)
4. Create `test_skeletal_define.py` (the verification — CHECK 16)
5. Install: `pip install pyyaml pytest` (or `pip install -e ".[dev]"`)
6. Run: `cd /Users/4jp/Workspace/a-organvm && pytest test_skeletal_define.py -v`
7. Run first observation: `python3 -c "from skeletal_define import observe, record_observation; record_observation(observe())"`
8. Verify 6 applicable CHECKs:
   - CHECK 1 (FLAT): all files are siblings ✓
   - CHECK 2 (NAMED): canonical name follows `{mechanism}--{verb}` ✓
   - CHECK 3 (SIGNED): signal-graph.yaml contains the function with KNOWLEDGE + TRACE outputs ✓
   - CHECK 11 (GENOME): SEED.md unchanged ✓
   - CHECK 16 (VERIFIED): all 18 pytest cases pass ✓
   - CHECK 17 (EXECUTION): pyproject.toml declares substrate ✓

---

## What This Does NOT Do

- Does not modify SEED.md (sealed)
- Does not create new gate contracts or issues
- Does not copy code from the old engine (this is a new function)
- Does not add `__init__.py` or any package structure
- Does not touch any repo outside `a-organvm/`
- Does not write `observations.jsonl` to the repo — the temporal log is an artifact of invocation, not a tracked file (add to .gitignore)

---

## Verification

After implementation, run from `/Users/4jp/Workspace/a-organvm/`:

```bash
# CHECK 16 — the bulb (all 18 tests)
pytest test_skeletal_define.py -v

# CHECK 1 — flatness (visual)
ls *.py *.yaml *.md *.toml

# CHECK 3 — signal graph has the function with both output types
python3 -c "
import yaml
g = yaml.safe_load(open('signal-graph.yaml'))
f = g['functions']['skeletal--define']
print('outputs:', f['outputs'])
assert 'KNOWLEDGE' in f['outputs']
assert 'TRACE' in f['outputs']
print('CHECK 3: PASS')
"

# First observation — the organism perceives itself for the first time
python3 -c "
from skeletal_define import observe, record_observation
obs = observe()
print(f'Mechanisms: {obs.summary[\"total_mechanisms\"]}')
print(f'Contracts: {obs.summary[\"total_contracts\"]}')
print(f'Gates pending: {obs.summary[\"gates_pending\"]}')
print(f'Signal types: {len(obs.signal_types)}')
record_observation(obs)
print('First observation recorded.')
"
```

---

## Files Created (summary)

| File | Purpose | Satisfies |
|------|---------|-----------|
| `pyproject.toml` | Tool config, dependency declaration | CHECK 17, GEN-002 |
| `skeletal_define.py` | First function — structure + signals + observation + recording + variance | SKL-001, CHECK 16 |
| `signal-graph.yaml` | Organism's wiring diagram with KNOWLEDGE + TRACE outputs | SIG-001, CHECK 3 |
| `test_skeletal_define.py` | 18 test cases covering all 5 capabilities | CHECK 16 |

**Also appended to `.gitignore`:** `observations.jsonl` (temporal artifact, not source)
