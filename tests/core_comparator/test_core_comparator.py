from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_core.py"
COMPLETE = ROOT / "examples" / "core" / "complete-model.example.json"
COMPARISON_CASES = ROOT / "examples" / "core" / "comparison" / "cases.json"

SPEC = importlib.util.spec_from_file_location("aduc_core", TOOL)
assert SPEC and SPEC.loader
aduc_core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aduc_core)


class UnifiedCoreComparatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(COMPLETE.read_text(encoding="utf-8"))
        cls.suite = json.loads(COMPARISON_CASES.read_text(encoding="utf-8"))
        cls.cases = cls.suite["cases"]

    def test_official_comparison_suite_has_expected_scenarios(self) -> None:
        self.assertEqual(len(self.cases), 24)
        ids = {case["id"] for case in self.cases}
        self.assertEqual(len(ids), len(self.cases))
        self.assertTrue({"01-identical-reordered", "19-left-invalid", "20-right-invalid", "24-unit-insufficient-information"}.issubset(ids))

    def test_each_comparison_fixture_produces_expected_overall_and_codes(self) -> None:
        for case in self.cases:
            with self.subTest(case=case["id"]):
                left, right = materialize(self.base, case)
                report = aduc_core.compare_contracts(left, right, left_source=case["id"] + ":left", right_source=case["id"] + ":right")
                self.assertEqual(report["overall"], case["expectedOverall"], report)
                self.assertEqual(report["reportVersion"], "0.1.0")
                self.assertIn("left", report)
                self.assertIn("right", report)
                found_codes = {item["code"] for item in report["changes"]}
                for code in case["expectedCodes"]:
                    self.assertIn(code, found_codes, report)
                assessments = {report.get("overallAssessment"), *(item.get("assessment") for item in report["changes"])}
                for assessment in case.get("expectedAssessments", []):
                    self.assertIn(assessment, assessments, report)
                for module in case["modules"]:
                    self.assertTrue(module == "contract" or any(item["module"] == module for item in report["changes"]), report)

    def test_identical_contracts_and_reordered_addressable_arrays_are_unchanged(self) -> None:
        case = by_id(self.cases, "01-identical-reordered")
        left, right = materialize(self.base, case)
        report = aduc_core.compare_contracts(left, right)
        self.assertTrue(report["comparable"])
        self.assertEqual(report["overall"], "unchanged")
        self.assertEqual(report["changes"], [])

    def test_field_add_remove_modify_classifications(self) -> None:
        expectations = {
            "02-add-optional-field": ("compatible", "ADUC-COMPARE-STRUCTURE-FIELD-ADDED-OPTIONAL-001"),
            "03-add-required-field": ("potentiallyIncompatible", "ADUC-COMPARE-STRUCTURE-FIELD-ADDED-REQUIRED-001"),
            "04-remove-field": ("incompatible", "ADUC-COMPARE-STRUCTURE-FIELD-REMOVED-001"),
            "05-change-primitive-type": ("incompatible", "ADUC-COMPARE-STRUCTURE-PRIMITIVE-001"),
        }
        for case_id, (overall, code) in expectations.items():
            with self.subTest(case=case_id):
                left, right = materialize(self.base, by_id(self.cases, case_id))
                report = aduc_core.compare_contracts(left, right)
                self.assertEqual(report["overall"], overall)
                self.assertIn(code, change_codes(report))

    def test_semantics_authority_identity_context_provenance_uncertainty_policy_and_extensions(self) -> None:
        expected = {
            "07-change-semantic-concept": "ADUC-COMPARE-SEMANTICS-CONCEPT-001",
            "08-change-unit": "ADUC-COMPARE-SEMANTICS-UNIT-001",
            "09-promote-authority": "ADUC-COMPARE-SEMANTICS-AUTHORITY-001",
            "10-conflict-appears": "ADUC-COMPARE-SEMANTICS-CONFLICT-001",
            "11-possible-identity-to-exact": "ADUC-COMPARE-IDENTITY-PROMOTION-001",
            "12-change-timezone": "ADUC-COMPARE-CONTEXT-TIMEZONE-001",
            "13-change-provenance": "ADUC-COMPARE-PROVENANCE-MODIFIED-001",
            "14-change-uncertainty": "ADUC-COMPARE-UNCERTAINTY-VALUE-001",
            "16-add-policy-prohibition": "ADUC-COMPARE-POLICY-PROHIBITION-ADDED-001",
            "17-add-optional-extension": "ADUC-COMPARE-EXTENSION-DECL-ADDED-001",
            "21-contract-status-and-version": "ADUC-COMPARE-CONTRACT-STATUS-001",
            "22-deprecated-semantic-object": "ADUC-COMPARE-SEMANTICS-LIFECYCLE-001",
        }
        for case_id, code in expected.items():
            with self.subTest(case=case_id):
                left, right = materialize(self.base, by_id(self.cases, case_id))
                report = aduc_core.compare_contracts(left, right)
                self.assertIn(code, change_codes(report), report)

    def test_change_type_and_normative_assessment_are_separate(self) -> None:
        left, right = materialize(self.base, by_id(self.cases, "08-change-unit"))
        report = aduc_core.compare_contracts(left, right)
        unit_change = next(item for item in report["changes"] if item["code"] == "ADUC-COMPARE-SEMANTICS-UNIT-001")
        self.assertEqual(unit_change["changeType"], "modified")
        self.assertEqual(unit_change["assessment"], "convertible")
        self.assertEqual(unit_change["classification"], "compatible")
        self.assertEqual(unit_change["evidence"]["evaluator"], "ADR-0007")
        self.assertTrue(unit_change["evidence"]["conversionSupported"])

    def test_all_normative_assessments_are_covered_by_fixtures(self) -> None:
        observed: set[str] = set()
        for case in self.cases:
            left, right = materialize(self.base, case)
            report = aduc_core.compare_contracts(left, right)
            observed.add(report["overallAssessment"])
            observed.update(item["assessment"] for item in report["changes"])
        self.assertTrue(set(aduc_core.ASSESSMENT_ORDER).issubset(observed), observed)

    def test_dangerous_architectural_contracts_are_not_indexed(self) -> None:
        duplicate_left = copy.deepcopy(self.base)
        duplicate_left["structure"]["records"][0]["fields"].append(copy.deepcopy(duplicate_left["structure"]["records"][0]["fields"][0]))
        duplicate_right = copy.deepcopy(self.base)
        duplicate_right["structure"]["records"][0]["fields"].append(copy.deepcopy(duplicate_right["structure"]["records"][0]["fields"][0]))
        broken_ref = copy.deepcopy(self.base)
        broken_ref["semantics"]["assertions"][0]["subjectRef"] = "urn:example:missing"
        required_extension = copy.deepcopy(self.base)
        required_extension["aduc"]["extensionDeclarations"][0]["required"] = True
        scenarios = [
            (duplicate_left, self.base, "ADUC-COMPARE-INPUT-LEFT-002"),
            (self.base, duplicate_right, "ADUC-COMPARE-INPUT-RIGHT-002"),
            (self.base, broken_ref, "ADUC-COMPARE-INPUT-RIGHT-002"),
            (self.base, required_extension, "ADUC-COMPARE-INPUT-RIGHT-002"),
        ]
        for left, right, expected in scenarios:
            with self.subTest(expected=expected):
                report = aduc_core.compare_contracts(left, right)
                self.assertFalse(report["comparable"])
                self.assertEqual(report["overall"], "notComparable")
                self.assertIn(expected, change_codes(report))

    def test_unit_assessment_convertible_incompatible_and_unknown(self) -> None:
        expectations = {
            "08-change-unit": "convertible",
            "23-unit-non-convertible": "incompatible",
            "24-unit-insufficient-information": "unknown",
        }
        for case_id, assessment in expectations.items():
            with self.subTest(case=case_id):
                left, right = materialize(self.base, by_id(self.cases, case_id))
                report = aduc_core.compare_contracts(left, right)
                unit_change = next(item for item in report["changes"] if item["code"] == "ADUC-COMPARE-SEMANTICS-UNIT-001")
                self.assertEqual(unit_change["assessment"], assessment, report)

    def test_relation_contradiction_is_comparable_but_incompatible(self) -> None:
        left, right = materialize(self.base, by_id(self.cases, "15-relation-contradiction"))
        report = aduc_core.compare_contracts(left, right)
        self.assertTrue(report["comparable"])
        self.assertFalse(report["right"]["valid"])
        self.assertEqual(report["right"]["outcome"], "blocked")
        self.assertEqual(report["overall"], "incompatible")
        self.assertIn("ADUC-COMPARE-RELATION-CONTRADICTION-001", change_codes(report))

    def test_schema_invalid_inputs_are_not_comparable(self) -> None:
        for case_id, expected in {
            "19-left-invalid": "ADUC-COMPARE-INPUT-LEFT-001",
            "20-right-invalid": "ADUC-COMPARE-INPUT-RIGHT-001",
        }.items():
            with self.subTest(case=case_id):
                left, right = materialize(self.base, by_id(self.cases, case_id))
                report = aduc_core.compare_contracts(left, right)
                self.assertFalse(report["comparable"])
                self.assertEqual(report["overall"], "notComparable")
                self.assertIn(expected, change_codes(report))

    def test_comparison_report_is_stable_across_runs_and_json_property_order(self) -> None:
        case = by_id(self.cases, "09-promote-authority")
        left, right = materialize(self.base, case)
        reordered_right = json.loads(json.dumps(right, sort_keys=True))
        first = aduc_core.compare_contracts(left, right, left_source="stable-left", right_source="stable-right")
        second = aduc_core.compare_contracts(left, reordered_right, left_source="stable-left", right_source="stable-right")
        third = aduc_core.compare_contracts(left, right, left_source="stable-left", right_source="stable-right")
        self.assertEqual(first, second)
        self.assertEqual(first, third)
        self.assertEqual(
            json.dumps(first, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
            json.dumps(third, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        )

    def test_compare_cli_text_json_and_exit_codes(self) -> None:
        unchanged = subprocess.run([sys.executable, str(TOOL), "compare", str(COMPLETE), str(COMPLETE)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr + unchanged.stdout)
        self.assertIn("COMPARE UNCHANGED", unchanged.stdout)

        left, right = materialize(self.base, by_id(self.cases, "03-add-required-field"))
        left_path, right_path = write_pair(left, right)
        try:
            review = subprocess.run([sys.executable, str(TOOL), "compare", str(left_path), str(right_path), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(review.returncode, 2, review.stderr + review.stdout)
            self.assertEqual(json.loads(review.stdout)["overall"], "potentiallyIncompatible")
        finally:
            left_path.unlink(missing_ok=True)
            right_path.unlink(missing_ok=True)

        left, right = materialize(self.base, by_id(self.cases, "05-change-primitive-type"))
        left_path, right_path = write_pair(left, right)
        try:
            incompatible = subprocess.run([sys.executable, str(TOOL), "compare", str(left_path), str(right_path)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(incompatible.returncode, 1, incompatible.stderr + incompatible.stdout)
        finally:
            left_path.unlink(missing_ok=True)
            right_path.unlink(missing_ok=True)

        missing = subprocess.run([sys.executable, str(TOOL), "compare", "missing-left.json", str(COMPLETE)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(missing.returncode, 3)
        self.assertNotIn("Traceback", missing.stderr + missing.stdout)


def by_id(cases: list[dict], case_id: str) -> dict:
    return next(case for case in cases if case["id"] == case_id)


def change_codes(report: dict) -> set[str]:
    return {item["code"] for item in report["changes"]}


def materialize(base: dict, case: dict) -> tuple[dict, dict]:
    left = copy.deepcopy(base)
    right = copy.deepcopy(base)
    apply_ops(left, case.get("left", []))
    apply_ops(right, case.get("right", []))
    return left, right


def apply_ops(document: dict, ops: list[dict]) -> None:
    for op in ops:
        name = op["op"]
        path = op["path"]
        if name == "set":
            parent, key = resolve_parent(document, path)
            parent[key] = copy.deepcopy(op["value"])
        elif name == "append":
            target = resolve(document, path)
            target.append(copy.deepcopy(op["value"]))
        elif name == "remove":
            parent, key = resolve_parent(document, path)
            del parent[key]
        elif name == "removeAt":
            target = resolve(document, path)
            del target[op["index"]]
        elif name == "reverse":
            target = resolve(document, path)
            target.reverse()
        else:
            raise AssertionError(f"unknown comparison fixture op: {name}")


def resolve(document, path: list):
    current = document
    for part in path:
        current = current[part]
    return current


def resolve_parent(document, path: list):
    return resolve(document, path[:-1]), path[-1]


def write_pair(left: dict, right: dict) -> tuple[Path, Path]:
    left_handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    right_handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with left_handle, right_handle:
        json.dump(left, left_handle, sort_keys=True)
        json.dump(right, right_handle, sort_keys=True)
    return Path(left_handle.name), Path(right_handle.name)


if __name__ == "__main__":
    unittest.main()
