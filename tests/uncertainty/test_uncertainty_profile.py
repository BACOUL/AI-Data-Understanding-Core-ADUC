from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "aduc_uncertainty.py"
EXAMPLES = ROOT / "examples" / "uncertainty"

spec = importlib.util.spec_from_file_location("aduc_uncertainty", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UncertaintyProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = json.loads((EXAMPLES / "reference-cases.json").read_text(encoding="utf-8"))
        cls.invalid = json.loads((EXAMPLES / "invalid-cases.json").read_text(encoding="utf-8"))
        cls.reference_by_id = {case["caseId"]: case for case in cls.reference["cases"]}
        cls.invalid_by_id = {
            specification["caseId"]: module.materialize_invalid_case(
                specification,
                cls.reference_by_id,
            )
            for specification in cls.invalid["cases"]
        }

    def test_reference_and_invalid_suites(self) -> None:
        report = module.run_suites(
            EXAMPLES / "reference-cases.json",
            EXAMPLES / "invalid-cases.json",
        )
        self.assertTrue(report["ok"], report["failures"])
        self.assertEqual(report["referenceAccepted"], 14)
        self.assertEqual(report["invalidRejected"], 24)

    def test_standard_uncertainty_is_valid_and_usable(self) -> None:
        result = module.evaluate_case(self.reference_by_id["standard-absolute-measurement"])
        self.assertTrue(result["valid"])
        self.assertTrue(result["usable"])

    def test_contested_unknown_uncertainty_is_preserved_but_not_usable(self) -> None:
        result = module.evaluate_case(self.reference_by_id["unknown-contested-uncertainty"])
        self.assertTrue(result["valid"])
        self.assertFalse(result["usable"])

    def test_affine_temperature_conversion_scales_uncertainty_without_offset(self) -> None:
        result = module.evaluate_case(
            self.reference_by_id["affine-temperature-uncertainty-conversion"]
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["result"]["standardUncertainty"], "0.9")

    def test_independent_additive_and_multiplicative_propagation(self) -> None:
        additive = module.evaluate_case(
            self.reference_by_id["independent-additive-propagation"]
        )
        multiplicative = module.evaluate_case(
            self.reference_by_id["independent-multiplicative-propagation"]
        )
        self.assertEqual(additive["result"]["standardUncertainty"], "5")
        self.assertEqual(
            multiplicative["result"]["relativeStandardUncertainty"],
            "0.05",
        )

    def test_resolution_contribution_is_reproducible(self) -> None:
        result = module.evaluate_case(
            self.reference_by_id["resolution-rectangular-contribution"]
        )
        self.assertTrue(result["valid"])
        self.assertEqual(
            result["result"]["standardUncertainty"],
            "0.028867513459481",
        )

    def test_unknown_dependence_blocks_propagation(self) -> None:
        result = module.evaluate_case(
            self.invalid_by_id["unknown-dependence-propagation"]
        )
        self.assertFalse(result["valid"])
        self.assertIn(
            "ADUC-PROP-002",
            {item["code"] for item in result["errors"]},
        )

    def test_uncalibrated_model_score_is_not_probability(self) -> None:
        result = module.evaluate_case(
            self.invalid_by_id["uncalibrated-categorical-score"]
        )
        self.assertFalse(result["valid"])
        self.assertIn(
            "ADUC-UNC-010",
            {item["code"] for item in result["errors"]},
        )

    def test_quality_completeness_claim_cannot_hide_missing_metric(self) -> None:
        result = module.evaluate_case(
            self.invalid_by_id["complete-quality-with-missing-metric"]
        )
        self.assertFalse(result["valid"])
        self.assertIn(
            "ADUC-DQV-003",
            {item["code"] for item in result["errors"]},
        )

    def test_cli_json_report_and_exit_code(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(TOOL_PATH),
                str(EXAMPLES / "reference-cases.json"),
                str(EXAMPLES / "invalid-cases.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["referenceAccepted"], 14)
        self.assertEqual(payload["invalidRejected"], 24)


if __name__ == "__main__":
    unittest.main()
