"""respiratory--ingest: the organism absorbs external material.

GEN-002: canonical '--' maps to '_' in .py filenames.

The respiratory system is the boundary between organism and environment.
It discovers what material exists outside, assesses ingestion readiness,
and tracks what has moved across the boundary.

Skeletal reads what EXISTS. Circulatory computes what FLOWS.
Cultvra documents what it MEANS. Immune verifies what is TRUE.
Respiratory absorbs what is OUTSIDE.

Three-phase pipeline inherited from predecessor (alchemia-ingestvm):
  INTAKE  — discover and catalogue available material
  ABSORB  — classify and resolve isotopes
  ALCHEMIZE — transform into organism-compatible form

This function does NOT copy predecessor code. It reads the predecessor's
structure through gate contracts and the cocoon-map, assessing what
material is available and what has been absorbed.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).parent


# -- data structures --


@dataclass
class SourceMaterial:
    """A unit of external material available for ingestion."""

    name: str
    origin: str  # repo path or URL
    channel: str  # gate contract stem that declares the source
    state: str  # AVAILABLE, UNREACHABLE, ABSORBED
    size_hint: int  # approximate lines declared in contract


@dataclass
class MigrationDirective:
    """A migration tracked from the cocoon-map — what moved and its state."""

    subject: str  # cocoon entry name
    migration_type: str  # the cocoon state: PLANNED, ERECTED, MOLTING, EMERGED
    from_location: str  # source repo/module
    to_location: str  # the cocoon (organism function it becomes)
    verb: str  # the action verb from the cocoon entry


@dataclass
class ChannelState:
    """Ingestion channel health for one alchemia phase."""

    name: str  # intake, absorb, alchemize, channels
    reachable: bool
    path: str
    note: str = ""


@dataclass
class IngestionReport:
    """Complete ingestion state at a moment in time."""

    timestamp: str
    sources: list[SourceMaterial]
    migrations: list[MigrationDirective]
    channels: list[ChannelState]
    summary: dict[str, int]


# -- reading --


def _load_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML file, returning empty dict on missing or non-dict."""
    if not path.is_file():
        return {}
    with path.open() as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_contracts(directory: Path | None = None) -> list[tuple[str, dict]]:
    """Read all gate contracts from the organism directory."""
    root = directory or _HERE
    results = []
    for p in sorted(root.glob("*--*.yaml")):
        if "--" not in p.stem:
            continue
        with p.open() as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            results.append((p.stem, data))
    return results


def load_cocoon_map(path: Path | None = None) -> dict[str, Any]:
    """Read the absorption blueprint."""
    return _load_yaml(path or (_HERE / "cocoon-map.yaml"))


# -- source discovery --


def _resolve_repo_path(origin: str, search_roots: list[Path] | None = None) -> Path | None:
    """Attempt to find a repo path on the local filesystem.

    Gate contracts reference repos like 'meta-organvm/organvm-engine' or
    'alchemia-ingestvm/'. We search relative to the organism's grandparent
    directories (the workspace).
    """
    if search_roots is None:
        # default: look in the workspace containing the organism
        workspace = _HERE.parent.parent.parent  # sovereign--ground → organvm → Workspace
        search_roots = [workspace, _HERE.parent.parent]  # Workspace/organvm/ as fallback

    # strip trailing slash and try each root
    clean = origin.rstrip("/")
    for root in search_roots:
        # try the full path (org/repo)
        candidate = root / clean
        if candidate.is_dir():
            return candidate
        # try just the repo name (last component)
        repo_name = clean.split("/")[-1] if "/" in clean else clean
        candidate = root / repo_name
        if candidate.is_dir():
            return candidate
    return None


def discover_sources(
    contracts: list[tuple[str, dict]] | None = None,
    directory: Path | None = None,
) -> list[SourceMaterial]:
    """Discover all source material declared in gate contracts."""
    if contracts is None:
        contracts = load_contracts(directory)

    sources: list[SourceMaterial] = []
    for stem, contract in contracts:
        for source_entry in contract.get("sources", []):
            if not isinstance(source_entry, dict):
                continue
            repo = source_entry.get("repo", "")
            modules = source_entry.get("modules", [])
            lines = source_entry.get("lines", 0)

            # check if the repo exists locally
            repo_path = _resolve_repo_path(repo)
            state = "AVAILABLE" if repo_path is not None else "UNREACHABLE"

            # check if the contract has all gates passing (ABSORBED)
            contract_state = contract.get("state", "CALLING")
            if contract_state in ("CONVERGING", "EMERGED"):
                all_pass = all(
                    g.get("status", "").upper() in ("PASS", "PASSED")
                    for g in contract.get("gate", [])
                    if isinstance(g, dict)
                )
                if all_pass and contract.get("gate"):
                    state = "ABSORBED"

            sources.append(SourceMaterial(
                name=f"{repo}:{','.join(modules[:3])}" if modules else repo,
                origin=repo,
                channel=stem,
                state=state,
                size_hint=lines,
            ))
    return sources


# -- channel enumeration --


_ALCHEMIA_PHASES = ["intake", "absorb", "alchemize", "channels"]


