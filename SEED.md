# SEED

A generative grammar for computational organisms.

This document is DNA, not a blueprint. It does not describe what the organism
will become. It describes how the organism grows. The final form is not
predetermined — it is emergent from the work the organism does and the
environment it inhabits.

It has no memory of what produced it. It references no specific system, project,
or history.

Every structural decision the organism makes — what to build, what to name it,
where to put it, what to connect it to — is derived from axioms through formal
procedures at the moment the decision is needed. Nothing is decided before it
is needed. Nothing is named before it exists.

Place this file in an empty directory. Begin working. The organism grows.

---

## 0. Axioms

Nine assertions. The only things taken without proof.

**A1 — Purpose.** The organism exists to do work. Work is the transformation
of inputs into outputs.

**A2 — Composition.** The output of one transformation can serve as the input
of another.

**A3 — Persistence.** The organism must maintain itself over time. It must not
decay into disorder without external intervention.

**A4 — Adaptation.** The organism must modify its own structure and behavior
in response to change.

**A5 — Minimality.** No structural element exists without a derivable reason.
If a structure can be removed without violating any axiom, it must be removed.
A7 overrides A5 when they conflict: the operator's needs are the terminal
authority. Minimality serves the operator; the operator does not serve
minimality.

**A6 — Organizational Closure.** The organism's governance governs itself.
The rules that constrain growth are subject to the same constraints.

**A7 — Individual Primacy.** The organism exists to serve the individual who
operates it. No structural optimization may override this purpose.

**A8 — Topological Plasticity.** The organism's structural organization is a
governed variable, not a frozen constant. Mechanisms may fuse, split, or
dissolve through governed evolution.

**A9 — Alchemical Inheritance.** When any structural element is dissolved, its
lineage must be preserved. Dissolution does not erase history.

---

## I. The One Structural Constraint

### Theorem 1: Depth

*All other structural parameters emerge from work. Depth does not. It is
derivable before the first function exists, because it concerns where things
live, not what they are.*

**Claim:** Optimal filesystem depth is 1 (all items are siblings in one
directory).

**Proof from A5 (minimality):**

Let D = directory levels below the instance root.

At D = 0: Undefined. A named item needs a container + a name = depth 1 minimum.

At D = 1: One classification decision — the name. If the naming convention
encodes all necessary classification, no further depth is needed.

At D > 1: Each intermediate directory is a classification choice. This either
(a) duplicates information the name already carries (violates A5), or
(b) introduces classification the name lacks (fix the name, not the depth — a
longer name is O(1), a deeper tree is O(D)).

Therefore D = 1 is the unique minimum.  **∎**

