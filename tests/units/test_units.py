from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "aduc_units.py"
EXAMPLES = ROOT / "examples" / "units"
VALID_CASES = EXAMPLES / "reference-cases.json"
INVALID_CASES = EXAMPLES / "invalid-cases.json"
REGISTRY = EXAMPLES / "registry.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


units = load_module("aduc_units", MODULE_PATH)


def load_cases(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


class UnitConversionTests(unittest.TestCase):
    def test_reference_cases_pass(self) -> None:
        report = units.evaluate_cases(VALID_CASES)
        self.assertTrue(report["valid"], report)
        self.assertEqual(len(report["results"]), 5)
        self.assertTrue(all(item["valid"] for item in report["results"]))

    def test_required_counterexamples_are_rejected(self) -> None:
        report = units.evaluate_cases(INVALID_CASES)
        self.assertTrue(report["valid"], report)
        self.assertEqual(len(report["results"]), 15)
        self.assertTrue(all(not item["valid"] for item in report["results"]))
        self.assertTrue(all(item["matchesExpectation"] for item in report["results"]))

    def test_absolute_temperature_conversion_is_affine(self) -> None:
        case = load_cases(VALID_CASES)[0]
        report = units.convert_case(case)
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["formula"], "affine-v0.1")
        self.assertEqual(report["referenceValue"], "362.15")
        self.assertEqual(report["output"]["exactValue"], "192.2")
        self.assertEqual(report["output"]["displayValue"], "192.2")

    def test_temperature_difference_ignores_offsets(self) -> None:
        case = load_cases(VALID_CASES)[1]
        report = units.convert_case(case)
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["formula"], "difference-multiplicative-v0.1")
        self.assertEqual(report["output"]["exactValue"], "18")
        self.assertEqual(report["output"]["displayValue"], "18.0")

    def test_uncertainty_is_scaled_without_offset(self) -> None:
        case = load_cases(VALID_CASES)[0]
        report = units.convert_case(case)
        self.assertEqual(report["uncertainty"]["exactValue"], "0.36")
        self.assertEqual(report["uncertainty"]["displayValue"], "0.4")

    def test_percent_and_unitless_have_explicit_scale(self) -> None:
        cases = load_cases(VALID_CASES)
        percent_to_ratio = units.convert_case(cases[3])
        ratio_to_percent = units.convert_case(cases[4])
        self.assertEqual(percent_to_ratio["output"]["exactValue"], "0.5")
        self.assertEqual(ratio_to_percent["output"]["exactValue"], "12.5")

    def test_registry_tampering_is_detected(self) -> None:
        case = deepcopy(load_cases(VALID_CASES)[0])
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copy2(REGISTRY, temp_root / "registry.json")
            with (temp_root / "registry.json").open("a", encoding="utf-8") as handle:
                handle.write(" ")
            report = units.convert_case(case, temp_root)
        codes = {item["code"] for item in report["errors"]}
        self.assertFalse(report["valid"])
        self.assertIn("ADUC-CONV-004", codes)

    def test_exact_fraction_and_half_even_rounding(self) -> None:
        self.assertEqual(units.fraction_to_exact_string(Fraction(1, 8)), "0.125")
        self.assertEqual(units.round_fraction(Fraction(125, 100), 1), "1.2")
        self.assertEqual(units.round_fraction(Fraction(135, 100), 1), "1.4")

    def test_cli_accepts_both_official_case_files(self) -> None:
        run = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                str(VALID_CASES),
                str(INVALID_CASES),
                "--compact",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr or run.stdout)
        report = json.loads(run.stdout)
        self.assertTrue(report["valid"])


if __name__ == "__main__":
    unittest.main()
