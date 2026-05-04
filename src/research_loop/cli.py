from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
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
DEFAULT_RESEARCH_TOPICS = [
    {
        "id": "decision_cadence",
        "title": "Decision cadence and workflow reality",
        "description": "Research whether the target users actually face recurring, high-stakes decisions matching the current objective.",
    },
    {
        "id": "workarounds",
        "title": "Existing tools and workarounds",
        "description": "Research current substitutes, including chat, docs, spreadsheets, advisors, meetings, and incumbent software.",
    },
    {
        "id": "switching_pressure",
        "title": "Switching pressure and willingness to pay",
        "description": "Research evidence of dissatisfaction, urgency, pilot interest, spend, or behavior change.",
    },
    {
        "id": "competitors",
        "title": "Competitor and adjacent product map",
        "description": "Research adjacent products and whether they already solve the practical workflow.",
    },
    {
        "id": "failure_modes",
        "title": "Failure modes and objections",
        "description": "Research evidence for kill criteria, adoption blockers, trust issues, and category risks.",
    },
    {
        "id": "pilot_design",
        "title": "Pilot design and measurable test",
        "description": "Research what concrete pilot, interview protocol, or primary evidence would validate or kill the wedge.",
    },
]


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
    run_parser.add_argument(
        "--research-mode",
        choices=["sequential", "planned"],
        default="sequential",
        help="Use the legacy single researcher or planned parallel desk research.",
    )
    run_parser.add_argument(
        "--research-engines",
        default="",
        help="Comma-separated engines for planned research. Defaults to the campaign researcher engine.",
    )
    run_parser.add_argument("--research-workers", type=int, default=6)
    run_parser.add_argument("--research-max-topics", type=int, default=6)
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
    research_config = build_research_config(args, campaign, registry)

    for _ in range(args.cycles):
        state = run_cycle(root, campaign, state, registry, research_config)
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


def build_research_config(args: argparse.Namespace, campaign: Campaign, registry: dict[str, Any]) -> dict[str, Any]:
    if args.research_workers < 1:
        raise ValueError("--research-workers must be at least 1")
    if args.research_max_topics < 1:
        raise ValueError("--research-max-topics must be at least 1")

    if args.research_mode == "sequential":
        engine_name = campaign.raw["engine_roles"]["researcher"]
        adapter = registry[engine_name]
        if not adapter.preflight().search_available:
            raise EngineError("Researcher search is required but not available.")
        return {
            "mode": "sequential",
            "engines": [engine_name],
            "workers": 1,
            "max_topics": 1,
        }

    requested = parse_research_engines(args.research_engines or campaign.raw["engine_roles"]["researcher"])
    usable: list[str] = []
    for engine_name in requested:
        if engine_name not in registry:
            print(f"WARNING: research engine `{engine_name}` is not configured and will be skipped.", flush=True)
            continue
        if not registry[engine_name].preflight().search_available:
            print(f"WARNING: research engine `{engine_name}` has no search capability and will be skipped.", flush=True)
            continue
        usable.append(engine_name)
    if not usable:
        raise EngineError("No configured research engine has search available.")
    return {
        "mode": "planned",
        "engines": usable,
        "workers": args.research_workers,
        "max_topics": args.research_max_topics,
    }


def parse_research_engines(raw: str) -> list[str]:
    engines: list[str] = []
    for item in raw.split(","):
        engine = item.strip()
        if engine and engine not in engines:
            engines.append(engine)
    if not engines:
        raise ValueError("--research-engines must include at least one engine")
    return engines


