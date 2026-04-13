from __future__ import annotations

from copy import deepcopy
from typing import Any

from .campaign import Campaign


def choose_next_objective(campaign: Campaign, state: dict[str, Any]) -> str:
    for claim_id in campaign.must_prove_claim_ids:
        claim_state = state["claim_status"][claim_id]
        if claim_state["status"] in {"untested", "contested", "rejected"}:
            return f"Evaluate claim `{claim_id}`: {claim_statement(campaign, claim_id)}"

    for criterion_id in sorted(campaign.kill_criteria_ids(), key=campaign.kill_priority):
        criterion_state = state["kill_criteria_status"][criterion_id]
        if criterion_state["status"] != "cleared":
            return f"Stress-test kill criterion `{criterion_id}`: {kill_statement(campaign, criterion_id)}"

    next_objective = state.get("next_objective")
    if next_objective:
        return str(next_objective)
    return "Synthesize whether the wedge is pilot-worthy and identify the strongest unresolved objection."


def apply_cycle_results(
    campaign: Campaign,
    state: dict[str, Any],
    cycle_number: int,
    judge_artifact: dict[str, Any],
) -> dict[str, Any]:
    updated = deepcopy(state)
    updated["cycle_count"] = cycle_number
    updated["next_objective"] = judge_artifact.get("next_recommended_objective")

    new_evidence = any(
        [
            judge_artifact.get("supports_claims"),
            judge_artifact.get("weakens_claims"),
            judge_artifact.get("triggered_kill_criteria"),
        ]
    )
    updated["no_evidence_streak"] = 0 if new_evidence else int(updated.get("no_evidence_streak", 0)) + 1

    for claim_id in judge_artifact.get("supports_claims", []):
        if claim_id not in updated["claim_status"]:
            continue
        claim_state = updated["claim_status"][claim_id]
        claim_state["supporting_cycles"] += 1
        claim_state["last_cycle"] = cycle_number
        claim_state["status"] = "supported"

    for claim_id in judge_artifact.get("weakens_claims", []):
        if claim_id not in updated["claim_status"]:
            continue
        claim_state = updated["claim_status"][claim_id]
        claim_state["weakening_cycles"] += 1
        claim_state["last_cycle"] = cycle_number
        claim_state["status"] = "contested" if claim_state["supporting_cycles"] else "rejected"

    for claim_id, explicit_status in judge_artifact.get("claim_statuses", {}).items():
        if claim_id in updated["claim_status"]:
            updated["claim_status"][claim_id]["status"] = explicit_status
            updated["claim_status"][claim_id]["last_cycle"] = cycle_number

    source_counts = judge_artifact.get("kill_criterion_source_counts", {})
    for criterion_id in judge_artifact.get("triggered_kill_criteria", []):
        if criterion_id not in updated["kill_criteria_status"]:
            continue
        criterion_state = updated["kill_criteria_status"][criterion_id]
        criterion_state["status"] = "triggered"
        criterion_state["triggered_cycles"] += 1
        criterion_state["last_cycle"] = cycle_number
        criterion_state["source_count"] = max(
            int(source_counts.get(criterion_id, 0)),
            int(criterion_state.get("source_count", 0)),
        )

    existing = set(updated.get("unresolved_contradictions", []))
    for item in judge_artifact.get("contradictions", []):
        contradiction_id = item if isinstance(item, str) else item.get("id")
        if contradiction_id:
            existing.add(contradiction_id)
    for contradiction_id in judge_artifact.get("resolved_contradictions", []):
        existing.discard(contradiction_id)
    updated["unresolved_contradictions"] = sorted(existing)

    updated["verdict"] = determine_verdict(campaign, updated, judge_artifact)
    return updated


def determine_verdict(
    campaign: Campaign,
    state: dict[str, Any],
    judge_artifact: dict[str, Any],
) -> str:
    rules = campaign.raw["verdict_rules"]
    confidence = float(judge_artifact.get("confidence", 0.0))
    if state["no_evidence_streak"] >= int(rules["stalled_after_consecutive_no_evidence_cycles"]):
        return "stalled"

    for criterion_id, criterion_state in state["kill_criteria_status"].items():
        if (
            criterion_state["status"] == "triggered"
            and int(criterion_state.get("source_count", 0)) >= 2
            and confidence >= float(rules["rejection_confidence_threshold"])
        ):
            return "rejected"

    if (
        judge_artifact.get("recommended_verdict") == "rejected"
        and state["unresolved_contradictions"]
        and confidence >= float(rules["rejection_confidence_threshold"])
    ):
        return "rejected"

    must_prove_supported = all(
        state["claim_status"][claim_id]["status"] == "supported"
        for claim_id in campaign.must_prove_claim_ids
    )
    no_triggered_kills = all(
        item["status"] != "triggered" for item in state["kill_criteria_status"].values()
    )
    pilot = judge_artifact.get("pilot_recommendation", {})
    pilot_complete = all(
        bool(pilot.get(field))
        for field in [
            "target_user",
            "pain_statement",
            "current_workaround",
            "why_existing_tools_fail",
        ]
    )
    if (
        must_prove_supported
        and no_triggered_kills
        and not state["unresolved_contradictions"]
        and confidence >= float(rules["plausible_confidence_threshold"])
        and (pilot_complete or not rules.get("plausible_requires_pilot_fields", True))
    ):
        return "plausible"

    if any(item["status"] == "supported" for item in state["claim_status"].values()):
        return "promising"
    return "active"


def claim_statement(campaign: Campaign, claim_id: str) -> str:
    for claim in campaign.raw["core_claims"]:
        if claim["id"] == claim_id:
            return claim["statement"]
    return claim_id


def kill_statement(campaign: Campaign, criterion_id: str) -> str:
    for criterion in campaign.raw["kill_criteria"]:
        if criterion["id"] == criterion_id:
            return criterion["statement"]
    return criterion_id

