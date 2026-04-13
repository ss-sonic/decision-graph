from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - exercised in CLI/tests without PyYAML
    yaml = None


REQUIRED_KEYS = {
    "idea",
    "wedge",
    "idea_source",
    "core_claims",
    "kill_criteria",
    "evidence_policy",
    "required_artifacts",
    "verdict_rules",
    "engine_roles",
    "notes_sources",
}


@dataclass(slots=True)
class Campaign:
    raw: dict[str, Any]
    path: Path

    @property
    def slug(self) -> str:
        wedge = self.raw["wedge"]
        return wedge["slug"]

    @property
    def name(self) -> str:
        return self.raw["idea"]["name"]

    @property
    def idea_source(self) -> Path:
        return self.path.parent.parent / self.raw["idea_source"]

    @property
    def notes_sources(self) -> list[Path]:
        return [self.path.parent.parent / item for item in self.raw.get("notes_sources", [])]

    @property
    def must_prove_claim_ids(self) -> list[str]:
        items = [claim["id"] for claim in self.raw["core_claims"] if claim.get("must_prove", False)]
        return sorted(items, key=lambda claim_id: self.claim_priority(claim_id))

    def claim_priority(self, claim_id: str) -> int:
        for claim in self.raw["core_claims"]:
            if claim["id"] == claim_id:
                return int(claim.get("priority", 999))
        return 999

    def kill_priority(self, criterion_id: str) -> int:
        for criterion in self.raw["kill_criteria"]:
            if criterion["id"] == criterion_id:
                return int(criterion.get("priority", 999))
        return 999

    def to_yaml_text(self) -> str:
        if yaml is not None:
            return yaml.safe_dump(self.raw, sort_keys=False)
        return json.dumps(self.raw, indent=2)

    def claim_ids(self) -> list[str]:
        return [claim["id"] for claim in self.raw["core_claims"]]

    def kill_criteria_ids(self) -> list[str]:
        return [criterion["id"] for criterion in self.raw["kill_criteria"]]


def load_campaign(path: Path) -> Campaign:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        raw = yaml.safe_load(text)
    else:
        raw = json.loads(text)
    if not isinstance(raw, dict):
        raise ValueError(f"Campaign file must contain a mapping: {path}")

    missing = sorted(REQUIRED_KEYS.difference(raw))
    if missing:
        raise ValueError(f"Campaign file missing keys: {', '.join(missing)}")

    _validate_named_section(raw, "idea", {"name", "description"})
    _validate_named_section(raw, "wedge", {"slug", "name", "description"})
    _validate_engine_roles(raw)
    _validate_items(raw, "core_claims", {"id", "statement"})
    _validate_items(raw, "kill_criteria", {"id", "statement"})

    return Campaign(raw=raw, path=path.resolve())


def _validate_named_section(raw: dict[str, Any], key: str, required: set[str]) -> None:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be a mapping")
    missing = sorted(required.difference(value))
    if missing:
        raise ValueError(f"{key} missing keys: {', '.join(missing)}")


def _validate_items(raw: dict[str, Any], key: str, required: set[str]) -> None:
    value = raw.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{key} entries must be mappings")
        missing = sorted(required.difference(item))
        if missing:
            raise ValueError(f"{key} entry missing keys: {', '.join(missing)}")


def _validate_engine_roles(raw: dict[str, Any]) -> None:
    roles = raw.get("engine_roles")
    required = {"researcher", "skeptic", "rebuttal", "judge"}
    if not isinstance(roles, dict):
        raise ValueError("engine_roles must be a mapping")
    missing = sorted(required.difference(roles))
    if missing:
        raise ValueError(f"engine_roles missing keys: {', '.join(missing)}")
    allowed = {"claude", "codex"}
    invalid = sorted({str(value) for value in roles.values()} - allowed)
    if invalid:
        raise ValueError(f"engine_roles contains unsupported engines: {', '.join(invalid)}")
