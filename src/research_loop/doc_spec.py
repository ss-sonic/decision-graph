from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    yaml = None


DEFAULT_DOC_SPEC: dict[str, Any] = {
    "document_type": "evidence_backed_document",
    "author": "author",
    "audience": "general reader",
    "goal": "improve truth, reasoning, evidence, and clarity",
    "tone": "clear and defensible",
    "risk_posture": "truthful",
    "private_evidence_policy": "use_for_confidence_do_not_quote",
    "diligence_language": "inline_when_needed",
    "forbidden_public_patterns": [],
}


def load_doc_spec(path: Path | None) -> dict[str, Any]:
    if path is None:
        return dict(DEFAULT_DOC_SPEC)
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        raw = yaml.safe_load(text)
    elif path.suffix.lower() == ".json":
        raw = json.loads(text)
    else:
        raw = parse_simple_yaml(text)
    if not isinstance(raw, dict):
        raise ValueError(f"Document spec must contain a mapping: {path}")
    spec = dict(DEFAULT_DOC_SPEC)
    spec.update(raw)
    _validate_doc_spec(spec, path)
    return spec


def parse_simple_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list_key is None:
                raise ValueError("YAML list item without a preceding key")
            result.setdefault(current_list_key, []).append(stripped[2:].strip().strip("\"'"))
            continue
        if ":" not in stripped:
            raise ValueError(f"Unsupported docs spec line: {line}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            result[key] = value.strip("\"'")
            current_list_key = None
        else:
            result[key] = []
            current_list_key = key
    return result


def _validate_doc_spec(spec: dict[str, Any], path: Path) -> None:
    for key in ["document_type", "author", "audience", "goal", "tone", "risk_posture"]:
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            raise ValueError(f"Document spec {path} requires non-empty string key `{key}`")
    patterns = spec.get("forbidden_public_patterns", [])
    if not isinstance(patterns, list) or not all(isinstance(item, str) for item in patterns):
        raise ValueError("Document spec `forbidden_public_patterns` must be a list of strings")

