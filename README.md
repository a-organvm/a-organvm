# a-organvm

A computational organism grown from a generative grammar.

Not a package. Not a library. A living system of functions, gate contracts,
and signal flows that reads its own structure, computes its own routing,
and documents its own state.

## Quick Start

```bash
pip install -e ".[dev]"

# Run the three organism functions
python3 skeletal_define.py      # reads structure → observations.jsonl
python3 circulatory_route.py    # computes routing → routes.jsonl
python3 cultvra_logos.py        # documents state → docs.jsonl

# Run all tests
python3 -m pytest -v            # 82 tests across 3 functions
```

## The Three Functions

| Function | Mechanism | Signal | What it does |
|----------|-----------|--------|-------------|
| `skeletal_define.py` | skeletal | QUERY → KNOWLEDGE, TRACE | Reads the organism's structure: contracts, mechanisms, signal types, gates |
| `circulatory_route.py` | circulatory | CONTRACT, STATE, TRACE → TRACE, CONTRACT, STATE | Computes signal flow: routes, attractions, defects |
| `cultvra_logos.py` | cultvra | KNOWLEDGE, STATE, TRACE → QUERY, TRACE | Documents the organism: inventory, coverage, documentation gaps |

These form a cycle: skeletal reads structure, circulatory routes it,
cultvra documents it, and the documentation gaps feed back as queries
to skeletal.

## Four Rendering Languages

The organism speaks four simultaneous languages about the same reality:

| Language | Format | What it renders |
|----------|--------|----------------|
| Logic | YAML (gate contracts) | Qualification proofs — pass/fail conditions |
| Math | JSONL (temporal artifacts) | Numerical evidence — counts, measurements, deltas |
| Biology | Python (functions) | Algorithmic embodiment — living computation |
| Logos | Markdown (documentation) | Natural-language discourse — meaning and context |

## File Categories

| Pattern | What it is |
|---------|-----------|
| `*.py` (no `test_` prefix) | Organism functions — living code |
| `test_*.py` | CHECK 16 verification — functional proof |
| `*--*.yaml` | Gate contracts — declared behavioral agreements |
| `signal-graph.yaml` | Organism wiring — the signal graph |
| `cocoon-map.yaml` | Absorption blueprint — maps predecessor code to mechanisms |
| `SEED.md` | The genome — generative grammar (sealed until conditions met) |
| `RELAY.md` | Session handoff — what was done, what is next |
| `*.md` | Documentation and design documents |

## Naming Convention

Canonical names use double hyphen: `skeletal--define`, `circulatory--route`,
`cultvra--logos`. Python filenames map to underscore: `skeletal_define.py`.
The mechanism prefix groups related contracts alphabetically.

## The Three-Layer System

This repository (THE SEED) sits between two predecessor codebases:

```
meta-organvm        THE BODY  — what was built (engine, corpus, schemas)
organvm-iv-taxis    THE MIND  — what orchestrated (conductor, agents, governance)
a-organvm           THE SEED  — what grows (axioms, gate contracts, functions)
```

See `TRIPTYCH.md` for the full relationship. Code does not copy — it is
called through gate contracts. See `SEED.md` for how the organism grows.

## Current State

```
3 functions · 1,020 lines of living code
82 tests passing (22 skeletal + 27 circulatory + 33 cultvra)
5 signal types · 16 mechanisms · 36 gate contracts
4 information edges · 1 signal cycle (CHECK 19)
```