def enumerate_channels(
    contracts: list[tuple[str, dict]] | None = None,
    directory: Path | None = None,
) -> list[ChannelState]:
    """Enumerate the alchemia ingestion channels (3-phase pipeline)."""
    if contracts is None:
        contracts = load_contracts(directory)

    # find the respiratory--ingest contract to get the predecessor repo
    predecessor_path: Path | None = None
    for stem, contract in contracts:
        if stem == "respiratory--ingest":
            for src in contract.get("sources", []):
                if isinstance(src, dict):
                    repo = src.get("repo", "")
                    predecessor_path = _resolve_repo_path(repo)
                    break
            break

    channels: list[ChannelState] = []
    for phase in _ALCHEMIA_PHASES:
        if predecessor_path is not None:
            phase_dir = predecessor_path / "src" / "alchemia" / phase
            if phase_dir.is_dir():
                channels.append(ChannelState(
                    name=phase,
                    reachable=True,
                    path=str(phase_dir),
                ))
                continue
        channels.append(ChannelState(
            name=phase,
            reachable=predecessor_path is not None,
            path=(
                str(predecessor_path / "src" / "alchemia" / phase)
                if predecessor_path else ""
            ),
            note=(
                "predecessor not found locally"
                if predecessor_path is None else "phase directory missing"
            ),
        ))

    return channels


# -- migration tracking --


def track_migrations(cocoon_map: dict[str, Any] | None = None) -> list[MigrationDirective]:
    """Track material migrations from the cocoon-map."""
    if cocoon_map is None:
        cocoon_map = load_cocoon_map()

    migrations: list[MigrationDirective] = []
    for name, entry in cocoon_map.items():
        if not isinstance(entry, dict):
            continue
        state = entry.get("state", "UNKNOWN")
        verb = entry.get("verb", "")
        absorbs = entry.get("absorbs_from", [])

        for source in absorbs:
            if not isinstance(source, str):
                continue
            # strip comments (everything after #)
            clean = source.split("#")[0].strip()
            migrations.append(MigrationDirective(
                subject=name,
                migration_type=state,
                from_location=clean,
                to_location=name,
                verb=verb,
            ))

    return migrations


# -- main operation --


def ingest(
    contract_dir: Path | None = None,
    cocoon_path: Path | None = None,
) -> IngestionReport:
    """The organism assesses its ingestion state."""
    root = contract_dir or _HERE
    contracts = load_contracts(root)
    cocoon_map = load_cocoon_map(cocoon_path or (root / "cocoon-map.yaml"))

    sources = discover_sources(contracts=contracts, directory=root)
    channels = enumerate_channels(contracts=contracts, directory=root)
    migrations = track_migrations(cocoon_map=cocoon_map)

    available = sum(1 for s in sources if s.state == "AVAILABLE")
    unreachable = sum(1 for s in sources if s.state == "UNREACHABLE")
    absorbed = sum(1 for s in sources if s.state == "ABSORBED")
    total_lines = sum(s.size_hint for s in sources)
    reachable_channels = sum(1 for c in channels if c.reachable)

    return IngestionReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        sources=sources,
        migrations=migrations,
        channels=channels,
        summary={
            "total_sources": len(sources),
            "available": available,
            "unreachable": unreachable,
            "absorbed": absorbed,
            "total_lines_declared": total_lines,
            "channels_reachable": reachable_channels,
            "channels_total": len(channels),
            "migrations_tracked": len(migrations),
        },
    )


# -- recording --


def record_ingestion(report: IngestionReport, path: Path | None = None) -> Path:
    """Append ingestion report to the ingestion log (TRACE output)."""
    log = path or (_HERE / "ingestions.jsonl")
    with log.open("a") as f:
        f.write(json.dumps(asdict(report), default=str) + "\n")
    return log


def load_ingestion_history(path: Path | None = None) -> list[IngestionReport]:
    """Read back the ingestion log."""
    log = path or (_HERE / "ingestions.jsonl")
    if not log.is_file():
        return []
    reports: list[IngestionReport] = []
    for line in log.read_text().splitlines():
        if line.strip():
            raw = json.loads(line)
            reports.append(IngestionReport(
                timestamp=raw["timestamp"],
                sources=[SourceMaterial(**s) for s in raw.get("sources", [])],
                migrations=[MigrationDirective(**m) for m in raw.get("migrations", [])],
                channels=[ChannelState(**c) for c in raw.get("channels", [])],
                summary=raw.get("summary", {}),
            ))
    return reports


# -- entry point --


if __name__ == "__main__":
    report = ingest()
    s = report.summary
    print(
        f"{s['total_sources']} sources "
        f"({s['available']} available / {s['unreachable']} unreachable / "
        f"{s['absorbed']} absorbed) · "
        f"{s['total_lines_declared']} lines declared"
    )
    print(
        f"{s['channels_reachable']}/{s['channels_total']} channels reachable · "
        f"{s['migrations_tracked']} migrations tracked"
    )

    log = record_ingestion(report)
    print(f"recorded → {log.name}")
