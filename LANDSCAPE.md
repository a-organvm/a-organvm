# Declarative Configuration Systems: Landscape Analysis

**Date**: 2026-04-21
**Purpose**: Inform the redesign of a-organvm's declaration layer
**Method**: Deep research into 8 systems from primary sources (theses, specifications, design documents)
**Status**: Research complete; design principles extracted; ORGANVM questions answered

---

## I. The Landscape Matrix

Eight systems studied. Nine dimensions extracted per system. Every finding traceable to a primary source.

### Core Primitive

| System | Primitive | Source |
|--------|-----------|--------|
| **Nix** | The derivation — a pure function from declared inputs to content-addressed store objects. All of Nix reduces to derivation instantiation (`.drv` file) and realization (built output). | Dolstra thesis §2, §4 |
| **Guix** | G-expression — staged code with automatic dependency tracking. Package definitions as first-class Scheme records. G-expressions resolve references at build time, not definition time. | Courtès GPCE'17 |
| **Dhall** | Typed lambda expression (System F-omega). Every program is a lambda calculus term guaranteed to reduce to a value. | dhall-lang.org spec |
| **CUE** | Constraint — a value on the lattice. Every CUE expression is a constraint that can be unified with other constraints. Types and values are the same thing at different specificity. | cuelang.org spec, van Lohuizen talks |
| **Jsonnet** | JSON object extended with expressions. Prototype-based objects with lazy field values, hidden status, and assertions. | Jsonnet spec (jsonnet.org/ref/spec.html) |
| **Terraform** | Resource block — `resource "type" "name" { ... }`. A typed, named declaration of desired infrastructure state. | HCL spec (github.com/hashicorp/hcl) |
| **Pulumi** | Resource registration — a `RegisterResource` gRPC call expressing desired state. All registrations together form the resource model. | Pulumi architecture docs |
| **Bazel** | Action — a declared transformation from input artifacts to output artifacts with a specific command. Actions are pure functions of their declared inputs. | Bazel rules documentation |

### Composition Model

