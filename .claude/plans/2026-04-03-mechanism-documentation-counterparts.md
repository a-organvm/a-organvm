# Mechanism Documentation Counterparts — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create documentation counterparts for all 16 mechanisms, combining derived synthesis (automated from contracts/cocoon-map/signal-graph) with authored ontology (requires research), tracking spread between the two.

**Architecture:** Each mechanism gets one `{mechanism}.md` file at root level (flat namespace). Two layers per document: DERIVED (extractable from existing data, regenerable) and AUTHORED (ontological positioning, requires research per mechanism). The spread between layers is the documentation maturity metric.

**Tech Stack:** Python (generation script reads YAML sources), GitHub Issues (tracking authored layer research)

**Source:** S54 session — cultvra_logos.py reports 16 mechanisms with no documentation counterpart (72% coverage, 16 missing).

---

## Design

### Document Structure

Each `{mechanism}.md` contains:

1. **Header** — Status (DERIVED/TENDING/AUTHORED), spread metric, timestamps
2. **Derived Layer** — Auto-extracted from gate contracts, cocoon-map.yaml, signal-graph.yaml
   - Functions (embodied + planned)
   - Gate contracts (name, state, verb, signals)
   - Signal flow (produces/consumes/defects)
   - Absorption state (cocoon count, lines, source repos)
3. **Authored Layer** — Requires research, initially vacant
   - What this mechanism IS (ontological positioning)
   - Critical lenses (Insider, Outsider, Adversary)
   - Plotted work
4. **Spread Table** — Derived fields vs authored fields, vacant count

### Status Progression

`DERIVED` (only extracted data) -> `TENDING` (authored work started) -> `AUTHORED` (both layers complete)

### Naming Convention

`{mechanism}.md` — e.g., `skeletal.md`, `nervous.md`, `cultvra.md`

cultvra_logos.py check (L192): `mech.lower() in md_files or f"cultvra--{mech}" in md_files`
Both patterns satisfy the check. Bare mechanism name is simpler and means "the mechanism documents itself."

### Existing File

`cultvra--logos.md` already exists as an authored ontological sketch for the cultvra mechanism. It uses a different structure (no derived layer). Decision: either rename to `cultvra.md` and add derived layer, or create `cultvra.md` separately and keep `cultvra--logos.md` as supplementary. Operator decision needed.

---

## Mechanism Inventory

| # | Mechanism | Gate Contracts | Cocoon Entries | Embodied Function | Lines Absorbed |
|---|-----------|---------------|----------------|-------------------|----------------|
| 1 | skeletal | 2 (define, consolidate) | 1 (skeletal--define) | skeletal_define.py | 5,626 |
| 2 | circulatory | 3 (route, contribute, relay) | 2 (route, contribute) | circulatory_route.py | 6,100 |
| 3 | cultvra | 1 (logos) | 0 (self-named, no cocoon) | cultvra_logos.py | 0 |
| 4 | nervous | 5 (govern, orchestrate, propose, swarm, synchronize) | 2 (govern, orchestrate) | — | 18,450 |
| 5 | digestive | 2 (measure, filter-migration) | 2 (measure, collider) | — | 22,985 |
| 6 | immune | 3 (verify, score, watch) | 3 (verify, score, watch) | — | 9,527 |
| 7 | muscular | 3 (execute, titan, smith) | 3 (execute, titan, smith) | — | 114,200 |
| 8 | integumentary | 4 (present, emit, render, report) | 1 (present) | — | 37,428 |
| 9 | endocrine | 1 (regulate) | 1 (regulate) | — | 9,000 |
| 10 | memory | 3 (remember, persist, migrate-index) | 1 (remember) | — | 9,450+ |
| 11 | mneme | 2 (catalogue, log-inquiry) | 0 | — | 0 |
| 12 | respiratory | 1 (ingest) | 1 (ingest) | — | 3,053 |
| 13 | reproductive | 2 (generate, instantiate) | 1 (generate) | — | 1,863 |
| 14 | excretory | 2 (filter, metabolize) | 0 | — | 0 |
| 15 | poiesis | 1 (architect) | 0 | — | 0 |
| 16 | theoria | 1 (define-omega) | 0 | — | 0 |

### Data Richness Tiers

- **Rich** (cocoon + multiple contracts + embodied function): skeletal, circulatory
- **Moderate** (cocoon + contracts, no function yet): nervous, digestive, immune, muscular, integumentary, endocrine, memory, respiratory, reproductive
- **Sparse** (contracts only, no cocoon): mneme, excretory, poiesis, theoria, cultvra

---

## Implementation Tasks

### Task 1: Write generation script

**Files:**
- Create: `generate_mechanism_docs.py` (one-time generation script, flat namespace sibling)

Script reads:
- `signal-graph.yaml` — functions per mechanism, signal types, edges
- `cocoon-map.yaml` — absorption data per cocoon
- All `*--*.yaml` gate contracts — identity, state, signals, dna, defect
- Existing `*.md` files — detect authored content already present

Outputs 16 `{mechanism}.md` files with derived layer populated and authored layer as vacant placeholders.

- [ ] Write generation script
- [ ] Run it: `python3 generate_mechanism_docs.py`
- [ ] Verify cultvra_logos.py reports 0 undocumented mechanisms: `python3 cultvra_logos.py`
- [ ] Run tests: `python3 -m pytest -v`
- [ ] Commit: `feat: mechanism documentation counterparts — derived layer (16 files)`

### Task 2: Create GitHub issues for authored layer research

16 mechanism-level issues + 1 umbrella tracking issue.

- [ ] Create umbrella issue: `DOC-001 Mechanism documentation counterparts — authored layer`
- [ ] Create 16 child issues: `DOC-{mechanism} {mechanism} mechanism — authored ontology research`
- [ ] Each issue body contains: what research is needed, which source repos to read, what lenses to apply
- [ ] Label all with `documentation`, `mechanism`, `research`
- [ ] Commit plan: `docs: mechanism documentation counterparts plan`

### Task 3: Update cultvra_logos.py spread tracking (optional, future)

Extend the inventory to detect derived-vs-authored layers and report spread per mechanism. Not blocking — cultvra_logos.py already detects the files exist. Spread tracking is a refinement.

---

## GitHub Issue Templates

### Umbrella Issue

**Title:** `DOC-001 Mechanism documentation counterparts — authored layer`
**Body:** 16 mechanisms need authored ontological documentation. Derived layer generated. Authored layer requires research per mechanism: reading source repos, understanding the mechanism's role in the organism, applying Insider/Outsider/Adversary lenses.

### Per-Mechanism Issue

**Title:** `DOC-{MECH} {mechanism} mechanism — authored ontology research`
**Body template:**
- Status: DERIVED (authored layer vacant)
- Gate contracts: {list}
- Cocoon entries: {list with line counts}
- Source repos to read: {from cocoon-map absorbs_from}
- Research questions:
  - What is this mechanism's ontological role in the organism?
  - How does it relate to its biological analog (if any)?
  - Insider: how does this mechanism see itself?
  - Outsider: how do other mechanisms see it?
  - Adversary: what would destroy it?
- Plotted work to discover during research

---

## Verification

After both tasks:
- `python3 cultvra_logos.py` should report 0 undocumented mechanisms (coverage ~95%+)
- 17 GitHub issues created (1 umbrella + 16 mechanism)
- Plan committed to `.claude/plans/`
