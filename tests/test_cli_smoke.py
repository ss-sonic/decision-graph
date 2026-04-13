from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "research-loop"


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def base_artifact(summary: str, **extra: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "objective": "test objective",
        "summary": summary,
        "findings": [{"title": summary, "detail": summary}],
        "sources": [{"title": "source", "locator": "https://example.com", "source_type": "web"}],
        "supports_claims": [],
        "weakens_claims": [],
        "triggered_kill_criteria": [],
        "contradictions": [],
        "open_questions": [],
        "next_recommended_objective": None,
        "confidence": 0.6,
    }
    payload.update(extra)
    return payload


class CliSmokeTests(unittest.TestCase):
    def test_init_preflight_run_status_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            copy_file(ROOT / "decision-graph.md", root / "decision-graph.md")
            copy_file(ROOT / "campaigns" / "manager-people.yaml", root / "campaigns" / "manager-people.yaml")
            for prompt_name in ["researcher.md", "skeptic.md", "rebuttal.md", "judge.md"]:
                copy_file(ROOT / "prompts" / prompt_name, root / "prompts" / prompt_name)
            copy_file(ROOT / "pyproject.toml", root / "pyproject.toml")

            scenario = {
                "claude": {
                    "researcher": base_artifact(
                        "Research step",
                        supports_claims=["pain_is_frequent", "continuity_beats_chat"],
                    ),
                    "rebuttal": base_artifact(
                        "Rebuttal step",
                        supports_claims=["pain_is_frequent", "continuity_beats_chat", "behavior_change_is_plausible", "pilot_can_be_narrow"],
                    ),
                },
                "codex": {
                    "skeptic": base_artifact(
                        "Skeptic step",
                        weakens_claims=["investor_story_has_substance"],
                        contradictions=[{"id": "comp-density", "detail": "Need a stronger comp map"}],
                    ),
                    "judge": base_artifact(
                        "Judge step",
                        supports_claims=[
                            "pain_is_frequent",
                            "continuity_beats_chat",
                            "behavior_change_is_plausible",
                            "pilot_can_be_narrow",
                        ],
                        contradictions=[],
                        resolved_contradictions=["comp-density"],
                        recommended_verdict="plausible",
                        confidence=0.82,
                        pilot_recommendation={
                            "target_user": "Frontline managers",
                            "pain_statement": "People decisions are emotionally loaded and recurring.",
                            "current_workaround": "ChatGPT plus docs plus ad hoc notes.",
                            "why_existing_tools_fail": "They do not preserve structured reasoning over time.",
                        },
                    ),
                },
            }
            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run([sys.executable, str(SCRIPT), "init"], cwd=root, env=env, check=True)
            subprocess.run([sys.executable, str(SCRIPT), "preflight"], cwd=root, env=env, check=True)
            subprocess.run([sys.executable, str(SCRIPT), "run", "--cycles", "1"], cwd=root, env=env, check=True)

            status = subprocess.run(
                [sys.executable, str(SCRIPT), "status"],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Verdict: plausible", status.stdout)

            report = subprocess.run(
                [sys.executable, str(SCRIPT), "report"],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("current-brief.md", report.stdout)
            self.assertTrue((root / "reports" / "manager-people" / "pilot.md").exists())


if __name__ == "__main__":
    unittest.main()