| System | How Primitives Combine |
|--------|----------------------|
| **Nix** | Fixed-point self-application via lazy evaluation. Nixpkgs is `fix pkgs_fun`. Overlays compose via `extends`/`composeExtensions`. Modules compose via type-directed merging in `evalModules`. |
| **Guix** | Service extension DAG. Services declare typed extensions to other services. `compose` combines contributions; `extend` merges them. Scheme-level functional composition. |
| **Dhall** | Function application and record merging. `//` (right-biased merge) and `/\` (recursive merge). No inheritance. |
| **CUE** | Unification (greatest lower bound on the lattice). **Commutative, associative, idempotent.** Multiple files impose independent constraints; CUE merges them all. No inheritance. |
| **Jsonnet** | Prototype-based OOP with mixin inheritance via `+` operator. `self` sees merged result; `super` sees left operand. **Non-commutative, non-idempotent.** |
| **Terraform** | Module composition — directories called via `module` blocks. Input variables as arguments, output values as returns. Flat dependency graph. |
| **Pulumi** | Component resources extending `ComponentResource`. Parent-child hierarchy. Full language-native abstraction (classes, functions, modules). |
| **Bazel** | Rule composition via dependency attributes. Providers communicate between rules. Aspects enable cross-cutting traversal. Three levels: macros (loading) → rules (analysis) → actions (execution). |

### Type/Constraint System

| System | How Correctness Is Expressed |
|--------|----------------------------|
| **Nix** | NixOS module option types (`lib.types`): runtime validation with `check`, merge semantics per type, documentation generation. Types include `bool`, `int`, `str`, `listOf`, `attrsOf`, `submodule`, `enum`, `either`, `coercedTo`. Not compile-time — all validation at evaluation time. |
| **Guix** | Scheme's dynamic typing plus Guix-specific record types. Compile-time checking via record field contracts. Convention-enforced. |
| **Dhall** | System F-omega: polymorphic lambda calculus with type operators. Static, strong, structural. Invalid states are unrepresentable by design (opaque `Text`, unions for enums). |
| **CUE** | Value lattice. Types and values on the same partial ordering. `string` → `=~"^[A-Z]"` → `"Hello"` are all constraints at different specificity. Validation IS unification. No separate schema language needed. |
| **Jsonnet** | None. Dynamic typing only. No schema language, no validation primitives, no constraint declarations. |
| **Terraform** | Primitive + complex types on variables. Provider schemas enforce attribute types. `validation` blocks with custom conditions. |
| **Pulumi** | Host language's type system (TypeScript strict mode, Go static types, etc.). Policy as Code for runtime constraints. |
| **Bazel** | Starlark dynamic types + rule attribute declarations (`attr.label`, `attr.string`, etc.) with `mandatory`, `default`, `values` constraints. |

### Evaluation Strategy

| System | Strategy |
|--------|----------|
| **Nix** | Lazy (call-by-need) with thunks and memoization. WHNF. Blackholing detects infinite recursion. Enables fixed-point overlays and self-referential module configs. |
| **Guix** | Scheme evaluation (eager) with monadic sequencing. G-expressions staged — evaluated lazily when lowered to derivations. |
| **Dhall** | Strict/eager with guaranteed termination. Full beta-normalization to unique canonical form. All imports resolve regardless of usage. |
| **CUE** | Lazy constraint propagation. Incomplete expressions remain unevaluated until concrete values requested. Permits cycle resolution via constraint satisfaction. |
| **Jsonnet** | Lazy throughout. Field values remain unevaluated expressions in object values. Errors only on dereference. |
| **Terraform** | Eager within dependency-ordered execution graph. Plan evaluates all expressions to compute diff. |
| **Pulumi** | Imperative execution generates declarative graph. Language host executes concurrently with engine processing. |
| **Bazel** | Three-phase: loading (Starlark eval), analysis (pure computation, no IO), execution (sandboxed actions). Content-addressed caching. |

### Module/Package System

| System | Organization |
|--------|-------------|
| **Nix** | Dual-level: derivations (build) + NixOS modules (config). Flakes add project-level: inputs/outputs/lock files. |
| **Guix** | Guile Scheme modules. Packages as first-class records. Channel mechanism for third-party sets. |
| **Dhall** | Convention-based: packages are records imported via URL/path with integrity hashes. No built-in module keyword. The import system IS the module system. |
| **CUE** | File-based packages. Files in the same package unify. Identifiers not starting with `_` are exported. |
| **Jsonnet** | `import`/`importstr`/`importbin` with file-path resolution. Cached by filename. No registry. |
| **Terraform** | Modules from local paths, Git, S3, or Registry. Semantic versioning. `terraform init` downloads. |
| **Pulumi** | Native language package managers (npm, PyPI, Go modules). Standard software distribution. |
| **Bazel** | `load()` for symbol imports. `MODULE.bazel` for external deps. Bzlmod with Minimum Version Selection. |

### Validation Mechanism

| System | When/How Errors Are Caught |
|--------|---------------------------|
| **Nix** | Multi-layered: store path hashes (input identity), content addressing (output identity), module type system (config values), reference scanning (closure completeness), `allowedReferences`/`disallowedReferences` (dependency graph constraints). |
| **Guix** | Build-time: successful derivation = correct output. Content addressing ensures integrity. Grafts handle post-build security patching. |
| **Dhall** | Type-checking. Invalid states are unrepresentable. Type errors are compile-time errors. Totality guarantees termination. |
| **CUE** | **Unification itself IS validation.** Schema & data → unify → either more specific value (valid) or bottom (invalid/conflict). No separate validation step. |
| **Jsonnet** | Object assertions (checked during manifestation only). No structural validation. External JSON Schema required. |
| **Terraform** | Provider schema validation, variable validation blocks, precondition/postcondition blocks, plan output as human review checkpoint. |
| **Pulumi** | Language-native type checking, unit/integration tests, Policy as Code, preview output. |
| **Bazel** | Validation actions (`_validation` output group), provider requirements, attribute constraints, static analysis of dependency graphs. |

### Versioning Approach

| System | How the System Evolves |
|--------|----------------------|
| **Nix** | No explicit versions — content addressing replaces versioning. Different inputs → different store paths. Multiple versions coexist. Flake lock files pin input revisions. |
| **Guix** | Git-based: each `guix pull` generation = specific commit. Two-dimensional rollback (packages × package manager). |
| **Dhall** | Semantic versioning for the language standard. "Stable hashes" decouple version from integrity checks. Semantic hashing survives refactoring. |
| **CUE** | Backward compatibility as lattice operation: schema B is backward-compatible with A iff A subsumes B. Mechanically checkable. |
| **Jsonnet** | No built-in versioning. Community uses git tags and jsonnet-bundler. |
| **Terraform** | Provider versioning via `required_providers`. Module versioning via semver. State file format version. |
| **Pulumi** | Standard package versioning per language ecosystem. Stack-based environment separation. |
| **Bazel** | Bzlmod with semver + Minimum Version Selection. Content hashing for cache key identity. |

### State Management

| System | State Model |
|--------|-------------|
| **Nix** | Stateless. Immutable store. Profiles provide generational rollback. Only mutable state: which generation is current. |
| **Guix** | Immutable store with generation-based profiles. Rollback = O(1) symlink switch. |
| **Dhall** | Stateless. No mutation. Configuration produces a pure value; host decides what to do. |
| **CUE** | Stateless. No mutation. Values cannot change once set (attempting produces bottom). |
| **Jsonnet** | Stateless. Pure computation → JSON/YAML output. |
| **Terraform** | **Stateful.** JSON state file maps config to real-world resource IDs. Remote backends with locking. State is the central coordination artifact AND the central failure point. |
| **Pulumi** | **Stateful.** JSON checkpoints in chosen backend. Transactional checkpointing. Secret encryption. |
| **Bazel** | No mutable state. Content-addressable storage is the only persistent artifact. Build graph derived fresh from source on every invocation. |

### Key Unique Insight

| System | The One Idea Worth Stealing |
|--------|-----------------------------|
| **Nix** | **Correctness = completeness + non-interference**, enforced by content-addressed storage. The filesystem IS the memory model. |
| **Guix** | **The deployment model is separable from the expression language.** You can have functional deployment without a DSL. |
| **Dhall** | **Totality as security.** Sacrificing Turing-completeness makes it safe to import and evaluate untrusted code. Unique normal form enables semantic integrity checks surviving refactoring. |
| **CUE** | **The type/value collapse.** Types and values on the same lattice eliminates the schema/data distinction. Validation is not applied TO data — it IS the data. |
| **Jsonnet** | **The manifest operation as sole side effect.** The entire language is pure computation producing JSON. Hermetic, referentially transparent, safely parallelizable. |
| **Terraform** | **The plan/apply cycle.** A human-reviewable diff between desired and actual state before any modification. |
| **Pulumi** | **Imperative execution generates declarative graphs.** Running the program IS declaring desired state. The engine doesn't care whether the graph came from TypeScript or YAML. |
| **Bazel** | **Hermeticity through restriction.** Remove capabilities (no IO, no recursion, no mutation after freeze) and you get: caching, remote execution, parallelism, reproducibility — all as consequences of one decision. |

---

## II. Universal Principles

Six principles shared by ALL or nearly all eight systems:

### 1. Declarative Intent
Every system describes WHAT should exist, not HOW to build it. Even Pulumi (imperative execution) generates a declarative resource graph. The progression: static data (YAML) → templates (Jsonnet) → typed expressions (Dhall) → constraint systems (CUE) → derivation functions (Nix). The deeper the declarativeness, the more the system can reason about itself.

### 2. Reproducibility / Determinism
Same inputs → same outputs. Nix: content-addressed store paths. Dhall: normalization to unique canonical form. CUE: commutative unification (order-independent). Jsonnet: hermetic evaluation. Bazel: sandboxed actions with content-addressed caching. The mechanism varies; the invariant is universal.

### 3. Composition Over Inheritance
ALL systems compose small things into larger things. None uses classical OOP inheritance as the primary composition model. CUE explicitly rejects inheritance (van Lohuizen: "copies the biggest mistakes of BCL"). Jsonnet uses OOP mixins and FAILS AT SCALE because of it — this is the direct motivation for CUE's creation. NixOS modules compose via type-directed merging. Bazel rules compose via dependency attributes and providers.

### 4. Immutability
Nix store objects are immutable. Dhall values are immutable. CUE values can only be NARROWED (made more specific), never widened. Starlark values freeze after module initialization. Terraform state is append-only (each serial increments). Modification produces new values/states — it does not mutate existing ones.

### 5. Separation of Declaration from Execution
Every system separates WHAT from WHEN:
- Nix: instantiate (declaration → .drv) then realize (.drv → output)
- Terraform: plan (declaration → diff) then apply (diff → infrastructure)
- Bazel: loading (BUILD → targets) then analysis (targets → actions) then execution (actions → outputs)
- Pulumi: program execution (code → resource graph) then deployment (graph → infrastructure)

### 6. Content Addressing / Identity from Content
Nix: store path hash encodes all inputs. Dhall: semantic hash of normal form. Bazel: action key = Starlark + SHA256 of inputs. CUE: lattice position IS identity. Exceptions: Terraform and Pulumi use external identity (cloud resource IDs) because infrastructure has identity outside the tool.

---

## III. Divergence Analysis

Where the systems disagree — and what the disagreements reveal.

### A. Custom DSL vs. Real Programming Language

| DSL | Real Language | In Between |
|-----|---------------|------------|
| Nix, HCL, Starlark, CUE, Dhall | Guix (Scheme), Pulumi (TS/Python/Go) | Jsonnet (Turing-complete DSL) |

**What Guix proves**: The deployment MODEL (immutable store, content addressing, pure derivations) is separable from the expression LANGUAGE. Guix reuses Nix's store daemon while replacing the language entirely with Scheme.

**What Pulumi proves**: Imperative execution can generate declarative graphs. The engine performs the same reconciliation regardless of source language.

**What CUE and Dhall prove**: RESTRICTING the language buys safety properties impossible in general-purpose languages. CUE's commutativity requires no inheritance. Dhall's totality requires no general recursion. These are features-by-absence.

**Resolution for ORGANVM**: The declaration layer needs CONSTRAINT semantics (CUE's insight), not a Turing-complete language. But the EVALUATION layer (the organism's functions) is already Python — a real language. The two layers serve different purposes. The declaration constrains; the code acts.

### B. Turing-Complete vs. Total/Restricted

| Turing-Complete | Intentionally Restricted |
|-----------------|-------------------------|
| Nix, Guix (Scheme), Pulumi, Jsonnet | Dhall (total), CUE (sub-Turing), Starlark (restricted Python), HCL (limited) |

**What totality buys** (Dhall): Guaranteed termination, guaranteed normalization (unique canonical form), safe import of untrusted expressions, semantic integrity checks surviving refactoring.

**What restriction buys** (Starlark): Hermeticity, safe concurrency (freeze mechanism), bounded execution, analyzability. Every restriction maps to a specific safety property.

**What Turing-completeness costs** (Jsonnet at scale): Unpredictable inheritance chains, inability to statically analyze configurations, difficulty with automation, impossible to prove properties about large configurations.

**Resolution for ORGANVM**: The declaration must be sub-Turing. The declaration layer describes the organism's STRUCTURE and CONSTRAINTS — it should be analyzable, normalizable, and self-enforcing. Turing-completeness is for the organism's FUNCTIONS (Python), not its declarations.

### C. Lazy vs. Eager Evaluation

| Lazy | Eager | Mixed |
|------|-------|-------|
| Nix, Jsonnet | Dhall, Guix, Terraform, Pulumi | CUE (lazy constraint propagation), Bazel (three-phase) |

**What laziness enables** (Nix): The fixed-point pattern. Modules can read their own merged configuration while defining their contribution. The entire 100K+ package set exists as a single value without evaluating everything. Self-reference through deferred computation.

**What eagerness enables** (Dhall): Guaranteed normalization. If it type-checks, it reduces to a unique value. No surprises from deferred evaluation. Import resolution is deterministic and complete.

**What CUE's hybrid does**: Lazy constraint propagation allows cycle resolution (a depends on b depends on a — resolved via constraint satisfaction), while incomplete expressions remain unevaluated until forced.

**Resolution for ORGANVM**: CUE's approach — lazy constraint propagation with cycle resolution. The signal graph has feedback loops (cultvra→skeletal, immune→skeletal, respiratory→skeletal). The declaration should handle these through constraint satisfaction, not through eager evaluation that would detect cycles as errors.

### D. Types vs. Constraints vs. Unification

| Static Types | Constraint Lattice | Runtime Type System | No Types |
|-------------|-------------------|--------------------|---------| 
| Dhall (System F) | CUE (types = values) | NixOS modules (option types + merge functions) | Jsonnet, Starlark |

**Dhall's approach**: Types prevent invalid states at compile time. Unions for enums (not strings). Opaque Text (no equality). Invalid configurations are unrepresentable.

**CUE's approach**: Types and values on the same lattice. `string` and `"hello"` differ only in specificity. Validation IS unification — no separate schema language. Backward compatibility is a subsumption check, not a manual test.

**NixOS's approach**: Runtime types with merge semantics. Each type defines HOW multiple definitions combine (lists concatenate, booleans OR, attrs recursively merge, submodules recursively evaluate). The type system governs COMPOSITION, not just validation.

**Resolution for ORGANVM**: CUE's lattice for the declaration (types = constraints = values), NixOS's merge semantics for composition (how multiple declarations of the same entity combine). The ideal is a constraint lattice with defined merge functions per type.

### E. Stateless vs. Stateful

| Stateless | Stateful |
|-----------|----------|
| Nix, Guix, Dhall, CUE, Jsonnet, Bazel | Terraform, Pulumi |

**When state is needed**: Only when managing external resources with identity that exists outside the tool (cloud infrastructure, database instances). State maps declarations to external IDs.

**When state is not needed**: For configuration (declaring what IS, not what should be DONE to external systems). ORGANVM declares the organism's own structure — no external resources to track.

**Resolution for ORGANVM**: Stateless. The declaration describes the organism. The organism's functions verify the declaration against actual state. There is no external infrastructure to reconcile. Content addressing (like Nix/Dhall) replaces state management.

---

## IV. Design Principles for the Ideal Form

Derived from the landscape. Not copied from any single system.

### Principle 1: CONSTRAINTS, NOT DATA

The declaration is not data describing the system. It is a SET OF CONSTRAINTS that the system must satisfy. (CUE's insight.)

`system.toml` currently says: `[elements.intake] symbol = "In" operation = "bring signal into the system"`. This is data — a key-value description. It constrains nothing. You can write `operation = "do backflips"` and nothing detects the violation.

The ideal declaration says: element operations MUST be one of the 10 discovered operations. The compound formula MUST reference only valid element symbols. The formation wiring MUST reference only valid compounds. These are CONSTRAINTS. Violating them produces an error, not a silent different value.

**Mechanism**: CUE's value lattice. Constraints narrow; they never widen. Once `operation` is constrained to the set of valid operations, setting it to anything else produces bottom (error). The declaration IS the validation.

### Principle 2: COMPOSITION THROUGH UNIFICATION

Multiple declarations of the same entity UNIFY rather than overriding. (CUE's commutative unification + NixOS's type-directed merging.)

The signal graph currently lists functions and edges in a single YAML file. If the declaration instead constrained functions and edges, multiple files could contribute constraints to the same function/edge, and CUE-style unification would combine them. Order would not matter. Adding a new constraint could only NARROW the space, never contradict previous constraints.

**Mechanism**: Unification (greatest lower bound). Commutative (order doesn't matter), associative (grouping doesn't matter), idempotent (applying the same constraint twice changes nothing). No inheritance. No override.

### Principle 3: DERIVATION, NOT DESCRIPTION

The signal graph, formation wiring, and dependency structure should be DERIVED from the declaration — not hand-maintained as separate artifacts. (Bazel's insight: the action graph is derived from BUILD files.)

Currently, `system.toml` describes elements, compounds, and formations as separate sections. `signal-graph.yaml` describes signal flow as a separate file. The two are disconnected. In the ideal form, the signal graph IS a derivation from the element/compound/formation constraints plus wiring declarations. Change a compound's formula → the derived signal graph changes. Remove an element → all compounds referencing it fail (constraints produce bottom).

**Mechanism**: The evaluator reads the flat declaration, resolves all constraints, and DERIVES the signal graph, dependency graph, naming, and governance cascade as computed outputs. Like Nix derives store paths from expressions. Like Bazel derives action graphs from BUILD files.

### Principle 4: TOTALITY (ALIVE BY CONSTRUCTION)

Every declaration either evaluates to a consistent value or fails with an explicit error. No silent inconsistencies. No half-valid states. (Dhall's insight: totality guarantees.)

Currently, `system.toml` can have a compound referencing a nonexistent element symbol. Nothing catches this. In the ideal form, evaluating the declaration ALWAYS produces either a fully consistent organism description OR an explicit list of constraint violations. There is no middle ground where the declaration appears valid but contains inconsistencies.

**Mechanism**: Constraint propagation with mandatory completion. Every constraint must resolve. Unresolved constraints are errors. The evaluator halts only when all constraints are satisfied or a conflict is reported.

### Principle 5: SEMANTIC IDENTITY (CONTENT-ADDRESSED)

The declaration's identity is its semantics, not its text. (Dhall's semantic hashing + Nix's content addressing.)

Two declarations that express the same constraints in different order, different formatting, or different variable names should have the same identity. This enables: caching, integrity verification, diff detection, and provenance tracking.

**Mechanism**: Normalize the declaration to a canonical form (like Dhall's beta-normalization). Hash the canonical form (like Dhall's semantic hash or Nix's store path hash). The hash IS the version.

### Principle 6: FLAT STORE, STRUCTURE IN DATA

No nested directories. Structure lives in constraint attributes, not in filesystem hierarchy. (Feedback memory: NEVER nest directories for structure.)

`ARCHITECTURE.md` currently proposes: `laws/physics/`, `laws/theory/`, `laws/constitution/`, etc. This is hierarchy in the filesystem. The ideal form: all governance levels are ATTRIBUTES of flat constraint declarations. The evaluator DERIVES the sovereignty cascade from the `level` attribute, not from the directory path.

**Mechanism**: One level of files maximum. Entity type, governance level, domain, sovereignty tier — all expressed as attributes in flat declarations. The evaluator sorts, filters, and cascades based on attributes. The filesystem holds files, not structure.

### Principle 7: SEPARATION OF DECLARATION FROM ORGANISM

The declaration constrains. The organism acts. The bridge between them is VERIFICATION.

The declaration says WHAT the organism SHOULD be. The organism's immune system reads the declaration, evaluates it, and checks the actual organism state against the evaluated constraints. This is the Terraform plan/apply pattern applied to the organism: declaration = desired state, organism = actual state, immune system = the diff.

**Mechanism**: `immune_verify.py` gains a new dimension: DECLARATION — verifying that the organism's actual structure (functions, signals, gates, contracts) satisfies the constraints in the declaration. The declaration is an input to verification, not a separate artifact.

---

## V. ORGANVM Mapping: Answers to the 8 Design Questions

### Q1: Should system.toml remain TOML or become an expression in a language with evaluation semantics?

**Answer: Neither TOML nor a new language. CUE.**

TOML is inert — readable but not evaluable, not composable, not self-enforcing. Creating a new language repeats Nix's mistake of building and maintaining a custom DSL. CUE provides exactly the properties needed:

- Constraints that self-validate through unification
- Types and values on the same lattice (no separate schema)
- Commutative, associative, idempotent composition
- Sub-Turing (alive, always terminates)
- No inheritance (matches the flat principle)
- Cycle resolution through constraint propagation

The declaration becomes one or more `.cue` files. CUE's evaluator resolves constraints and produces a normalized organism description. The immune system reads the evaluated output.

**Alternative considered**: Dhall. Offers totality and semantic hashing but lacks CUE's type/value collapse. Dhall requires a SEPARATE schema + data pattern; CUE's schema IS the data. For a system where "the declaration IS the validation," CUE wins.

**Alternative considered**: NixOS module system. Offers excellent merge semantics but requires the entire Nix ecosystem. Too heavy for a flat declaration layer. However, NixOS's MERGE FUNCTION concept (different types merge differently) should be imported into the CUE design.

### Q2: How should elements/compounds/formations be typed?

**Answer: CUE definitions (closed structs) with constraint hierarchies.**

```
// The element type — closed, enforced
#Element: {
    symbol:    =~"^[A-Z][a-z]$"       // 2-letter symbol
    operation: string & strings.MinRunes(5)
    status:    "discovered" | "hypothesized" | "refuted"
}

