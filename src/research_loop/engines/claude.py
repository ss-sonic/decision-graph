from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from .base import EngineAdapter, EngineError, PreflightResult


class ClaudeAdapter(EngineAdapter):
    engine_name = "claude"
    command_name = "claude"
    auth_env_keys = ("ANTHROPIC_API_KEY",)

    def preflight(self) -> PreflightResult:
        base = super().preflight()
        mode = os.getenv("RESEARCH_LOOP_CLAUDE_SEARCH_MODE", "assume").strip().lower()
        search_available = mode != "off"
        details = []
        if mode == "assume":
            details.append("Search capability is assumed; set RESEARCH_LOOP_CLAUDE_SEARCH_MODE=on|off to lock it.")
        elif mode == "on":
            details.append("Search capability marked as available by environment.")
        else:
            details.append("Search capability disabled by environment.")
        return PreflightResult(
            engine=base.engine,
            available=base.available,
            auth_configured=base.auth_configured,
            search_available=search_available,
            search_mode=mode,
            details=details,
        )

    def invoke(
        self,
        role: str,
        prompt_text: str,
        output_dir: Path,
        search_required: bool,
    ) -> Path:
        preflight = self.preflight()
        if search_required and not preflight.search_available:
            raise EngineError("Claude search is required for the researcher role but is disabled.")

        schema_json = json.dumps(self._schema_payload(), separators=(",", ":"))
        output_path = output_dir / "raw.json"
        command = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--json-schema",
            schema_json,
            "--dangerously-skip-permissions",
            prompt_text,
        ]
        self._run(command, output_path)
        return output_path

    def _schema_payload(self) -> dict:
        from ..prompts import artifact_schema

        return artifact_schema()

