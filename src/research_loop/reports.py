from __future__ import annotations

from pathlib import Path
from typing import Any

from .campaign import Campaign
from .utils import ensure_directory

ALLOWED_REPORT_FILES = {
    "current-brief.md",
    "objections.md",
    "pilot.md",
    "investor.md",
}


def write_reports(root: Path, campaign: Campaign, state: dict[str, Any], latest_judge: dict[str, Any]) -> list[Path]:
    report_dir = ensure_directory(root / "reports" / campaign.slug)
    files = [
        _write_current_brief(report_dir / "current-brief.md", campaign, state, latest_judge),
        _write_objections(report_dir / "objections.md", campaign, state, latest_judge),
        _write_pilot(report_dir / "pilot.md", campaign, state, latest_judge),
        _write_investor(report_dir / "investor.md", campaign, state, latest_judge),
    ]
    apply_merged_report_mutations(report_dir, state)
    return files


def apply_merged_report_mutations(report_dir: Path, state: dict[str, Any]) -> None:
    merged = state.get("merged_mutations", {})
    if not isinstance(merged, dict):
        return
    for target_file, mutation in merged.items():
        if target_file not in ALLOWED_REPORT_FILES:
            continue
        if not isinstance(mutation, dict):
            continue
        content = mutation.get("content")
        if not isinstance(content, str) or not content.strip():
            continue
        (report_dir / target_file).write_text(content, encoding="utf-8")


def _write_current_brief(path: Path, campaign: Campaign, state: dict[str, Any], artifact: dict[str, Any]) -> Path:
    supported = [claim_id for claim_id, item in state["claim_status"].items() if item["status"] == "supported"]
    rejected = [claim_id for claim_id, item in state["claim_status"].items() if item["status"] == "rejected"]
    supported_lines = [f"- `{claim_id}`" for claim_id in supported] or ["- None yet"]
    rejected_lines = [f"- `{claim_id}`" for claim_id in rejected] or ["- None yet"]
    path.write_text(
        "\n".join(
            [
                f"# {campaign.name} — Current Brief",
                "",
                f"- Verdict: `{state['verdict']}`",
                f"- Cycles run: `{state['cycle_count']}`",
                f"- Current objective: {artifact.get('objective', 'n/a')}",
                "",
                "## Summary",
                artifact.get("summary", "No summary yet."),
                "",
                "## Supported Claims",
                *supported_lines,
                "",
                "## Rejected Or Contested Claims",
                *rejected_lines,
                "",
                "## Next Objective",
                artifact.get("next_recommended_objective") or "No next objective yet.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_objections(path: Path, campaign: Campaign, state: dict[str, Any], artifact: dict[str, Any]) -> Path:
    triggered = [
        criterion_id
        for criterion_id, item in state["kill_criteria_status"].items()
        if item["status"] == "triggered"
    ]
    triggered_lines = [f"- `{criterion_id}`" for criterion_id in triggered] or ["- None currently triggered"]
    contradiction_lines = [f"- `{item}`" for item in state["unresolved_contradictions"]] or ["- None"]
    question_lines = [f"- {item}" for item in artifact.get("open_questions", [])] or ["- None"]
    path.write_text(
        "\n".join(
            [
                f"# {campaign.name} — Objections Memo",
                "",
                "## Triggered Kill Criteria",
                *triggered_lines,
                "",
                "## Unresolved Contradictions",
                *contradiction_lines,
                "",
                "## Open Questions",
                *question_lines,
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_pilot(path: Path, campaign: Campaign, state: dict[str, Any], artifact: dict[str, Any]) -> Path:
    pilot = artifact.get("pilot_recommendation", {})
    path.write_text(
        "\n".join(
            [
                f"# {campaign.name} — Pilot Memo",
                "",
                f"- Verdict gate: `{state['verdict']}`",
                "",
                "## Target User",
                pilot.get("target_user", "Not yet specified."),
                "",
                "## Pain Statement",
                pilot.get("pain_statement", "Not yet specified."),
                "",
                "## Current Workaround",
                pilot.get("current_workaround", "Not yet specified."),
                "",
                "## Why Existing Tools Fail",
                pilot.get("why_existing_tools_fail", "Not yet specified."),
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_investor(path: Path, campaign: Campaign, state: dict[str, Any], artifact: dict[str, Any]) -> Path:
    supported = [claim_id for claim_id, item in state["claim_status"].items() if item["status"] == "supported"]
    supported_lines = [f"- `{claim_id}`" for claim_id in supported] or ["- None yet"]
    risk_lines = [f"- `{item}`" for item in state["unresolved_contradictions"]] or ["- No major contradictions recorded yet"]
    path.write_text(
        "\n".join(
            [
                f"# {campaign.name} — Investor Memo",
                "",
                f"- Current verdict: `{state['verdict']}`",
                "",
                "## Why This May Matter",
                artifact.get("summary", "Not enough evidence yet."),
                "",
                "## Currently Supported Claims",
                *supported_lines,
                "",
                "## Main Risks",
                *risk_lines,
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path