// The compound type — formula references valid element symbols
#Compound: {
    formula:   [...#Element.symbol] & list.MinItems(2)
    modifier?: string
    domain:    "protective" | "economic" | "epistemic" | "relational" | "structural"
    operation: string & strings.MinRunes(10)
}

// The formation type — compounds references valid compound names
#Formation: {
    description: string
    compounds:   [...string] & list.MinItems(2)  // validated against declared compounds
    wiring:      string                           // parsed into signal graph
    trigger:     string
}
```

Elements are CONSTRAINTS, not data. A compound's `formula` field is constrained to reference only valid element symbols. Adding a compound with `formula: ["Xx"]` (nonexistent element) fails because `"Xx"` does not unify with any declared element symbol. The type system IS the validation.

### Q3: What composition model fits the 4 operators (chain, parallel, envelope, feedback)?

**Answer: The operators are PATTERNS of constraint unification, not separate mechanisms.**

The signal graph currently declares four operators: `→` (chain), `||` (parallel), `⊃` (envelope), `↻` (feedback). In the CUE model:

- **Chain** (`→`): Sequential constraint dependency. A depends on B means A's input constraints include B's output. Like Nix derivation dependencies.
- **Parallel** (`||`): Independent constraints unified. Two compounds operating on the same signal independently. Like Bazel parallel actions.
- **Envelope** (`⊃`): Nesting constraint — an outer constraint wraps and contextualizes an inner one. Like Guix's G-expression staging (host-side wrapping build-side).
- **Feedback** (`↻`): Self-referential constraint resolved through CUE's cycle resolution. Like Nix's fixed-point pattern (module reading its own merged config). CUE permits this naturally through lazy constraint propagation.

The operators are not special syntax — they are WIRING PATTERNS in the signal graph, each corresponding to a specific constraint relationship. The evaluator derives the signal flow from these relationships.

### Q4: How should the 10-level governance cascade be enforced?

**Answer: CUE constraint specificity on the lattice, inspired by NixOS priority mechanism.**

NixOS uses numeric priority: `mkDefault` (1000), normal (100), `mkForce` (50). Lower number = higher precedence. The 10 governance levels map to 10 priority tiers:

```
// Governance level as constraint specificity
#GovernanceLevel: {
    level:       int & >=1 & <=10
    description: string
    sovereignty: 11 - level    // higher level = higher sovereignty = more specific constraint
}

