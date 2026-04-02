# Plan: cultvra--logos — The Fourth Rendering Language

## Context

The organism speaks three simultaneous languages (Logic/YAML, Math/JSONL, Biology/Python) but has no **Logos** rendering — no natural-language documentation layer that records, critiques, and responds to the technical organs. The `cultvra--logos.md` (currently untracked) is the operator's ontological sketch of this gap.

**Problem**: Every component has code, contracts, and measurements — but no documentation counterpart. The organism cannot describe itself to strangers. No README.md exists. No function generates documentation state. The recording IS the existence proof (pre-historic = un-recorded).

**Intent**: Embody the Logos layer as:
1. A **new mechanism** (`cultvra`) — the 16th mechanism, self-named (no biological analog per Convergence 3)
2. A **gate contract** (`cultvra--logos.yaml`) — formal declaration entering the contract system
3. A **design document** (`cultvra--logos.md`) — remains as the birth document alongside the contract
4. The **third function** (`cultvra_logos.py`) — closes CHECK 19 (CIRCULATION)
5. **Seed documentation** (`README.md`) — bootstrap the documentation the function will maintain

This closes CHECK 19 via the cycle: `skeletal--define →[KNOWLEDGE]→ circulatory--route →[STATE]→ cultvra--logos →[QUERY]→ skeletal--define`.

---

## Step 0: Run existing functions (RELAY directive — do not skip)

```bash
python3 skeletal_define.py
python3 circulatory_route.py
```

Capture current observations and routing state as baseline.

---

## Step 1: Derive the third function (SEED §II Procedure 1)

### Step 1.1 — Signal signature

```
cultvra--logos : {KNOWLEDGE, STATE, TRACE} → {QUERY, TRACE} @ on-demand
```

- **Inputs**: KNOWLEDGE (structure from skeletal), STATE (routing from circulatory), TRACE (temporal observations from either)
- **Outputs**: QUERY (what needs documentation? what changed? → feeds back to skeletal), TRACE (what was documented, when)
- **Temporal mode**: on-demand (operator invokes)

### Step 1.2 — Ontological type

**Capability** — authorized transformation (transforms structure + state into documentation + queries)

### Step 1.3 — Directory?

No. Text output only. Function (file), not product (directory).

### Step 1.4 — Mechanism classification

Does `(input: structural metadata + routing state, output: documentation + queries, mode: on-demand)` match any existing mechanism?

