from __future__ import annotations

import json
from pathlib import Path
from string import Template
from typing import Any

from .campaign import Campaign
from .utils import read_text


ROLE_TO_TEMPLATE = {
    "researcher": "researcher.md",
    "skeptic": "skeptic.md",
    "rebuttal": "rebuttal.md",
    "judge": "judge.md",
}


def artifact_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "objective",
            "summary",
            "findings",
            "sources",
            "supports_claims",
            "weakens_claims",
            "triggered_kill_criteria",
            "contradictions",
            "open_questions",
            "next_recommended_objective",
            "confidence",
            "proposed_mutations",
            "recommended_verdict",
            "claim_statuses",
            "kill_criterion_source_counts",
            "resolved_contradictions",
            "pilot_recommendation",
        ],
        "properties": {
            "objective": {"type": "string"},
            "summary": {"type": "string"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["title", "detail", "claim_id", "kill_criterion_id", "strength"],
                    "properties": {
                        "title": {"type": "string"},
                        "detail": {"type": "string"},
                        "claim_id": {"type": ["string", "null"]},
                        "kill_criterion_id": {"type": ["string", "null"]},
                        "strength": {"type": ["string", "null"]},
                    },
                },
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["title", "locator", "source_type"],
                    "properties": {
                        "title": {"type": "string"},
                        "locator": {"type": "string"},
                        "source_type": {"type": "string"},
                    },
                },
            },
            "supports_claims": {"type": "array", "items": {"type": "string"}},
            "weakens_claims": {"type": "array", "items": {"type": "string"}},
            "triggered_kill_criteria": {"type": "array", "items": {"type": "string"}},
            "contradictions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "detail"],
                    "properties": {
                        "id": {"type": "string"},
                        "detail": {"type": "string"},
                    },
                },
            },
            "open_questions": {"type": "array", "items": {"type": "string"}},
            "next_recommended_objective": {"type": ["string", "null"]},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "proposed_mutations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["target_type", "target_file", "operation", "content", "reason"],
                    "properties": {
                        "target_type": {"type": "string", "enum": ["report"]},
                        "target_file": {"type": "string"},
                        "operation": {"type": "string", "enum": ["replace_file"]},
                        "content": {"type": "string"},
                        "reason": {"type": ["string", "null"]},
                    },
                },
            },
            "recommended_verdict": {
                "type": "string",
                "enum": ["active", "promising", "plausible", "rejected", "stalled"],
            },
            "claim_statuses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["claim_id", "status"],
                    "properties": {
                        "claim_id": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
            "kill_criterion_source_counts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["kill_criterion_id", "source_count"],
                    "properties": {
                        "kill_criterion_id": {"type": "string"},
                        "source_count": {"type": "integer"},
                    },
                },
            },
            "resolved_contradictions": {"type": "array", "items": {"type": "string"}},
            "pilot_recommendation": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "target_user",
                    "pain_statement",
                    "current_workaround",
                    "why_existing_tools_fail",
                ],
                "properties": {
                    "target_user": {"type": ["string", "null"]},
                    "pain_statement": {"type": ["string", "null"]},
                    "current_workaround": {"type": ["string", "null"]},
                    "why_existing_tools_fail": {"type": ["string", "null"]},
                },
            },
        },
    }


def render_prompt(
    root: Path,
    role: str,
    campaign: Campaign,
    objective: str,
    context_sections: list[tuple[str, str]],
) -> str:
    template_path = root / "prompts" / ROLE_TO_TEMPLATE[role]
    template = Template(read_text(template_path))
    rendered_context = "\n\n".join(
        f"## {title}\n{content}" for title, content in context_sections if content.strip()
    )
    return template.substitute(
        objective=objective,
        campaign_yaml=campaign.to_yaml_text(),
        context_sections=rendered_context or "No extra context provided.",
        artifact_contract=json.dumps(artifact_schema(), indent=2),
    )
