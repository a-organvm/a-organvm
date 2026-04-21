# a-organvm Architecture

The full stack, bottom to top. Each layer depends only on the layer below it.

```
┌─────────────────────────────────────────────┐
│  products/          — stable outputs        │  ← what the world sees
├─────────────────────────────────────────────┤
│  formations/        — wired compositions    │  ← aegis, oikonomia, praxis, tessera
├─────────────────────────────────────────────┤
│  compounds/         — named compositions    │  ← assessor, guardian, ledger, etc.
├─────────────────────────────────────────────┤
│  elements/          — 10 irreducible ops    │  ← the periodic table
├═════════════════════════════════════════════┤
│  naming/            — algorithmic identity  │  ← how things get named (protocol, not choice)
├─────────────────────────────────────────────┤
│  schemas/           — data contracts        │  ← what signals look like
├─────────────────────────────────────────────┤
│  enforcement/       — rule execution        │  ← semgrep, semver, linting, validation
├─────────────────────────────────────────────┤
│  laws/              — constitutional ground │  ← axioms, derivations, protocols
├─────────────────────────────────────────────┤
│  intake/            — prima materia         │  ← everything enters here
└─────────────────────────────────────────────┘
```

---

## Layer 0: LAWS (governance stack)

The laws layer is itself a hierarchy. Each sublayer constrains everything below it
and CANNOT override anything above it.

```
laws/
├── physics/             # DISCOVERED truth — the 10 elements exist because
│                        #   signal MUST enter (intake), MUST persist (store),
│                        #   MUST exit (emit). You can't violate these.
│                        #   Source: PERIODIC-TABLE.md (discovered from codebase scan)
│
├── theory/              # WHY the physics works — explanations, proofs, models
│                        #   Isomorphisms, scale invariance, ontological foundations
│                        #   Source: sovereign--ground, system-system--system--monad,
│                        #   scale-threshold-emergence
│
├── constitution/        # CHOSEN foundational contract — the 7 root LAWS of σ_E
│                        #   These are axioms, not discoveries. They could be different.
│                        #   But once chosen, everything derives from them.
│                        #   Source: system-system--system/LAWS.md (7 laws, 9 proofs, 21 derivations)
│
├── declarations/        # IDENTITY statements — who is this system, what does it serve
│                        #   Manifesto, vision, mission, the "a" in a-organvm
│                        #   Source: SPEC-000 (System Manifesto), VISION.md
│
├── amendments/          # GOVERNED additions to the constitution
│                        #   New specs, new instruments, new formations
│                        #   Source: SPEC-025 (institutional primitives), INST-COMPOSITION, etc.
│                        #   Each amendment references which constitutional article it extends
│
├── statutes/            # SPECIFIC operational rules derived from above
│                        #   Naming protocol, promotion state machine, formation crystallization,
│                        #   versioning (semver), schema validation, dependency rules
│                        #   Source: governance-rules.json, INST-FORMATION, naming/PROTOCOL.md
│
└── precedent/           # DECISIONS interpreting the rules in specific cases
                         #   ADRs, the fossil record, IRF resolutions
                         #   Source: docs/adr/, FOSSIL-RECORD.md, INST-INDEX-RERUM-FACIENDARUM.md
```

**Sovereignty cascade**: physics > theory > constitution > declarations > amendments > statutes > precedent.
A statute cannot violate the constitution. An amendment cannot violate physics.
If a formation violates a law, the formation is wrong. If a law contradicts physics, the law is wrong.

---

## Layer 1: SCHEMAS (data contracts)

What signals look like. Every element takes STATE_IN and produces STATE_OUT.
Schemas define the shape of state at every interface.

```
schemas/
├── signal.schema.json       # The universal signal shape
├── element-io/              # Per-element input/output contracts
├── compound-io/             # Per-compound contracts
├── formation-io/            # Per-formation contracts
└── registry.schema.json     # How the registry describes entities
```

Source: `schema-definitions` (existing repo — already has 6 canonical schemas).

---

## Layer 2: ENFORCEMENT (rule execution)

The mechanisms that MAKE the laws and schemas stick.

```
enforcement/
├── validators/          # Schema validators (runtime)
├── linters/             # Semgrep rules, naming checks (static)
├── versioning/          # Semver protocol — how versions advance
├── promotion/           # State machine: LOCAL → CANDIDATE → GRADUATED → ARCHIVED
└── audit/               # Compliance checks against laws + schemas
```

Source: `vox--architectura-gubernatio` (voice governance), `system-governance-framework`
(promotion state machine), `call-function--ontological` (naming validation).

---

## Layer 3: NAMING (algorithmic identity)

**Nothing gets named by human choice. Names are computed from properties.**

### The Protocol

Every entity in the system has a **type** and **properties**. The name is a function:

```
name = NAMING_PROTOCOL(type, properties)
```

### Naming Rules by Type

**Elements**: single lowercase word, the operation itself.
```
intake, store, retrieve, evaluate, transform, synthesize, route, authorize, bind, emit
```
No protocol needed — there are exactly 10 and they're defined.

**Compounds**: element formula as prefix, function as name.
```
${formula}--${function}
Example: In.Ev.Em--assessor     (intake + evaluate + emit = assessor)
Example: In.St.St--ledger       (intake + store + store = ledger)
```

**Formations**: single Latin/Greek noun, the institutional function.
```
aegis, oikonomia, praxis, tessera
```
Named when they crystallize. The crystallization protocol (SPEC-025 COMP-007) governs this.

**Products**: human-readable, market-facing. No formula prefix.
```
public-record-data-scrapper, classroom-rpg-aetheria
```
Products escape the formula naming — they face the world, not the system.

