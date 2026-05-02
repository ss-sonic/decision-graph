from __future__ import annotations

from typing import Any

from .engines.base import EngineError


DOC_ROLES = ("extractor", "researcher", "improver", "skeptic", "editor", "judge")


def string_array_schema() -> dict[str, Any]:
    return {"type": "array", "items": {"type": "string"}}


def source_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "title", "locator", "source_type", "summary"],
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "locator": {"type": "string"},
            "source_type": {"type": "string"},
            "summary": {"type": "string"},
        },
    }


def doc_artifact_schema(role: str) -> dict[str, Any]:
    schemas = {
        "extractor": extractor_schema(),
        "researcher": researcher_schema(),
        "improver": improver_schema(),
        "skeptic": skeptic_schema(),
        "editor": editor_schema(),
        "judge": judge_schema(),
    }
    try:
        return schemas[role]
    except KeyError as exc:
        raise ValueError(f"Unsupported doc role: {role}") from exc


def extractor_schema() -> dict[str, Any]:
    return strict_object(
        required=[
            "document_summary",
            "audience_assumptions",
            "claims",
            "top_evidence_gaps",
            "structure_problems",
            "summary",
        ],
        properties={
            "document_summary": {"type": "string"},
            "audience_assumptions": string_array_schema(),
            "claims": {
                "type": "array",
                "items": strict_object(
                    required=["id", "text", "type", "importance", "support_status", "issue"],
                    properties={
                        "id": {"type": "string"},
                        "text": {"type": "string"},
                        "type": {"type": "string"},
                        "importance": {"type": "string"},
                        "support_status": {"type": "string"},
                        "issue": {"type": "string"},
                    },
                ),
            },
            "top_evidence_gaps": {
                "type": "array",
                "items": strict_object(
                    required=["id", "claim_ids", "question", "importance", "research_hint"],
                    properties={
                        "id": {"type": "string"},
                        "claim_ids": string_array_schema(),
                        "question": {"type": "string"},
                        "importance": {"type": "string"},
                        "research_hint": {"type": "string"},
                    },
                ),
            },
            "structure_problems": string_array_schema(),
            "summary": {"type": "string"},
        },
    )


def researcher_schema() -> dict[str, Any]:
    return strict_object(
        required=["summary", "researched_gap_ids", "evidence_items", "unresolved_gaps"],
        properties={
            "summary": {"type": "string"},
            "researched_gap_ids": string_array_schema(),
            "evidence_items": {
                "type": "array",
                "items": strict_object(
                    required=[
                        "id",
                        "source",
                        "locator",
                        "source_type",
                        "claim_ids",
                        "supports_or_weakens",
                        "finding",
                        "confidence",
                    ],
                    properties={
                        "id": {"type": "string"},
                        "source": {"type": "string"},
                        "locator": {"type": "string"},
                        "source_type": {"type": "string"},
                        "claim_ids": string_array_schema(),
                        "supports_or_weakens": {"type": "string"},
                        "finding": {"type": "string"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                ),
            },
            "unresolved_gaps": string_array_schema(),
        },
    )


def improver_schema() -> dict[str, Any]:
    return strict_object(
        required=["summary", "proposals"],
        properties={
            "summary": {"type": "string"},
            "proposals": {
                "type": "array",
                "items": strict_object(
                    required=[
                        "id",
                        "edit_type",
                        "target_heading",
                        "original_excerpt",
                        "replacement",
                        "reason",
                        "evidence_ids",
                        "confidence",
                        "overclaiming_risk",
                    ],
                    properties={
                        "id": {"type": "string"},
                        "edit_type": {"type": "string"},
                        "target_heading": {"type": "string"},
                        "original_excerpt": {"type": "string"},
                        "replacement": {"type": "string"},
                        "reason": {"type": "string"},
                        "evidence_ids": string_array_schema(),
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "overclaiming_risk": {"type": "string"},
                    },
                ),
            },
        },
    )


def skeptic_schema() -> dict[str, Any]:
    return strict_object(
        required=["summary", "approved_proposal_ids", "rejections", "required_softening"],
        properties={
            "summary": {"type": "string"},
            "approved_proposal_ids": string_array_schema(),
            "rejections": {
                "type": "array",
                "items": strict_object(
                    required=["proposal_id", "reason"],
                    properties={
                        "proposal_id": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                ),
            },
            "required_softening": string_array_schema(),
        },
    )


def editor_schema() -> dict[str, Any]:
    return strict_object(
        required=[
            "summary",
            "revised_markdown",
            "internal_notes_markdown",
            "changelog",
            "applied_proposal_ids",
        ],
        properties={
            "summary": {"type": "string"},
            "revised_markdown": {"type": "string"},
            "internal_notes_markdown": {"type": "string"},
            "changelog": string_array_schema(),
            "applied_proposal_ids": string_array_schema(),
        },
    )


def judge_schema() -> dict[str, Any]:
    return strict_object(
        required=["summary", "verdict", "next_focus", "remaining_high_value_issues", "stop_reason"],
        properties={
            "summary": {"type": "string"},
            "verdict": {
                "type": "string",
                "enum": [
                    "improved",
                    "needs_more_research",
                    "blocked_on_primary_research",
                    "stable",
                    "overclaiming_risk",
                ],
            },
            "next_focus": {"type": ["string", "null"]},
            "remaining_high_value_issues": string_array_schema(),
            "stop_reason": {"type": ["string", "null"]},
        },
    )


def strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }


def validate_doc_artifact(role: str, payload: dict[str, Any]) -> None:
    if role not in DOC_ROLES:
        raise EngineError(f"Unsupported doc role: {role}")
    if not isinstance(payload, dict):
        raise EngineError(f"{role} artifact must be a JSON object")
    required = set(doc_artifact_schema(role)["required"])
    missing = sorted(required.difference(payload))
    if missing:
        raise EngineError(f"{role} artifact missing required keys: {', '.join(missing)}")

    if role == "researcher":
        _validate_researcher(payload)
    if role == "editor":
        _validate_editor_shape(payload)


def validate_editor_against_skeptic(editor: dict[str, Any], skeptic: dict[str, Any]) -> None:
    approved = set(skeptic.get("approved_proposal_ids", []))
    applied = set(editor.get("applied_proposal_ids", []))
    unexpected = sorted(applied - approved)
    missing = sorted(approved - applied)
    if unexpected:
        raise EngineError(f"editor applied unapproved proposal ids: {', '.join(unexpected)}")
    if missing:
        raise EngineError(f"editor did not apply approved proposal ids: {', '.join(missing)}")


def _validate_researcher(payload: dict[str, Any]) -> None:
    researched = payload.get("researched_gap_ids", [])
    evidence = payload.get("evidence_items", [])
    if researched and not evidence:
        raise EngineError("researcher researched gaps but returned no evidence_items")
    for item in evidence:
        if not isinstance(item, dict):
            raise EngineError("researcher evidence_items entries must be objects")
        if not item.get("locator") or not item.get("source"):
            raise EngineError("researcher evidence_items require source and locator")


def _validate_editor_shape(payload: dict[str, Any]) -> None:
    if not isinstance(payload.get("revised_markdown"), str) or not payload["revised_markdown"].strip():
        raise EngineError("editor revised_markdown must be non-empty")
    if not isinstance(payload.get("internal_notes_markdown"), str):
        raise EngineError("editor internal_notes_markdown must be a string")
    if not isinstance(payload.get("changelog"), list):
        raise EngineError("editor changelog must be a list")
    if not isinstance(payload.get("applied_proposal_ids"), list):
        raise EngineError("editor applied_proposal_ids must be a list")
