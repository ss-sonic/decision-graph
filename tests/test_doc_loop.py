from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research_loop.doc_artifacts import validate_doc_artifact, validate_editor_against_skeptic
from research_loop.doc_cli import (
    build_research_config,
    build_research_plan,
    merge_research_artifacts,
    validate_editor_against_doc_spec,
)
from research_loop.doc_spec import load_doc_spec
from research_loop.doc_state import doc_slug, initialize_doc_state, next_doc_cycle_dir
from research_loop.engines.base import EngineError, PreflightResult


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "doc-loop"


class FakeAdapter:
    def __init__(self, engine: str, search_available: bool) -> None:
        self.engine = engine
        self.search_available = search_available

    def preflight(self) -> PreflightResult:
        return PreflightResult(
            engine=self.engine,
            available=True,
            auth_configured=True,
            search_available=self.search_available,
            search_mode="test",
            details=[],
        )


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def copy_doc_prompts(root: Path) -> None:
    for prompt in (ROOT / "doc-prompts").glob("*.md"):
        copy_file(prompt, root / "doc-prompts" / prompt.name)


def scenario() -> dict[str, object]:
    return {
        "claude": {
            "extractor": {
                "document_summary": "A short thesis doc.",
                "audience_assumptions": ["Investors"],
                "claims": [
                    {
                        "id": "claim-1",
                        "text": "Decision quality is costly.",
                        "type": "market",
                        "importance": "high",
                        "support_status": "weakly_supported",
                        "issue": "Needs evidence.",
                    }
                ],
                "top_evidence_gaps": [
                    {
                        "id": "gap-1",
                        "claim_ids": ["claim-1"],
                        "question": "What evidence supports costly decision errors?",
                        "importance": "high",
                        "research_hint": "Find credible research.",
                    }
                ],
                "structure_problems": ["Lead with the testable claim."],
                "summary": "Extractor found one high-value evidence gap.",
            },
            "researcher": {
                "summary": "Found one supporting source.",
                "researched_gap_ids": ["gap-1"],
                "evidence_items": [
                    {
                        "id": "ev-1",
                        "source": "Example Research",
                        "locator": "https://example.com/research",
                        "source_type": "research",
                        "claim_ids": ["claim-1"],
                        "supports_or_weakens": "supports",
                        "finding": "Decision errors can create material rework.",
                        "confidence": 0.7,
                    }
                ],
                "unresolved_gaps": [],
            },
            "editor": {
                "summary": "Applied approved evidence-backed edit.",
                "revised_markdown": "# Sample\n\nDecision quality can create material rework [ev-1].\n",
                "internal_notes_markdown": "# Internal Notes\n\nKeep the private evidence out of the public draft.\n",
                "changelog": ["Softened and evidenced the main claim."],
                "applied_proposal_ids": ["edit-1"],
            },
        },
        "codex": {
            "improver": {
                "summary": "Proposed one evidence-backed edit and one risky edit.",
                "proposals": [
                    {
                        "id": "edit-1",
                        "edit_type": "evidence_addition",
                        "target_heading": "Sample",
                        "original_excerpt": "Decision quality matters.",
                        "replacement": "Decision quality can create material rework [ev-1].",
                        "reason": "Adds support without overclaiming.",
                        "evidence_ids": ["ev-1"],
                        "confidence": 0.75,
                        "overclaiming_risk": "low",
                    },
                    {
                        "id": "edit-2",
                        "edit_type": "audience_alignment",
                        "target_heading": "Sample",
                        "original_excerpt": "Decision quality matters.",
                        "replacement": "This is a massive market.",
                        "reason": "Sounds stronger.",
                        "evidence_ids": [],
                        "confidence": 0.2,
                        "overclaiming_risk": "high",
                    },
                ],
            },
            "skeptic": {
                "summary": "Approved only the evidenced edit.",
                "approved_proposal_ids": ["edit-1"],
                "rejections": [{"proposal_id": "edit-2", "reason": "Unsupported market overclaim."}],
                "required_softening": [],
            },
            "judge": {
                "summary": "Document improved; another cycle could inspect remaining claims.",
                "verdict": "improved",
                "next_focus": "Inspect remaining unsupported claims.",
                "remaining_high_value_issues": ["Other claims need evidence."],
                "stop_reason": None,
            },
        },
    }


