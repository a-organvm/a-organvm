# Plan: Fortify a-organvm from Taxis Interaction Data + Post-Mortem

**Date:** 2026-04-05
**Scope:** a-organvm (the Seed) — gate contract amendments only
**Source:** Exported session `2026-04-05-122815-reference.txt` (2952 lines) + ORGAN-REPORT.md + DISSECTION.md

---

## Context

ORGAN-IV Taxis is dissolving. Its final major session produced 20 SOPs via bidirectional process crystallization, a promotion readiness audit, gap closure (pyproject.toml + ruff), and cross-session code review. The *artifacts* (SOPs, configs) already exist in orchestration-start-here. What hasn't yet been captured is the **meta-knowledge** — patterns of how the work was done, what went wrong, what corrections were needed, what principles emerged from the interaction itself.

The user's directive: take this lived experience ("reality") and distill it into principles ("ideal") that feed directly into what's becoming ("the-reality-becoming" = a-organvm). The TRIPTYCH model governs: code doesn't move, identity moves. RELAY.md enforces: "only bare intent crosses the firewall."

This plan injects **7 bare intents** as gate conditions into existing a-organvm contracts. No new functions, no new mechanisms, no new files. Each gate makes an existing contract stronger. Zero references to ORGAN-IV, Taxis, SOPs, conductors, or any predecessor-specific structure.

---

## Meta-Learnings: 10 Extracted, 7 Injected, 3 Already Captured

| # | Learning | Inject? | Rationale |
|---|----------|---------|-----------|
| 1 | ADDITIVE_ONLY — subagents overwrite by default; must instruct additive behavior | YES → immune--watch G3 | The immune watch system should detect mutations/overwrites |
| 2 | VERIFICATION_IMMUNE — automated assessments hallucinate ~30%; adversarial re-read mandatory | YES → immune--verify G4 | Verification must verify itself |
| 3 | DUAL_INSTANCE_OBLIGATION — fix THIS version AND document evolutionary edge for successor | YES → nervous--govern G6 | Governance rule: coexistence discipline |
| 4 | VACUUM_IMPERATIVE — N/A = vacuum where something should be; research, plan, log | YES → skeletal--consolidate G3 | Structural consolidation should detect holes |
| 5 | CLOSE_LITURGY — ritual two-pass close catches what single pass misses | YES → circulatory--relay G4 | Relay handoffs need two-pass verification |
| 6 | CONCURRENT_WRITE_GAP — two writers on shared file = data integrity risk without coordination gate | YES → nervous--synchronize G3 | Synchronization must include write coordination |
| 7 | BIDIRECTIONAL_CRYSTALLIZATION — extracting latent + injecting explicit produces same artifact at different maturity levels | YES → respiratory--ingest dna | Enriches ingest methodology without regressing CONVERGING state |
| 8 | EMERGENT_DEPENDENCY — formalizing latent processes reveals implicit dependency chains | SKIP | Already expressed by signal attraction system in SEED.md §V |
| 9 | PARITY_AXIOM — local:remote = 1:1; if machine dies, soul persists | SKIP | Already captured by memory--persist.yaml G1 (REMOTE_PARITY) |
| 10 | NOTHING_LOST — recovery is immediate and non-negotiable | SKIP | Already expressed by Axiom A3 (Persistence) + close protocol chain |

---

## Implementation: 7 Gate Amendments + 1 DNA Enrichment

### 1. immune--watch.yaml — Add G3: ADDITIVE_AUDIT

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/immune--watch.yaml`
**Current gates:** G1 (TESTS_PASS, PENDING), G2 (REGISTRY_IMPORT_CANONICAL, PASS)

Add after G2:

```yaml
  - id: G3
    check: ADDITIVE_AUDIT
    condition: "when multiple agents modify shared artifacts, the watch system detects non-additive mutations — any change that overwrites existing content rather than appending triggers an audit finding"
    status: PENDING
```

**Bare intent:** Modification to shared state must be additive. Mutation = violation.

### 2. immune--verify.yaml — Add G4: ADVERSARIAL_RECHECK

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/immune--verify.yaml`
**Current gates:** G1 (TESTS_PASS), G2 (SECURITY_SCRIPTS_ABSORBED), G3 (STANDALONE_SCRIPTS_DISSOLVED) — all PENDING

Add after G3:

```yaml
  - id: G4
    check: ADVERSARIAL_RECHECK
    condition: "automated verification outputs are themselves verified — every machine-generated finding is cross-checked against primary evidence before being reported as fact; unverified claims are marked UNVERIFIED, not reported as findings"
    status: PENDING
```

**Bare intent:** The verifier must be verified. Claims require evidence.

