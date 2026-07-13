from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "aduc_identity.py"
REFERENCE = ROOT / "examples" / "identity" / "reference-cases.json"
INVALID = ROOT / "examples" / "identity" / "invalid-cases.json"

SPEC = importlib.util.spec_from_file_location("aduc_identity", TOOL_PATH)
assert SPEC and SPEC.loader
aduc_identity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aduc_identity)


class IdentityProfileTests(unittest.TestCase):
    def test_reference_cases_match_expected_decisions(self) -> None:
        results, failures = aduc_identity.check_reference_file(REFERENCE)
        self.assertEqual([], failures)
        self.assertEqual(9, len(results))
        self.assertTrue(all(result["valid"] for result in results))

    def test_invalid_cases_are_rejected_for_expected_reason(self) -> None:
        results, failures = aduc_identity.check_invalid_file(INVALID)
        self.assertEqual([], failures)
        self.assertEqual(17, len(results))
        self.assertTrue(all(not result["valid"] for result in results))

    def test_canonical_crosswalk_allows_strong_equality(self) -> None:
        document = aduc_identity.load_json(REFERENCE)
        case = next(item for item in document["cases"] if item["id"] == "canonical-crosswalk-allows-merge")
        result = aduc_identity.evaluate_case(case)
        self.assertEqual("mergeAllowed", result["decision"])
        self.assertTrue(result["owlSameAsAllowed"])

    def test_inferred_candidate_never_merges(self) -> None:
        document = aduc_identity.load_json(REFERENCE)
        case = next(item for item in document["cases"] if item["id"] == "inferred-candidate-never-merges")
        result = aduc_identity.evaluate_case(case)
        self.assertEqual("candidateOnly", result["decision"])
        self.assertFalse(result["owlSameAsAllowed"])

    def test_same_lexical_value_across_namespaces_is_unresolved(self) -> None:
        document = aduc_identity.load_json(REFERENCE)
        case = next(item for item in document["cases"] if item["id"] == "same-lexical-different-namespaces-unresolved")
        result = aduc_identity.evaluate_case(case)
        self.assertEqual("unresolved", result["decision"])

    def test_recycled_identifier_resolves_by_evaluation_time(self) -> None:
        document = aduc_identity.load_json(REFERENCE)
        case = next(item for item in document["cases"] if item["id"] == "recycled-identifier-resolves-by-time")
        result = aduc_identity.evaluate_case(case)
        self.assertEqual(["urn:aduc:entity:new-machine"], result["activeSubjects"])

    def test_privacy_purpose_is_enforced(self) -> None:
        document = aduc_identity.load_json(INVALID)
        case = next(item for item in document["cases"] if item["id"] == "privacy-purpose-mismatch")
        result = aduc_identity.evaluate_case(case)
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("ADUC-PRIV-001", codes)

    def test_cli_text_report_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL_PATH), str(REFERENCE), str(INVALID)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("Validated 9 identity reference cases and 17 required counterexamples", completed.stdout)

    def test_cli_json_report_is_machine_readable(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL_PATH), str(REFERENCE), str(INVALID), "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(9, report["validCases"])
        self.assertEqual(17, report["invalidCases"])
        self.assertEqual([], report["failures"])


if __name__ == "__main__":
    unittest.main()
