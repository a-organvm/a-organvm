# Stranger Report: meta-organvm core repos

**Governance:** integumentary--report (CALLING)
**Methodology:** Context-free code audit. No CLAUDE.md, README, seed.yaml, or
governance files were read. Source code only.

## Scan Summary

- **Total source lines:** 92,388
- **Repos scanned:** 6 (engine, ontologia, mcp-server, dashboard, alchemia, schemas)
- **Unique modules found:** 56
- **Isotope pairs found:** 8

## Engine Modules (37 + 4 foundation)

| Module | Verb | Lines | Mechanism (derived) |
|--------|------|-------|-------------------|
| organ_config | maps | 338 | skeletal (structure) |
| paths | resolves | 153 | skeletal (structure) |
| domain | fingerprints | 35 | digestive (decomposition) |
| project_slug | derives | 132 | skeletal (structure) |
| atoms | links | 1900 | digestive (indexing) |
| audit | verifies | 1600 | immune (verification) |
| ci | audits | 1700 | immune (verification) |
| content | discovers | 530 | respiratory (intake) |
| contextmd | generates | 1650 | reproductive (generation) |
| coordination | coordinates | 1100 | nervous (control) |
| deadlines | parses | 270 | digestive (decomposition) |
| debt | scans | 230 | immune (detection) |
| dispatch | routes | 600 | circulatory (routing) |
| distill | distills | 800 | reproductive (distillation) |
| distillatio | transforms | 387 | reproductive (distillation) |
| ecosystem | discovers | 2300 | digestive (indexing) |
| events | records | 500 | memory (recording) |
| fossil | excavates | 3200 | memory (excavation) |
| git | manages | 870 | muscular (operations) |
| governance | enforces | 9400 | nervous (enforcement) |
| indexer | indexes | 900 | digestive (indexing) |
| irf | parses | 370 | digestive (parsing) |
| ledger | chains | 1300 | memory (chaining) |
| metrics | calculates | 4400 | digestive (measurement) |
| network | discovers | 1700 | circulatory (mapping) |
| omega | evaluates | 830 | immune (evaluation) |
| ontologia (bridge) | bridges | 2100 | skeletal (identity) |
| ontology | classifies | 640 | skeletal (classification) |
| pitchdeck | generates | 1750 | integumentary (presentation) |
| plans | atomizes | 1500 | digestive (atomization) |
| prompting | loads | 180 | skeletal (standards) |
| prompts | extracts | 2960 | digestive (extraction) |
| pulse | senses | 7900 | endocrine (regulation) |
| registry | loads | 1200 | skeletal (registration) |
| schemas | loads | 0 | skeletal (placeholder) |
| seed | discovers | 1600 | circulatory (discovery) |
| session | parses | 2700 | digestive (parsing) |
| sop | discovers | 620 | digestive (discovery) |
| testament | renders | 3300 | integumentary (rendering) |
| trivium | detects | 2200 | digestive (detection) |
| verification | proves | 780 | immune (proving) |
| cli | exposes | 13200 | muscular (execution) |

## Ontologia Modules (11)

| Module | Verb | Lines | Mechanism |
|--------|------|-------|-----------|
| entity | identifies | 650 | skeletal |
| events | emits | 580 | memory |
| governance | governs | 365 | nervous |
| inference | infers | 360 | endocrine |
| metrics | measures | 380 | digestive |
| registry (store) | stores | 970 | skeletal |
| sensing | senses | 740 | endocrine |
| state | snapshots | 570 | memory |
| structure | models | 500 | skeletal |
| variables | resolves | 450 | skeletal |
| bootstrap | migrates | 213 | reproductive |

## Other Repos

| Repo | Modules | Lines | Primary Mechanism |
|------|---------|-------|------------------|
| organvm-mcp-server | server + 27 tools + data | 7256 | integumentary (exposure) |
| system-dashboard | app + 17 routes + data | 2772 | integumentary (rendering) |
| alchemia-ingestvm | 5 stages + channels + cli | 3053 | respiratory (ingestion) |
| schema-definitions | 28 schemas + validator | 200 | skeletal (definition) |

## Isotopes (same function, different locations)

1. **Registry loading**: engine/registry vs alchemia/absorb/registry_loader (TRUE ISOTOPE — independent reimplementation)
2. **Organ config**: engine/organ_config vs alchemia/synthesize::ORGAN_MAP vs conductor/constants::ORGANS (TRIPLE ISOTOPE — 3 copies of organ mapping)
3. **Inference bridges**: engine/ontologia/inference_bridge vs engine/pulse/inference_bridge (internal isotope — 2 bridges to same ontologia code)
4. **Events**: engine/events/spine vs ontologia/events/bus (COMPLEMENTARY — system vs entity level)
5. **Governance**: engine/governance vs ontologia/governance (COMPLEMENTARY — enforcement vs evolution)
6. **Metrics**: engine/metrics vs ontologia/metrics (COMPLEMENTARY — system vs entity level)
7. **Sensing**: engine/ontologia/sensors vs ontologia/sensing (BRIDGE — engine adapts ontologia)
8. **Path resolution**: engine/paths vs mcp-server/data/paths (EXTENSION — mcp extends engine)
