from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .campaign import Campaign, load_campaign
from .engines import build_registry
from .engines.base import EngineError
from .prompts import render_prompt
from .reports import ALLOWED_REPORT_FILES, write_reports
from .scoring import apply_cycle_results, choose_next_objective
from .state import load_or_initialize_state, next_cycle_dir, save_state
from .utils import ensure_directory, read_json, read_text, write_json


ROLE_SEQUENCE = ["researcher", "skeptic", "rebuttal", "judge"]
DEFAULT_CAMPAIGN = "campaigns/client-discovery.yaml"


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
    run_parser.add_argument("--campaign", default=DEFAULT_CAMPAIGN)
    run_parser.add_argument("--cycles", type=int, default=1)
    run_parser.set_defaults(func=cmd_run)

    status_parser = subparsers.add_parser("status", help="Show campaign state")
    status_parser.add_argument("--campaign", default=DEFAULT_CAMPAIGN)
    status_parser.set_defaults(func=cmd_status)

    report_parser = subparsers.add_parser("report", help="Render campaign reports")
    report_parser.add_argument("--campaign", default=DEFAULT_CAMPAIGN)
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
    cycle_log_path = cycle_dir / "cycle.log"
    latest_artifacts: dict[str, str] = {}
    normalized_artifacts: dict[str, dict[str, Any]] = {}

    log_cycle_line(cycle_log_path, f"=== Cycle {cycle_number} ===")
    log_cycle_line(cycle_log_path, f"Objective: {objective}")

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
        log_cycle_line(
            cycle_log_path,
            f"Starting `{role}` with `{engine_name}`. Prompt: {prompt_path.relative_to(root)}",
        )
        role_started = time.monotonic()
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
        elapsed = time.monotonic() - role_started
        log_artifact_summary(cycle_log_path, role, engine_name, artifact, elapsed)

    judge_artifact = normalized_artifacts["judge"]
    updated_state = apply_cycle_results(campaign, state, cycle_number, judge_artifact)
    updated_state["latest_artifacts"] = latest_artifacts
    mutation_log = validate_and_merge_mutations(root, campaign, updated_state, cycle_dir, judge_artifact)
    updated_state["history"].append(
        {
            "cycle": cycle_number,
            "objective": objective,
            "verdict": updated_state["verdict"],
            "judge_summary": judge_artifact.get("summary"),
            "merged_mutation_count": len(mutation_log["merged"]),
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


def log_cycle_line(path: Path, message: str) -> None:
    line = message.rstrip()
    print(line, flush=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def log_artifact_summary(
    cycle_log_path: Path,
    role: str,
    engine_name: str,
    artifact: dict[str, Any],
    elapsed: float,
) -> None:
    summary = artifact.get("summary", "").strip().replace("\n", " ")
    if len(summary) > 220:
        summary = summary[:217] + "..."
    lines = [
        f"Finished `{role}` with `{engine_name}` in {elapsed:.1f}s",
        f"Summary: {summary or '(empty summary)'}",
        f"Confidence: {artifact.get('confidence', 'n/a')}",
        f"Supports claims: {', '.join(artifact.get('supports_claims', [])) or '(none)'}",
        f"Weakens claims: {', '.join(artifact.get('weakens_claims', [])) or '(none)'}",
        f"Triggered kills: {', '.join(artifact.get('triggered_kill_criteria', [])) or '(none)'}",
    ]
    contradictions = artifact.get("contradictions", [])
    if contradictions:
        rendered = []
        for item in contradictions:
            if isinstance(item, str):
                rendered.append(item)
            else:
                rendered.append(item.get("id", "unknown"))
        lines.append(f"Contradictions: {', '.join(rendered)}")
    for line in lines:
        log_cycle_line(cycle_log_path, line)


def validate_and_merge_mutations(
    root: Path,
    campaign: Campaign,
    state: dict[str, Any],
    cycle_dir: Path,
    judge_artifact: dict[str, Any],
) -> dict[str, Any]:
    proposed = judge_artifact.get("proposed_mutations", [])
    if not isinstance(proposed, list):
        proposed = []

    approved: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    merged: list[dict[str, Any]] = []

    for index, mutation in enumerate(proposed):
        decision = validate_mutation(mutation)
        decision["index"] = index
        if decision["approved"]:
            approved.append(decision)
            target_file = decision["target_file"]
            state["merged_mutations"][target_file] = {
                "content": decision["content"],
                "cycle": state["cycle_count"],
                "reason": decision.get("reason"),
            }
            merged.append(decision)
            state["mutation_history"].append(
                {
                    "cycle": state["cycle_count"],
                    "status": "merged",
                    "target_file": target_file,
                    "operation": decision["operation"],
                    "reason": decision.get("reason"),
                }
            )
        else:
            rejected.append(decision)
            state["mutation_history"].append(
                {
                    "cycle": state["cycle_count"],
                    "status": "rejected",
                    "target_file": mutation.get("target_file"),
                    "operation": mutation.get("operation"),
                    "reason": decision["rejection_reason"],
                }
            )

    mutation_log = {
        "proposed": proposed,
        "approved": approved,
        "rejected": rejected,
        "merged": merged,
    }
    write_json(cycle_dir / "mutation-log.json", mutation_log)
    if merged:
        print(f"Merged {len(merged)} approved file mutation(s).", flush=True)
    if rejected:
        print(f"Rejected {len(rejected)} proposed file mutation(s).", flush=True)
    return mutation_log


def validate_mutation(mutation: Any) -> dict[str, Any]:
    if not isinstance(mutation, dict):
        return {"approved": False, "rejection_reason": "Mutation must be an object"}

    target_type = mutation.get("target_type")
    if target_type != "report":
        return {"approved": False, "rejection_reason": "Only report mutations are allowed"}

    operation = mutation.get("operation")
    if operation != "replace_file":
        return {"approved": False, "rejection_reason": "Only replace_file mutations are allowed"}

    target_file = mutation.get("target_file")
    if target_file not in ALLOWED_REPORT_FILES:
        return {"approved": False, "rejection_reason": "Target file is not allowlisted"}

    content = mutation.get("content")
    if not isinstance(content, str) or not content.strip():
        return {"approved": False, "rejection_reason": "Mutation content must be a non-empty string"}

    if len(content) > 30000:
        return {"approved": False, "rejection_reason": "Mutation content exceeds max length"}

    return {
        "approved": True,
        "target_type": target_type,
        "target_file": target_file,
        "operation": operation,
        "content": content,
        "reason": mutation.get("reason"),
    }
