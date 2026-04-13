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
        "additionalProperties": True,
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
        ],
        "properties": {
            "objective": {"type": "string"},
            "summary": {"type": "string"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["title", "detail"],
                    "properties": {
                        "title": {"type": "string"},
                        "detail": {"type": "string"},
                        "claim_id": {"type": "string"},
                        "kill_criterion_id": {"type": "string"},
                        "strength": {"type": "string"},
                    },
                },
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
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
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object",
                            "required": ["id", "detail"],
                            "properties": {
                                "id": {"type": "string"},
                                "detail": {"type": "string"},
                            },
                        },
                    ]
                },
            },
            "open_questions": {"type": "array", "items": {"type": "string"}},
            "next_recommended_objective": {"type": ["string", "null"]},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "recommended_verdict": {
                "type": "string",
                "enum": ["active", "promising", "plausible", "rejected", "stalled"],
            },
            "claim_statuses": {
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
            "kill_criterion_source_counts": {
                "type": "object",
                "additionalProperties": {"type": "integer"},
            },
            "resolved_contradictions": {"type": "array", "items": {"type": "string"}},
            "pilot_recommendation": {
                "type": "object",
                "properties": {
                    "target_user": {"type": "string"},
                    "pain_statement": {"type": "string"},
                    "current_workaround": {"type": "string"},
                    "why_existing_tools_fail": {"type": "string"},
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