### 3. nervous--govern.yaml — Add G6: COEXISTENCE_DISCIPLINE

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/nervous--govern.yaml`
**Current gates:** G1, G1b, G2, G3, G4, G5 — all PENDING

Add after G5:

```yaml
  - id: G6
    check: COEXISTENCE_DISCIPLINE
    condition: "when a successor formation exists alongside its predecessor, governance enforces dual obligation — the predecessor is improved in earnest (not deferred to successor), and every constraint encountered is documented as evolutionary edge material for the successor; both live simultaneously"
    status: PENDING
```

**Bare intent:** Coexisting versions are both built honestly. The gap between them is the evolutionary record.

### 4. skeletal--consolidate.yaml — Add G3: VACUUM_DETECTION

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/skeletal--consolidate.yaml`
**Current gates:** G1 (NO_DRIFT), G2 (UNIVERSAL_NAMESPACE) — both PENDING

Add after G2:

```yaml
  - id: G3
    check: VACUUM_DETECTION
    condition: "structural audits treat absence as signal, not silence — every field marked N/A, every index with no entry, every mechanism with no gate is classified as a vacuum and logged for investigation; absence of data is itself data"
    status: PENDING
```

**Bare intent:** N/A is a vacuum. Absence demands investigation.

### 5. circulatory--relay.yaml — Add G4: TWO_PASS_CLOSE

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/circulatory--relay.yaml`
**Current gates:** G1 (ASYNC_DISPATCH), G2 (LINEAGE_PRESERVATION), G3 (HANDSHAKE_ENVELOPE) — all PENDING

Add after G3:

```yaml
  - id: G4
    check: TWO_PASS_CLOSE
    condition: "relay handoff includes a mandatory second verification pass — first pass inventories and commits, second pass audits the first pass output for stale counts, missed indices, and unchecked vacuums; single-pass closure is treated as incomplete"
    status: PENDING
```

**Bare intent:** One pass finds the work. Two passes verify the finding.

### 6. nervous--synchronize.yaml — Add G3: WRITE_COORDINATION

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/nervous--synchronize.yaml`
**Current gates:** G1 (ATOMIC_ID_GEN), G2 (PIPELINE_MANIFEST) — both PENDING

Add after G2:

```yaml
  - id: G3
    check: WRITE_COORDINATION
    condition: "concurrent writers to shared state files are coordinated through a claims mechanism — no two processes may modify the same canonical file without a lock, reservation, or serialization guarantee; rebase-after-collision is recovery, not coordination"
    status: PENDING
```

**Bare intent:** Recovery from collision is not the same as preventing it.

### 7. respiratory--ingest.yaml — Enrich DNA (no new gate)

**File:** `/Users/4jp/sovereign--ground/holds--same/a-organvm/respiratory--ingest.yaml`
**Current state:** CONVERGING (all 3 gates PASS). Adding a PENDING gate would regress to CALLING. Instead, enrich the `dna` section.

Add to dna list:

```yaml
  - "bidirectional intake — when ingesting material, simultaneously extract latent methodology (patterns performed but never named) and inject explicit methodology (patterns named but not yet formalized); both directions produce the same artifact type at different maturity levels"
```

**Bare intent:** Ingest runs in two directions at once. What was done unconsciously is as valuable as what was done deliberately.

---

## Session Protocol

The a-organvm RELAY.md specifies a strict read order. This session must follow it:

1. Read AGENTS.md
2. Read RELAY.md (already done during planning)
3. Read SEED.md (already done during planning)
4. Read signal-graph.yaml (already done during planning)
5. Run all three functions: `python3 skeletal_define.py && python3 circulatory_route.py && python3 cultvra_logos.py`
6. **THEN** apply the 7 amendments + 1 enrichment
7. Run all three functions again to verify no regressions
8. Run all 82 tests: `python3 -m pytest`

---

## Verification

1. **Gate count:** 101 → 107 (6 new gates + 1 dna enrichment, not 7 gates — respiratory gets dna, not gate)
2. **State preservation:** respiratory--ingest stays CONVERGING (dna enrichment, not gate addition)
3. **Axiom compliance:**
   - A5 (Minimality): 3 learnings skipped because already captured. No redundancy.
   - A9 (Alchemical Inheritance): Each gate condition preserves the lineage of the interaction that produced it — not by naming the source, but by encoding its distilled principle.
   - A7 (Individual Primacy): The operator's interaction patterns are what generated these learnings. They serve the operator.
4. **Firewall compliance:** Zero references to ORGAN-IV, Taxis, conductors, SOPs, Sovereign Systems, or any predecessor-specific terminology in any gate condition text.
5. **No new files:** All edits are to existing contracts. D=1 flat structure preserved.
6. **Test suite:** 82 tests should still pass (gate conditions are metadata, not executable code).

---

## Post-Implementation

1. Update RELAY.md with session record (what was done, what advanced)
2. Update organism vitals (gate count 101→107)
3. Commit + push (PARITY_AXIOM: local:remote = 1:1)
4. Copy this plan to a-organvm plans directory with dated name
