from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research_loop.doc_artifacts import validate_editor_against_skeptic
from research_loop.doc_state import doc_slug, initialize_doc_state, next_doc_cycle_dir
from research_loop.engines.base import EngineError


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "doc-loop"


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

    def test_editor_rejects_unapproved_proposal_ids(self) -> None:
        editor = {"applied_proposal_ids": ["edit-2"]}
        skeptic = {"approved_proposal_ids": ["edit-1"]}
        with self.assertRaises(EngineError):
            validate_editor_against_skeptic(editor, skeptic)

    def test_run_status_latest_with_mock_engines(self) -> None:
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
                [sys.executable, str(SCRIPT), "run", "--doc", "sample.md", "--cycles", "1"],
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
            self.assertTrue((cycle_dir / "judge" / "normalized.json").exists())


if __name__ == "__main__":
    unittest.main()