def planned_scenario() -> dict[str, object]:
    payload = scenario()
    payload["claude"]["extractor"]["research_units"] = [
        {
            "id": "unit-1",
            "kind": "evidence_gap",
            "claim_ids": ["claim-1"],
            "target_heading": "Sample",
            "question": "What evidence supports costly decision errors?",
            "importance": "critical",
            "research_hint": "Find credible research.",
            "success_criteria": "Find a source that supports or weakens claim-1.",
        },
        {
            "id": "unit-2",
            "kind": "section_risk",
            "claim_ids": ["claim-1"],
            "target_heading": "Sample",
            "question": "What wording would overclaim the evidence?",
            "importance": "medium",
            "research_hint": "Check for caveats.",
            "success_criteria": "Find caveats relevant to claim-1.",
        },
    ]
    payload["claude"]["researcher-0001"] = {
        "summary": "Claude researched the critical evidence gap.",
        "researched_gap_ids": ["unit-1"],
        "evidence_items": [
            {
                "id": "ev-claude-1",
                "source": "Example Research",
                "locator": "https://example.com/research",
                "source_type": "research",
                "claim_ids": ["claim-1"],
                "supports_or_weakens": "supports",
                "finding": "Decision errors can create material rework.",
                "confidence": 0.7,
            }
        ],
        "unresolved_gaps": [],
    }
    payload["codex"]["researcher-0002"] = {
        "summary": "Codex confirmed the same critical evidence gap.",
        "researched_gap_ids": ["unit-1"],
        "evidence_items": [
            {
                "id": "ev-codex-1",
                "source": "Example Research",
                "locator": "https://example.com/research",
                "source_type": "research",
                "claim_ids": ["claim-1"],
                "supports_or_weakens": "supports",
                "finding": "Decision errors can create material rework.",
                "confidence": 0.8,
            }
        ],
        "unresolved_gaps": [],
    }
    payload["claude"]["researcher-0003"] = {
        "summary": "Claude researched the section risk.",
        "researched_gap_ids": ["unit-2"],
        "evidence_items": [
            {
                "id": "ev-claude-2",
                "source": "Caveat Source",
                "locator": "https://example.com/caveat",
                "source_type": "analysis",
                "claim_ids": ["claim-1"],
                "supports_or_weakens": "weakens",
                "finding": "The claim should avoid overgeneralizing decision costs.",
                "confidence": 0.65,
            }
        ],
        "unresolved_gaps": [],
    }
    return payload


