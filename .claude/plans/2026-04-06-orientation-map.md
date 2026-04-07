# Plan: Orientation Map — "Where am I?"

## Context

The operator built a system to prevent chaos and lost control of the system itself. Things get moved and forgotten (`materia-collider/bench/organ-reset-2026-03-11/` holds 53 dissolved repos the operator couldn't find). Multiple directories at `$HOME` root (`sovereign--ground/`, `system-system--system/`, `system-system--system--monad/`) coexist with the `~/Workspace/` hierarchy, and no single command tells you what's where or what state it's in.

The immediate need isn't another governance framework. It's a command you run when you sit down that answers: **where is everything, what happened last, what do I do next.**

## What to Build

A single Python script: `~/bin/organvm-orient` (or added as `domus orient` subcommand — TBD by user preference).

### Output Format

```
ORGANVM Orientation — 2026-04-06T21:30:00

PHYSICAL MAP
  ~/Workspace/                          128 repos across 9 org dirs
  ~/sovereign--ground/                  6 analysis categories (holds/lacks/joins/bounds/cuts/moves)
  ~/system-system--system/              formal layer (7 Laws, 89 atoms) [main]
  ~/system-system--system--monad/       ↳ worktree [monad/synthesizer-architecture, +4 commits ahead]

KEY LOCATIONS
  organism (a-organvm)                  ~/sovereign--ground/holds--same/a-organvm/
  engine                                ~/Workspace/meta-organvm/organvm-engine/
  conductor                             ~/Workspace/organvm-iv-taxis/tool-interaction-design/
  dissolved repos (53)                  ~/Workspace/meta-organvm/materia-collider/bench/organ-reset-2026-03-11/
  skills (144)                          ~/Workspace/organvm-iv-taxis/a-i--skills/
  registry                              ~/Workspace/meta-organvm/organvm-corpvs-testamentvm/registry-v2.json

ORGANISM VITALS (a-organvm)
  3 functions · 82 tests · 107 gates (10 lit / 97 dim) · 16 mechanisms
  Last commit: ea7e8dd (2026-04-06) — docs: UMFAS plan
  Next (from RELAY.md): CHECK 19 formal closure, AOR-018 cultvra ontology

RECENT ACTIVITY (last 48h across all repos)
  system-system--system     3 commits   monad branch +4 ahead
  a-organvm                 2 commits   UMFAS plan
  organvm-iv-taxis          5 commits   UMFAS + submodule sync
  [... sorted by recency ...]

PENDING (from RELAY.md + IRF)
  P0: Memory chezmoi tracking — HUMAN ACTION: chezmoi add ~/.claude/projects/...
  P1: CHECK 19 formal closure
  P1: Cultvra ontology (AOR-018/#87)
```

### What It Reads (all read-only)

| Source | What it provides |
|--------|-----------------|
| `~/sovereign--ground/` | Directory existence check |
| `~/system-system--system/` | `git log`, `git worktree list` |
| `~/sovereign--ground/holds--same/a-organvm/RELAY.md` | "What is next" section |
| `~/sovereign--ground/holds--same/a-organvm/signal-graph.yaml` | Function count, signal types |
| `~/Workspace/meta-organvm/materia-collider/bench/organ-reset-2026-03-11/manifest.json` | Dissolved repo count |
| `~/Workspace/*/` | `git log --oneline -1` per repo for recent activity |
| Registry (`registry-v2.json`) | Total repo count, active/archived |

### What It Does NOT Do

- No new governance
- No new frameworks
- No new classification systems
- No writing to files
- No internet access
- No MCP tools
- Runs in < 5 seconds

## Implementation

**Single file**: `~/bin/organvm-orient` (~120 lines Python)

1. Scan known root directories (`$HOME/sovereign--ground`, `$HOME/system-system--system*`, `$HOME/Workspace`)
2. For each: existence check, git status if repo, latest commit
3. Parse `RELAY.md` for "What is next" section (simple string search)
4. Parse `signal-graph.yaml` for function/signal counts
5. Read `manifest.json` for dissolved count
6. Read `registry-v2.json` for total/active/archived counts
7. Scan `~/Workspace/*/` for git repos with commits in last 48h
8. Print formatted report to stdout

**Dependencies**: Python 3.11+ (already on system), PyYAML (already installed for a-organvm), `git` CLI.

**Installation**: `chmod +x ~/bin/organvm-orient` — immediately available in PATH (domus manages `~/.local/bin/`).

## Verification

```bash
# Run it
organvm-orient

# Verify it finds the dissolved repos
organvm-orient | grep "dissolved"

# Verify it reads RELAY
organvm-orient | grep "CHECK 19"

# Verify it shows recent activity
organvm-orient | grep "commits"
```

## What This Solves

When you sit down confused about where things are:
1. Run `organvm-orient`
2. See the physical map (where is everything)
3. See what happened last (recent commits)
4. See what to do next (RELAY + IRF items)
5. See the dissolved repos location (they're not lost, they're at materia-collider/bench/)

It doesn't solve the deeper unification problem. It solves the "I can't find things" problem today.