// Physics (level 1) has sovereignty 10 — most specific, cannot be overridden
// Record (level 10) has sovereignty 1 — least specific, can be overridden by anything above

// Constraint: higher-sovereignty declarations subsume lower ones
// A statute (level 6, sovereignty 5) cannot violate the constitution (level 4, sovereignty 7)
// In CUE terms: constitution constraints are MORE SPECIFIC than statute constraints
// Attempting to widen a constitutional constraint at statute level produces bottom (error)
```

This is CUE's lattice in action: constraints at higher sovereignty levels are MORE SPECIFIC (lower in the lattice). A statute attempting to contradict the constitution would unify a specific value with a broader constraint — which in CUE produces either the specific value (if compatible) or bottom (if contradictory). The cascade enforces itself.

### Q5: Should the signal graph be DERIVED from the declaration?

**Answer: YES. Unambiguously.**

Like Bazel derives the action graph from BUILD files. Like NixOS derives systemd units from module configuration. Like Nix derives store paths from expressions.

The current `signal-graph.yaml` is hand-maintained alongside `system.toml`. They can drift. In the redesigned system:

1. The declaration constrains functions, their signal types, their inputs/outputs, and their wiring
2. The evaluator resolves all constraints
3. The signal graph IS the evaluated output — computed, not maintained
4. `immune_verify.py` checks the actual organism against the derived signal graph

If a function is added to the declaration but not implemented, the derived signal graph shows it as "declared but unembodied." If a function exists in code but not in the declaration, `immune_verify` flags it as "uncontracted."

### Q6: What versioning model allows evolution without breakage?

**Answer: CUE subsumption checks + Dhall-style semantic hashing.**

CUE provides a mechanical backward-compatibility test: schema B is backward-compatible with schema A if and only if A subsumes B (B is more specific than A). This means:
- Adding a new optional field is backward-compatible (more specific)
- Narrowing a constraint is backward-compatible (more specific)
- Widening a constraint is NOT backward-compatible (less specific, could break existing valid configs)
- Removing a field is NOT backward-compatible

Combined with Dhall-style semantic hashing: normalize the declaration to canonical form, hash it. The hash changes if and only if the semantics change. Formatting changes, comment changes, and reordering do not change the hash. This gives content-addressed versioning — no manual version bumps needed.

**Evolution protocol**: Every change to the declaration is tested for backward compatibility via subsumption check against the previous version. Breaking changes require explicit sovereignty (governance level sufficient to authorize the breakage).

### Q7: How to bridge system.toml → immune_verify.py?

**Answer: The declaration becomes an INPUT to the immune system.**

Current state: `immune_verify.py` reads `signal-graph.yaml` and gate contracts. It does NOT read `system.toml`. The two are disconnected.

Redesigned flow:
1. Declaration (`.cue` files) is evaluated by the CUE evaluator → produces normalized organism description
2. `immune_verify.py` reads the normalized output as the SPECIFICATION
3. `immune_verify.py` reads the actual organism (functions, contracts, signal graph) as the REALITY
4. A new verification dimension — **Declaration** — compares specification to reality
5. Findings: "declared but unimplemented," "implemented but undeclared," "constraint violated," "governance level insufficient"

This is the Terraform plan pattern: declaration = desired state, organism = actual state, immune system = the diff. The immune system does not modify anything — it reports the delta.

### Q8: What does "self-enforcing" mean precisely?

**Answer: CUE's value lattice. The declaration IS the validation.**

In CUE:
1. Writing a constraint and validating against it are the SAME operation (unification)
2. Any violation produces bottom (⊥) — an error that cannot be ignored or suppressed
3. The constraint is INTRINSIC to the value, not an external check applied after the fact
4. Composition preserves enforcement — unifying two valid configurations produces a valid configuration (or bottom if they conflict)
5. Concrete values are FINAL — once a field has a concrete value, it cannot be changed (attempting produces bottom)

Self-enforcing means: **the system cannot be in a state that violates its own constraints.** Not because a separate validator catches violations (that's external enforcement), but because the REPRESENTATION ITSELF makes violations unrepresentable. An element with an invalid symbol doesn't silently exist with the wrong symbol — it fails to exist at all. A compound referencing a nonexistent element doesn't produce a compound with a dangling reference — it produces bottom.

This is the difference between:
- **Dead files**: `system.toml` says `symbol = "In"` and nothing checks it
- **Externally validated files**: A JSON Schema validates `system.toml` after writing
- **Self-enforcing declarations**: The declaration's TYPE is its CONSTRAINT is its VALIDATION. Invalid states are not checked for — they are structurally impossible.

---

## VI. Sources

### Primary Sources (theses, specifications, design documents)

| Source | System | Used For |
|--------|--------|----------|
| Dolstra, "The Purely Functional Software Deployment Model" (PhD thesis, Utrecht, 2006) | Nix | Derivation model, store, purity, closures |
| NixOS Manual: Module System | Nix | evalModules, option types, merge functions |
| nixpkgs/lib/modules.nix, nixpkgs/lib/types.nix source | Nix | Module evaluation algorithm, type merge behaviors |
| Courtès, "Code Staging in GNU Guix" (GPCE'17, arXiv:1709.00833) | Guix | G-expressions, code staging |
| Guix Reference Manual (Service Types and Services) | Guix | Service extension DAG, compose/extend |
| dhall-lang.org specification | Dhall | Type system, totality, imports, normalization |
| Gonzalez, "Design Choices" (dhall-lang.org/discussions) | Dhall | Rationale for restrictions |
| dhall-lang binary encoding standard | Dhall | CBOR format, semantic hashing |
| cuelang.org/docs/reference/spec | CUE | Value lattice, unification, type system |
| van Lohuizen, "The Logic of CUE" (cuelang.org) | CUE | Lattice theory, constraint model |
| van Lohuizen, GopherCon talk on CUE design | CUE | Google Borg/BCL background, why inheritance fails |
| jsonnet.org/ref/spec.html | Jsonnet | Operational semantics, object model, manifestation |
| Cunningham, "Jsonnet Design" (jsonnet.org/articles/design.html) | Jsonnet | Design rationale, Google internal usage |
| HCL specification (github.com/hashicorp/hcl) | Terraform | Language constructs, block model |
| Terraform plugin protocol (developer.hashicorp.com) | Terraform | Provider architecture, gRPC interface |
| Duffy, "Hello, Pulumi!" (joeduffyblog.com, 2018) | Pulumi | Founding rationale, architecture |
| Pulumi architecture docs (pulumi.com/docs/iac/concepts) | Pulumi | Three-layer model, state backends |
| Starlark specification (github.com/bazelbuild/starlark) | Bazel | Language restrictions, freeze mechanism |
| Bazel rules documentation (bazel.build/extending/rules) | Bazel | Three phases, action graph, providers |
| Bazel hermeticity docs (bazel.build/basics/hermeticity) | Bazel | Sandboxing, content addressing, remote execution |

### Secondary Sources (comparative analysis, criticism)

| Source | Used For |
|--------|----------|
| CUE vs Jsonnet discussion (github.com/cue-lang/cue/discussions/669) | Why CUE replaces Jsonnet |
| "The Configuration Complexity Curse" (blog.cedriccharly.com) | Inheritance failure analysis |
| "Why CUE for Configuration" (holos.run/blog) | CUE vs alternatives |
| Terraform vs Pulumi tradeoff analysis (gautierblandin.com) | State management comparison |
| Fzakaria, "Bazel Knowledge: Reproducible Outputs" | Reproducibility mechanisms |

---

## VII. Diagnosis of Current Declaration Files

### system.toml

**Claim**: "Like NixOS configuration.nix — the ENTIRE system described flat."

**Reality**: Has ZERO properties of a NixOS configuration:
- No evaluation semantics (TOML is data, not expressions)
- No type system (string values unconstrained)
- No merge function (cannot compose multiple files)
- No derivation mechanism (nothing is computed from it)
- No validation (compounds can reference nonexistent elements)
- No content addressing (identity is filename, not semantics)

**What it IS**: A well-organized key-value catalog. Accurate as documentation. Inert as governance.

### ARCHITECTURE.md

**Claim**: 8-layer stack with sovereignty cascade.

**Problems**:
- Proposes nested directories: `laws/physics/`, `laws/theory/`, `laws/constitution/` — hierarchy in filesystem
- Layers are DESCRIBED, not CONSTRAINED — nothing enforces the sovereignty cascade
- The directory tree IS the architecture — if the directories don't exist, the architecture doesn't exist
- No evaluation mechanism turns the description into enforcement

**What it should become**: Flat constraint declarations where `governance_level` is an ATTRIBUTE, not a directory depth. The evaluator derives the cascade from the attribute values.

### PERIODIC-TABLE.md

**Status**: Accurate specification of the 10 elements. Well-documented with analogies and compositions.

**What it should become**: Part of the constraint declaration. The 10 elements are the FIXED POINTS of the lattice — the most specific type constraints for operations. Everything else (compounds, formations) constrains RELATIVE TO them.

---

## VIII. Next Steps

This research answers WHAT the declaration should become. Implementation requires:

1. **Install CUE** (`brew install cue`) and prototype the element/compound/formation constraints
2. **Translate system.toml → .cue** preserving all information but adding type constraints, validation, and composition
3. **Add a declaration dimension to immune_verify.py** that reads evaluated CUE output and compares against actual organism state
4. **Derive the signal graph** from the declaration rather than maintaining it as a separate artifact
5. **Git-initialize ~/Workspace/a-organvm/** — it is not currently a git repo
6. **Implement the sovereignty cascade** as CUE constraint specificity with numeric priority

The living organism (sovereign--ground/holds--same/a-organvm/) continues as-is — it is healthy. The declaration layer wraps AROUND it as the specification it validates against.
