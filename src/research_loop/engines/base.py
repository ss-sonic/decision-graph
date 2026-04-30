from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
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
        normalized = unwrap_artifact_payload(payload)
        normalized = canonicalize_artifact(normalized)
        validate_normalized_artifact(normalized)
        return normalized

    def output_schema(self, role: str) -> dict[str, Any]:
        return artifact_schema()

    def _write_schema_file(self, role: str = "") -> Path:
        handle = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
        json.dump(self.output_schema(role), handle)
        handle.flush()
        handle.close()
        return Path(handle.name)

    def _run(self, command: list[str], output_path: Path) -> None:
        ensure_directory(output_path.parent)
        stderr_path = output_path.parent / "stderr.txt"
        heartbeat_seconds = int(os.getenv("RESEARCH_LOOP_HEARTBEAT_SECS", "5"))
        timeout_seconds = engine_timeout_seconds()
        label = output_path.parent.name
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
                print(f"[{self.engine_name}:{label}] still running... {elapsed}s elapsed", flush=True)
                if timeout_seconds is not None and elapsed >= timeout_seconds:
                    process.kill()
                    stdout, stderr = process.communicate()
                    stderr_path.write_text(stderr, encoding="utf-8")
                    raise EngineError(
                        f"{self.engine_name} invocation timed out after {timeout_seconds}s for step `{label}`"
                    )

        stderr_path.write_text(stderr, encoding="utf-8")
        if stdout:
            output_path.write_text(stdout, encoding="utf-8")
        if process.returncode != 0:
            details = stderr.strip() or stdout.strip() or "(no stdout/stderr from engine)"
            raise EngineError(
                f"{self.engine_name} invocation failed with code {process.returncode}:\n{details}"
            )


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


def engine_timeout_seconds() -> int | None:
    raw = os.getenv("RESEARCH_LOOP_ENGINE_TIMEOUT_SECS", "").strip().lower()
    if raw in {"", "0", "none", "no", "off", "false"}:
        return None
    return int(raw)


def unwrap_artifact_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        structured = payload.get("structured_output")
        if isinstance(structured, dict):
            return structured

        result = payload.get("result")
        if isinstance(result, str):
            stripped = unwrap_json_text(result)
            if stripped is not None:
                parsed = json.loads(stripped)
                if isinstance(parsed, dict):
                    return parsed

        return payload

    if isinstance(payload, str):
        stripped = unwrap_json_text(payload)
        if stripped is not None:
            parsed = json.loads(stripped)
            if isinstance(parsed, dict):
                return parsed

    raise EngineError("Artifact output is not a JSON object and could not be unwrapped")


def unwrap_json_text(text: str) -> str | None:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped
    if stripped.startswith("```json") and stripped.endswith("```"):
        inner = stripped[len("```json") : -len("```")].strip()
        if inner.startswith("{") and inner.endswith("}"):
            return inner
    if stripped.startswith("```") and stripped.endswith("```"):
        inner = stripped[len("```") : -len("```")].strip()
        if inner.startswith("{") and inner.endswith("}"):
            return inner
    return None


def canonicalize_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    contradictions = payload.get("contradictions", [])
    if isinstance(contradictions, list):
        canonical = []
        for item in contradictions:
            if isinstance(item, dict):
                identifier = str(item.get("id") or item.get("detail") or "contradiction").strip()
                detail = str(item.get("detail") or item.get("id") or "").strip()
                canonical.append({"id": identifier, "detail": detail})
            elif isinstance(item, str):
                text = item.strip()
                if text:
                    canonical.append({"id": text[:80], "detail": text})
        payload["contradictions"] = canonical

    claim_statuses = payload.get("claim_statuses", [])
    if isinstance(claim_statuses, dict):
        payload["claim_statuses"] = [
            {"claim_id": str(claim_id), "status": str(status)}
            for claim_id, status in claim_statuses.items()
            if claim_id and status is not None
        ]

    kill_counts = payload.get("kill_criterion_source_counts", [])
    if isinstance(kill_counts, dict):
        payload["kill_criterion_source_counts"] = [
            {"kill_criterion_id": str(criterion_id), "source_count": int(source_count)}
            for criterion_id, source_count in kill_counts.items()
            if criterion_id and source_count is not None
        ]
    return payload