- skeletal: reads structure → NO (cultvra writes about structure, doesn't define it)
- circulatory: routes signals → NO (cultvra narrates, doesn't route)
- nervous: orchestrates/governs → NO (cultvra records/critiques, doesn't command)
- integumentary: presents → CLOSE but distinct (integumentary renders UI; cultvra produces discourse)
- memory: persists → NO (memory stores; cultvra generates meaning from what's stored)

**New mechanism discovered: `cultvra`** — cultural cultivation, discourse, recording. No biological analog. Self-named per Convergence 3: "If the organism discovers a mechanism with no biological analog, it names the mechanism itself."

### Step 1.5 — Name

`cultvra--logos` (mechanism: cultvra, verb: logos/discourse)
Python: `cultvra_logos.py` (GEN-002)

### Step 1.6 — Wiring (signal-graph.yaml updates)

New edges:
```yaml
information:
  # existing
  - from: skeletal--define
    to: circulatory--route
    signal: KNOWLEDGE
    direction: feedfront
    rationale: "the router reads the structure that the skeleton defines"
  # new
  - from: circulatory--route
    to: cultvra--logos
    signal: STATE
    direction: feedfront
    rationale: "the documenter reads the routing state to know what flows and what is broken"
  - from: skeletal--define
    to: cultvra--logos
    signal: KNOWLEDGE
    direction: feedfront
    rationale: "the documenter reads the structure to describe the organism"
  - from: cultvra--logos
    to: skeletal--define
    signal: QUERY
    direction: feedback
    rationale: "documentation gaps become structural queries — what is undocumented? what is stale?"
```

**CHECK 19 cycle**: skeletal →[KNOWLEDGE]→ circulatory →[STATE]→ cultvra →[QUERY]→ skeletal

---

## Step 2: Create gate contract — `cultvra--logos.yaml`

**File**: `cultvra--logos.yaml`

Structure follows existing contract pattern (cf. `skeletal--define.yaml`, `nervous--propose.yaml`):

```yaml
# cultvra--logos.yaml — formation gate contract

identity:
  name: cultvra--logos
  mechanism: cultvra
  verb: logos
  signal_inputs: [KNOWLEDGE, STATE, TRACE]
  signal_outputs: [QUERY, TRACE]

sources:
  - repo: a-organvm
    modules: [signal-graph.yaml, skeletal_define.py, circulatory_route.py, "*.yaml gate contracts"]
    note: "Reads the organism's own structure as source material for documentation"
  - repo: meta-organvm/organvm-corpvs-testamentvm
    modules: [INST-INDEX-RERUM-FACIENDARUM.md]
    note: "Work registry provides context for documentation state"

gate:
  - id: G1
    check: READS_STRUCTURE
    condition: "Function reads signal-graph.yaml and gate contracts to build documentation model"
    status: PENDING
  - id: G2
    check: PRODUCES_DOCUMENTATION_STATE
    condition: "Function outputs docs.jsonl with per-element documentation status (documented/stale/missing)"
    status: PENDING
  - id: G3
    check: EMITS_QUERIES
    condition: "Function produces QUERY signals identifying documentation gaps that feed back to skeletal"
    status: PENDING
  - id: G4
    check: CYCLE_CLOSES
    condition: "CHECK 19 passes — full signal cycle demonstrated end-to-end"
    status: PENDING

dna:
  - "signal-graph.yaml reader — parse functions, edges, signal types into documentation model"
  - "gate contract scanner — parse all *--*.yaml contracts into documentation inventory"
  - "documentation state computer — compare existing .md docs against organism structure"
  - "gap detector — identify undocumented, stale, or missing documentation"
  - "QUERY emitter — output structural queries from documentation gaps"

defect:
  - "No prior documentation function exists — this is the first Logos mechanism function"
  - "No TEACHING or NARRATIVE signal type yet — function may discover new signal types"
  - "cultvra has no biological analog — naming is self-derived, may need refinement"

state: CALLING
```

**Note**: The RELAY says "do not create gate contracts without matching issues." A GitHub issue (IRF-AOR-xxx) should be created for this work. If the operator waives this constraint given the explicit directive, proceed without.

---

## Step 3: Implement `cultvra_logos.py`

**File**: `cultvra_logos.py` (~200-300 lines)

### Architecture (modeled after existing functions)

```python
"""cultvra--logos: the organism documents itself.

GEN-002: canonical '--' maps to '_' in .py filenames.

The cultvra system records, critiques, and narrates the organism's state.
Skeletal reads what EXISTS. Circulatory computes what FLOWS. Cultvra
describes what it all MEANS — documentation as the fourth rendering language.
"""
```

### Data structures

```python
@dataclass
class DocumentationEntry:
    """One element's documentation state."""
    element_name: str           # e.g., "skeletal--define", "QUERY", "skeletal"
    element_type: str           # "function", "signal_type", "mechanism", "gate_contract"
    documented: bool            # has documentation counterpart?
    documentation_path: str     # path to doc if exists, empty if not
    staleness: str              # "current", "stale", "missing"
    last_code_change: str       # file mtime or git date
    last_doc_change: str        # doc mtime if exists

@dataclass
class DocumentationState:
    """Full documentation inventory of the organism."""
    timestamp: str
    entries: list[DocumentationEntry]
    queries: list[dict]         # QUERY signals: documentation gaps
    summary: dict[str, int]     # counts by status
```

### Core logic

1. **Read organism structure** (reuse patterns from `skeletal_define.py`):
   - Parse `signal-graph.yaml` for functions, signal types, edges
   - Scan `*--*.yaml` for gate contracts
   - Derive mechanism list from contracts and signal graph

2. **Scan existing documentation**:
   - Check for README.md, per-element .md files
   - Check docstrings in .py files
   - Check gate contract completeness (all sections present?)

3. **Compute documentation state**:
   - For each element: is it documented? is the doc stale?
   - Generate entries list

4. **Emit QUERY signals**:
   - Missing documentation → QUERY("undocumented: {element}")
   - Stale documentation → QUERY("stale: {element} — code changed since doc")
   - Structural gaps → QUERY("gap: {description}")

5. **Persist output**:
   - Write `docs.jsonl` (temporal artifact, gitignored)
   - Print summary to stdout (like skeletal and circulatory do)

### Key patterns to reuse from existing functions

From `skeletal_define.py`:
- `_read_contracts()` — reads gate contracts (reuse directly or extract)
- `_HERE = Path(__file__).parent` pattern
- YAML loading via `yaml.safe_load()`
- JSONL append pattern for temporal artifacts
- Observation/Variance dataclass pattern

From `circulatory_route.py`:
- Signal graph parsing
- Route/Attraction/Defect pattern → DocumentationEntry/Query pattern
- Summary dict pattern

---

## Step 4: Write seed documentation — `README.md`

**File**: `README.md`

The README is the Logos layer's bootstrap — the organism's face to strangers. Content:

1. **What this is** — computational organism grown from a generative grammar
2. **Quick start** — run the three functions, see what they produce
3. **Architecture** — the three-layer system (BODY/MIND/SEED), three rendering languages + Logos
4. **Current state** — 3 functions, X tests, Y signal types, Z mechanisms
5. **Growth protocol** — pointer to SEED.md §II
6. **File guide** — what each file category is (functions, contracts, wiring, documentation)

This is NOT a duplicate of CLAUDE.md (which is agent-facing navigation). README is human-facing documentation — the stranger's entry point.

---

## Step 5: Write tests — `test_cultvra_logos.py`

**File**: `test_cultvra_logos.py`

Test pattern follows existing test files (hit real data, no mocks):

### Test classes

```
TestDocumentationInventory:
  - test_all_functions_have_entries        # every function in signal-graph has a doc entry
  - test_all_signal_types_have_entries     # every signal type has a doc entry
  - test_all_mechanisms_have_entries       # every mechanism has a doc entry
  - test_entry_staleness_computed          # staleness is not empty for any entry

TestQueryEmission:
  - test_queries_produced_for_gaps         # undocumented elements generate QUERY signals
  - test_query_format                      # each query has element_name + gap_type

TestOutputPersistence:
  - test_docs_jsonl_written                # docs.jsonl is created/appended
  - test_summary_counts                    # summary has documented/stale/missing counts

TestSignalGraphCompliance:
  - test_function_in_signal_graph          # cultvra--logos is declared in signal-graph.yaml
  - test_inputs_declared                   # KNOWLEDGE, STATE, TRACE declared as inputs
  - test_outputs_declared                  # QUERY, TRACE declared as outputs
  - test_cycle_exists                      # information graph has ≥1 cycle (CHECK 6)
  - test_check_19_cycle                    # skeletal → circulatory → cultvra → skeletal demonstrated
```

~15-20 tests, targeting parity with existing test files.

---

## Step 6: Update signal-graph.yaml

Add to `signal_types` if the function discovers a new type during implementation (possible but not prescribed).

Add to `functions`:
```yaml
cultvra--logos:
  inputs: [KNOWLEDGE, STATE, TRACE]
  outputs: [QUERY, TRACE]
  mechanism: cultvra
  temporal_mode: on-demand
  ontological_type: Capability
  traceability:
    upward: "A3 + A7: the organism must persist (A3) and serve the operator (A7) — an organism that cannot describe itself cannot be operated"
    downward: "documentation state inventory (docs.jsonl) + QUERY signals for documentation gaps + README.md as bootstrap artifact"
```

Add new edges (per Step 1.6 above).

---

## Step 7: Update .gitignore

Add `docs.jsonl` to `.gitignore` (temporal artifact, like `observations.jsonl` and `routes.jsonl`).

---

## Step 8: Track cultvra--logos.md

The existing `cultvra--logos.md` (currently untracked) should be `git add`-ed. It is the design document / birth record for the mechanism — it persists alongside the gate contract.

---

## Files to create/modify

| File | Action | Purpose |
|------|--------|---------|
| `cultvra--logos.yaml` | **CREATE** | Gate contract for the third function |
| `cultvra_logos.py` | **CREATE** | Third function — the organism documents itself |
| `test_cultvra_logos.py` | **CREATE** | CHECK 16 verification (~15-20 tests) |
| `README.md` | **CREATE** | Seed documentation — organism's face to strangers |
| `signal-graph.yaml` | **MODIFY** | Add cultvra--logos function + 3 new edges |
| `.gitignore` | **MODIFY** | Add docs.jsonl |
| `cultvra--logos.md` | **TRACK** | git add the existing design document |

---

## Verification

```bash
# 1. Run all three functions
python3 skeletal_define.py
python3 circulatory_route.py
python3 cultvra_logos.py

# 2. Run all tests
python3 -m pytest -v                          # all tests (should be ~65-70)
python3 -m pytest test_cultvra_logos.py -v     # new tests only

# 3. Lint
ruff check .

# 4. Verify CHECKs
# CHECK 1 (FLAT): ls -1 — all files at depth 1
# CHECK 2 (NAMED): cultvra--logos matches {mechanism}--{verb}
# CHECK 3 (SIGNED): cultvra--logos in signal-graph.yaml with inputs/outputs
# CHECK 6 (CYCLIC): information graph has cycle (skeletal → circulatory → cultvra → skeletal)
# CHECK 7 (CONNECTED): all 3 functions have degree_in > 0 and degree_out > 0
# CHECK 15 (TRACEABILITY): upward trace reaches A3+A7, downward reaches docs.jsonl
# CHECK 16 (VERIFIED): tests pass
# CHECK 19 (CIRCULATION): full cycle demonstrated (≥3 functions, cyclic, end-to-end)
```

---

## Constraints honored

- Flat namespace (Theorem 1, CHECK 1) — all new files are siblings at root
- Functions derived from need (SEED §II) — the most acute gap is self-description
- Three rendering languages + Logos — the function produces the fourth language
- No SEED.md modification (sealed until ≥3 functions — but ≥3 functions achieved here, so CHECK 19 cycle assessment unlocks SEED review in NEXT session)
- Gate contract created alongside function (cultvra--logos.yaml)
- Tests hit real data (no mocks for organism structure)
- Alchemical frame: cultvra--logos calcines the organism's raw structure into documented meaning