def run_cycle(
    root: Path,
    campaign: Campaign,
    state: dict[str, Any],
    registry: dict[str, Any],
    research_config: dict[str, Any],
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
        if role == "researcher" and research_config["mode"] == "planned":
            planned_result = run_planned_research(
                root=root,
                campaign=campaign,
                state=state,
                registry=registry,
                cycle_dir=cycle_dir,
                cycle_log_path=cycle_log_path,
                objective=objective,
                context_cache=context_cache,
                research_config=research_config,
            )
            latest_artifacts["researcher"] = str(planned_result["normalized_path"])
            normalized_artifacts["researcher"] = planned_result["artifact"]
            continue

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


def run_planned_research(
    *,
    root: Path,
    campaign: Campaign,
    state: dict[str, Any],
    registry: dict[str, Any],
    cycle_dir: Path,
    cycle_log_path: Path,
    objective: str,
    context_cache: list[tuple[str, str]],
    research_config: dict[str, Any],
) -> dict[str, Any]:
    plan = build_campaign_research_plan(
        campaign=campaign,
        objective=objective,
        usable_engines=research_config["engines"],
        max_topics=research_config["max_topics"],
    )
    write_json(cycle_dir / "research-plan.json", plan)
    log_cycle_line(
        cycle_log_path,
        f"Planned {len(plan['assignments'])} researcher(s) across {len(plan['topics'])} topic(s).",
    )

    worker_results: list[dict[str, Any]] = []
    failed_workers: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, int(research_config["workers"]))) as executor:
        futures = {
            executor.submit(
                invoke_research_worker,
                root,
                campaign,
                state,
                registry,
                cycle_dir,
                cycle_log_path,
                objective,
                context_cache,
                assignment,
            ): assignment
            for assignment in plan["assignments"]
        }
        for future in as_completed(futures):
            assignment = futures[future]
            try:
                worker_results.append(future.result())
            except Exception as exc:  # noqa: BLE001 - worker failures are recorded and merged.
                failed = {
                    "worker_id": assignment["worker_id"],
                    "engine": assignment["engine"],
                    "topic_id": assignment["topic"]["id"],
                    "error": str(exc),
                }
                failed_workers.append(failed)
                log_cycle_line(
                    cycle_log_path,
                    f"WARNING: `{assignment['worker_id']}` with `{assignment['engine']}` failed: {exc}",
                )

    worker_results.sort(key=lambda item: str(item.get("worker_id") or ""))
    failed_workers.sort(key=lambda item: str(item.get("worker_id") or ""))
    merged, metadata = merge_campaign_research_artifacts(worker_results, failed_workers)
    metadata["plan"] = plan
    write_json(cycle_dir / "research-merge.json", metadata)
    researcher_dir = ensure_directory(cycle_dir / "researcher")
    normalized_path = researcher_dir / "normalized.json"
    write_json(normalized_path, merged)
    log_cycle_line(
        cycle_log_path,
        f"Merged {len(worker_results)} successful researcher(s); {len(failed_workers)} failed.",
    )
    log_artifact_summary(cycle_log_path, "researcher", "merged", merged, 0.0)
    return {"artifact": merged, "normalized_path": normalized_path}


def build_campaign_research_plan(
    *,
    campaign: Campaign,
    objective: str,
    usable_engines: list[str],
    max_topics: int,
) -> dict[str, Any]:
    if not usable_engines:
        raise EngineError("Planned research requires at least one usable engine.")
    topics = [
        {
            **topic,
            "objective": objective,
            "campaign_slug": campaign.slug,
        }
        for topic in DEFAULT_RESEARCH_TOPICS[:max_topics]
    ]
    assignments = []
    for index, topic in enumerate(topics, start=1):
        engine = usable_engines[(index - 1) % len(usable_engines)]
        assignments.append(
            {
                "worker_id": f"researcher-{index:04d}",
                "engine": engine,
                "topic": topic,
                "assignment_reason": f"Desk-research topic `{topic['id']}` assigned to `{engine}`.",
            }
        )
    return {
        "mode": "planned",
        "campaign": campaign.slug,
        "objective": objective,
        "usable_engines": usable_engines,
        "topics": topics,
        "assignments": assignments,
    }


def invoke_research_worker(
    root: Path,
    campaign: Campaign,
    state: dict[str, Any],
    registry: dict[str, Any],
    cycle_dir: Path,
    cycle_log_path: Path,
    objective: str,
    context_cache: list[tuple[str, str]],
    assignment: dict[str, Any],
) -> dict[str, Any]:
    role = "researcher"
    worker_id = assignment["worker_id"]
    engine_name = assignment["engine"]
    adapter = registry[engine_name]
    role_dir = ensure_directory(cycle_dir / worker_id)
    write_json(role_dir / "engine.json", {"engine": engine_name})
    write_json(role_dir / "topic.json", assignment["topic"])

    role_context = build_role_context(role, campaign, state, {}, context_cache)
    role_context.append(("Assigned Research Topic", json.dumps(assignment["topic"], indent=2, sort_keys=True)))
    prompt_text = render_prompt(root, role, campaign, objective, role_context)
    prompt_path = role_dir / "prompt.txt"
    prompt_path.write_text(prompt_text, encoding="utf-8")
    log_cycle_line(
        cycle_log_path,
        f"Starting `{worker_id}` with `{engine_name}`. Prompt: {prompt_path.relative_to(root)}",
    )
    started = time.monotonic()
    raw_output_path = adapter.invoke(
        role=worker_id,
        prompt_text=prompt_text,
        output_dir=role_dir,
        search_required=True,
    )
    artifact = adapter.normalize(raw_output_path)
    normalized_path = role_dir / "normalized.json"
    write_json(normalized_path, artifact)
    log_artifact_summary(cycle_log_path, worker_id, engine_name, artifact, time.monotonic() - started)
    return {
        "worker_id": worker_id,
        "engine": engine_name,
        "topic_id": assignment["topic"]["id"],
        "artifact": artifact,
        "normalized_path": str(normalized_path),
    }


