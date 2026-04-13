from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .base import EngineAdapter, EngineError, PreflightResult, validate_normalized_artifact
from .claude import ClaudeAdapter
from .codex import CodexAdapter


class MockAdapter(EngineAdapter):
    def __init__(self, engine_name: str, scenario: dict[str, Any]) -> None:
        self.engine_name = engine_name
        self.command_name = engine_name
        self.auth_env_keys = ()
        self._scenario = scenario

    def preflight(self) -> PreflightResult:
        return PreflightResult(
            engine=self.engine_name,
            available=True,
            auth_configured=True,
            search_available=True,
            search_mode="mock",
            details=["Using mock engine responses."],
        )

    def invoke(
        self,
        role: str,
        prompt_text: str,
        output_dir: Path,
        search_required: bool,
    ) -> Path:
        output_path = output_dir / "raw.json"
        payload = self._scenario[self.engine_name][role]
        output_path.write_text(json.dumps(payload), encoding="utf-8")
        return output_path


def build_registry() -> dict[str, EngineAdapter]:
    if os.getenv("RESEARCH_LOOP_MOCK_ENGINES") == "1":
        scenario_path = os.getenv("RESEARCH_LOOP_MOCK_FILE")
        if not scenario_path:
            raise EngineError("RESEARCH_LOOP_MOCK_FILE is required when RESEARCH_LOOP_MOCK_ENGINES=1")
        scenario = json.loads(Path(scenario_path).read_text(encoding="utf-8"))
        return {
            "claude": MockAdapter("claude", scenario),
            "codex": MockAdapter("codex", scenario),
        }
    return {
        "claude": ClaudeAdapter(),
        "codex": CodexAdapter(),
    }