class DocLoopTests(unittest.TestCase):
    def test_doc_slug_and_cycle_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            doc = root / "docs" / "My Doc.md"
            doc.parent.mkdir()
            doc.write_text("# Test\n", encoding="utf-8")
            state = initialize_doc_state(root, doc)
            self.assertEqual(doc_slug(root, doc), "docs-my-doc")
            self.assertEqual(next_doc_cycle_dir(root, doc, state).name, "cycle-0001")

    def test_doc_spec_coerces_string_booleans(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "docspec.yaml"
            path.write_text(
                "document_type: test\n"
                "author: author\n"
                "audience: audience\n"
                "goal: goal\n"
                "tone: tone\n"
                "risk_posture: posture\n"
                "strict_public_pattern_validation: 'false'\n",
                encoding="utf-8",
            )
            self.assertFalse(load_doc_spec(path)["strict_public_pattern_validation"])

    def test_editor_rejects_unapproved_proposal_ids(self) -> None:
        editor = {"applied_proposal_ids": ["edit-2"]}
        skeptic = {"approved_proposal_ids": ["edit-1"]}
        with self.assertRaises(EngineError):
            validate_editor_against_skeptic(editor, skeptic)

    def test_extractor_accepts_research_units(self) -> None:
        artifact = scenario()["claude"]["extractor"]
        artifact["research_units"] = [
            {
                "id": "unit-1",
                "kind": "evidence_gap",
                "claim_ids": ["claim-1"],
                "target_heading": "Sample",
                "question": "What evidence supports the claim?",
                "importance": "critical",
                "research_hint": "Find primary research.",
                "success_criteria": "Return evidence that supports or weakens claim-1.",
            }
        ]
        validate_doc_artifact("extractor", artifact)

    def test_research_plan_duplicates_critical_units_across_engines(self) -> None:
        extractor = planned_scenario()["claude"]["extractor"]
        plan = build_research_plan(
            extractor,
            usable_engines=["claude", "codex"],
            budget="standard",
            max_units=8,
            max_workers=4,
        )
        assignments_by_unit = {}
        for assignment in plan["assignments"]:
            assignments_by_unit.setdefault(assignment["work_unit"]["id"], []).append(assignment["engine"])
        self.assertEqual(assignments_by_unit["unit-1"], ["claude", "codex"])
        self.assertEqual(assignments_by_unit["unit-2"], ["claude"])

    def test_research_merge_dedupes_sources_and_preserves_claims(self) -> None:
        worker_results = [
            {
                "worker_id": "researcher-0001",
                "engine": "claude",
                "work_unit_id": "unit-1",
                "artifact": planned_scenario()["claude"]["researcher-0001"],
            },
            {
                "worker_id": "researcher-0002",
                "engine": "codex",
                "work_unit_id": "unit-1",
                "artifact": planned_scenario()["codex"]["researcher-0002"],
            },
        ]
        merged, metadata = merge_research_artifacts(worker_results, failed_workers=[])
        self.assertEqual(len(merged["evidence_items"]), 1)
        self.assertEqual(merged["evidence_items"][0]["claim_ids"], ["claim-1"])
        self.assertEqual(metadata["evidence_groups"][0]["confirmation_status"], "multi_engine_confirmed")
        self.assertEqual(metadata["evidence_groups"][0]["engines"], ["claude", "codex"])

    def test_research_config_excludes_engines_without_search(self) -> None:
        args = argparse.Namespace(
            research_mode="planned",
            research_engines="claude,codex",
            research_budget="standard",
            research_workers=None,
            research_max_units=None,
        )
        config = build_research_config(
            args,
            {
                "claude": FakeAdapter("claude", True),
                "codex": FakeAdapter("codex", False),
            },
        )
        self.assertEqual(config["engines"], ["claude"])

    def test_doc_spec_allows_negated_fatwa_disclaimer(self) -> None:
        spec = {
            "forbidden_public_assertions": ["Blinq is Sharia-compliant", "This is a fatwa"],
            "forbidden_public_patterns": ["automatically compliant"],
            "strict_public_pattern_validation": False,
            "allowed_disclaimer_patterns": [
                "This proposal does not assert that Blinq is Sharia-compliant.",
                "This is not a fatwa, legal opinion, or final compliance claim.",
            ],
        }
        validate_editor_against_doc_spec(
            {
                "revised_markdown": (
                    "This is not a fatwa, legal opinion, or final compliance claim. "
                    "This proposal does not assert that Blinq is Sharia-compliant."
                    "\n\n## Why \"All Prediction Markets Are Halal\" Is Not the Right Claim\n\n"
                    "> All prediction markets are Sharia-compliant.\n"
                )
            },
            spec,
        )
        warnings = validate_editor_against_doc_spec(
            {"revised_markdown": "This could become automatically compliant after review."},
            spec,
        )
        self.assertEqual(len(warnings), 1)
        with self.assertRaises(EngineError):
            validate_editor_against_doc_spec(
                {"revised_markdown": "This is a fatwa."},
                spec,
            )
        with self.assertRaises(EngineError):
            validate_editor_against_doc_spec(
                {"revised_markdown": "Blinq is Sharia-compliant."},
                spec,
            )

    def test_run_status_latest_with_mock_engines(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample.md"
            sample.write_text("# Sample\n\nDecision quality matters.\n", encoding="utf-8")
            support = root / "supporting.md"
            support.write_text(
                "# Supporting Evidence\n\n"
                "## Evidence Items\n\n"
                "### EV-PRIVATE-1: Internal repository\n"
                "- Type: private_repo\n"
                "- Locator: https://example.com/private\n"
                "- Supports: Decision quality workflow exists\n"
                "- Publicly quotable: no\n",
                encoding="utf-8",
            )
            spec = root / "sample.docspec.yaml"
            spec.write_text(
                "document_type: partner_proposal\n"
                "author: SampleCo\n"
                "audience: Partner BD team\n"
                "goal: Secure a technical exploration\n"
                "tone: confident and clear\n"
                "risk_posture: defensible_not_defensive\n"
                "private_evidence_policy: use_for_confidence_do_not_quote\n"
                "diligence_language: internal_notes_only\n"
                "forbidden_public_patterns:\n"
                "  - publicly verifiable status is limited\n"
                "  - unverified\n",
                encoding="utf-8",
            )
            copy_doc_prompts(root)

            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(scenario()), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    "--doc",
                    "sample.md",
                    "--supporting-doc",
                    "supporting.md",
                    "--spec",
                    "sample.docspec.yaml",
                    "--research-mode",
                    "sequential",
                    "--cycles",
                    "1",
                ],
                cwd=root,
                env=env,
                check=True,
            )
            status = subprocess.run(
                [sys.executable, str(SCRIPT), "status", "--doc", "sample.md"],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Verdict: improved", status.stdout)

            latest = subprocess.run(
                [sys.executable, str(SCRIPT), "latest", "--doc", "sample.md"],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            latest_path = Path(latest)
            self.assertTrue(latest_path.exists())
            self.assertIn("[ev-1]", latest_path.read_text(encoding="utf-8"))
            self.assertEqual(sample.read_text(encoding="utf-8"), "# Sample\n\nDecision quality matters.\n")

            cycle_dir = root / "doc-runs" / "sample" / "cycle-0001"
            self.assertTrue((cycle_dir / "input.md").exists())
            self.assertTrue((cycle_dir / "change-log.md").exists())
            self.assertTrue((cycle_dir / "internal-notes.md").exists())
            self.assertTrue((cycle_dir / "judge" / "normalized.json").exists())
            state = json.loads((root / "doc-runs" / "sample" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["supporting_docs"], [str(support.resolve())])
            self.assertEqual(state["doc_spec_path"], str(spec.resolve()))
            self.assertEqual(Path(state["latest_internal_notes"]).resolve(), (cycle_dir / "internal-notes.md").resolve())
            prompt = (cycle_dir / "researcher" / "prompt.txt").read_text(encoding="utf-8")
            self.assertIn("Supporting Evidence Documents", prompt)
            self.assertIn("EV-PRIVATE-1", prompt)
            self.assertIn("do not expose private locators", prompt)
            editor_prompt = (cycle_dir / "editor" / "prompt.txt").read_text(encoding="utf-8")
            self.assertIn("Document Intent Spec", editor_prompt)
            self.assertIn("partner_proposal", editor_prompt)
            self.assertIn("internal notes", editor_prompt.lower())

    def test_planned_research_with_mock_engines_creates_worker_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample.md"
            sample.write_text("# Sample\n\nDecision quality matters.\n", encoding="utf-8")
            copy_doc_prompts(root)

            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(planned_scenario()), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    "--doc",
                    "sample.md",
                    "--research-engines",
                    "claude,codex",
                    "--research-budget",
                    "standard",
                    "--research-workers",
                    "3",
                    "--cycles",
                    "1",
                ],
                cwd=root,
                env=env,
                check=True,
            )

            cycle_dir = root / "doc-runs" / "sample" / "cycle-0001"
            self.assertTrue((cycle_dir / "research-plan.json").exists())
            self.assertTrue((cycle_dir / "research-merge.json").exists())
            self.assertTrue((cycle_dir / "researcher-0001" / "engine.json").exists())
            self.assertTrue((cycle_dir / "researcher-0002" / "engine.json").exists())
            self.assertTrue((cycle_dir / "researcher" / "normalized.json").exists())
            merged = json.loads((cycle_dir / "researcher" / "normalized.json").read_text(encoding="utf-8"))
            self.assertEqual(len(merged["evidence_items"]), 2)
            merge = json.loads((cycle_dir / "research-merge.json").read_text(encoding="utf-8"))
            statuses = {group["confirmation_status"] for group in merge["evidence_groups"]}
            self.assertIn("multi_engine_confirmed", statuses)

    def test_planned_research_continues_when_one_worker_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample.md"
            sample.write_text("# Sample\n\nDecision quality matters.\n", encoding="utf-8")
            copy_doc_prompts(root)

            payload = planned_scenario()
            payload["codex"]["researcher-0002"] = {"__error__": "simulated codex failure"}
            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    "--doc",
                    "sample.md",
                    "--research-engines",
                    "claude,codex",
                    "--research-budget",
                    "standard",
                    "--cycles",
                    "1",
                ],
                cwd=root,
                env=env,
                check=True,
            )

            merge = json.loads(
                (root / "doc-runs" / "sample" / "cycle-0001" / "research-merge.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(merge["failed_workers"][0]["worker_id"], "researcher-0002")
            self.assertTrue((root / "doc-runs" / "sample" / "cycle-0001" / "revised.md").exists())

    def test_sequential_research_mode_preserves_current_researcher_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample.md"
            sample.write_text("# Sample\n\nDecision quality matters.\n", encoding="utf-8")
            copy_doc_prompts(root)

            scenario_path = root / "mock-scenario.json"
            scenario_path.write_text(json.dumps(scenario()), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            env["RESEARCH_LOOP_MOCK_ENGINES"] = "1"
            env["RESEARCH_LOOP_MOCK_FILE"] = str(scenario_path)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    "--doc",
                    "sample.md",
                    "--research-mode",
                    "sequential",
                    "--cycles",
                    "1",
                ],
                cwd=root,
                env=env,
                check=True,
            )

            cycle_dir = root / "doc-runs" / "sample" / "cycle-0001"
            self.assertTrue((cycle_dir / "researcher" / "normalized.json").exists())
            self.assertFalse((cycle_dir / "research-plan.json").exists())
            self.assertFalse((cycle_dir / "researcher-0001").exists())


if __name__ == "__main__":
    unittest.main()
