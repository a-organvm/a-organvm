# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**a-organvm** — a computational organism grown from a generative grammar (SEED.md). Not a package, not a library. A living system of functions, gate contracts, and signal flows that absorbs capabilities from two predecessor codebases (meta-organvm + organvm-iv-taxis) through a cocoon metamorphosis process.

The organism has a flat filesystem (Theorem 1 in SEED.md) — everything is a sibling at depth 1. No subdirectories for code organization.

## Commands

```bash
# Run tests (all tests are siblings at root — testpaths=["."])
python3 -m pytest -v                              # all 135 tests
python3 -m pytest test_skeletal_define.py -v       # skeletal only (22 tests)
python3 -m pytest test_circulatory_route.py -v     # circulatory only (27 tests)
python3 -m pytest test_cultvra_logos.py -v          # cultvra only (33 tests)
python3 -m pytest test_immune_verify.py -v          # immune only (21 tests)
python3 -m pytest test_respiratory_ingest.py -v     # respiratory only (23 tests)
python3 -m pytest test_signal_propagation.py -v     # signal propagation (9 tests)

# Lint
ruff check .                      # line-length=100, target py311, select E/F/W/I
ruff check --fix .                # auto-fix

# Run the organism's functions (produces temporal artifacts)
python3 skeletal_define.py        # observation → observations.jsonl + scope-*.svg
python3 circulatory_route.py      # routing snapshot → routes.jsonl
python3 cultvra_logos.py           # documentation → docs.jsonl
python3 immune_verify.py           # verification → verifications.jsonl (no CLI output)
python3 respiratory_ingest.py      # ingestion → ingestions.jsonl

# Dependencies
pip install -e ".[dev]"           # pyyaml + pytest + ruff
```

## Architecture

### The Three-Layer System

This repo (THE SEED) sits between two predecessor repos:

| Path | Role | Contents |
|------|------|----------|
| `meta-organvm/` | THE BODY | organvm-engine (37 modules), corpus, schemas, dashboard |
| `organvm-iv-taxis/` | THE MIND | conductor, skills, agents, governance |
| `a-organvm/` (here) | THE SEED | axioms, gate contracts, organism functions |

See TRIPTYCH.md for the full relationship. Code does not copy — it is *called* through gate contracts.

### File Categories

**Functions** (`*.py` without `test_` prefix): The organism's living code. Each function is a biological verb — it reads inputs, produces outputs, and declares its signal signature in signal-graph.yaml.

| Function | Mechanism | What it does |
|----------|-----------|-------------|
| `skeletal_define.py` | skeletal | Reads the organism's own structure: contracts, mechanisms, signal types, gates, phases. Produces observations. |
| `circulatory_route.py` | circulatory | Computes signal flow: routes, attractions (candidate connections), defects (structural gaps). |
| `cultvra_logos.py` | cultvra | Documents the organism: inventories every element, detects gaps, emits QUERY signals for undocumented parts. |
| `immune_verify.py` | immune | Validates integrity: 6 checks across 4 dimensions (structural, temporal, governance, coherence). |
| `respiratory_ingest.py` | respiratory | Absorbs external material: discovers sources, enumerates channels, tracks migrations from cocoon-map. |

**Tests** (`test_*.py`): CHECK 22 verification. Tests run against REAL gate contracts and signal graph — no fixtures or mocks for organism structure.

**Gate contracts** (`*--*.yaml`, 35 files): Declare what each future function will absorb from the BODY/MIND. Format: `identity` (name, mechanism, verb, signals), `sources` (which repos/modules), `gate` (pass conditions), `dna` (what the code contains), `defect` (known issues), `state` (CALLING/PENDING/...).

**Organism wiring** (`signal-graph.yaml`): Declares all functions, their signal types, edges between them, boundary signals, and products. Updated as functions are built.

**Absorption blueprint** (`cocoon-map.yaml`, 16K lines): Maps every module from BODY + MIND to a biological mechanism. States: PLANNED → ERECTED → MOLTING → EMERGED.

**Temporal artifacts** (gitignored): `observations.jsonl`, `routes.jsonl`, `docs.jsonl`, `verifications.jsonl`, `ingestions.jsonl`, `scope-*.svg` — produced by running functions, not source code.

### Naming Convention (GEN-002)

Canonical names use double-hyphen: `skeletal--define`, `circulatory--route`
Python filenames use underscore: `skeletal_define.py`, `circulatory_route.py`
The mapping is 1:1 and bidirectional. The mechanism prefix groups related contracts alphabetically.

Single hyphen separates words within a segment. Double hyphen separates mechanism from verb.

### Signal Graph Model

Functions declare signal inputs/outputs. Nine signal types exist: QUERY, KNOWLEDGE, TRACE, CONTRACT, STATE, REPORT, VALIDATION, SOURCE, MIGRATION. New types are *discovered*, not prescribed — each is named when a function encounters a qualitatively new kind of information.

Edges connect functions via four families: dependency, information, governance, evolution. 10 information edges, 2 governance edges, and 3 feedback loops form the current wiring. The feedback loops are: cultvra→skeletal (QUERY), immune→skeletal (REPORT), respiratory→skeletal (KNOWLEDGE).

### Growth Protocol (SEED §II Procedure 1)

New functions are derived, not designed. The 7-step procedure:
1. Define the signal signature (inputs → outputs @ temporal_mode)
2. Determine function vs product (file vs directory)
3. Classify the mechanism (biological system)
4. Name it ({mechanism}--{verb})
5. Wire it (update signal-graph.yaml with edges)
6. Implement it
7. Verify it (CHECK 16 tests)

## Session Protocol

Read order at session start:
1. `AGENTS.md` — routing table (who does what)
2. `RELAY.md` — last session's output + next session's input
3. `SEED.md` — the genome (procedures, axioms, CHECKs, convergence criteria)
4. `signal-graph.yaml` — current wiring
5. Run all five functions to get current state

## Constraints

- **Flat namespace enforced** — no subdirectories for code. All files are siblings (Theorem 1, CHECK 1).
- **SEED.md seal is lifted** — ≥3 functions exist (5 embodied). SEED.md may now be amended per CHECK 19 cycle.
- **Tests hit real data** — gate contracts and signal graph are the test fixtures. Do not mock organism structure.
- **Functions are derived from need** — never build a function for cycle-closure convenience or architectural symmetry. The most acute capability gap determines the next function (SEED §II).
- **Gate contracts declare state** — do not create gate contracts without matching tracked issues.
- **Temporal artifacts are gitignored** — `observations.jsonl`, `routes.jsonl`, `scope-*.svg` are invocation output.
- **`cocoon-map.yaml` is read-only reference** — it maps the absorption plan. Functions read it; sessions do not edit it casually.
