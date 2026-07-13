from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "aduc_epistemic.py"
REFERENCE_PATH = ROOT / "examples" / "epistemic-status" / "reference-cases.json"
INVALID_PATH = ROOT / "examples" / "epistemic-status" / "invalid-cases.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


aduc_epistemic = load_module("aduc_epistemic", MODULE_PATH)


class EpistemicLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = load_json(REFERENCE_PATH)
        self.invalid = load_json(INVALID_PATH)

    def test_reference_cases_cover_all_seven_effective_states(self) -> None:
        report = aduc_epistemic.evaluate_collection(self.reference)
        self.assertTrue(report["valid"], report["errors"])
        self.assertTrue(report["allRecordSetsValid"])
        states = {result["effectiveState"] for result in report["results"]}
        self.assertEqual(
            states,
            {
                "unknown",
                "inferred",
                "reviewed",
                "verified",
                "canonical",
                "contested",
                "deprecated",
            },
        )

    def test_counterexamples_are_rejected_for_the_expected_reason_class(self) -> None:
        report = aduc_epistemic.evaluate_collection(self.invalid)
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(report["allRecordSetsValid"])
        self.assertTrue(report["results"])
        for result in report["results"]:
            with self.subTest(case=result["caseId"]):
                self.assertFalse(result["valid"])
                self.assertEqual(result["effectiveState"], "invalid")
                self.assertEqual(result["action"], "rejected")
                self.assertTrue(result["errors"])

    def test_reviewed_verified_and_canonical_have_distinct_requirements(self) -> None:
        results = {
            item["caseId"]: item
            for item in aduc_epistemic.evaluate_collection(self.reference)["results"]
        }
        self.assertEqual(results["reviewed-usable-by-policy"]["action"], "usable")
        self.assertEqual(
            results["verified-usable-by-method-policy"]["action"], "usable"
        )
        self.assertEqual(
            results["canonical-recognized-authority"]["action"], "authoritative"
        )
        self.assertEqual(
            results["reviewed-usable-by-policy"]["effectiveState"], "reviewed"
        )
        self.assertEqual(
            results["verified-usable-by-method-policy"]["effectiveState"],
            "verified",
        )
        self.assertEqual(
            results["canonical-recognized-authority"]["effectiveState"],
            "canonical",
        )

    def test_open_challenge_blocks_selection_without_erasing_authority(self) -> None:
        case = next(
            case
            for case in self.reference["cases"]
            if case["caseId"] == "open-challenge-blocks-selection"
        )
        result = aduc_epistemic.evaluate_case(case)
        self.assertTrue(result["valid"])
        self.assertEqual(result["effectiveState"], "contested")
        self.assertEqual(result["action"], "blocked")
        self.assertIsNone(result["selectedAssertionId"])
        self.assertEqual(result["challengeIds"], ["urn:challenge:flow:1"])
        self.assertEqual(
            case["recordSet"]["assertions"][0]["authorityStatus"], "reviewed"
        )

    def test_deprecated_assertion_is_historical_but_replacement_is_selectable(self) -> None:
        results = {
            item["caseId"]: item
            for item in aduc_epistemic.evaluate_collection(self.reference)["results"]
        }
        self.assertEqual(
            results["only-deprecated-assertion-remains"]["effectiveState"],
            "deprecated",
        )
        self.assertEqual(
            results["only-deprecated-assertion-remains"]["action"], "historical"
        )
        self.assertEqual(
            results["deprecated-assertion-with-active-replacement"]["effectiveState"],
            "canonical",
        )
        self.assertEqual(
            results["deprecated-assertion-with-active-replacement"][
                "selectedAssertionId"
            ],
            "urn:assertion:flow:new",
        )

    def test_unrecognized_canonical_authority_is_blocked_not_downgraded(self) -> None:
        record_set = {
            "source": "urn:source:test",
            "validFor": "urn:schema:test:1",
            "localReference": "/properties/x",
            "coverage": [],
            "assertions": [
                {
                    "id": "urn:assertion:canonical:unrecognized",
                    "semanticTarget": "urn:concept:X",
                    "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
                    "authorityStatus": "canonical",
                    "assertedBy": "urn:org:unknown-publisher",
                    "assertedAt": "2026-07-13T16:00:00Z",
                    "authority": {
                        "sourceAuthority": "urn:org:unknown-publisher",
                        "evidence": ["urn:evidence:self-declaration"],
                    },
                }
            ],
            "challenges": [],
            "deprecations": [],
        }
        result = aduc_epistemic.evaluate_record_set(record_set, {})
        self.assertTrue(result["valid"])
        self.assertEqual(result["effectiveState"], "canonical")
        self.assertEqual(result["action"], "blocked")

    def test_cli_confirms_both_reference_and_counterexample_expectations(self) -> None:
        for path in (REFERENCE_PATH, INVALID_PATH):
            with self.subTest(path=path.name):
                run = subprocess.run(
                    [sys.executable, str(MODULE_PATH), str(path)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(run.returncode, 0, run.stderr or run.stdout)
                report = json.loads(run.stdout)
                self.assertTrue(report["expectationsMet"])


if __name__ == "__main__":
    unittest.main()
