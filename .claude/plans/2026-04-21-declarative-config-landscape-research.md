# Declarative Configuration Landscape Research

**Date**: 2026-04-21
**Slug**: declarative-config-landscape-research
**Type**: strategic research (architecture)

## Context

Last session identified that `~/Workspace/a-organvm/` contains 6 static files (system.toml, ARCHITECTURE.md, BLUEPRINT.md, PERIODIC-TABLE.md, FOSSIL-RECORD.md, fossil-record.json) that declare ORGANVM's structure but are "dead" — no validation, no versioning, no enforcement. `system.toml` claims to be "like NixOS configuration.nix" but has zero properties of a Nix expression: no types, no evaluation, no module system, no derivation semantics.

Meanwhile, the **living organism** at `~/Workspace/organvm/sovereign--ground/holds--same/a-organvm/` has 5 Python functions, 140 tests, a real signal graph, and immune verification — but it does NOT read or validate `system.toml`. The declaration and the organism are structurally disconnected.

**Directive**: Before creating more files in a-organvm/, perform deep research into the landscape of declarative configuration systems, extract common principles, then design from those principles.

## Research Targets (Genealogical Order)

### Phase 1: The Root — Nix
- Eelco Dolstra's 2006 PhD thesis "The Purely Functional Software Deployment Model"
- NixOS module system (`nixpkgs/lib/modules.nix`, `nixpkgs/lib/types.nix`)
- configuration.nix pattern, Flakes, content-addressed store
- **Why first**: intellectual root of the field; every other system responds to Nix

### Phase 2: The Divergence — Guix
- GNU Guile Scheme approach, g-expressions, service model
- Courtes 2013 FOSSA paper
- **Why**: tests whether the deployment model is separable from the language

### Phase 3: The Type-Theoretic Alternative — Dhall
- System F with records/unions, totality guarantee, no Turing-completeness
- Import system with integrity hashes
- **Why**: answers "what if declarations were guaranteed to terminate and type-check?"

### Phase 4: The Constraint Lattice — CUE
- Van Lohuizen's value lattice, unification as core operation
- Types and values on the same lattice (declaration IS validation)
- **Why**: directly relevant to "self-enforcing" — no separate schema needed

### Phase 5: The Hermetic Template — Jsonnet
- Google's pragmatic approach, mixins, deterministic evaluation
- **Why**: shows the "minimal viable" declarative system at scale

### Phase 6: The Stateful Pair — Terraform/HCL + Pulumi
- Plan/apply cycle, state management, DSL vs. real languages
- **Why**: the tension between safety and expressiveness

### Phase 7: The Build System — Bazel/Starlark
- Restricted Python, BUILD files, action graph, hermeticity enforcement
- **Why**: strongest reproducibility guarantees in production

## Extraction Framework (Per System)

| Dimension | Question |
|-----------|----------|
| Core Primitive | What is the irreducible unit? |
| Composition Model | How do primitives combine? |
| Type/Constraint System | How is correctness expressed? |
| Evaluation Strategy | Lazy/eager? Pure/effectful? Hermetic? Total? |
| Module/Package System | How does code organize and import? |
| Validation Mechanism | When and how are errors caught? |
| Versioning Approach | How does the system evolve? |
| State Management | Stateless or stateful? Where does state live? |
| Key Unique Insight | The one idea worth stealing |

## Deliverables

1. **Landscape Matrix** — all 8 systems × 9 dimensions in one comparative view
2. **Universal Principles** — what ALL systems share (reproducibility, immutability, content addressing, etc.)
3. **Divergence Analysis** — where they disagree and why (DSL vs. language, total vs. Turing-complete, lazy vs. eager, stateless vs. stateful)
4. **Design Principles for Ideal Form** — synthesized from landscape, not copied from any single system
5. **ORGANVM Mapping** — how principles apply to specific needs (flat store, alive files, self-enforcing, signal graph derivation)

## ORGANVM-Specific Questions to Answer

1. Should `system.toml` remain TOML or become an expression in a language with evaluation semantics?
2. How should elements/compounds/formations be typed? (Dhall types? CUE constraints? NixOS options?)
3. What composition model fits the 4 operators (chain, parallel, envelope, feedback)?
4. How should the 10-level governance cascade be enforced?
5. Should the signal graph be DERIVED from the declaration (like Bazel derives action graphs from BUILD files)?
6. What versioning model allows evolution without breakage?
7. How to bridge system.toml → immune_verify.py? (declaration generates verification? verification reads declaration?)
8. What does "self-enforcing" mean precisely? (CUE lattice? Dhall totality? NixOS option merge?)

## Critical Files

- `~/Workspace/a-organvm/system.toml` — the dead declaration (primary redesign target)
- `~/Workspace/a-organvm/ARCHITECTURE.md` — structural description
- `~/Workspace/organvm/sovereign--ground/holds--same/a-organvm/immune_verify.py` — living verification
- `~/Workspace/organvm/sovereign--ground/holds--same/a-organvm/signal-graph.yaml` — wiring diagram
- `~/Workspace/organvm/sovereign--ground/holds--same/a-organvm/skeletal_define.py` — structure reader

## Execution Plan

1. **Research phases 1–7** using web search + web fetch for primary sources (theses, specs, design docs)
2. **Fill extraction framework** for each system as I go
3. **Synthesize** landscape matrix, universal principles, divergence analysis
4. **Design** ideal form principles specific to ORGANVM
5. **Write** the research document as a single flat file in the a-organvm/ directory (once it earns git tracking)

## Verification

- Every claim traceable to a primary source (not Wikipedia summaries)
- Design principles validated against ≥3 systems
- Architecture proposal checked against the living organism's existing structure
- The 8 ORGANVM-specific questions each have a clear answer

## Priority Note

The critical quartet is **Nix, Dhall, CUE, and the NixOS module system**. Terraform/Pulumi and Bazel are narrower contributions. If time is limited, depth on the quartet > breadth across all 8.
