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
        "findings": [
            {
                "title": summary,
                "detail": summary,
                "claim_id": None,
                "kill_criterion_id": None,
                "strength": None,
            }
        ],
        "sources": [{"title": "source", "locator": "https://example.com", "source_type": "web"}],
        "supports_claims": [],
        "weakens_claims": [],
        "triggered_kill_criteria": [],
        "contradictions": [],
        "open_questions": [],
        "next_recommended_objective": None,
        "confidence": 0.6,
        "proposed_mutations": [],
        "recommended_verdict": "active",
        "claim_statuses": {},
        "kill_criterion_source_counts": {},
        "resolved_contradictions": [],
        "pilot_recommendation": {
            "target_user": "Not yet specified.",
            "pain_statement": "Not yet specified.",
            "current_workaround": "Not yet specified.",
            "why_existing_tools_fail": "Not yet specified.",
        },
    }
    payload.update(extra)
    return payload


class CliSmokeTests(unittest.TestCase):
    def test_planned_research_run_creates_worker_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            copy_file(ROOT / "decision-graph.md", root / "decision-graph.md")
            copy_file(ROOT / "campaigns" / "client-discovery.yaml", root / "campaigns" / "client-discovery.yaml")
            for prompt_name in ["researcher.md", "skeptic.md", "rebuttal.md", "judge.md"]:
                copy_file(ROOT / "prompts" / prompt_name, root / "prompts" / prompt_name)

            scenario = {
                "claude": {
                    "researcher-0001": base_artifact(
                        "Cadence research",
                        supports_claims=["right_client_segment_exists"],
                        findings=[
                            {
                                "title": "Cadence signal",
                                "detail": "Founders face recurring high-stakes decisions.",
                                "claim_id": "right_client_segment_exists",
                                "kill_criterion_id": None,
                                "strength": "moderate",
                            }
                        ],
                    ),
                    "researcher-0003": base_artifact(
                        "Switching research",
                        weakens_claims=["switching_pressure_exists"],
                        findings=[
                            {
                                "title": "Switching pressure weak",
                                "detail": "Public evidence does not prove switching pressure.",
                                "claim_id": "switching_pressure_exists",
                                "kill_criterion_id": None,
                                "strength": "weakening",
                            }
                        ],
                    ),
                    "rebuttal": base_artifact("Rebuttal step", supports_claims=["right_client_segment_exists"]),
                },
                "codex": {
                    "researcher-0002": base_artifact(
                        "Workaround research",
                        weakens_claims=["existing_tools_are_good_enough"],
                        findings=[
                            {
                                "title": "Workaround pressure",
                                "detail": "Existing tools are common but fragmented.",
                                "claim_id": None,
                                "kill_criterion_id": "existing_tools_are_good_enough",
                                "strength": "moderate",
                            }
                        ],
                    ),
                    "skeptic": base_artifact("Skeptic step"),
                    "judge": base_artifact(
                        "Judge step",
                        supports_claims=["right_client_segment_exists"],
                        recommended_verdict="promising",
                    ),
                },
            }
            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    "--campaign",
                    "campaigns/client-discovery.yaml",
                    "--research-mode",
                    "planned",
                    "--research-engines",
                    "claude,codex",
                    "--research-workers",
                    "3",
                    "--research-max-topics",
                    "3",
                    "--cycles",
                    "1",
                ],
                cwd=root,
                env=env,
                check=True,
            )

            cycle_dir = root / "runs" / "client-discovery" / "cycle-0001"
            self.assertTrue((cycle_dir / "research-plan.json").exists())
            self.assertTrue((cycle_dir / "research-merge.json").exists())
            self.assertTrue((cycle_dir / "researcher-0001" / "topic.json").exists())
            self.assertTrue((cycle_dir / "researcher-0002" / "engine.json").exists())
            self.assertTrue((cycle_dir / "researcher" / "normalized.json").exists())
            merged = json.loads((cycle_dir / "researcher" / "normalized.json").read_text(encoding="utf-8"))
            self.assertIn("right_client_segment_exists", merged["supports_claims"])
            self.assertIn("switching_pressure_exists", merged["weakens_claims"])

    def test_init_preflight_run_status_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            copy_file(ROOT / "decision-graph.md", root / "decision-graph.md")
            copy_file(ROOT / "campaigns" / "client-discovery.yaml", root / "campaigns" / "client-discovery.yaml")
            copy_file(ROOT / "campaigns" / "manager-people.yaml", root / "campaigns" / "manager-people.yaml")
            copy_file(ROOT / "campaigns" / "pip-continuity.yaml", root / "campaigns" / "pip-continuity.yaml")
            for prompt_name in ["researcher.md", "skeptic.md", "rebuttal.md", "judge.md"]:
                copy_file(ROOT / "prompts" / prompt_name, root / "prompts" / prompt_name)
            copy_file(ROOT / "pyproject.toml", root / "pyproject.toml")

            scenario = {
                "claude": {
                    "researcher": base_artifact(
                        "Research step",
                        supports_claims=["right_client_segment_exists", "decision_fatigue_maps_to_workflow"],
                    ),
                    "rebuttal": base_artifact(
                        "Rebuttal step",
                        supports_claims=[
                            "right_client_segment_exists",
                            "decision_fatigue_maps_to_workflow",
                            "product_shape_can_be_tuned",
                            "switching_pressure_exists",
                            "pilot_path_is_accessible",
                        ],
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
                            "right_client_segment_exists",
                            "decision_fatigue_maps_to_workflow",
                            "product_shape_can_be_tuned",
                            "switching_pressure_exists",
                            "pilot_path_is_accessible",
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
                        proposed_mutations=[
                            {
                                "target_type": "report",
                                "target_file": "pilot.md",
                                "operation": "replace_file",
                                "content": "# Custom Pilot\n\nMerged from approved mutation.\n",
                                "reason": "Provide a cleaner pilot memo than the default template.",
                            }
                        ],
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
            self.assertTrue((root / "reports" / "client-discovery" / "pilot.md").exists())
            pilot_text = (root / "reports" / "client-discovery" / "pilot.md").read_text(encoding="utf-8")
            self.assertIn("Custom Pilot", pilot_text)
            mutation_log = json.loads((root / "runs" / "client-discovery" / "cycle-0001" / "mutation-log.json").read_text(encoding="utf-8"))
            self.assertEqual(len(mutation_log["merged"]), 1)


if __name__ == "__main__":
    unittest.main()
