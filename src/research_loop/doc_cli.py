from __future__ import annotations

import argparse
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

    researcher = registry[ROLE_ENGINES["researcher"]]
    if not researcher.preflight().search_available:
        raise EngineError("Document researcher search is required but not available.")

    for _ in range(args.cycles):
        state = run_doc_cycle(root, doc_path, state, registry)
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


def run_doc_cycle(
    root: Path,
    doc_path: Path,
    state: dict[str, Any],
    registry: dict[str, Any],
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

    for role in ROLE_SEQUENCE:
        engine_name = ROLE_ENGINES[role]
        adapter = registry[engine_name]
        role_dir = ensure_directory(cycle_dir / role)
        prompt_text = render_doc_prompt(
            root=root,
            role=role,
            doc_path=doc_path,
            input_markdown=input_markdown,
            focus=focus,
            context_sections=build_doc_context(state, artifacts, supporting_context, doc_spec),
        )
        prompt_path = role_dir / "prompt.txt"
        prompt_path.write_text(prompt_text, encoding="utf-8")
        log_doc_line(cycle_log_path, f"Starting `{role}` with `{engine_name}`. Prompt: {prompt_path.relative_to(root)}")
        started = time.monotonic()
        raw_path = adapter.invoke(
            role=role,
            prompt_text=prompt_text,
            output_dir=role_dir,
            search_required=(role == "researcher"),
        )
        artifact = normalize_doc_output(role, raw_path)
        if role == "editor":
            validate_editor_against_skeptic(artifact, artifacts["skeptic"])
        normalized_path = role_dir / "normalized.json"
        write_json(normalized_path, artifact)
        artifacts[role] = artifact
        latest_artifacts[role] = str(normalized_path)
        log_doc_summary(cycle_log_path, role, engine_name, artifact, time.monotonic() - started)

    editor = artifacts["editor"]
    judge = artifacts["judge"]
    revised_path = cycle_dir / "revised.md"
    internal_notes_path = cycle_dir / "internal-notes.md"
    changelog_path = cycle_dir / "change-log.md"
    validate_editor_against_doc_spec(editor, doc_spec)
    revised_path.write_text(editor["revised_markdown"].rstrip() + "\n", encoding="utf-8")
    internal_notes_path.write_text(editor["internal_notes_markdown"].rstrip() + "\n", encoding="utf-8")
    changelog_path.write_text(render_changelog(cycle_number, editor), encoding="utf-8")

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


def validate_editor_against_doc_spec(editor: dict[str, Any], doc_spec: dict[str, Any]) -> None:
    revised = str(editor.get("revised_markdown") or "")
    forbidden = [item for item in doc_spec.get("forbidden_public_patterns", []) if str(item).strip()]
    matches = [pattern for pattern in forbidden if re.search(re.escape(str(pattern)), revised, re.IGNORECASE)]
    if matches:
        raise EngineError(f"editor public revised_markdown contains forbidden spec pattern(s): {', '.join(matches)}")


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


if __name__ == "__main__":
    raise SystemExit(main())
