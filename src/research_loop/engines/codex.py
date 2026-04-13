from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from .base import EngineAdapter, EngineError, PreflightResult


class CodexAdapter(EngineAdapter):
    engine_name = "codex"
    command_name = "codex"
    auth_env_keys = ("OPENAI_API_KEY",)

    def preflight(self) -> PreflightResult:
        base = super().preflight()
        mode = os.getenv("RESEARCH_LOOP_CODEX_SEARCH_MODE", "off").strip().lower()
        details = [
            "Codex search is optional in this loop and not required for skeptic/judge roles."
        ]
        return PreflightResult(
            engine=base.engine,
            available=base.available,
            auth_configured=base.auth_configured or (Path.home() / ".codex").exists(),
            search_available=mode == "on",
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
        if search_required and not self.preflight().search_available:
            raise EngineError("Codex search was requested but is not enabled.")

        schema_path = self._write_schema_file()
        output_path = output_dir / "raw.json"
        command = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--dangerously-bypass-approvals-and-sandbox",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
            prompt_text,
        ]
        if search_required:
            command.insert(2, "--search")
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        try:
            schema_path.unlink(missing_ok=True)
        except OSError:
            pass
        if result.returncode != 0:
            raise EngineError(
                f"codex invocation failed with code {result.returncode}:\n{result.stderr.strip()}"
            )
        if not output_path.exists():
            raise EngineError("codex finished without writing the final message output file")
        return output_path

