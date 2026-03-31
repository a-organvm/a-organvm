# AGENTS.md — a-organvm instance routing surface

Global policy from `/Users/4jp/AGENTS.md` applies first and cannot be overridden here.

## Purpose

This file is the local routing half of the session handoff handshake.

- `RELAY.md` says what was completed, what is next, and the boundary of the last session.
- `AGENTS.md` says which agent is allowed to take which class of work in this instance.

Together they form the handoff envelope tracked by:

- `NRV-005` — relay handoff format
- `GEN-004` — local agent routing surface

## Read Order

At session start, read in this order:

1. `AGENTS.md`
2. `RELAY.md` when present
3. `SEED.md`
4. active `*.yaml` gate contracts for the cocoon being touched

## Routing Table

| Work type | Preferred agent | Why |
|-----------|-----------------|-----|
| Architecture decisions, ontology, gate design | Claude | Needs SEED philosophy and cross-contract judgment |
| Isotope dissolution, mechanical import rewrites, repetitive edits | Codex / OpenCode | Pattern-following with tight file discipline |
| Long-context cross-reference, corpus synthesis, broad issue migration | Gemini | Large context window |
| Test execution, parallel verification, result collation | Codex | Fast parallel execution and concrete reporting |
| SOP / doc triage, research synthesis | Gemini | Better long-form reading and compression |
| Gate status updates with clear evidence already in hand | Any | Low-judgment state mutation |

## Local Boundaries

- Default write scope: `a-organvm/`
- Default read scope: `a-organvm/`, `meta-organvm/post-flood/`, `meta-organvm/organvm-engine/`, and tracked source repos named by a cocoon contract
- Do not touch source repo code unless a gate explicitly requires it
- Do not assume permission to resolve unrelated worktree drift

## Containership

- The relay declares what the next session should do.
- This file declares who may do it.
- If a task is not clearly owned by one route above, create or cite a tracked ID before improvising.
