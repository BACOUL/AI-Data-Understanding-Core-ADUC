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

    def test_identity_strategy_is_the_single_active_task(self) -> None:
        text = NEXT_ACTION.read_text(encoding="utf-8")
        self.assertIn("entity identity and equivalence", text)
        self.assertIn("ADOPTION_AND_VALUE_VALIDATION.md", text)
        self.assertIn("temporal profile", text)
        self.assertNotIn("implement the JSON/CSV compiler now", text.lower())

    def test_readme_exposes_cross_cutting_and_temporal_gates(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("ADOPTION_AND_VALUE_VALIDATION.md", text)
        self.assertIn("manual mapping", text)
        self.assertIn("with and without ADUC", text)
        self.assertIn("TEMPORAL_PROFILE_0_1.md", text)
        self.assertIn("2026-07-13T12:00:00Z", text)


if __name__ == "__main__":
    unittest.main()
