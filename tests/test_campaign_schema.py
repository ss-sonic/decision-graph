from pathlib import Path
import tempfile
import unittest

from research_loop.campaign import load_campaign


ROOT = Path(__file__).resolve().parents[1]


class CampaignSchemaTests(unittest.TestCase):
    def test_manager_people_campaign_loads(self) -> None:
        campaign = load_campaign(ROOT / "campaigns" / "manager-people.yaml")
        self.assertEqual(campaign.slug, "manager-people")
        self.assertIn("pain_is_frequent", campaign.claim_ids())

    def test_missing_keys_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.yaml"
            path.write_text("idea: {}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_campaign(path)


if __name__ == "__main__":
    unittest.main()

