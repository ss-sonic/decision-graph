import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research_loop.campaign import load_campaign
from research_loop.engines.base import canonicalize_artifact, engine_timeout_seconds, unwrap_artifact_payload


ROOT = Path(__file__).resolve().parents[1]


class CampaignSchemaTests(unittest.TestCase):
    def test_manager_people_campaign_loads(self) -> None:
        campaign = load_campaign(ROOT / "campaigns" / "manager-people.yaml")
        self.assertEqual(campaign.slug, "manager-people")
        self.assertIn("pain_is_frequent", campaign.claim_ids())

    def test_pip_continuity_campaign_starts_with_continuity(self) -> None:
        campaign = load_campaign(ROOT / "campaigns" / "pip-continuity.yaml")
        self.assertEqual(campaign.slug, "pip-continuity")
        self.assertEqual(campaign.must_prove_claim_ids[0], "continuity_beats_chat")
        self.assertIn("pip_cases_recur_over_time", campaign.claim_ids())

    def test_client_discovery_campaign_starts_with_segment_search(self) -> None:
        campaign = load_campaign(ROOT / "campaigns" / "client-discovery.yaml")
        self.assertEqual(campaign.slug, "client-discovery")
        self.assertEqual(campaign.must_prove_claim_ids[0], "right_client_segment_exists")
        self.assertIn("product_shape_can_be_tuned", campaign.claim_ids())

    def test_missing_keys_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.yaml"
            path.write_text("idea: {}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_campaign(path)

    def test_unwraps_claude_cli_structured_output(self) -> None:
        wrapped = {
            "type": "result",
            "structured_output": {
                "objective": "o",
                "summary": "s",
                "findings": [],
                "sources": [],
                "supports_claims": [],
                "weakens_claims": [],
                "triggered_kill_criteria": [],
                "contradictions": [],
                "open_questions": [],
                "next_recommended_objective": None,
                "confidence": 0.5,
                "proposed_mutations": [],
                "recommended_verdict": "active",
                "claim_statuses": {},
                "kill_criterion_source_counts": {},
                "resolved_contradictions": [],
                "pilot_recommendation": {
                    "target_user": None,
                    "pain_statement": None,
                    "current_workaround": None,
                    "why_existing_tools_fail": None,
                },
            },
        }
        unwrapped = unwrap_artifact_payload(wrapped)
        self.assertEqual(unwrapped["objective"], "o")

    def test_unwraps_json_fenced_result(self) -> None:
        wrapped = {
            "type": "result",
            "result": "```json\n{\n  \"objective\": \"o\",\n  \"summary\": \"s\",\n  \"findings\": [],\n  \"sources\": [],\n  \"supports_claims\": [],\n  \"weakens_claims\": [],\n  \"triggered_kill_criteria\": [],\n  \"contradictions\": [],\n  \"open_questions\": [],\n  \"next_recommended_objective\": null,\n  \"confidence\": 0.5,\n  \"proposed_mutations\": [],\n  \"recommended_verdict\": \"active\",\n  \"claim_statuses\": {},\n  \"kill_criterion_source_counts\": {},\n  \"resolved_contradictions\": [],\n  \"pilot_recommendation\": {\"target_user\": null, \"pain_statement\": null, \"current_workaround\": null, \"why_existing_tools_fail\": null}\n}\n```",
        }
        unwrapped = unwrap_artifact_payload(wrapped)
        self.assertEqual(unwrapped["objective"], "o")

    def test_canonicalizes_string_contradictions(self) -> None:
        artifact = {
            "objective": "o",
            "summary": "s",
            "findings": [],
            "sources": [],
            "supports_claims": [],
            "weakens_claims": [],
            "triggered_kill_criteria": [],
            "contradictions": ["Generic AI may be good enough"],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.5,
            "proposed_mutations": [],
            "recommended_verdict": "active",
            "claim_statuses": {},
            "kill_criterion_source_counts": {},
            "resolved_contradictions": [],
            "pilot_recommendation": {
                "target_user": None,
                "pain_statement": None,
                "current_workaround": None,
                "why_existing_tools_fail": None,
            },
        }
        canonical = canonicalize_artifact(artifact)
        self.assertEqual(canonical["contradictions"][0]["detail"], "Generic AI may be good enough")

    def test_timeout_is_disabled_by_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(engine_timeout_seconds())


if __name__ == "__main__":
    unittest.main()
