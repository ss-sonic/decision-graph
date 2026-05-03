from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from .doc_artifacts import (
    DOC_ROLES,
    doc_artifact_schema,
    validate_doc_artifact,
    validate_editor_against_skeptic,
)
from .doc_prompts import render_doc_prompt
from .doc_spec import load_doc_spec
from .doc_state import (
    TERMINAL_DOC_VERDICTS,
    doc_run_dir,
    latest_doc_input_path,
    load_or_initialize_doc_state,
    next_doc_cycle_dir,
    save_doc_state,
)
from .engines import build_registry
from .engines.base import EngineError, unwrap_artifact_payload
from .engines.claude import ClaudeAdapter
from .engines.codex import CodexAdapter
from .utils import ensure_directory, read_json, read_text, write_json


ROLE_SEQUENCE = ["extractor", "researcher", "improver", "skeptic", "editor", "judge"]
ROLE_ENGINES = {
    "extractor": "claude",
    "researcher": "claude",
    "improver": "codex",
    "skeptic": "codex",
    "editor": "claude",
    "judge": "codex",
}
DOWNSTREAM_ROLES = ["improver", "skeptic", "editor", "judge"]
BUDGET_DEFAULTS = {
    "cheap": {"workers": 2, "max_units": 4},
    "standard": {"workers": 4, "max_units": 8},
    "deep": {"workers": 8, "max_units": 16},
    "audit": {"workers": 8, "max_units": 16},
}
IMPORTANCE_RANK = {
    "critical": 0,
    "highest": 0,
    "high": 1,
    "medium": 2,
    "moderate": 2,
    "low": 3,
}


class DocClaudeAdapter(ClaudeAdapter):
    def output_schema(self, role: str) -> dict[str, Any]:
        return doc_artifact_schema(role)


class DocCodexAdapter(CodexAdapter):
    def output_schema(self, role: str) -> dict[str, Any]:
        return doc_artifact_schema(role)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, EngineError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="doc-loop")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run evidence-backed document improvement cycles")
    run_parser.add_argument("--doc", required=True)
    run_parser.add_argument(
        "--supporting-doc",
        action="append",
        default=[],
        help="Markdown evidence file to provide as private/supporting context. May be repeated.",
    )
    run_parser.add_argument(
        "--spec",
        help="YAML/JSON document intent spec controlling audience, voice, risk posture, and public/internal notes.",
    )
    run_parser.add_argument(
        "--research-mode",
        choices=["sequential", "planned"],
        default="planned",
        help="Use the legacy single researcher or planned parallel research.",
    )
    run_parser.add_argument(
        "--research-engines",
        default="claude",
        help="Comma-separated research engines to use in planned mode, e.g. claude,codex.",
    )
    run_parser.add_argument(
        "--research-budget",
        choices=sorted(BUDGET_DEFAULTS),
        default="standard",
        help="Research planning budget profile.",
    )
    run_parser.add_argument("--research-workers", type=int)
    run_parser.add_argument("--research-max-units", type=int)
    run_parser.add_argument("--cycles", type=int, default=1)
    run_parser.set_defaults(func=cmd_run)

    status_parser = subparsers.add_parser("status", help="Show document improvement state")
    status_parser.add_argument("--doc", required=True)
    status_parser.set_defaults(func=cmd_status)

    latest_parser = subparsers.add_parser("latest", help="Print the latest revised markdown path")
    latest_parser.add_argument("--doc", required=True)
    latest_parser.set_defaults(func=cmd_latest)

    return parser


def cmd_run(args: argparse.Namespace) -> int:
    root = Path.cwd()
    doc_path = resolve_doc(root, args.doc)
    registry = build_doc_registry()
    state = load_or_initialize_doc_state(root, doc_path)
    if args.supporting_doc:
        state["supporting_docs"] = [str(path) for path in resolve_supporting_docs(root, args.supporting_doc)]
        save_doc_state(root, doc_path, state)
    if args.spec:
        spec_path = resolve_spec(root, args.spec)
        load_doc_spec(spec_path)
        state["doc_spec_path"] = str(spec_path)
        save_doc_state(root, doc_path, state)

    research_config = build_research_config(args, registry)

    for _ in range(args.cycles):
        state = run_doc_cycle(root, doc_path, state, registry, research_config)
        save_doc_state(root, doc_path, state)
        print(f"Cycle {state['cycle_count']} complete. Verdict: {state['verdict']}")
        if state["verdict"] in TERMINAL_DOC_VERDICTS:
            break
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path.cwd()
    doc_path = resolve_doc(root, args.doc)
    state = load_or_initialize_doc_state(root, doc_path)
    print(f"Document: {doc_path}")
    print(f"Run directory: {doc_run_dir(root, doc_path)}")
    print(f"Verdict: {state['verdict']}")
    print(f"Cycles: {state['cycle_count']}")
    print(f"Latest revision: {state.get('latest_revision') or '(none yet)'}")
    print(f"Latest internal notes: {state.get('latest_internal_notes') or '(none yet)'}")
    print(f"Next focus: {state.get('next_focus') or '(none)'}")
    if state.get("doc_spec_path"):
        print(f"Spec: {state['doc_spec_path']}")
    supporting_docs = state.get("supporting_docs") or []
    if supporting_docs:
        print("Supporting docs:")
        for path in supporting_docs:
            print(f"- {path}")
    return 0