**Scaling note.** At 30+ functions, flat `ls` output becomes cognitively dense.
The operator may use filesystem views — symlinks, shell aliases, filtered
listings (`ls nervous--*`), IDE groupings — to navigate the flat namespace.
These views carry no ontological weight. They are presentation, not structure.
The canonical layout remains flat. The mechanism prefix provides natural
grouping: alphabetical sort clusters by system (A7: the organism serves the
operator's navigability needs without compromising structural integrity).

The instance is one directory. Everything inside it is a sibling.

```
INSTANCE/
├── {name}.ext          # function or config — as needed
├── {name}/             # product — when physics demands a directory
├── signal-graph.yaml   # wiring — created with first function
├── SEED.md             # this file
└── .gitignore
```

---

## II. How to Grow

The organism starts empty. Growth is driven by work. Every growth event
follows these procedures.

### Procedure 1: When you need to do something

You have work to do. No existing function does it.

**Step 1 — Define the transformation.**

What does it take in? What does it put out? Express this as a signal signature:

```
f : {input types} → {output types}
```

Signal types are not prescribed. They are discovered. A signal type is any
qualitatively distinct kind of information the organism exchanges. When you
encounter a new kind of input or output that does not match any existing type,
you have discovered a new signal type. Name it. Add it to the vocabulary.

*The first function's inputs and outputs bootstrap the signal type vocabulary.
There is no predetermined list.*

Also declare the function's **temporal mode** — when does it execute?

| Mode         | When it fires |
|--------------|--------------|
| event-driven | On occurrence of a triggering event |
| periodic     | At regular intervals |
| continuous   | Always running |
| on-demand    | When explicitly invoked by the operator |

The temporal mode is part of the signal signature: `f : {inputs} → {outputs} @ {mode}`.
It is needed in Step 3 for mechanism classification.

**Step 1a — Classify the ontological type.**

What kind of thing are you creating? Seven categories, informed by formal
ontology (BFO, DOLCE, mereological analysis), are stipulated as the primitive
vocabulary for any system that does work (A1) on persistent structures (A3).
They are not derived from A1 and A3 alone — they are adopted from prior
ontological research and asserted as the organism's classification grammar.
If a category is shown to be reducible or a missing category is identified,
the set evolves through governed extension (§VII).

| Type       | What it is |
|------------|-----------|
| Entity     | persistent object with identity |
| Value      | property of an entity |
| Relation   | typed connection between entities |
| Event      | occurrence that changes state |
| State      | configuration of entities at a point in time |
| Constraint | rule limiting valid states |
| Capability | authorized transformation |

Classification procedure (follow in order — first match wins):

```
1. Does it persist independently with its own identity?     → Entity
2. Does it attach to an Entity as a measurable property?    → Value
3. Does it connect two Entities as a typed link?            → Relation
4. Does it describe a point-in-time configuration?          → State
5. Does it limit what States are valid?                     → Constraint
6. Does it record something that happened?                  → Event
7. Does it authorize a transformation from input to output? → Capability
```

Two developers classifying the same element must arrive at the same type. If
they diverge, the predicates above are applied in order until agreement. The
classification determines how the element behaves under evolution (A4), what
identity discipline applies (A9), and what constraints bind it (A6).

**Step 2 — Determine if it needs a directory.**

Does this work require heterogeneous physical assets (images, binary files,
content collections, compiled artifacts)?

- **No** → it is a **function** (a file). It contains logic only.
- **Yes** → it is a **product** (a directory). It contains assets and declares
  which functions it composes. It does not contain logic.

**How products compose functions.** A product's root contains a `compose.yaml`
declaring which function files it depends on. The execution substrate (CHECK 17)
determines how composition is realized — options include: build step (functions
run, output deposited into product directory), runtime import (product code
references function modules), or orchestration (product manifest triggers
functions at deploy time). The SEED does not prescribe the runtime mechanism.
It prescribes that composition is declared, not implicit.

This is a physical question, not a classification question. There is no
judgment call.

**Step 3 — Classify it.**

What *mechanism* does this function serve? Not what *purpose* (that comes
later, from the signal graph), but what *kind of work* is it?

A mechanism is a class of computational operation. The organism discovers its
mechanisms as it grows. The procedure for determining whether a function
belongs to an existing mechanism or reveals a new one:

```
For each existing mechanism m:
  Does f's (input class, output class, temporal mode) match m's
  characteristic tuple?

If match: f belongs to mechanism m.
If no match: f reveals a new mechanism. Name it. Add it to the vocabulary.
```

For the first function, the mechanism IS whatever the function reveals. There
are no peers to compare against. Name it descriptively from its characteristic
tuple. The granularity rule (below) activates when the second function arrives.

Mechanism names are the organism's own vocabulary. They are not prescribed.
When the organism is young and has one function, it has one mechanism. As it
grows, mechanisms differentiate.

Granularity rule: a mechanism is the **coarsest** classification that still
distinguishes all its functions by verb alone. If two functions share both a
mechanism and a verb, the mechanism is too coarse — split it. If a mechanism
contains only one function and could merge with a sibling mechanism without
losing verb-level distinction, the mechanism is too fine — merge it. This
makes granularity derivable, not chosen.

*However*: biology has solved the persistence + adaptation problem over 3.5
billion years. Biological organ systems are a known-good vocabulary for
mechanisms in persistent, adaptive systems. When a mechanism is discovered,
check whether a biological analog exists. If it does, adopt the biological name
(nervous, digestive, circulatory, etc.). This is not a mandate — it is a
recognition that convergent evolution produces convergent names.

**Step 4 — Name it.**

```
name = {mechanism}--{verb}.{ext}
```

- mechanism = from Step 3
- verb = imperative form of the dominant operation (what it *does*)
- ext = file format

The name is not chosen. It is assembled from the classification (Step 3)
and the declared operation. If two functions would produce the same name,
they are either redundant (merge them — A5) or under-specified (refine the
verb).

**Step 5 — Connect it.**

The signal graph (`signal-graph.yaml`) is the organism's self-awareness. It is
not bookkeeping — it is the organism perceiving itself. Every function is in it.
Every function can read it. The graph is both the territory and the map: the
compressed image of the whole that every part can access. When a function reads
the graph, it locates itself, senses its relations, inherits its history
(evolution edges), and sees the shape of the entire organism. This is how
structure becomes sensation — not through a separate observability layer, but
through the signal graph being simultaneously the wiring AND the world model.

It is created with the FIRST function (not the second), because even one
function has a signal signature that must be recorded. The schema:

```yaml
# signal-graph.yaml — the organism's wiring diagram
signal_types:
  TYPE_NAME:
    description: "what this signal type carries"
    discovered_by: function-that-first-emitted-or-consumed-it

functions:
  mechanism--verb:
    inputs: [TYPE_A, TYPE_B]
    outputs: [TYPE_C]
    mechanism: mechanism-name
    temporal_mode: event-driven | periodic | continuous | on-demand
    ontological_type: Entity | Value | Relation | Event | State | Constraint | Capability
    traceability:
      upward: "axiom or capability gap this serves"
      downward: "artifacts and outputs this produces"

edges:
  dependency: []    # must be acyclic (DAG)
  information: []   # must contain ≥1 cycle (when ≥3 functions exist)
  governance: []    # hierarchical, flows from genome downward
  evolution: []     # temporal, records structural change

products:
  mechanism--name:
    composes: [function-a, function-b]
    assets: "description of physical contents"
```

For the first function, create this file with one entry in `functions:`,
its signal types in `signal_types:`, and empty edge lists.

For subsequent functions:

**5a — Classify edge type.** Every connection is one of four independent
relationship types:

| Edge type    | What it means |
|--------------|---------------|
| dependency   | what must exist before what can be built |
| information  | what signals flow where at runtime |
| governance   | what constrains what |
| evolution    | what changes what over time |

These must not collapse into one graph (see Law 4, §IIIa).

**5b — Validate the signal.** A signal is valid only if:

1. its type is declared in the vocabulary
2. its producer is identifiable
3. its intended receiver type is lawful
4. its schema or structure is legible
5. its interpretation burden is defined (the receiver knows what to do with it)

**5c — Check prohibited couplings.** See Law 1 (§IIIa). No connection may
create a prohibited pattern.

**5d — Declare direction.** Every signal flow is one of:

- **Feedback** — downstream to upstream: error, constraint, evidence, failure,
  performance mismatch, or semantic ambiguity. Feedback proposes correction.
  It may not silently rewrite upstream structure.
- **Feedfront** — upstream to downstream: primitives, schemas, methods,
  aesthetic seeds, coordination patterns. Feedfront may condition downstream
  work but may not bind it as canonical unless canonical law ratifies the signal.

**5e — Route for preservation.** If the output is intended for reuse, it must
route to at least one preservation function. Unrouted reusable output is a
structural defect (A3: persistence requires memory).

**5f — Declare external dependencies.** If the function depends on anything
outside the organism — libraries, APIs, databases, network services, operating
systems — declare these as **boundary signals** in `signal-graph.yaml`. A
boundary signal has type EXTERNAL, a named source (the external system), and
a direction (inbound or outbound). The signal graph records the dependency but
does not govern the external system. The organism's governance extends to its
boundary, not beyond it.

External code that is vendored (copied into the organism's directory) is NOT
a function. It has no signal signature, no mechanism classification, no name
in the `{mechanism}--{verb}` convention. It is a dependency of a function,
declared in that function's boundary signals. Vendored code inflates line
counts and obscures the organism's actual size. CHECK 10 (WASTE) should
surface vendored directories that are not declared as boundary dependencies.

Record all connections in `signal-graph.yaml`.

**Step 6 — Assert traceability.**

The function must trace in both directions:

- **Upward** — to the constitutional purpose it serves. State the specific
  capability gap: "I need this function because no existing function does X."
  This must be non-trivially stated even for the first function. "The organism
  needs to do work" (A1) is not sufficient. "The organism has no way to read
  its own structure" is sufficient.
- **Downward** — to the actual artifacts, outputs, and effects it produces.
  Name them concretely.

A function without upward trace is ungrounded. A function without downward
trace is theoretical debris. Neither is a legitimate structural element (A5).

**Step 7 — Evaluate the function.**

Before running organism-wide health checks, evaluate the function itself on
six dimensions. These assess the function's individual quality, not the
graph's structural integrity:

| Dimension | Question |
|-----------|----------|
| Ontological Legibility | Is its role and output type clear to a stranger? |
| Signal Utility | Does it emit anything usable by the organism? |
| Boundary Discipline | Does it remain within its declared scope? |
| Modulation Safety | Does it couple without destabilizing others? |
| Yield | Does it produce reusable output — not just activity? |
| Migration Worthiness | Has it generated anything canonically significant? |

A function failing legibility or boundary discipline is structurally unsound.
Fix before proceeding.

**Step 8 — Validate.**

Run the health checks (§IV). If any fail, the growth event introduced a
structural defect. The check identifies the defect. Fix it before continuing.

### Procedure 2: When something breaks or decays

The organism detects problems through its health checks (§IV). When a check
fails, the failure identifies what is wrong:

- A function with no connections → either connect it or remove it (A5)
- A signal type with no emitter → something is missing; what should produce it?
- A dependency cycle → break the cycle; which function should be built first?
- An information graph with no cycles → feedback is missing; where should
  execution outcomes feed back into governance?

Each failure is a diagnostic. The fix is derivable from the failed predicate.

**Self-test (BIST).** The organism can run its own health checks without
operator intervention. On startup, on schedule, or on-demand, the organism
walks its signal graph, runs CHECK 18 (integration) on every active edge,
and surfaces any dead connections as REPORT signals. This is the built-in
self-test: the organism probes its own wiring and tells the operator what's
broken before the operator has to guess. An organism that cannot self-test
cannot self-correct (A4).

**Reversal.** When a growth event introduces a defect that cannot be fixed by
the procedures above, the growth event may be reversed: the function is
removed, the signal graph is restored to its pre-event state, and the reversal
is recorded in the evolution edge family (A9: lineage is preserved even for
failed growth). Reversal is a governed dissolution, not an undo — the organism
remembers what was tried and why it was rolled back.

### Procedure 3: When something changes

A function renamed is the same function (its identity is its unique identifier,
not its name — see §III). Update the name. Update the graph. The identity
persists.

A function whose signals change may need reclassification. Re-run Step 3 of
Procedure 1. If the mechanism changes, the name changes. This is the organism
adapting (A4).

A mechanism that no function serves is dead tissue. Remove it from the
vocabulary. The organism has shed what it no longer needs (A8).

When a function is dissolved, its lineage record persists. What it was, what it
produced, and why it was removed remain part of the organism's history (A9).

### Procedure 4: When something moves

When an output, method, or structural element moves from one part of the
organism to another (or from experimental to canonical status), migration law
governs. Five modes:

| Mode         | What moves |
|--------------|-----------|
| EXTRACTIVE   | Only a specific output is absorbed |
| METHODIC     | The function's method becomes standard practice |
| STRUCTURAL   | The organism gains a new internal law or mechanism |
| PEDAGOGICAL  | The output enters teaching or explanatory canon |
| ARCHIVAL     | The function becomes preserved reference without live authority |

Migration conditions — an output may be migrated only if it is:

1. repeatable (not a one-time accident)
2. traceable (ancestry chain reaches the axioms)
3. cross-context useful (or constitutionally necessary)
4. non-accidental (intentionally produced)
5. expressible in canonical terms (the organism's vocabulary can describe it)

No function becomes canonical merely by scale, complexity, novelty, or
philosophical ambition. Canonicalization requires explicit review.

### Procedure 5: When you digest a predecessor

If the organism inherits material from a dead or dying system, it must not
absorb that material whole. The predecessor's self-description (its READMEs,
its governance files, its metadata) is the dead organism's story about itself.
That story is contaminated by the biases, proliferation patterns, and
structural errors that killed it.

**The stranger test.** Read only source code, git history, and test files.
Ignore all metadata, documentation, and governance files. For each unit of
inherited material, produce a stranger report:

```
name:        {whatever it is called}
does:        {one verb — derived from reading actual code, not docs}
consumes:    {actual imports — what it reads from outside itself}
produces:    {actual exports — what it makes available}
alive:       {true/false — has the code changed recently? do tests pass?}
metabolizes: {true/false — does it transform input→output, or just exist?}
lines:       {hand-written source only — exclude vendored, generated, venv}
```

**Triage.** The stranger reports sort material into shapes:

| Shape | Signature | Action |
|-------|-----------|--------|
| Living | lines > threshold, alive = true, metabolizes = true | Decompose into functions. These ARE the organism. |
| Embryo | lines > 0, alive = false or metabolizes = false | Harvest the idea into a living function's purpose. Archive the shell. |
| Ghost | lines = 0, governance files present | The governance was a wish. Nothing to extract. Archive. |
| Isotope | does = same verb as another unit | Fuse into the stronger twin. Preserve lineage (A9). |
| Scaffold | lines = 0, boilerplate only | Remove. Boilerplate is not energy. |
| Misplaced | code that belongs in another unit | Extract. Relocate to where the code belongs. |

**Two-pass separation.** Pass one: uncontaminated observation (stranger
reports). Pass two: constitutional analysis of observations (apply the SEED's
procedures to the living material). The observer does not know the law. The law
does not read the predecessor's self-description. They never mix.

### Procedure 6: When you examine anything

The organism can examine any function, mechanism, product, or structural
decision through seven diagnostic dimensions. This is the structural
interrogation — a universal diagnostic for discovering hidden problems:

| Dimension  | Question |
|------------|----------|
| Existence  | What must exist for this to exist? What is missing? What is illegitimate? |
| Identity   | What is it? What makes it distinct? When does it cease to be itself? |
| Structure  | How is it arranged? What depends on what? |
| Law        | What governs it? Are the governing rules consistent? |
| Process    | How does it change? What transitions are illegal or undefined? |
| Relation   | How does it affect other things? What affects it? |
| Teleology  | What is it for? Does its purpose align with the organism's purpose? |

If a subject cannot answer all seven clearly, it is structurally incomplete.
The unanswered dimension identifies the gap.

---

## III. Structural Properties

These are not rules imposed on the organism. They are properties that emerge
from the axioms. Violating them violates an axiom.

### From A1 (purpose):

Every function declares a signal signature: `f : {inputs} → {outputs}`.
A function without declared inputs and outputs has no defined work. It is
not a function (violates A1).

### From A2 (composition):

**Composability.** f∘g is valid iff `output(g) ∩ input(f) ≠ ∅`.
This is set intersection. It is computable.

### From A3 (persistence):

**Closed circulation.** For every signal type t in the organism:
`(∃f : t ∈ output(f)) ∧ (∃g : t ∈ input(g))`.
Dead emissions (no receiver) and starving inputs (no emitter) violate
persistence. They are structural defects, not design choices.

**Acyclic dependencies.** The build-order graph (what must exist before what)
must be acyclic. A cycle means nothing can be built first. The organism
cannot bootstrap.

**Reservoir law.** Functions whose mechanism is preservation (memory, archival)
may not emit RULE-class or KNOWLEDGE-class signals as canonical authority.
If memory governs, governance becomes unauditable. Persistence requires
knowing what governs you.

**Attenuation.** Connections between functions must declare coupling intensity.
Unregulated coupling produces turbulence that degrades persistence.

| Policy       | Behavior |
|--------------|----------|
| none         | Full intensity |
| threshold    | Fires above a declared value |
| review-gated | Requires approval |
| buffered     | Queued, delivered in batches |
| scheduled    | Passes at declared intervals |

### From A4 (adaptation):

**Cyclic information.** The signal flow graph must contain at least one cycle.
Execution traces must feed back into governance. Without feedback, the organism
executes but never learns. A4 is violated.

**Identity separation.** Three layers, always distinct:

| Layer        | Nature   | Why |
|--------------|----------|-----|
| Identity     | Stable   | Without persistent identity, adaptation destroys continuity (violates A3) |
| Expression   | Mutable  | Name, path, format change during adaptation. Identity cannot depend on them. |
| Relationship | Versioned | Connections evolve. Track the evolution. |

### From A5 (minimality):

**Container decoupling.** The directory, repository, or organization a function
lives in carries no classification information (Theorem 1: the name carries
it all). Therefore containers carry no ontological weight.

**Products contain no logic.** A product carries assets. Logic lives in
function files. If a product contained logic, that logic would be structurally
invisible to the signal graph (hidden inside a directory, not a named sibling).
Hidden structure violates A5.

**Waste detection.** The organism must detect:

| Waste condition | How to detect |
|-----------------|---------------|
| Isolated function | degree(f) = 0 in signal graph |
| Stale function | last_modified(f) > threshold |
| Dead edge | target ∉ function set |
| Orphan product | composition references missing functions |
| Unemitted signal type | no function outputs it |
| Unconsumed signal type | no function inputs it |

Detection surfaces waste. The operator decides what to keep.

### From A6 (organizational closure):

**Self-governance.** The health checks check themselves. The naming convention
names itself. The signal graph graphs itself. Any governance mechanism that
exempts itself from its own constraints is structurally invalid. The genome
(this document) is subject to its own evolution law (§VII).

### From A7 (individual primacy):

**Purpose alignment.** No structural optimization may override the purpose of
serving the individual who operates the organism. System efficiency that
reduces operator capability is a structural defect, not an improvement.

### From A8 (topological plasticity):

**Governed reorganization.** Functions may reorganize, mechanisms may fuse,
split, or dissolve — all through governed evolution. The organism's topology
is never frozen. Any structural element that cannot be changed through a
governed process has become a structural pathology (it has escaped governance).

### From A9 (alchemical inheritance):

**Lineage preservation.** When a function is removed, renamed, merged, or
split, its identity chain must be preserved: what it was, what it produced,
why it changed. The organism's memory of its own history is part of its
structural identity. Dissolution without lineage is amnesia.

---

## IIIa. Structural Laws

Seven laws derived from the axioms. These are universal constraints — not
per-growth-event procedures (those are in §II) but structural patterns that
must hold across the entire organism at all times.

### Law 1 — Prohibited Couplings

Seven structural patterns that violate the axioms. Their presence in the signal
graph is always a defect, regardless of the organism's age or complexity.

| Prohibition | Violated axiom |
|-------------|---------------|
| Unbounded mutual recursion between functions | A3 (persistence — infinite loops degrade the organism) |
| Silent mutation of upstream structure by downstream tooling | A6 (closure — governance must be auditable) |
| Preservation layers acting as hidden governance authority | A6 (closure — memory is not law) |
| Routing functions inventing theory or canonical knowledge | A1 + A5 (purpose + minimality — routers route, they do not create) |
| Experimental functions bypassing review to become canonical | A6 (closure — canonicalization requires explicit governance) |
| Presentation layers redefining the organism's foundation | A6 (closure — the boundary does not define the interior) |
| Governance exceeding the complexity of what it governs | A5 (minimality — governance serves function, not the reverse) |

### Law 2 — Feedback and Feedfront

Two distinct modes of signal flow, each with its own governance:

**Feedback** (downstream → upstream) is lawful when it returns: error,
constraint, evidence, performance mismatch, semantic ambiguity, or operational
failure. Feedback may propose correction but may not silently rewrite upstream
structure.

**Feedfront** (upstream → downstream) is lawful when it emits: primitives,
schemas, methods, aesthetic seeds, coordination patterns, or conceptual
operators. Feedfront may condition downstream work but may not bind it as
canonical unless canonical law already ratifies the signal.

The organism must distinguish these. They carry different attenuation policies
and different authority levels.

### Law 3 — Signal Preservation

All outputs intended for reuse must route to at least one preservation
function. Unrouted reusable outputs are ephemeral — they will be lost when the
producing function changes or dissolves. This violates A3 (persistence) and A9
(inheritance).

### Law 4 — Multiplex Flow

The organism maintains at least four independent relationship types on its
function set. These are different KINDS of edges, not different instances of
one kind:

| Edge family  | What it governs | Admissibility rule |
|--------------|-----------------|-------------------|
| Dependency   | What must exist before what can be built | Must be acyclic (DAG) |
| Information  | What signals flow where at runtime | Must contain at least one cycle |
| Governance   | What constrains what | Hierarchical — flows from genome downward |
| Evolution    | What changes what over time | Temporal — records structural change |

These must not collapse into one graph. A dependency edge and an information
edge between the same two functions carry different semantics. Collapsing them
contaminates every downstream analysis.

### Law 5 — Structural Interrogation

Any function, mechanism, product, or structural decision can be examined
through the seven diagnostic dimensions defined in Procedure 6 (§II). If a
subject cannot answer all seven clearly, it is structurally incomplete.

This is not a per-event procedure — it is a standing diagnostic capability.
The organism must be able to interrogate itself at any time. An organism that
cannot examine its own structure cannot adapt (violates A4).

### Law 6 — Meta-Evolution

The organism distinguishes four evolutionary strata. Higher strata require
greater governance rigor because they have wider blast radius.

| Stratum | What changes | Examples | Governance |
|---------|-------------|----------|-----------|
| State | Variables and metrics | Counts, scores, health values | Routine — no review |
| Structure | Relationships and topology | Functions reorganized, mechanisms split | Governed review (A8) |
| Ontology | Classification schemes | New categories, taxonomy splits, mergers | Constitutional review |
| Meta-Evolution | The rules of change themselves | New governance policies, new health checks, new axioms | Highest review — the genome changes (§VII) |

The organism may modify its own evolution rules, but each modification must be
traceable to constitutional warrant. Self-modification without governance is
cancer, not adaptation.

### Law 7 — Concurrency

Growth events are atomic. The signal graph (`signal-graph.yaml`) is a shared
mutable resource. Concurrent mutation without coordination violates A3
(persistence — the organism's self-knowledge becomes inconsistent).

If multiple operators or agents grow the organism simultaneously, growth must
be serialized through a coordination mechanism. That mechanism is itself a
function of the organism (mechanism: nervous, verb: coordinate or serialize).
It emerges when the organism first encounters concurrent growth — which is
itself a health check failure (conflicting signal-graph.yaml states) that
Procedure 2 diagnoses and resolves.

---

## IV. Health Checks

All structural properties are decidable. Each is computable from the
filesystem and `signal-graph.yaml`. Run them after every growth event.

Governance scales with the organism. Not all checks apply at birth:

| Activation     | Checks |
|----------------|--------|
| From function 1 | 1 (FLAT), 2 (NAMED), 3 (SIGNED), 11 (GENOME), 16 (VERIFIED), 17 (EXECUTION) |
| From function 2 | + 5 (ACYCLIC), 7 (CONNECTED), 12 (VALID), 15 (TRACED), 18 (INTEGRATION) |
| From function 3 | + 4 (CIRCULATING), 6 (CYCLIC), 13 (PROHIBITED), 14 (MULTIPLEX), 19 (CIRCULATION), 20 (RESILIENCE) |
| When relevant   | 8 (RESERVOIR — when memory-class exists), 9 (PRODUCT — when products exist), 10 (WASTE — at operator's cadence) |

```
CHECK 1 — FLAT
  ∀ items at instance root: depth = 1 (excluding product internals)
  Violation → something was nested. Move it to root. Rename if needed.

CHECK 2 — NAMED
  ∀ functions f: name(f) = {mechanism}--{verb}.{ext}
  Violation → name does not reflect classification. Re-derive (Procedure 1, Steps 3-4).

CHECK 3 — SIGNED
  ∀ functions f: f has declared (inputs, outputs) in signal-graph.yaml
  Violation → function exists without signal signature. Declare it.

CHECK 4 — CIRCULATING
  ∀ signal types t: (∃f: t ∈ output(f)) ∧ (∃g: t ∈ input(g))
  Violation → dead or starving signal type. Add the missing emitter/consumer or
  remove the type.

CHECK 5 — ACYCLIC DEPENDENCIES
  topological_sort(dependency_graph) succeeds
  Violation → circular build dependency. Identify the cycle. Break it.

CHECK 6 — CYCLIC INFORMATION
  ∃ at least one cycle in the information graph
  Violation → no feedback path. The organism cannot learn from its own execution.
  Add a feedback connection.

CHECK 7 — CONNECTED (applies when |functions| ≥ 2)
  ∀ functions f: degree_in(f) > 0 ∧ degree_out(f) > 0
  Violation → orphan function. Connect it or remove it (A5).
  Note: a single-function organism is exempt. The first function has no
  peers to connect to. CHECK 7 activates when the second function arrives.

CHECK 8 — RESERVOIR LAW
  ∀ functions f where mechanism = memory-class:
    {RULE, KNOWLEDGE} ∩ canonical_output(f) = ∅
  Violation → memory function governing. Remove canonical authority from output.

CHECK 9 — PRODUCT PURITY
  ∀ products p: p contains no logic files at root level
  Violation → logic inside a product. Extract to a named function sibling.

CHECK 10 — WASTE
  Report all waste conditions from §III.
  Any non-empty result → review and resolve.

CHECK 11 — GENOME INTEGRITY
  SEED.md exists. Its hash matches the last recorded hash (or evolution was
  formally applied per §VII).
  Violation → unauthorized genome modification.

CHECK 12 — SIGNAL VALIDITY
  ∀ signals s in active connections:
    type(s) declared ∧ producer(s) identifiable ∧ receiver(s) lawful ∧
    schema(s) legible ∧ interpretation(s) defined
  Violation → invalid signal in the graph. Declare the missing properties.

CHECK 13 — PROHIBITED COUPLINGS
  No prohibited coupling pattern from Law 1 (§IIIa) exists in the signal graph.
  Violation → structural prohibition violated. Identify the pattern. Break it.

CHECK 14 — MULTIPLEX SEPARATION
  Dependency, information, governance, and evolution edges are tracked as
  independent relationship types, not collapsed into one graph.
  Violation → edge types conflated. Separate them.

CHECK 15 — TRACEABILITY
  ∀ functions f:
    upward_trace(f) reaches a constitutional purpose or axiom ∧
    downward_trace(f) reaches at least one artifact or output
  Violation → ungrounded or unproductive function. Establish the missing trace.

CHECK 16 — FUNCTIONAL VERIFICATION
  ∀ functions f with a declared signal signature:
    f has at least one verifiable example: given this input, it produces
    this output. The example is the minimum unit of functional proof.
  Violation → unverified function. Add at least one input→output demonstration.
  Note: this does not prescribe a test framework. It requires that the organism
  can demonstrate its functions work, not merely that they are correctly wired.

CHECK 17 — EXECUTION SUBSTRATE
  The organism declares how signal flow is realized. The signal graph describes
  potential connections. Actual flow requires an execution context — a runtime,
  a build system, a scheduler, or manual invocation. The execution substrate
  must respect: signal directions, attenuation policies, prohibited couplings,
  and multiplex edge separation.
  Violation → the organism has a signal graph but no way to run it. Declare the
  execution substrate (even if it is "manual invocation by the operator").

CHECK 18 — INTEGRATION (the strand)
  For every information edge (f → g) in the signal graph:
    f actually produces an output that g actually consumes. Not declared —
    DEMONSTRATED. Run f, capture its output, feed it to g, verify g processes
    it without error. This is the continuity test: does current flow through
    the wire, or is the connection declared but dead?
  Violation → declared connection that does not carry signal. Either the
  producer's output format changed, or the consumer's input expectations
  drifted. Fix the interface or remove the edge.
  Activation: when |functions| ≥ 2 and at least one information edge exists.

CHECK 19 — CIRCULATION (the full cycle)
  At least one complete signal cycle executes end-to-end:
    f₁ → f₂ → ... → fₙ → f₁ (where the chain follows information edges
    and the final output feeds back to the first function's input).
  This is the system test: does the tree light up? Not each bulb individually
  (CHECK 16), not each strand (CHECK 18), but the whole display.
  Violation → the organism has functions and connections but no demonstrated
  end-to-end cycle. The information graph says feedback exists; this check
  proves it flows.
  Activation: when |functions| ≥ 3 and CHECK 6 (CYCLIC) passes.

CHECK 20 — RESILIENCE
  A failing function does not kill the signal graph. The organism must
  demonstrate that when one function errors, raises, or produces no output:
    (a) other functions continue to operate (circuit breaker pattern)
    (b) the failure is recorded in the signal graph as a REPORT signal
    (c) the operator is informed (the failure is visible, not silent)
  This is not a design prescription — it is a survivability test. HOW the
  organism achieves resilience (try/except, process isolation, queue retry,
  manual intervention) is its own business. THAT it achieves it is required
  by A3 (persistence: the organism must not decay from a single failure).
  Activation: when |functions| ≥ 3.
```

Checks 1–17 verify STRUCTURE (is the organism correctly wired?).
Checks 18–20 verify SIGNAL FLOW (does current actually move through the wires?).

The testing hierarchy:
  CHECK 16 — the bulb (does each function work alone?)
  CHECK 18 — the strand (does signal flow between connected functions?)
  CHECK 19 — the tree (does the full cycle complete?)
  CHECK 20 — the fuse (does one blown bulb leave the rest lit?)

If all checks pass, the organism is structurally healthy AND operationally alive.
If any check fails, the check identifies the defect and the axiom it
violates. The fix is derivable.

---

## V. Convergence

*This section is not prescriptive. It is predictive.*

When the generative procedures (§II) are applied to a persistent, adaptive
system (A3 + A4) over sufficient time, the organism converges toward certain
structural properties. These convergences are **conjectures** — supported by
the axioms and by the observation that biological systems solve analogous
persistence + adaptation problems. They are not formally proven. They describe
the mature organism, not the newborn. If a conjecture is falsified by a real
organism's growth, the conjecture is wrong and must be revised.

### Convergence 1: Mechanism count

A persistent system (A3) requires mechanisms for: intake, processing,
transport, structure, defense, waste removal, boundary.

An adaptive system (A4) additionally requires: control, regulation, execution,
memory, reproduction.

Each has a unique (input class, output class, temporal mode) tuple. No pair
merges without losing a distinct capability.

**The mature organism converges on at least 12 mechanisms.** A young organism
may have fewer. That is correct for its age. Growth adds mechanisms as
capability gaps appear. The convergence proof shows where growth leads, not
where it starts.

### Convergence 2: Signal type vocabulary

Signals pass through a lifecycle as they flow through the organism. Each
lifecycle phase transforms the signal's nature qualitatively:

```
SOURCE → KNOWLEDGE → RULE → STATE → CONTRACT → TRACE → VALIDATION/REPORT
```

Additional types arise from composition (SYNTHESIS), knowledge transfer
(TEACHING), external absorption (MIGRATION), open inquiry (QUESTION),
preservation (ARCHIVE), and expressive context (AESTHETIC).

**The mature vocabulary converges on at least 14 types.** A young organism
may have 2 (the input and output of its first function). Each new function
may discover new signal types. The lifecycle derivation shows where the
vocabulary leads, not where it starts.

### Convergence 3: Biological correspondence

The 12 mechanisms correspond to biological organ systems (nervous, digestive,
circulatory, skeletal, immune, excretory, integumentary, respiratory,
endocrine, muscular, reproductive, memory). This is convergent evolution, not
analogy. Biology and computation both solve the persistence + adaptation
problem. They converge on the same mechanism set.

Adopting biological names is a recognition of this convergence. It is not
a mandate. If the organism discovers a mechanism with no biological analog,
it names the mechanism itself.

### Convergence 4: Formation differentiation

As functions accumulate, they differentiate into at least 7 archetypes — each
with a distinct (dominant operation, coordination mode, cadence profile):

| Archetype    | What it does |
|--------------|-------------|
| Generator    | Produces primitives, schemas, theoretical constructs |
| Transformer  | Converts one material class into another |
| Router       | Coordinates flow, synchronization, dispatch |
| Reservoir    | Preserves, indexes, curates, reactivates |
| Interface    | Mediates between the organism and external systems |
| Laboratory   | Conducts bounded experimentation without canonical obligation |
| Synthesizer  | Combines outputs from multiple functions into composite regimes |

A young organism has undifferentiated functions. Differentiation is emergent —
it occurs when the organism is complex enough to benefit from specialization.

### Convergence 5: Graph decomposition

The single signal graph decomposes into at least 4 independent edge families
(Law 4, §IIIa) as the organism matures. Each family develops its own
diagnostic indices:

- **Dependency** → acyclicity score, build-order depth
- **Information** → feedback density, signal coverage
- **Governance** → constitutional reachability, authority path length
- **Evolution** → migration rate, lineage completeness

The mature organism tracks composite health indices across all four families.

### Convergence 6: Ontological self-model

The mature organism develops a multi-layer self-index — a model of itself
covering identity, hierarchy, relation, state, event, and governance. This
index senses structural drift, infers implications of local changes, evolves
its own categories, and preserves its own history.

A young organism has no self-model. Self-awareness emerges as the organism
becomes complex enough that local changes have non-obvious global effects.

### Convergence 7: Developmental phases

Growth proceeds through recognizable regimes:

| Regime        | What happens |
|---------------|-------------|
| Emergence     | Impulse → identity → boundary. The organism becomes real. |
| Design        | Ontology → logic → architecture. The organism becomes formal. |
| Embodiment    | Architecture → implementation. The organism becomes material. |
| Stabilization | Testing → hardening → integration. The organism becomes reliable. |
| Completion    | Validation → governance → evolution. The organism becomes self-sustaining. |

Each regime has diagnostic questions and transition predicates. The organism
discovers its phase by checking whether transition conditions are satisfied,
not by following a schedule. The operational rule: replace "what should we do
next?" with "what transition condition has not yet been met?"

### Convergence 8: Formation lifecycle

Functions develop a governed lifecycle as the organism matures:

```
PROPOSED → INCUBATING → ACTIVE → UNDER_REVIEW → MIGRATING/BUFFERED → ARCHIVED/DISSOLVED
```

A young organism has only active functions. The lifecycle emerges when the
organism develops enough governance capacity to distinguish between proposed
and active work, to review and buffer, and to formally archive or dissolve.

### Convergence 9: Self-rendering

The mature organism renders its own state into perceptible form. Every
function becomes simultaneously a generative function — producing artifacts
that make the organism's internal state visible to its operator. The organism
does not merely track data. It renders its own density into experience.

An organism that cannot be perceived by its operator is structurally opaque —
it exists but cannot be governed, because governance requires visibility.

### Convergence 10: Temporal cadence differentiation

The mature organism develops multiple temporal modes:

| Mode             | When signals fire |
|------------------|------------------|
| Event-driven     | On occurrence |
| Periodic         | At regular intervals |
| Continuous       | Always flowing |
| Archive-triggered | When preservation thresholds are met |
| Review-gated     | When explicit approval is given |
| Hybrid           | Combination of modes |

A young organism operates in a single mode. Cadence differentiates as
functions specialize and require different temporal disciplines.

### Convergence 11: Functional taxonomy

The mechanism classification (Step 3) describes HOW a function works — what
kind of computation it performs. Orthogonal to this, a functional taxonomy
describes WHAT KIND of artifact a function produces. As the organism matures,
its functions differentiate along this second axis into recognizable artifact
classes: constitutional charters, knowledge corpora, reusable frameworks,
processing engines, user-facing applications, internal infrastructure,
verification instruments, preserved archives, bounded experiments, and
operational tooling.

This taxonomy is orthogonal to mechanism: a Generator (Convergence 4) might
produce a charter OR a framework. A Reservoir might preserve a corpus OR an
archive. The two axes cross-classify, producing richer structural awareness.

A young organism produces undifferentiated artifacts. The taxonomy emerges when
the organism has enough functions that "what does it produce?" becomes a
non-trivial question.

### What convergence does NOT predict

- The specific functions the organism will have
- The specific products it will build
- The specific connections in its signal graph
- Its named purposes or emergent clusters
- Its total size, complexity, or lifespan

These emerge from work. They are not derivable from axioms alone. The organism
discovers them by growing.

---

## VI. Reproduction

A new organism is created by placing this file in an empty directory.

The offspring inherits:
- This seed (the axioms + procedures + laws + health checks)
- Nothing else

No mechanisms. No signal types. No functions. No graph. Empty.

The offspring grows by doing work. It discovers its own mechanisms, names its
own signal types, builds its own functions, wires its own graph. It may
converge on the same structures as its parent, or it may discover forms its
parent never reached.

The genome does not constrain the organism's potential. It constrains only
the structural discipline of its growth.

---

## VII. Evolution of the Genome

This document is itself subject to governed change (A6: organizational closure).

| Mode | Scope | Gate |
|------|-------|------|
| Conservative | Adds procedures or health checks compatible with existing axioms | None |
| Constrained extension | Adds new axioms compatible with existing ones | Review |
| Breaking revision | Changes or removes axioms | Full review + migration for all dependents |

If a derivation is shown to be wrong, the parameters it predicted are wrong.
Fix the derivation. The predictions change. This is not failure. This is the
genome adapting.

If an axiom is shown to be wrong, the organism's foundation changes. This is
the most consequential possible evolution. It requires the most rigorous
review and a migration path for everything that depended on the old axiom (A9:
the old axiom's lineage is preserved even as the new axiom replaces it).

---

## Summary

Nine axioms. One structural constraint (depth = 1). Six growth procedures.
Seven structural laws. Twenty health checks. Eleven convergence conjectures.

The organism is not defined by its final form. It is defined by how it grows.

Place this file in an empty directory. Begin working. Grow.
