from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import ensure_directory, read_json, slugify, write_json


TERMINAL_DOC_VERDICTS = {"blocked_on_primary_research", "stable", "overclaiming_risk"}


def doc_slug(root: Path, doc_path: Path) -> str:
    resolved = doc_path.resolve()
    try:
        relative = resolved.relative_to(root.resolve())
    except ValueError:
        relative = Path(resolved.name)
    return slugify(str(relative.with_suffix("")))


def doc_run_dir(root: Path, doc_path: Path) -> Path:
    return ensure_directory(root / "doc-runs" / doc_slug(root, doc_path))


def doc_state_path(root: Path, doc_path: Path) -> Path:
    return doc_run_dir(root, doc_path) / "state.json"


def initialize_doc_state(root: Path, doc_path: Path) -> dict[str, Any]:
    return {
        "doc_slug": doc_slug(root, doc_path),
        "source_doc": str(doc_path.resolve()),
        "cycle_count": 0,
        "verdict": "not_started",
        "next_focus": "Extract and strengthen the highest-impact unsupported claims in the document.",
        "latest_revision": None,
        "latest_internal_notes": None,
        "latest_cycle_dir": None,
        "latest_artifacts": {},
        "supporting_docs": [],
        "doc_spec_path": None,
        "history": [],
    }


def load_or_initialize_doc_state(root: Path, doc_path: Path) -> dict[str, Any]:
    path = doc_state_path(root, doc_path)
    if path.exists():
        state = read_json(path)
        state.setdefault("latest_artifacts", {})
        state.setdefault("history", [])
        state.setdefault("supporting_docs", [])
        state.setdefault("doc_spec_path", None)
        state.setdefault("latest_internal_notes", None)
        return state
    state = initialize_doc_state(root, doc_path)
    save_doc_state(root, doc_path, state)
    return state


def save_doc_state(root: Path, doc_path: Path, state: dict[str, Any]) -> None:
    write_json(doc_state_path(root, doc_path), state)


def next_doc_cycle_dir(root: Path, doc_path: Path, state: dict[str, Any]) -> Path:
    preferred = int(state.get("cycle_count", 0)) + 1
    existing_numbers: list[int] = []
    for path in doc_run_dir(root, doc_path).glob("cycle-*"):
        if not path.is_dir():
            continue
        try:
            existing_numbers.append(int(path.name.split("-")[-1]))
        except ValueError:
            continue
    cycle_number = max(preferred, max(existing_numbers, default=0) + 1)
    return ensure_directory(doc_run_dir(root, doc_path) / f"cycle-{cycle_number:04d}")


def latest_doc_input_path(doc_path: Path, state: dict[str, Any]) -> Path:
    latest = state.get("latest_revision")
    if latest:
        return Path(str(latest))
    return doc_path.resolve()