def cmd_latest(args: argparse.Namespace) -> int:
    root = Path.cwd()
    doc_path = resolve_doc(root, args.doc)
    state = load_or_initialize_doc_state(root, doc_path)
    latest = state.get("latest_revision")
    if not latest:
        raise ValueError("No revised version exists yet. Run at least one doc cycle first.")
    print(latest)
    return 0


def resolve_doc(root: Path, raw_path: str) -> Path:
    path = resolve_user_path(root, raw_path)
    if not path.exists():
        raise ValueError(f"Document not found: {path}")
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("doc-loop v1 only supports markdown documents")
    return path


def resolve_supporting_docs(root: Path, raw_paths: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for raw_path in raw_paths:
        path = resolve_user_path(root, raw_path)
        if not path.exists():
            raise ValueError(f"Supporting document not found: {path}")
        if path.suffix.lower() not in {".md", ".markdown"}:
            raise ValueError("supporting documents must be markdown files")
        resolved.append(path)
    return resolved


def resolve_spec(root: Path, raw_path: str) -> Path:
    path = resolve_user_path(root, raw_path)
    if not path.exists():
        raise ValueError(f"Document spec not found: {path}")
    if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
        raise ValueError("document spec must be a YAML or JSON file")
    return path


def resolve_user_path(root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def build_doc_registry() -> dict[str, Any]:
    import os

    if os.getenv("RESEARCH_LOOP_MOCK_ENGINES") == "1":
        return build_registry()
    return {
        "claude": DocClaudeAdapter(),
        "codex": DocCodexAdapter(),
    }


def build_research_config(args: argparse.Namespace, registry: dict[str, Any]) -> dict[str, Any]:
    defaults = BUDGET_DEFAULTS[args.research_budget]
    workers = args.research_workers if args.research_workers is not None else defaults["workers"]
    max_units = args.research_max_units if args.research_max_units is not None else defaults["max_units"]
    if workers < 1:
        raise ValueError("--research-workers must be at least 1")
    if max_units < 1:
        raise ValueError("--research-max-units must be at least 1")

    if args.research_mode == "sequential":
        adapter = registry[ROLE_ENGINES["researcher"]]
        if not adapter.preflight().search_available:
            raise EngineError("Document researcher search is required but not available.")
        return {
            "mode": "sequential",
            "budget": args.research_budget,
            "engines": [ROLE_ENGINES["researcher"]],
            "workers": 1,
            "max_units": 1,
        }

    requested = parse_research_engines(args.research_engines)
    usable: list[str] = []
    for engine in requested:
        if engine not in registry:
            print(f"WARNING: research engine `{engine}` is not configured and will be skipped.", flush=True)
            continue
        preflight = registry[engine].preflight()
        if not preflight.search_available:
            print(f"WARNING: research engine `{engine}` has no search capability and will be skipped.", flush=True)
            continue
        usable.append(engine)
    if not usable:
        raise EngineError("No configured research engine has search available.")
    return {
        "mode": "planned",
        "budget": args.research_budget,
        "engines": usable,
        "workers": workers,
        "max_units": max_units,
    }


def parse_research_engines(raw: str) -> list[str]:
    engines = []
    for item in raw.split(","):
        engine = item.strip()
        if engine and engine not in engines:
            engines.append(engine)
    if not engines:
        raise ValueError("--research-engines must include at least one engine")
    return engines


def run_doc_cycle(
    root: Path,
    doc_path: Path,
    state: dict[str, Any],
    registry: dict[str, Any],
    research_config: dict[str, Any],
) -> dict[str, Any]:
    cycle_dir = next_doc_cycle_dir(root, doc_path, state)
    cycle_number = int(state.get("cycle_count", 0)) + 1
    focus = str(state.get("next_focus") or "Improve document truth, reasoning, evidence, and clarity.")
    cycle_log_path = cycle_dir / "cycle.log"
    input_path = latest_doc_input_path(doc_path, state)
    input_markdown = read_text(input_path)
    (cycle_dir / "input.md").write_text(input_markdown, encoding="utf-8")
    supporting_context = load_supporting_context(state)
    if supporting_context:
        (cycle_dir / "supporting-docs.md").write_text(supporting_context, encoding="utf-8")
    doc_spec = load_current_doc_spec(state)
    (cycle_dir / "doc-spec.json").write_text(json.dumps(doc_spec, indent=2, sort_keys=True), encoding="utf-8")

    artifacts: dict[str, dict[str, Any]] = {}
    latest_artifacts: dict[str, str] = {}

    log_doc_line(cycle_log_path, f"=== Doc Cycle {cycle_number} ===")
    log_doc_line(cycle_log_path, f"Document: {doc_path}")
    log_doc_line(cycle_log_path, f"Input: {input_path}")
    log_doc_line(cycle_log_path, f"Focus: {focus}")

    extractor = invoke_doc_role(
        root=root,
        cycle_dir=cycle_dir,
        doc_path=doc_path,
        input_markdown=input_markdown,
        focus=focus,
        state=state,
        artifacts=artifacts,
        supporting_context=supporting_context,
        doc_spec=doc_spec,
        registry=registry,
        role="extractor",
        role_dir_name="extractor",
        engine_name=ROLE_ENGINES["extractor"],
        cycle_log_path=cycle_log_path,
    )
    artifacts["extractor"] = extractor["artifact"]
    latest_artifacts["extractor"] = str(extractor["normalized_path"])

    if research_config["mode"] == "sequential":
        researcher = invoke_doc_role(
            root=root,
            cycle_dir=cycle_dir,
            doc_path=doc_path,
            input_markdown=input_markdown,
            focus=focus,
            state=state,
            artifacts=artifacts,
            supporting_context=supporting_context,
            doc_spec=doc_spec,
            registry=registry,
            role="researcher",
            role_dir_name="researcher",
            engine_name=ROLE_ENGINES["researcher"],
            cycle_log_path=cycle_log_path,
            search_required=True,
        )
        artifacts["researcher"] = researcher["artifact"]
        latest_artifacts["researcher"] = str(researcher["normalized_path"])
    else:
        research = run_planned_research(
            root=root,
            cycle_dir=cycle_dir,
            doc_path=doc_path,
            input_markdown=input_markdown,
            focus=focus,
            state=state,
            artifacts=artifacts,
            supporting_context=supporting_context,
            doc_spec=doc_spec,
            registry=registry,
            research_config=research_config,
            cycle_log_path=cycle_log_path,
        )
        artifacts["researcher"] = research["artifact"]
        latest_artifacts["researcher"] = str(research["normalized_path"])

    for role in DOWNSTREAM_ROLES:
        engine_name = ROLE_ENGINES[role]
        result = invoke_doc_role(
            root=root,
            cycle_dir=cycle_dir,
            doc_path=doc_path,
            input_markdown=input_markdown,
            focus=focus,
            state=state,
            artifacts=artifacts,
            supporting_context=supporting_context,
            doc_spec=doc_spec,
            registry=registry,
            role=role,
            role_dir_name=role,
            engine_name=engine_name,
            cycle_log_path=cycle_log_path,
        )
        if role == "editor":
            validate_editor_against_skeptic(result["artifact"], artifacts["skeptic"])
        artifacts[role] = result["artifact"]
        latest_artifacts[role] = str(result["normalized_path"])

    editor = artifacts["editor"]
    judge = artifacts["judge"]
    revised_path = cycle_dir / "revised.md"
    internal_notes_path = cycle_dir / "internal-notes.md"
    changelog_path = cycle_dir / "change-log.md"
    validation_warnings = validate_editor_against_doc_spec(editor, doc_spec)
    revised_path.write_text(editor["revised_markdown"].rstrip() + "\n", encoding="utf-8")
    internal_notes_path.write_text(
        render_internal_notes(editor["internal_notes_markdown"], validation_warnings),
        encoding="utf-8",
    )
    changelog_path.write_text(render_changelog(cycle_number, editor), encoding="utf-8")
    for warning in validation_warnings:
        log_doc_line(cycle_log_path, f"WARNING: {warning}")

    updated = dict(state)
    updated["cycle_count"] = cycle_number
    updated["verdict"] = judge["verdict"]
    updated["next_focus"] = judge.get("next_focus")
    updated["latest_revision"] = str(revised_path)
    updated["latest_internal_notes"] = str(internal_notes_path)
    updated["latest_cycle_dir"] = str(cycle_dir)
    updated["latest_artifacts"] = latest_artifacts
    updated.setdefault("history", []).append(
        {
            "cycle": cycle_number,
            "verdict": judge["verdict"],
            "summary": judge.get("summary"),
            "revised_path": str(revised_path),
            "internal_notes_path": str(internal_notes_path),
            "applied_proposal_ids": editor.get("applied_proposal_ids", []),
        }
    )
    return updated


def invoke_doc_role(
    *,
    root: Path,
    cycle_dir: Path,
    doc_path: Path,
    input_markdown: str,
    focus: str,
    state: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    supporting_context: str,
    doc_spec: dict[str, Any],
    registry: dict[str, Any],
    role: str,
    role_dir_name: str,
    engine_name: str,
    cycle_log_path: Path,
    search_required: bool = False,
    extra_context: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    adapter = registry[engine_name]
    role_dir = ensure_directory(cycle_dir / role_dir_name)
    context_sections = build_doc_context(state, artifacts, supporting_context, doc_spec)
    if extra_context:
        context_sections.extend(extra_context)
    prompt_text = render_doc_prompt(
        root=root,
        role=role,
        doc_path=doc_path,
        input_markdown=input_markdown,
        focus=focus,
        context_sections=context_sections,
    )
    prompt_path = role_dir / "prompt.txt"
    prompt_path.write_text(prompt_text, encoding="utf-8")
    log_doc_line(cycle_log_path, f"Starting `{role_dir_name}` with `{engine_name}`. Prompt: {prompt_path.relative_to(root)}")
    started = time.monotonic()
    raw_path = adapter.invoke(
        role=role_dir_name if role == "researcher" and role_dir_name.startswith("researcher-") else role,
        prompt_text=prompt_text,
        output_dir=role_dir,
        search_required=search_required,
    )
    artifact = normalize_doc_output(role, raw_path)
    normalized_path = role_dir / "normalized.json"
    write_json(normalized_path, artifact)
    log_doc_summary(cycle_log_path, role_dir_name, engine_name, artifact, time.monotonic() - started)
    return {"artifact": artifact, "normalized_path": normalized_path}


def run_planned_research(
    *,
    root: Path,
    cycle_dir: Path,
    doc_path: Path,
    input_markdown: str,
    focus: str,
    state: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    supporting_context: str,
    doc_spec: dict[str, Any],
    registry: dict[str, Any],
    research_config: dict[str, Any],
    cycle_log_path: Path,
) -> dict[str, Any]:
    plan = build_research_plan(
        artifacts["extractor"],
        usable_engines=research_config["engines"],
        budget=research_config["budget"],
        max_units=research_config["max_units"],
        max_workers=research_config["workers"],
    )
    plan_path = cycle_dir / "research-plan.json"
    write_json(plan_path, plan)
    log_doc_line(
        cycle_log_path,
        f"Planned {len(plan['assignments'])} research worker(s) across {len(plan['selected_units'])} unit(s).",
    )

    worker_results: list[dict[str, Any]] = []
    failed_workers: list[dict[str, str]] = []
    max_workers = max(1, int(plan["max_parallel_workers"]))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                invoke_research_worker,
                root,
                cycle_dir,
                doc_path,
                input_markdown,
                focus,
                state,
                artifacts,
                supporting_context,
                doc_spec,
                registry,
                assignment,
                cycle_log_path,
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
                    "work_unit_id": assignment["work_unit"]["id"],
                    "error": str(exc),
                }
                failed_workers.append(failed)
                log_doc_line(
                    cycle_log_path,
                    f"WARNING: `{assignment['worker_id']}` with `{assignment['engine']}` failed: {exc}",
                )

    worker_results.sort(key=lambda item: str(item.get("worker_id") or ""))
    failed_workers.sort(key=lambda item: str(item.get("worker_id") or ""))
    merged, metadata = merge_research_artifacts(worker_results, failed_workers)
    metadata["plan_path"] = str(plan_path)
    merge_path = cycle_dir / "research-merge.json"
    write_json(merge_path, metadata)
    researcher_dir = ensure_directory(cycle_dir / "researcher")
    normalized_path = researcher_dir / "normalized.json"
    write_json(normalized_path, merged)
    log_doc_line(
        cycle_log_path,
        f"Merged {len(worker_results)} successful research worker(s); {len(failed_workers)} failed.",
    )
    return {"artifact": merged, "normalized_path": normalized_path}


def invoke_research_worker(
    root: Path,
    cycle_dir: Path,
    doc_path: Path,
    input_markdown: str,
    focus: str,
    state: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    supporting_context: str,
    doc_spec: dict[str, Any],
    registry: dict[str, Any],
    assignment: dict[str, Any],
    cycle_log_path: Path,
) -> dict[str, Any]:
    role_dir = ensure_directory(cycle_dir / assignment["worker_id"])
    write_json(role_dir / "engine.json", {"engine": assignment["engine"]})
    write_json(role_dir / "work-unit.json", assignment["work_unit"])
    result = invoke_doc_role(
        root=root,
        cycle_dir=cycle_dir,
        doc_path=doc_path,
        input_markdown=input_markdown,
        focus=focus,
        state=state,
        artifacts=artifacts,
        supporting_context=supporting_context,
        doc_spec=doc_spec,
        registry=registry,
        role="researcher",
        role_dir_name=assignment["worker_id"],
        engine_name=assignment["engine"],
        cycle_log_path=cycle_log_path,
        search_required=True,
        extra_context=[
            ("Assigned Research Work Unit", json.dumps(assignment["work_unit"], indent=2, sort_keys=True)),
            ("Research Assignment", json.dumps(assignment, indent=2, sort_keys=True)),
        ],
    )
    return {
        "worker_id": assignment["worker_id"],
        "engine": assignment["engine"],
        "work_unit_id": assignment["work_unit"]["id"],
        "artifact": result["artifact"],
        "normalized_path": str(result["normalized_path"]),
    }


def build_research_plan(
    extractor_artifact: dict[str, Any],
    *,
    usable_engines: list[str],
    budget: str,
    max_units: int,
    max_workers: int,
) -> dict[str, Any]:
    if not usable_engines:
        raise EngineError("Research planning requires at least one usable engine.")
    units = extract_research_units(extractor_artifact)
    selected = sorted(units, key=research_unit_sort_key)[:max_units]
    if not selected:
        raise EngineError("Extractor did not produce any researchable gaps or units.")

    assignments: list[dict[str, Any]] = []
    round_robin_index = 0
    for unit in selected:
        assigned_engines: list[str]
        if budget == "audit":
            assigned_engines = list(usable_engines)
        elif should_duplicate_unit(unit, budget) and len(usable_engines) > 1:
            assigned_engines = list(usable_engines)
        else:
            assigned_engines = [usable_engines[round_robin_index % len(usable_engines)]]
            round_robin_index += 1
        for engine in assigned_engines:
            worker_id = f"researcher-{len(assignments) + 1:04d}"
            assignments.append(
                {
                    "worker_id": worker_id,
                    "engine": engine,
                    "work_unit": unit,
                    "assignment_reason": research_assignment_reason(unit, engine, assigned_engines, budget),
                    "priority": str(unit.get("importance") or "medium"),
                }
            )

    return {
        "mode": "planned",
        "budget": budget,
        "usable_engines": usable_engines,
        "max_units": max_units,
        "max_parallel_workers": max_workers,
        "selected_units": selected,
        "assignments": assignments,
    }


def extract_research_units(extractor_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    raw_units = extractor_artifact.get("research_units") or []
    if raw_units:
        return [canonical_research_unit(item, f"unit-{index}") for index, item in enumerate(raw_units, start=1)]

    gaps = extractor_artifact.get("top_evidence_gaps") or []
    if gaps:
        return [
            canonical_research_unit(
                {
                    "id": gap.get("id") or f"gap-{index}",
                    "kind": "evidence_gap",
                    "claim_ids": gap.get("claim_ids") or [],
                    "target_heading": "",
                    "question": gap.get("question") or "",
                    "importance": gap.get("importance") or "medium",
                    "research_hint": gap.get("research_hint") or "",
                    "success_criteria": "Return evidence that directly supports or weakens the linked claim ids.",
                },
                f"gap-{index}",
            )
            for index, gap in enumerate(gaps, start=1)
        ]

    units = []
    for index, claim in enumerate(extractor_artifact.get("claims") or [], start=1):
        status = str(claim.get("support_status") or "").lower()
        if status in {"supported", "well_supported", "strongly_supported"}:
            continue
        units.append(
            canonical_research_unit(
                {
                    "id": f"claim-{index}",
                    "kind": "unsupported_claim",
                    "claim_ids": [str(claim.get("id") or f"claim-{index}")],
                    "target_heading": "",
                    "question": str(claim.get("issue") or claim.get("text") or ""),
                    "importance": str(claim.get("importance") or "medium"),
                    "research_hint": "Find evidence that directly supports or weakens this claim.",
                    "success_criteria": "Return evidence that makes the claim more defensible or shows it should be softened.",
                },
                f"claim-{index}",
            )
        )
    return units


def canonical_research_unit(raw: dict[str, Any], fallback_id: str) -> dict[str, Any]:
    return {
        "id": str(raw.get("id") or fallback_id),
        "kind": str(raw.get("kind") or "evidence_gap"),
        "claim_ids": [str(item) for item in raw.get("claim_ids", [])],
        "target_heading": str(raw.get("target_heading") or ""),
        "question": str(raw.get("question") or ""),
        "importance": str(raw.get("importance") or "medium"),
        "research_hint": str(raw.get("research_hint") or ""),
        "success_criteria": str(raw.get("success_criteria") or "Return exact evidence for this work unit."),
    }


def research_unit_sort_key(unit: dict[str, Any]) -> tuple[int, int, str]:
    importance = IMPORTANCE_RANK.get(str(unit.get("importance") or "").lower(), 2)
    kind = str(unit.get("kind") or "").lower()
    kind_rank = 0 if kind == "evidence_gap" else 1 if "claim" in kind else 2
    return (importance, kind_rank, str(unit.get("id") or ""))


def should_duplicate_unit(unit: dict[str, Any], budget: str) -> bool:
    if budget == "cheap":
        return is_critical_research_unit(unit)
    if budget in {"standard", "deep"}:
        return is_critical_research_unit(unit)
    return False


def is_critical_research_unit(unit: dict[str, Any]) -> bool:
    importance = str(unit.get("importance") or "").lower()
    searchable_text = " ".join(
        str(unit.get(key) or "")
        for key in ["kind", "target_heading", "question", "research_hint", "success_criteria"]
    ).lower()
    critical_markers = [
        "compliance",
        "legal",
        "religious",
        "sharia",
        "financial",
        "spec-critical",
        "spec critical",
        "contradiction",
        "safety",
    ]
    return importance == "critical" or any(marker in searchable_text for marker in critical_markers)


def research_assignment_reason(
    unit: dict[str, Any],
    engine: str,
    assigned_engines: list[str],
    budget: str,
) -> str:
    if len(assigned_engines) > 1:
        return f"{budget} budget duplicates critical or sensitive unit across engines; `{engine}` assigned."
    return f"{budget} budget assigns unit to `{engine}` for coverage."


def merge_research_artifacts(
    worker_results: list[dict[str, Any]],
    failed_workers: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not worker_results:
        raise EngineError("All planned research workers failed; no valid researcher artifact can be merged.")

    groups: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    researched_gap_ids: list[str] = []
    unresolved_gaps: list[str] = []
    summaries: list[str] = []

    for result in worker_results:
        artifact = result["artifact"]
        summary = str(artifact.get("summary") or "").strip()
        if summary:
            summaries.append(f"{result['worker_id']} ({result['engine']}): {summary}")
        researched_gap_ids = append_unique_many(researched_gap_ids, artifact.get("researched_gap_ids", []))
        unresolved_gaps = append_unique_many(unresolved_gaps, artifact.get("unresolved_gaps", []))
        for item in artifact.get("evidence_items", []):
            key = evidence_dedupe_key(item)
            if key not in groups:
                groups[key] = {
                    "canonical": dict(item),
                    "items": [],
                    "worker_ids": [],
                    "engines": [],
                    "work_unit_ids": [],
                }
                order.append(key)
            group = groups[key]
            group["items"].append(item)
            group["worker_ids"] = append_unique(group["worker_ids"], result["worker_id"])
            group["engines"] = append_unique(group["engines"], result["engine"])
            group["work_unit_ids"] = append_unique(group["work_unit_ids"], result["work_unit_id"])
            group["canonical"]["claim_ids"] = append_unique_many(
                group["canonical"].get("claim_ids", []),
                item.get("claim_ids", []),
            )
            group["canonical"]["confidence"] = max(
                float(group["canonical"].get("confidence") or 0),
                float(item.get("confidence") or 0),
            )

    if not order:
        raise EngineError("Planned research returned no evidence_items to merge.")

    evidence_items = [groups[key]["canonical"] for key in order]
    evidence_groups = []
    for key in order:
        group = groups[key]
        evidence_groups.append(
            {
                "dedupe_key": key,
                "canonical_evidence_id": group["canonical"].get("id"),
                "engines": group["engines"],
                "worker_ids": group["worker_ids"],
                "work_unit_ids": group["work_unit_ids"],
                "source_variants": [
                    {
                        "id": item.get("id"),
                        "source": item.get("source"),
                        "locator": item.get("locator"),
                        "supports_or_weakens": item.get("supports_or_weakens"),
                        "confidence": item.get("confidence"),
                    }
                    for item in group["items"]
                ],
                "confirmation_status": confirmation_status(group),
            }
        )

    merged = {
        "summary": "Merged planned research evidence from parallel workers.\n\n" + "\n".join(summaries),
        "researched_gap_ids": researched_gap_ids,
        "evidence_items": evidence_items,
        "unresolved_gaps": unresolved_gaps,
    }
    metadata = {
        "successful_workers": [
            {
                "worker_id": result["worker_id"],
                "engine": result["engine"],
                "work_unit_id": result["work_unit_id"],
                "normalized_path": result.get("normalized_path"),
            }
            for result in worker_results
        ],
        "failed_workers": failed_workers,
        "evidence_groups": evidence_groups,
    }
    return merged, metadata


def evidence_dedupe_key(item: dict[str, Any]) -> str:
    locator = str(item.get("locator") or "").strip().lower().rstrip("/")
    if locator:
        return f"locator:{locator}"
    source = str(item.get("source") or "").strip().lower()
    title = str(item.get("title") or item.get("finding") or "").strip().lower()
    return f"source:{source}|{title}"


def confirmation_status(group: dict[str, Any]) -> str:
    engines = group["engines"]
    stances = {
        str(item.get("supports_or_weakens") or "").strip().lower()
        for item in group["items"]
        if str(item.get("supports_or_weakens") or "").strip()
    }
    if len(engines) > 1 and len(stances) > 1:
        return "conflicting"
    if len(engines) > 1:
        return "multi_engine_confirmed"
    if any(float(item.get("confidence") or 0) < 0.35 for item in group["items"]):
        return "needs_human_review"
    return "single_engine"


def append_unique(values: list[str], value: Any) -> list[str]:
    text = str(value)
    if text and text not in values:
        values.append(text)
    return values


def append_unique_many(values: list[str], candidates: Any) -> list[str]:
    if not isinstance(candidates, list):
        return values
    for item in candidates:
        append_unique(values, item)
    return values


def normalize_doc_output(role: str, raw_path: Path) -> dict[str, Any]:
    payload = read_json(raw_path)
    normalized = unwrap_artifact_payload(payload)
    validate_doc_artifact(role, normalized)
    return normalized


def load_supporting_context(state: dict[str, Any]) -> str:
    paths = [Path(path) for path in state.get("supporting_docs", [])]
    if not paths:
        return ""
    sections = [
        "Use the following supporting documents as private evaluation context.",
        "If a supporting document marks material as private or not publicly quotable, do not expose private locators, repository paths, or private URLs in the revised public document.",
        "Use private evidence to decide whether a claim is supportable, then phrase the public document without leaking private evidence locations.",
    ]
    for path in paths:
        sections.extend(
            [
                "",
                f"## Supporting Document: {path}",
                read_text(path),
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def load_current_doc_spec(state: dict[str, Any]) -> dict[str, Any]:
    raw_path = state.get("doc_spec_path")
    return load_doc_spec(Path(str(raw_path)) if raw_path else None)


def validate_editor_against_doc_spec(editor: dict[str, Any], doc_spec: dict[str, Any]) -> list[str]:
    revised = str(editor.get("revised_markdown") or "")
    assertions = [item for item in doc_spec.get("forbidden_public_assertions", []) if str(item).strip()]
    assertion_matches = [
        assertion
        for assertion in assertions
        if public_assertion_is_forbidden(str(assertion), revised, doc_spec)
    ]
    if assertion_matches:
        raise EngineError(
            f"editor public revised_markdown contains forbidden spec assertion(s): {', '.join(assertion_matches)}"
        )
    forbidden = [item for item in doc_spec.get("forbidden_public_patterns", []) if str(item).strip()]
    matches = [
        pattern
        for pattern in forbidden
        if public_pattern_is_forbidden(str(pattern), revised)
    ]
    if matches and doc_spec.get("strict_public_pattern_validation", False):
        raise EngineError(f"editor public revised_markdown contains forbidden spec pattern(s): {', '.join(matches)}")
    if matches:
        return [f"public revised_markdown contains advisory pattern(s): {', '.join(matches)}"]
    return []


def public_assertion_is_forbidden(assertion: str, text: str, doc_spec: dict[str, Any]) -> bool:
    cleaned = remove_rejected_claim_contexts(remove_allowed_disclaimers(text.lower(), doc_spec))
    return re.search(re.escape(assertion.lower().strip()), cleaned, re.IGNORECASE) is not None


def remove_rejected_claim_contexts(text: str) -> str:
    cleaned_lines: list[str] = []
    skip_next_quote = False
    for line in text.splitlines():
        stripped = line.strip()
        if "not the right claim" in stripped or "wrong claim" in stripped:
            skip_next_quote = True
            continue
        if skip_next_quote and (not stripped or stripped.startswith(">")):
            continue
        skip_next_quote = False
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def remove_allowed_disclaimers(text: str, doc_spec: dict[str, Any]) -> str:
    cleaned = text
    for raw_pattern in doc_spec.get("allowed_disclaimer_patterns", []):
        pattern = str(raw_pattern).strip().lower()
        if not pattern:
            continue
        cleaned = cleaned.replace(pattern, "")
    return cleaned


def public_pattern_is_forbidden(pattern: str, text: str) -> bool:
    lower_pattern = pattern.lower().strip()
    lower_text = text.lower()
    if not lower_pattern:
        return False
    unsafe_text = remove_negated_pattern_mentions(lower_text, lower_pattern)
    if lower_pattern == "fatwa":
        return "fatwa" in unsafe_text
    if lower_pattern not in unsafe_text:
        return False
    return re.search(re.escape(lower_pattern), unsafe_text, re.IGNORECASE) is not None


def remove_negated_pattern_mentions(text: str, pattern: str) -> str:
    escaped = re.escape(pattern)
    replacements = [
        rf"\bnot\s+(?:an?\s+)?{escaped}\b",
        rf"\bdoes\s+not\s+(?:assert|claim|state|mean|say|imply)\s+(?:that\s+[^.\n]{{0,120}})?{escaped}\b",
        rf"\bdo\s+not\s+(?:assert|claim|state|say|imply|describe)\s+(?:[^.\n]{{0,120}})?{escaped}\b",
        rf"\bwithout\s+(?:a\s+)?{escaped}\b",
    ]
    cleaned = text
    for expression in replacements:
        cleaned = re.sub(expression, "", cleaned, flags=re.IGNORECASE)
    return cleaned


def build_doc_context(
    state: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    supporting_context: str = "",
    doc_spec: dict[str, Any] | None = None,
) -> list[tuple[str, str]]:
    sections = []
    if doc_spec:
        sections.append(("Document Intent Spec", json.dumps(doc_spec, indent=2, sort_keys=True)))
    if supporting_context:
        sections.append(("Supporting Evidence Documents", supporting_context))
    sections.append(("Document State", json.dumps(state, indent=2, sort_keys=True)))
    for role in ROLE_SEQUENCE:
        if role in artifacts:
            sections.append((f"{role.title()} Artifact", json.dumps(artifacts[role], indent=2, sort_keys=True)))
    return sections


def log_doc_line(path: Path, message: str) -> None:
    line = message.rstrip()
    print(line, flush=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def log_doc_summary(
    cycle_log_path: Path,
    role: str,
    engine_name: str,
    artifact: dict[str, Any],
    elapsed: float,
) -> None:
    summary = str(
        artifact.get("summary")
        or artifact.get("document_summary")
        or artifact.get("verdict")
        or ""
    ).replace("\n", " ")
    if len(summary) > 220:
        summary = summary[:217] + "..."
    log_doc_line(cycle_log_path, f"Finished `{role}` with `{engine_name}` in {elapsed:.1f}s")
    log_doc_line(cycle_log_path, f"Summary: {summary or '(empty summary)'}")


def render_changelog(cycle_number: int, editor_artifact: dict[str, Any]) -> str:
    lines = [
        f"# Document Improvement Cycle {cycle_number} Changelog",
        "",
        "## Applied Proposal IDs",
    ]
    applied = editor_artifact.get("applied_proposal_ids", [])
    lines.extend([f"- `{item}`" for item in applied] or ["- None"])
    lines.extend(["", "## Changes"])
    lines.extend([f"- {item}" for item in editor_artifact.get("changelog", [])] or ["- None"])
    return "\n".join(lines) + "\n"


def render_internal_notes(raw_notes: str, validation_warnings: list[str]) -> str:
    notes = raw_notes.rstrip()
    if not validation_warnings:
        return notes + "\n"
    lines = [notes, "", "## Validation Warnings"]
    lines.extend([f"- {warning}" for warning in validation_warnings])
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
