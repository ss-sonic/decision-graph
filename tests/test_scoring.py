import unittest

from research_loop.campaign import load_campaign
from research_loop.cli import validate_mutation
from research_loop.scoring import apply_cycle_results, choose_next_objective
from research_loop.state import initialize_state


from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScoringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.campaign = load_campaign(ROOT / "campaigns" / "manager-people.yaml")

    def test_choose_next_objective_starts_with_first_must_prove_claim(self) -> None:
        state = initialize_state(self.campaign)
        objective = choose_next_objective(self.campaign, state)
        self.assertIn("pain_is_frequent", objective)

    def test_choose_next_objective_prefers_judge_recommendation(self) -> None:
        state = initialize_state(self.campaign)
        state["next_objective"] = "Run the direct benchmark."
        objective = choose_next_objective(self.campaign, state)
        self.assertEqual(objective, "Run the direct benchmark.")

    def test_plausible_requires_all_must_prove_claims(self) -> None:
        state = initialize_state(self.campaign)
        judge_artifact = {
            "objective": "test",
            "summary": "test",
            "findings": [],
            "sources": [{"title": "A", "locator": "https://example.com", "source_type": "web"}],
            "supports_claims": self.campaign.must_prove_claim_ids,
            "weakens_claims": [],
            "triggered_kill_criteria": [],
            "contradictions": [],
            "resolved_contradictions": [],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.8,
            "proposed_mutations": [],
            "recommended_verdict": "plausible",
            "claim_statuses": {},
            "kill_criterion_source_counts": {},
            "pilot_recommendation": {
                "target_user": "Manager",
                "pain_statement": "Pain",
                "current_workaround": "Chat",
                "why_existing_tools_fail": "No continuity",
            },
        }
        updated = apply_cycle_results(self.campaign, state, 1, judge_artifact)
        self.assertEqual(updated["verdict"], "plausible")

    def test_kill_criterion_can_reject(self) -> None:
        state = initialize_state(self.campaign)
        judge_artifact = {
            "objective": "test",
            "summary": "test",
            "findings": [],
            "sources": [{"title": "A", "locator": "https://example.com", "source_type": "web"}],
            "supports_claims": [],
            "weakens_claims": ["behavior_change_is_plausible"],
            "triggered_kill_criteria": ["users_will_not_switch"],
            "kill_criterion_source_counts": {"users_will_not_switch": 2},
            "contradictions": [],
            "resolved_contradictions": [],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.9,
            "proposed_mutations": [],
            "recommended_verdict": "rejected",
            "claim_statuses": {},
            "pilot_recommendation": {
                "target_user": None,
                "pain_statement": None,
                "current_workaround": None,
                "why_existing_tools_fail": None,
            },
        }
        updated = apply_cycle_results(self.campaign, state, 1, judge_artifact)
        self.assertEqual(updated["verdict"], "rejected")

    def test_no_evidence_streak_can_stall(self) -> None:
        state = initialize_state(self.campaign)
        empty_artifact = {
            "objective": "test",
            "summary": "test",
            "findings": [],
            "sources": [],
            "supports_claims": [],
            "weakens_claims": [],
            "triggered_kill_criteria": [],
            "contradictions": [],
            "resolved_contradictions": [],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.1,
            "proposed_mutations": [],
            "recommended_verdict": "active",
            "claim_statuses": {},
            "kill_criterion_source_counts": {},
            "pilot_recommendation": {
                "target_user": None,
                "pain_statement": None,
                "current_workaround": None,
                "why_existing_tools_fail": None,
            },
        }
        for cycle in range(1, 4):
            state = apply_cycle_results(self.campaign, state, cycle, empty_artifact)
        self.assertEqual(state["verdict"], "stalled")

    def test_unsupported_claim_status_maps_to_rejected(self) -> None:
        state = initialize_state(self.campaign)
        judge_artifact = {
            "objective": "test",
            "summary": "test",
            "findings": [],
            "sources": [],
            "supports_claims": [],
            "weakens_claims": [],
            "triggered_kill_criteria": [],
            "contradictions": [],
            "resolved_contradictions": [],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.4,
            "proposed_mutations": [],
            "recommended_verdict": "active",
            "claim_statuses": [{"claim_id": "pain_is_frequent", "status": "unsupported"}],
            "kill_criterion_source_counts": [],
            "pilot_recommendation": {
                "target_user": None,
                "pain_statement": None,
                "current_workaround": None,
                "why_existing_tools_fail": None,
            },
        }
        updated = apply_cycle_results(self.campaign, state, 1, judge_artifact)
        self.assertEqual(updated["claim_status"]["pain_is_frequent"]["status"], "rejected")

    def test_noncanonical_claim_statuses_map_to_contested(self) -> None:
        state = initialize_state(self.campaign)
        judge_artifact = {
            "objective": "test",
            "summary": "test",
            "findings": [],
            "sources": [],
            "supports_claims": [],
            "weakens_claims": [],
            "triggered_kill_criteria": [],
            "contradictions": [],
            "resolved_contradictions": [],
            "open_questions": [],
            "next_recommended_objective": None,
            "confidence": 0.4,
            "proposed_mutations": [],
            "recommended_verdict": "active",
            "claim_statuses": [
                {"claim_id": "pain_is_frequent", "status": "weakly_supported_narrowed_unproven"},
                {"claim_id": "continuity_beats_chat", "status": "untested_flagged"},
            ],
            "kill_criterion_source_counts": [],
            "pilot_recommendation": {
                "target_user": None,
                "pain_statement": None,
                "current_workaround": None,
                "why_existing_tools_fail": None,
            },
        }
        updated = apply_cycle_results(self.campaign, state, 1, judge_artifact)
        self.assertEqual(updated["claim_status"]["pain_is_frequent"]["status"], "contested")
        self.assertEqual(updated["claim_status"]["continuity_beats_chat"]["status"], "contested")

    def test_report_mutation_is_allowlisted(self) -> None:
        approved = validate_mutation(
            {
                "target_type": "report",
                "target_file": "pilot.md",
                "operation": "replace_file",
                "content": "# Pilot\ncustom\n",
            }
        )
        self.assertTrue(approved["approved"])

    def test_non_allowlisted_mutation_is_rejected(self) -> None:
        rejected = validate_mutation(
            {
                "target_type": "report",
                "target_file": "../hack.md",
                "operation": "replace_file",
                "content": "bad",
            }
        )
        self.assertFalse(rejected["approved"])


if __name__ == "__main__":
    unittest.main()
