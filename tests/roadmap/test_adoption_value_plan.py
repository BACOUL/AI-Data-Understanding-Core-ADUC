from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs" / "roadmap" / "ADOPTION_AND_VALUE_VALIDATION.md"
NEXT_ACTION = ROOT / "docs" / "roadmap" / "NEXT_ACTION.md"
README = ROOT / "README.md"


class AdoptionValuePlanTests(unittest.TestCase):
    def test_plan_contains_required_gates(self) -> None:
        text = PLAN.read_text(encoding="utf-8")
        required = [
            "structure-only",
            "sample-assisted",
            "documentation-assisted",
            "publisher-assisted",
            "Review-tax gate",
            "manual total time",
            "assisted total time",
            "With-ADUC versus without-ADUC evaluation",
            "Confidence and calibration",
            "MCP integration boundary",
            "median assisted human time is at least 30% lower",
            "no critical false mapping is silently accepted",
        ]
        for value in required:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_core_model_is_the_single_active_task(self) -> None:
        text = NEXT_ACTION.read_text(encoding="utf-8")
        self.assertIn("normative ADUC Core object model", text)
        self.assertIn("ADR-0013", text)
        self.assertIn("ADUC_CORE_MODEL_0_1.md", text)
        self.assertNotIn("implement the JSON/CSV compiler now", text.lower())

    def test_readme_exposes_cross_cutting_and_completed_profiles(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("ADOPTION_AND_VALUE_VALIDATION.md", text)
        self.assertIn("manual mapping", text)
        self.assertIn("with and without ADUC", text)
        self.assertIn("TEMPORAL_PROFILE_0_1.md", text)
        self.assertIn("IDENTITY_PROFILE_0_1.md", text)
        self.assertIn("PROVENANCE_PROFILE_0_1.md", text)
        self.assertIn("UNCERTAINTY_PROFILE_0_1.md", text)
        self.assertIn("RELATION_PROFILE_0_1.md", text)
        self.assertIn("POLICY_PROFILE_0_1.md", text)
        self.assertIn("candidateOnly", text)
        self.assertIn("replayable", text)
        self.assertIn("0.9 °F", text)
        self.assertIn("skos:closeMatch", text)
        self.assertIn("requiresHumanReview", text)


if __name__ == "__main__":
    unittest.main()