**Repos**: `${domain}--${descriptor}` (existing double-hyphen convention)
```
recursive-engine--generative-entity
tool-interaction--conductor
```

### Variables

Every name is also a resolvable variable:

```toml
# In naming/variables.toml or equivalent
[elements]
In = "intake"
St = "store"
Re = "retrieve"
Ev = "evaluate"
Tr = "transform"
Sy = "synthesize"
Ro = "route"
Au = "authorize"
Bi = "bind"
Em = "emit"

[compounds]
assessor = { formula = "In.Ev.Em", domain = "protective" }
guardian = { formula = "In.Ev.Em.loop", domain = "protective" }
ledger   = { formula = "In.St.Re", domain = "economic" }

[formations]
aegis     = { compounds = ["guardian", "assessor", "counselor", "mandator", "archivist"] }
oikonomia = { compounds = ["ledger", "appraiser", "optimizer", "allocator", "collector", "auditor"] }

[system]
org       = "a-organvm"
workspace = "organvm"
corpus    = "organvm-corpvs-testamentvm"
engine    = "organvm-engine"
```

Everything resolves. Change `system.org` from `a-organvm` to something else →
every reference updates. Like chezmoi templates for the whole system.

### Astronomical Analogy

| Astronomy | a-organvm |
|-----------|-----------|
| Star discovered → Bayer designation (α Centauri) | Element discovered → symbol assigned (In, St, Re...) |
| Planet → parent star + letter (Kepler-22b) | Compound → formula + function (In.Ev.Em--assessor) |
| Asteroid → number + proposer name | Formation → crystallization number + Latin noun |
| Comet → discoverer + year + letter | Product → market name (human choice, the only exception) |

The system names itself. You don't think about it. The protocol determines.

---

## Layer 4-7: ELEMENTS → COMPOUNDS → FORMATIONS → PRODUCTS

(Already defined in PERIODIC-TABLE.md and BLUEPRINT.md)

---

## Cross-Layer: RESEARCH

Theoretical investigation that feeds ALL layers:

```
research/
├── isomorphisms/        # Structural invariants (from sovereign--ground)
├── scales/              # Scale-invariant properties (from system-system--system)
├── primitives/          # Primitive discovery research (from monad worktree)
├── ontology/            # Ontological foundations
└── logic/               # Formal logic, proofs, verification
```

This is where `system-system--system`, `sovereign--ground`, and
`system-system--system--monad` live. They're not elements or compounds —
they're the RESEARCH that discovers the laws the system operates under.

---

## The Full Blueprint (updated)

```
a-organvm/
├── PERIODIC-TABLE.md
├── FOSSIL-RECORD.md
├── fossil-record.json
├── BLUEPRINT.md
├── ARCHITECTURE.md         ← this file
│
├── laws/                   # Layer 0: governance stack (sovereignty cascade)
│   ├── physics/            #   discovered truth (the 10 elements)
│   ├── theory/             #   why physics works (isomorphisms, proofs)
│   ├── constitution/       #   chosen axioms (the 7 LAWS of σ_E)
│   ├── declarations/       #   identity + intent (manifesto, vision)
│   ├── amendments/         #   governed additions (new specs)
│   ├── statutes/           #   operational rules (protocols, naming, promotion)
│   └── precedent/          #   case law (ADRs, decisions, fossil record)
│
├── schemas/                # Layer 1: data contracts
│   └── signal.schema.json
│
├── enforcement/            # Layer 2: rule execution
│   ├── validators/
│   ├── linters/
│   ├── versioning/
│   ├── promotion/
│   └── audit/
│
├── naming/                 # Layer 3: algorithmic identity
│   ├── PROTOCOL.md
│   ├── variables.toml
│   └── templates/
│
├── elements/               # Layer 4: 10 irreducible operations
│   ├── intake/
│   ├── store/
│   ├── retrieve/
│   ├── evaluate/
│   ├── transform/
│   ├── synthesize/
│   ├── route/
│   ├── authorize/
│   ├── bind/
│   └── emit/
│
├── compounds/              # Layer 5: named element compositions
├── formations/             # Layer 6: wired compound compositions
│   ├── aegis/
│   ├── oikonomia/
│   ├── praxis/
│   └── tessera/
│
├── products/               # Layer 7: stable external outputs
├── intake/                 # Layer -1: prima materia entrance
└── discovery/              # THE FRONTIER — runs parallel to ALL layers
    ├── ocean/              #   below: undiscovered sub-elements?
    ├── sky/                #   above: undiscovered super-formations?
    └── horizon/            #   the edge: open questions, anomalies, hypotheses
```

---

## The Discovery Layer

Discovery is not a phase. It is permanent. It runs ALONGSIDE every other layer
like the ocean runs below the ground and space runs above it.

The 10 elements are a current best theory. There might be 9. There might be 12.
The 4 formations are pressure-crystallized predictions. Others will emerge.
The 7 governance sublayers are modeled on human legal systems — structures we
haven't imagined yet may exist.

```
discovery/
├── ocean/              # Below: what exists beneath the elements?
│                       #   Sub-elemental operations? Are some elements compounds?
│
├── sky/                # Above: what exists beyond formations?
│                       #   Do formations compose into something larger?
│                       #   What emerges from the singularity property?
│
└── horizon/            # The edge: open questions under investigation
                        #   Hypotheses being tested. Anomalies that don't fit.
                        #   Things found during scans that resist classification.
```

Everything in `discovery/` is provisional. Promoted into the proper layer
when understood. Dissolved when refuted. The frontier never closes.
