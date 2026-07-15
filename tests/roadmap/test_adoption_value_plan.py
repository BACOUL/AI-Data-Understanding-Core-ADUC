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

    def test_conformance_runner_is_the_single_active_task(self) -> None:
        text = NEXT_ACTION.read_text(encoding="utf-8")
        self.assertIn("provider-neutral full-Core conformance runner", text)
        self.assertIn("validators, comparators and formatters", text)
        self.assertIn("frozen machine-readable test manifest", text)
        self.assertIn("reference engine as the specification", text)
        self.assertIn("JSON/CSV compiler remains blocked", text)
        self.assertNotIn("Define and implement the deterministic complete-contract formatter", text)
        self.assertNotIn("migration path from the standalone semantic-mapping profile", text)

    def test_readme_exposes_cross_cutting_core_schema_validator_comparator_and_formatter_status(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("ADOPTION_AND_VALUE_VALIDATION.md", text)
        self.assertIn("manual mapping", text)
        self.assertIn("with and without ADUC", text)
        self.assertIn("ADUC_CORE_MODEL_0_1.md", text)
        self.assertIn("aduc-core.schema.json", text)
        self.assertIn("tools/aduc_core.py validate", text)
        self.assertIn("tools/aduc_core.py compare", text)
        self.assertIn("tools/aduc_core_format.py", text)
        self.assertIn("changeType", text)
        self.assertIn("assessment", text)
        self.assertIn("requiresHumanReview", text)
        self.assertIn("semantic-mapping profile", text)
        self.assertIn("provider-neutral full-Core conformance runner", text)


if __name__ == "__main__":
    unittest.main()
