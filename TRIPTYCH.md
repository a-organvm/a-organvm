# TRIPTYCH — The Three Become One

Three directories. One transition. The old form dissolves. The new form emerges.

```
/Users/4jp/Workspace/meta-organvm        THE BODY     — what was built (engine, corpus, schemas, dashboard)
/Users/4jp/Workspace/organvm-iv-taxis    THE MIND     — what orchestrated (conductor, skills, agents, governance)
/Users/4jp/Workspace/a-organvm           THE SEED     — what grows (axioms, gate contracts, functions)
```

## The Transition

The BODY and the MIND contain working code — 128+ repos, 5,800+ tests, 37 engine modules, 14 contrib workspaces. This code does not move. It stays where it is. What moves is its *identity* — its declaration of what it does, expressed as a verb.

The SEED contains gate contracts. Each contract CALLS code from the BODY or the MIND. When all gates pass, the code is said to have *emerged* — it exists in the new organism not by copying, but by being called from a place that understands it.

## Current State

### THE BODY (meta-organvm)
- 13 repos, 2 flagship, 9 standard, 2 infrastructure
- ORGAN-REPORT.md generated — 54 nodes assessed
- Key assets: organvm-engine (37 modules), organvm-corpvs-testamentvm (IRF + corpus), system-dashboard, schema-definitions
- Submodule pointers track each repo's current commit

### THE MIND (organvm-iv-taxis)
- 24 repos, 9 tracked submodules, 5 untracked core, 14 contrib workspaces
- ORGAN-REPORT.md generated — 95 nodes assessed
- Key assets: tool-interaction-design (conductor, fleet, contribution ledger), orchestration-start-here (contrib engine), agentic-titan, a-i--skills
- Wave 1+2 of contribution ledger shipped (receipt, timecard, energy, scorecard, prompt patches)

### THE SEED (a-organvm)
- 1 function exists: `skeletal_define.py` (510 lines, 22 tests)
- 36 gate contracts in state CALLING
- 97 gates total (10 lit / 87 dim)
- 15 mechanisms classified
- 3 observations recorded
- Second function selected: `circulatory--route`
- signal-graph edges: empty (activates at function 2)

## The Cocoon Map

`a-organvm/cocoon-map.yaml` (16,287 lines) is the absorption blueprint. It maps every module from the BODY and the MIND to a biological mechanism in the SEED:

| Mechanism | Verb | Source (BODY + MIND) | Gates |
|-----------|------|---------------------|-------|
| skeletal | define | engine/registry, ontologia, schema-definitions | 4 |
| nervous | orchestrate | conductor/fleet, conductor/session | 5 |
| nervous | govern | engine/governance, conductor/governance | 5 |
| digestive | measure | engine/metrics, atoms, indexer, ecosystem, trivium | 4 |
| circulatory | route | engine/dispatch, seed, network | 3 |
| immune | verify | engine/governance/state_machine, schema validation | 3 |
| respiratory | ingest | alchemia-ingestvm | 3 |
| integumentary | present | system-dashboard, stakeholder-portal | 4 |
| memory | remember | engine/contextmd, organvm-mcp-server | 3 |
| muscular | execute | agentic-titan runtime, conductor/cross_verify | 3 |
| reproductive | generate | engine/pitchdeck, content syndication | 2 |

## How to Use This Document

**If you arrive at any of the three directories**, read this file first. It tells you:
1. Where you are in the transition
2. What the other two directories contain
3. How they connect through the cocoon map

**If you are building in a-organvm**: the BODY and MIND are your source material. Gate contracts tell you what to call.

**If you are maintaining meta-organvm or organvm-iv-taxis**: your code is being absorbed. The ORGAN-REPORT.md shows what each piece does. The cocoon map shows where it goes.

**The transition is not a migration.** No code copies. The old organs continue to function. The new organism grows around them, calling their capabilities through gate contracts. When enough gates pass, the old organ's purpose is fulfilled by the new organism — and the old organ can rest.

## Portal Paths

```
meta-organvm/ORGAN-REPORT.md           → what the BODY contains
organvm-iv-taxis/ORGAN-REPORT.md       → what the MIND contains
a-organvm/cocoon-map.yaml              → where everything goes
a-organvm/signal-graph.yaml            → what's wired so far
a-organvm/SEED.md                      → the generative grammar
a-organvm/RELAY.md                     → what to do next
```

---

*This file exists identically in all three directories. It is the portal.*