def merge_campaign_research_artifacts(
    worker_results: list[dict[str, Any]],
    failed_workers: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not worker_results:
        raise EngineError("All planned researchers failed; no valid researcher artifact can be merged.")

    findings: list[dict[str, Any]] = []
    sources_by_key: dict[str, dict[str, Any]] = {}
    source_provenance: dict[str, list[str]] = {}
    supports: list[str] = []
    weakens: list[str] = []
    kills: list[str] = []
    contradictions: dict[str, dict[str, str]] = {}
    open_questions: list[str] = []
    resolved: list[str] = []
    summaries: list[str] = []
    claim_statuses: dict[str, str] = {}
    kill_counts: dict[str, int] = {}
    pilot = {
        "target_user": None,
        "pain_statement": None,
        "current_workaround": None,
        "why_existing_tools_fail": None,
    }

    for result in worker_results:
        artifact = result["artifact"]
        summaries.append(f"{result['worker_id']} ({result['topic_id']}): {artifact.get('summary', '').strip()}")
        findings.extend(artifact.get("findings", []))
        supports = append_unique_many(supports, artifact.get("supports_claims", []))
        weakens = append_unique_many(weakens, artifact.get("weakens_claims", []))
        kills = append_unique_many(kills, artifact.get("triggered_kill_criteria", []))
        open_questions = append_unique_many(open_questions, artifact.get("open_questions", []))
        resolved = append_unique_many(resolved, artifact.get("resolved_contradictions", []))
        for item in artifact.get("contradictions", []):
            if not isinstance(item, dict):
                continue
            identifier = str(item.get("id") or item.get("detail") or "contradiction")
            contradictions[identifier] = {"id": identifier, "detail": str(item.get("detail") or "")}
        for source in artifact.get("sources", []):
            key = source_dedupe_key(source)
            sources_by_key.setdefault(key, source)
            source_provenance.setdefault(key, [])
            source_provenance[key] = append_unique(source_provenance[key], result["worker_id"])
        for item in artifact.get("claim_statuses", []):
            if isinstance(item, dict) and item.get("claim_id"):
                claim_statuses[str(item["claim_id"])] = str(item.get("status") or "untested")
        for item in artifact.get("kill_criterion_source_counts", []):
            if isinstance(item, dict) and item.get("kill_criterion_id"):
                criterion_id = str(item["kill_criterion_id"])
                kill_counts[criterion_id] = max(
                    kill_counts.get(criterion_id, 0),
                    int(item.get("source_count") or 0),
                )
        artifact_pilot = artifact.get("pilot_recommendation") or {}
        for key in pilot:
            if not pilot[key] and artifact_pilot.get(key):
                pilot[key] = artifact_pilot[key]

    if not findings and not sources_by_key:
        raise EngineError("Planned researchers returned no findings or sources to merge.")

    confidence_values = [
        float(result["artifact"].get("confidence") or 0)
        for result in worker_results
    ]
    merged = {
        "objective": "Merged planned desk research across campaign subtopics.",
        "summary": "Merged planned desk research from multiple researcher workers.\n\n" + "\n".join(summaries),
        "findings": findings,
        "sources": list(sources_by_key.values()),
        "supports_claims": supports,
        "weakens_claims": weakens,
        "triggered_kill_criteria": kills,
        "contradictions": list(contradictions.values()),
        "open_questions": open_questions,
        "next_recommended_objective": first_non_empty(
            [result["artifact"].get("next_recommended_objective") for result in worker_results]
        ),
        "confidence": sum(confidence_values) / len(confidence_values),
        "proposed_mutations": [],
        "recommended_verdict": "active",
        "claim_statuses": [
            {"claim_id": claim_id, "status": status}
            for claim_id, status in sorted(claim_statuses.items())
        ],
        "kill_criterion_source_counts": [
            {"kill_criterion_id": criterion_id, "source_count": source_count}
            for criterion_id, source_count in sorted(kill_counts.items())
        ],
        "resolved_contradictions": resolved,
        "pilot_recommendation": pilot,
    }
    metadata = {
        "successful_workers": [
            {
                "worker_id": result["worker_id"],
                "engine": result["engine"],
                "topic_id": result["topic_id"],
                "normalized_path": result.get("normalized_path"),
            }
            for result in worker_results
        ],
        "failed_workers": failed_workers,
        "source_provenance": [
            {
                "dedupe_key": key,
                "source": sources_by_key[key],
                "worker_ids": workers,
            }
            for key, workers in sorted(source_provenance.items())
        ],
    }
    return merged, metadata


def source_dedupe_key(source: dict[str, Any]) -> str:
    locator = str(source.get("locator") or "").strip().lower().rstrip("/")
    if locator:
        return f"locator:{locator}"
    return f"title:{str(source.get('title') or '').strip().lower()}"


def append_unique(values: list[str], value: Any) -> list[str]:
    text = str(value)
    if text and text not in values:
        values.append(text)
    return values


def append_unique_many(values: list[str], candidates: Any) -> list[str]:
    if isinstance(candidates, list):
        for item in candidates:
            append_unique(values, item)
    return values


def first_non_empty(values: list[Any]) -> Any:
    for value in values:
        if value:
            return value
    return None


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
