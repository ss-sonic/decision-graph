from __future__ import annotations

import os
import subprocess
import tempfile
import time
from pathlib import Path

from .base import EngineAdapter, EngineError, PreflightResult, engine_timeout_seconds


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

        schema_path = self._write_schema_file(role)
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
        stderr_path = output_dir / "stderr.txt"
        heartbeat_seconds = int(os.getenv("RESEARCH_LOOP_HEARTBEAT_SECS", "5"))
        timeout_seconds = engine_timeout_seconds()
        start = time.monotonic()
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout = ""
        stderr = ""
        while True:
            try:
                stdout, stderr = process.communicate(timeout=heartbeat_seconds)
                break
            except subprocess.TimeoutExpired:
                elapsed = int(time.monotonic() - start)
                print(f"[{self.engine_name}:{role}] still running... {elapsed}s elapsed", flush=True)
                if timeout_seconds is not None and elapsed >= timeout_seconds:
                    process.kill()
                    stdout, stderr = process.communicate()
                    stderr_path.write_text(stderr, encoding="utf-8")
                    try:
                        schema_path.unlink(missing_ok=True)
                    except OSError:
                        pass
                    raise EngineError(
                        f"{self.engine_name} invocation timed out after {timeout_seconds}s for step `{role}`"
                    )
        stderr_path.write_text(stderr, encoding="utf-8")
        try:
            schema_path.unlink(missing_ok=True)
        except OSError:
            pass
        if process.returncode != 0:
            raise EngineError(
                f"codex invocation failed with code {process.returncode}:\n{stderr.strip()}"
            )
        if not output_path.exists():
            raise EngineError("codex finished without writing the final message output file")
        return output_path
