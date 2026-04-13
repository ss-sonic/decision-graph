from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .campaign import Campaign, load_campaign
from .engines import build_registry
from .engines.base import EngineError
from .prompts import render_prompt
from .reports import write_reports
from .scoring import apply_cycle_results, choose_next_objective
from .state import load_or_initialize_state, next_cycle_dir, save_state
from .utils import ensure_directory, read_json, read_text, write_json


ROLE_SEQUENCE = ["researcher", "skeptic", "rebuttal", "judge"]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, EngineError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="research-loop")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize the local research loop workspace")
    init_parser.set_defaults(func=cmd_init)

    preflight_parser = subparsers.add_parser("preflight", help="Check local runtime and engine readiness")
    preflight_parser.set_defaults(func=cmd_preflight)

    run_parser = subparsers.add_parser("run", help="Execute one or more research cycles")
    run_parser.add_argument("--campaign", default="campaigns/manager-people.yaml")
    run_parser.add_argument("--cycles", type=int, default=1)
    run_parser.set_defaults(func=cmd_run)

    status_parser = subparsers.add_parser("status", help="Show campaign state")
    status_parser.add_argument("--campaign", default="campaigns/manager-people.yaml")
    status_parser.set_defaults(func=cmd_status)

    report_parser = subparsers.add_parser("report", help="Render campaign reports")
    report_parser.add_argument("--campaign", default="campaigns/manager-people.yaml")
    report_parser.set_defaults(func=cmd_report)

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        subprocess.run(["git", "init"], check=True)

    for relative in ["bin", "campaigns", "prompts", "reports", "runs", "src", "tests"]:
        ensure_directory(root / relative)

    print("Initialized git and research-loop directories.")
    return 0


def cmd_preflight(args: argparse.Namespace) -> int:
    root = Path.cwd()
    registry = build_registry()
    print(f"Workspace: {root}")
    print(f"Python: {sys.version.split()[0]}")
    failed = False
    for engine_name, adapter in registry.items():
        result = adapter.preflight()
        print(f"\n[{engine_name}]")
        print(f"available={result.available}")
        print(f"auth_configured={result.auth_configured}")
        print(f"search_available={result.search_available}")
        print(f"search_mode={result.search_mode}")
        for detail in result.details:
            print(f"- {detail}")
        if not result.available:
            failed = True
    return 1 if failed else 0


def cmd_run(args: argparse.Namespace) -> int:
    root = Path.cwd()
    campaign = resolve_campaign(root, args.campaign)
    registry = build_registry()
    state = load_or_initialize_state(root, campaign)

    researcher_engine = registry[campaign.raw["engine_roles"]["researcher"]]
    if not researcher_engine.preflight().search_available:
        raise EngineError("Researcher search is required but not available. Adjust Claude search mode and retry.")

    for _ in range(args.cycles):
        state = run_cycle(root, campaign, state, registry)
        save_state(root, campaign, state)
        print(f"Cycle {state['cycle_count']} complete. Verdict: {state['verdict']}")
        if state["verdict"] in {"rejected", "plausible", "stalled"}:
            break
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path.cwd()
    campaign = resolve_campaign(root, args.campaign)
    state = load_or_initialize_state(root, campaign)
    print(f"Campaign: {campaign.slug}")
    print(f"Verdict: {state['verdict']}")
    print(f"Cycles: {state['cycle_count']}")
    print(f"No-evidence streak: {state['no_evidence_streak']}")
    print("Claim status:")
    for claim_id, item in state["claim_status"].items():
        print(f"- {claim_id}: {item['status']}")
    print("Kill criteria:")
    for criterion_id, item in state["kill_criteria_status"].items():
        print(f"- {criterion_id}: {item['status']} (sources={item['source_count']})")
    print("Unresolved contradictions:")
    for item in state["unresolved_contradictions"] or ["none"]:
        print(f"- {item}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    root = Path.cwd()
    campaign = resolve_campaign(root, args.campaign)
    state = load_or_initialize_state(root, campaign)
    latest = latest_judge_artifact(root, campaign, state)
    if latest is None:
        raise ValueError("No judge artifact found yet. Run at least one cycle first.")
    files = write_reports(root, campaign, state, latest)
    for file_path in files:
        print(file_path)
    return 0


def resolve_campaign(root: Path, raw_path: str) -> Campaign:
    path = (root / raw_path).resolve()
    if not path.exists():
        raise ValueError(f"Campaign file not found: {path}")
    return load_campaign(path)


def run_cycle(
    root: Path,
    campaign: Campaign,
    state: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    cycle_dir = next_cycle_dir(root, campaign, state)
    cycle_number = int(state["cycle_count"]) + 1
    objective = choose_next_objective(campaign, state)
    latest_artifacts: dict[str, str] = {}
    normalized_artifacts: dict[str, dict[str, Any]] = {}

    context_cache: list[tuple[str, str]] = [
        ("Idea Source", read_text(campaign.idea_source)),
    ]

    for note_path in campaign.notes_sources:
        if note_path.exists():
            context_cache.append((f"Founder Note: {note_path.name}", read_text(note_path)))

    for role in ROLE_SEQUENCE:
        engine_name = campaign.raw["engine_roles"][role]
        adapter = registry[engine_name]
        role_dir = ensure_directory(cycle_dir / role)
        role_context = build_role_context(role, campaign, state, normalized_artifacts, context_cache)
        prompt_text = render_prompt(root, role, campaign, objective, role_context)
        prompt_path = role_dir / "prompt.txt"
        prompt_path.write_text(prompt_text, encoding="utf-8")
        raw_output_path = adapter.invoke(
            role=role,
            prompt_text=prompt_text,
            output_dir=role_dir,
            search_required=(role == "researcher"),
        )
        artifact = adapter.normalize(raw_output_path)
        normalized_path = role_dir / "normalized.json"
        write_json(normalized_path, artifact)
        latest_artifacts[role] = str(normalized_path)
        normalized_artifacts[role] = artifact

    judge_artifact = normalized_artifacts["judge"]
    updated_state = apply_cycle_results(campaign, state, cycle_number, judge_artifact)
    updated_state["latest_artifacts"] = latest_artifacts
    updated_state["history"].append(
        {
            "cycle": cycle_number,
            "objective": objective,
            "verdict": updated_state["verdict"],
            "judge_summary": judge_artifact.get("summary"),
        }
    )
    write_reports(root, campaign, updated_state, judge_artifact)
    return updated_state


def build_role_context(
    role: str,
    campaign: Campaign,
    state: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    shared_context: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    sections = list(shared_context)
    sections.append(("Campaign State", json.dumps(state, indent=2, sort_keys=True)))
    if role == "researcher":
        return sections
    if "researcher" in artifacts:
        sections.append(("Researcher Artifact", json.dumps(artifacts["researcher"], indent=2, sort_keys=True)))
    if role in {"rebuttal", "judge"} and "skeptic" in artifacts:
        sections.append(("Skeptic Artifact", json.dumps(artifacts["skeptic"], indent=2, sort_keys=True)))
    if role == "judge" and "rebuttal" in artifacts:
        sections.append(("Rebuttal Artifact", json.dumps(artifacts["rebuttal"], indent=2, sort_keys=True)))
    return sections


def latest_judge_artifact(root: Path, campaign: Campaign, state: dict[str, Any]) -> dict[str, Any] | None:
    latest = state.get("latest_artifacts", {}).get("judge")
    if not latest:
        return None
    return read_json(Path(latest))

