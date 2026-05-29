# a-organvm Blueprint

**The new structure. Nothing was moved. This is the declaration.**

Old: `~/Workspace/organvm/` — 113 repos, flat, as they are.
New: `~/Workspace/a-organvm/` — the ideal form, empty folders, waiting.

The diff between old and new IS the work.

---

## Structure

```
a-organvm/
├── PERIODIC-TABLE.md           # The 10 elements (this system's physics)
├── FOSSIL-RECORD.md            # Old→New mapping for every repo
├── BLUEPRINT.md                # This file (the declaration)
│
├── elements/                   # The 10 irreducible operations
│   ├── intake/                 # Implementations of INTAKE
│   ├── store/                  # Implementations of STORE
│   ├── retrieve/               # Implementations of RETRIEVE
│   ├── evaluate/               # Implementations of EVALUATE
│   ├── transform/              # Implementations of TRANSFORM
│   ├── synthesize/             # Implementations of SYNTHESIZE
│   ├── route/                  # Implementations of ROUTE
│   ├── authorize/              # Implementations of AUTHORIZE
│   ├── bind/                   # Implementations of BIND
│   └── emit/                   # Implementations of EMIT
│
├── compounds/                  # Named compositions of elements
│   │                           # (the 19 institutional primitives live here
│   │                           #  once they're built from elements)
│   └── ...
│
├── formations/                 # Wired compositions of compounds
│   ├── aegis/                  # Defensive perimeter
│   ├── oikonomia/              # Survival economics
│   ├── praxis/                 # Income generation
│   └── tessera/                # Identity and standing
│
├── products/                   # Stable, externally-consumable outputs
│   │                           # (the "presets" — packaged configurations)
│   └── ...
│
└── intake/                     # Prima materia — undifferentiated input
                                # Everything enters here. Gets alchemized up.
```

---

## How It Works

1. **Elements** are the building blocks. Each element folder contains
   implementations of that single irreducible operation. An INTAKE
   implementation knows how to bring signal in — from a file, an API,
   a user, a sensor. A STORE implementation knows how to persist state.

2. **Compounds** are named compositions. The "assessor" compound is
   INTAKE + EVALUATE(frame) + EMIT. It lives in compounds/assessor/
   and its code wires those three elements together.

3. **Formations** are wired compositions of compounds. AEGIS wires
   guardian + assessor + counselor + mandator. The formation folder
   contains the wiring diagram and the glue code.

4. **Products** are crystallized formations packaged for external use.
   public-record-data-scrapper, once rebuilt from elements, lands here.

5. **Intake** is where everything new enters. Ideas, data, material.
   The alchemical pipeline (INTAKE → ABSORB → ALCHEMIZE) promotes
   things upward through the layers.

---

## The Core Insight

The old system has ONE repo (organvm-engine) that contains ALL 10 elements.
That's a god-object. The new system separates elements into their own
implementations, then composes them.

The old system has 113 repos that each implement their own version of
INTAKE, their own EVALUATE, their own EMIT. That's duplication.
The new system has ONE intake, ONE evaluate, ONE emit — composed
differently for each use case.

**Old**: 113 repos × ad-hoc element implementations = sprawl
**New**: 10 elements × N compositions = flat, composable, minimal

---

## What Exists vs. What's Declared

| Layer | Old (exists) | New (declared) | Gap |
|-------|-------------|---------------|-----|
| Elements | Scattered across 113 repos, duplicated, inconsistent | 10 clean folders | BUILD these |
| Compounds | The 19 institutional primitives are specs only (SPEC-025) | compounds/ folder ready | BUILD these from elements |
| Formations | Named in specs, not implemented | 4 formation folders ready | WIRE these from compounds |
| Products | A few alive repos (scrapper, portal, classroom-rpg) | products/ folder ready | REBUILD these from formations |
| Intake | ~/Workspace/intake/ has raw material | intake/ folder ready | ROUTE existing material here |
