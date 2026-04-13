from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from .campaign import Campaign
from .utils import ensure_directory, read_json, write_json


def campaign_run_dir(root: Path, campaign: Campaign) -> Path:
    return ensure_directory(root / "runs" / campaign.slug)


def state_path(root: Path, campaign: Campaign) -> Path:
    return campaign_run_dir(root, campaign) / "state.json"


def initialize_state(campaign: Campaign) -> dict[str, Any]:
    claim_status = {
        claim["id"]: {
            "status": "untested",
            "supporting_cycles": 0,
            "weakening_cycles": 0,
            "last_cycle": None,
        }
        for claim in campaign.raw["core_claims"]
    }
    kill_status = {
        criterion["id"]: {
            "status": "inactive",
            "triggered_cycles": 0,
            "source_count": 0,
            "last_cycle": None,
        }
        for criterion in campaign.raw["kill_criteria"]
    }
    return {
        "campaign_slug": campaign.slug,
        "campaign_path": str(campaign.path),
        "verdict": "active",
        "cycle_count": 0,
        "no_evidence_streak": 0,
        "next_objective": None,
        "claim_status": claim_status,
        "kill_criteria_status": kill_status,
        "unresolved_contradictions": [],
        "latest_artifacts": {},
        "history": [],
    }


def load_or_initialize_state(root: Path, campaign: Campaign) -> dict[str, Any]:
    path = state_path(root, campaign)
    if path.exists():
        return read_json(path)
    state = initialize_state(campaign)
    save_state(root, campaign, state)
    return state


def save_state(root: Path, campaign: Campaign, state: dict[str, Any]) -> None:
    write_json(state_path(root, campaign), state)


def next_cycle_dir(root: Path, campaign: Campaign, state: dict[str, Any]) -> Path:
    cycle_number = int(state["cycle_count"]) + 1
    return ensure_directory(campaign_run_dir(root, campaign) / f"cycle-{cycle_number:04d}")


def append_history(state: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(state)
    updated["history"] = [*updated.get("history", []), entry]
    return updated

