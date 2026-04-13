from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..prompts import artifact_schema
from ..utils import command_exists, ensure_directory, read_json, write_json


class EngineError(RuntimeError):
    pass


@dataclass(slots=True)
class PreflightResult:
    engine: str
    available: bool
    auth_configured: bool
    search_available: bool
    search_mode: str
    details: list[str]


class EngineAdapter:
    engine_name = "base"
    command_name = ""
    auth_env_keys: tuple[str, ...] = ()

    def preflight(self) -> PreflightResult:
        available = command_exists(self.command_name)
        auth_configured = any(os.getenv(key) for key in self.auth_env_keys)
        return PreflightResult(
            engine=self.engine_name,
            available=available,
            auth_configured=auth_configured,
            search_available=False,
            search_mode="unsupported",
            details=[],
        )

    def invoke(
        self,
        role: str,
        prompt_text: str,
        output_dir: Path,
        search_required: bool,
    ) -> Path:
        raise NotImplementedError

    def normalize(self, raw_output_path: Path) -> dict[str, Any]:
        payload = json.loads(raw_output_path.read_text(encoding="utf-8"))
        validate_normalized_artifact(payload)
        return payload

    def _write_schema_file(self) -> Path:
        handle = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
        json.dump(artifact_schema(), handle)
        handle.flush()
        handle.close()
        return Path(handle.name)

    def _run(self, command: list[str], output_path: Path) -> None:
        ensure_directory(output_path.parent)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise EngineError(
                f"{self.engine_name} invocation failed with code {result.returncode}:\n{result.stderr.strip()}"
            )
        output_path.write_text(result.stdout, encoding="utf-8")


def validate_normalized_artifact(payload: dict[str, Any]) -> None:
    required = {
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
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise EngineError(f"Artifact missing required keys: {', '.join(missing)}")

    if not isinstance(payload["sources"], list):
        raise EngineError("Artifact sources must be a list")
    if not isinstance(payload["findings"], list):
        raise EngineError("Artifact findings must be a list")
    if not isinstance(payload["supports_claims"], list):
        raise EngineError("Artifact supports_claims must be a list")
    if not isinstance(payload["weakens_claims"], list):
        raise EngineError("Artifact weakens_claims must be a list")
    if not isinstance(payload["triggered_kill_criteria"], list):
        raise EngineError("Artifact triggered_kill_criteria must be a list")
    if not isinstance(payload["open_questions"], list):
        raise EngineError("Artifact open_questions must be a list")
    confidence = payload["confidence"]
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        raise EngineError("Artifact confidence must be a number between 0 and 1")

    has_external_claims = bool(
        payload["supports_claims"] or payload["weakens_claims"] or payload["triggered_kill_criteria"]
    )
    if has_external_claims and not payload["sources"]:
        raise EngineError("Artifacts with claim or kill-criterion updates must include at least one source")

