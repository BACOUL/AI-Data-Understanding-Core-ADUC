from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_core.py"
COMPLETE = ROOT / "examples" / "core" / "complete-model.example.json"
VALID_CASES = ROOT / "examples" / "core" / "valid" / "cases.json"
INVALID_CASES = ROOT / "examples" / "core" / "invalid" / "cases.json"

SPEC = importlib.util.spec_from_file_location("aduc_core", TOOL)
assert SPEC and SPEC.loader
aduc_core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aduc_core)


class UnifiedCoreValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.complete = json.loads(COMPLETE.read_text(encoding="utf-8"))
        cls.valid_cases = json.loads(VALID_CASES.read_text(encoding="utf-8"))["cases"]
        cls.invalid_cases = json.loads(INVALID_CASES.read_text(encoding="utf-8"))["cases"]

    def test_loads_fourteen_draft_2020_12_schemas_offline(self) -> None:
        schemas, _registry = aduc_core.aduc_core_validate.load_schema_family()
        self.assertEqual(len(schemas), 14)
        for filename, schema in schemas.items():
            with self.subTest(filename=filename):
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                Draft202012Validator.check_schema(schema)
                self.assertTrue(all(not ref.startswith(("http://", "https://")) for ref in walk_refs(schema)))

    def test_complete_contract_is_valid_with_stable_report_shape(self) -> None:
        report = aduc_core.validate_contract(self.complete, source="complete")
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["outcome"], "valid")
        self.assertEqual(report["contractId"], self.complete["aduc"]["contractId"])
        self.assertEqual(report["coreVersion"], self.complete["aduc"]["coreVersion"])
        self.assertEqual(report["summary"], {"errors": 0, "warnings": 0, "humanReview": 0})
        self.assertEqual(report["diagnostics"], [])
        self.assertEqual(set(report["modules"]), set(aduc_core.MODULE_ORDER))

    def test_all_valid_fixture_contracts_pass(self) -> None:
        self.assertEqual(len(self.valid_cases), 11)
        for case in self.valid_cases:
            with self.subTest(case=case["id"]):
                report = aduc_core.validate_contract(case["document"], source=case["id"])
                self.assertTrue(report["valid"], report)
                self.assertIn(report["outcome"], {"valid", "validWithWarnings", "requiresHumanReview"})

    def test_all_invalid_fixture_contracts_fail_for_documented_code(self) -> None:
        self.assertEqual(len(self.invalid_cases), 15)
        for case in self.invalid_cases:
            with self.subTest(case=case["id"]):
                report = aduc_core.validate_contract(case["document"], source=case["id"], schema_only=True)
                found = {item["code"] for item in report["diagnostics"]}
                self.assertFalse(report["valid"], report)
                self.assertEqual(report["outcome"], "blocked")
                self.assertIn(case["expectedCode"], found)

    def test_global_identifier_uniqueness_is_architectural(self) -> None:
        document = copy.deepcopy(self.complete)
        document["structure"]["records"][0]["fields"].append(copy.deepcopy(document["structure"]["records"][0]["fields"][0]))
        schema_only = aduc_core.validate_contract(document, source="duplicate", schema_only=True)
        full = aduc_core.validate_contract(document, source="duplicate")
        self.assertTrue(schema_only["pipeline"]["schemaValid"])
        self.assertFalse(full["pipeline"]["architectureValid"])
        self.assertIn("ADUC-CORE-ID-002", codes(full))

    def test_reference_resolution_and_module_dependencies_are_reported(self) -> None:
        broken_ref = copy.deepcopy(self.complete)
        broken_ref["semantics"]["assertions"][0]["subjectRef"] = "urn:example:missing:field"
        ref_report = aduc_core.validate_contract(broken_ref, source="broken-ref")
        self.assertIn("ADUC-CORE-REF-001", codes(ref_report))
        self.assertTrue(all(item["path"].startswith("$") for item in ref_report["diagnostics"]))

        broken_dependency = copy.deepcopy(self.complete)
        broken_dependency.pop("provenance")
        dependency_report = aduc_core.validate_contract(broken_dependency, source="broken-dependency")
        self.assertEqual(dependency_report["outcome"], "blocked")
        self.assertIn("ADUC-SCHEMA-DEPENDENCY", codes(dependency_report))

    def test_extensions_qualification_and_policy_review_are_profile_diagnostics(self) -> None:
        required_extension = copy.deepcopy(self.complete)
        required_extension["aduc"]["extensionDeclarations"][0]["required"] = True
        extension_report = aduc_core.validate_contract(required_extension, source="required-extension")
        self.assertIn("ADUC-CORE-EXT-003", codes(extension_report))

        inferred = copy.deepcopy(self.complete)
        inferred["semantics"]["assertions"][1]["status"] = "inferred"
        inferred["semantics"]["assertions"][1]["confidence"] = 0.6
        inferred["semantics"]["assertions"][1]["confidenceMethodIri"] = "urn:example:method:model-confidence"
        inferred_report = aduc_core.validate_contract(inferred, source="inferred")
        self.assertEqual(inferred_report["outcome"], "requiresHumanReview")
        self.assertIn("ADUC-CORE-QUAL-002", codes(inferred_report))

        closed_policy = copy.deepcopy(self.complete)
        closed_policy["policy"]["policies"][0]["mode"] = "closed"
        policy_report = aduc_core.validate_contract(closed_policy, source="closed-policy")
        self.assertEqual(policy_report["outcome"], "requiresHumanReview")
        self.assertIn("ADUC-CORE-POLICY-002", codes(policy_report))

    def test_profile_adapters_call_accepted_evaluators(self) -> None:
        with (
            mock.patch.object(aduc_core.aduc_epistemic, "evaluate_record_set", wraps=aduc_core.aduc_epistemic.evaluate_record_set) as epistemic,
            mock.patch.object(aduc_core.aduc_source_binding, "validate_digest", wraps=aduc_core.aduc_source_binding.validate_digest) as binding,
            mock.patch.object(aduc_core.aduc_units, "load_registry", wraps=aduc_core.aduc_units.load_registry) as units,
            mock.patch.object(aduc_core.aduc_time, "resolve", wraps=aduc_core.aduc_time.resolve) as time,
            mock.patch.object(aduc_core.aduc_identity, "validate_entities", wraps=aduc_core.aduc_identity.validate_entities) as identity,
            mock.patch.object(aduc_core.aduc_provenance, "validate_entities", wraps=aduc_core.aduc_provenance.validate_entities) as provenance,
            mock.patch.object(aduc_core.aduc_uncertainty, "validate_uncertainty", wraps=aduc_core.aduc_uncertainty.validate_uncertainty) as uncertainty,
            mock.patch.object(aduc_core.aduc_relations, "validate_assertion", wraps=aduc_core.aduc_relations.validate_assertion) as relations,
            mock.patch.object(aduc_core.aduc_policy, "validate_policy", wraps=aduc_core.aduc_policy.validate_policy) as policy,
        ):
            report = aduc_core.validate_contract(self.complete, source="profiles")
        self.assertTrue(report["valid"], report)
        for patched in (epistemic, binding, units, time, identity, provenance, uncertainty, relations, policy):
            self.assertGreater(patched.call_count, 0, patched)
        evaluations = {item["profile"]: item for item in report["profileEvaluations"]}
        self.assertEqual(set(evaluations), set(aduc_core.PROFILE_ORDER))
        self.assertEqual(evaluations["ADR-0013"]["status"], "indeterminate")
        self.assertTrue(evaluations["ADR-0013"]["requiresRequest"])

    def test_profile_evaluator_codes_are_preserved_without_false_success(self) -> None:
        report = aduc_core.validate_contract(self.complete, source="profiles")
        uncertainty = next(item for item in report["profileEvaluations"] if item["profile"] == "ADR-0011")
        units = next(item for item in report["profileEvaluations"] if item["profile"] == "ADR-0007")
        self.assertEqual(uncertainty["status"], "unknown")
        self.assertIn("ADUC-UNC-001", {item["code"] for item in uncertainty["missingData"]})
        self.assertEqual(units["status"], "unknown")
        self.assertIn("ADUC-CORE-PROFILE-UNIT-DATA", {item["code"] for item in units["missingData"]})

    def test_non_applicable_profiles_are_reported_explicitly(self) -> None:
        minimal = self.valid_cases[0]["document"]
        report = aduc_core.validate_contract(minimal, source="minimal")
        evaluations = {item["profile"]: item for item in report["profileEvaluations"]}
        self.assertIn("notApplicable", {item["status"] for item in evaluations.values()})
        self.assertTrue(any(item["notApplicable"] for item in evaluations.values()))
        self.assertTrue(report["valid"], report)

    def test_diagnostics_are_deduplicated_and_ordered_deterministically(self) -> None:
        first = aduc_core.diagnostic("B", "warning", "schema", "$.resource", "second", module="resource", blocking=False)
        second = aduc_core.diagnostic("A", "error", "reference", "$.semantics", "first", module="semantics")
        ordered = aduc_core.stable_diagnostics([first, second, first])
        self.assertEqual([item["code"] for item in ordered], ["A", "B"])
        self.assertEqual(len(ordered), 2)

    def test_json_property_order_does_not_change_validation_report(self) -> None:
        left = copy.deepcopy(self.complete)
        right = json.loads(json.dumps(self.complete, sort_keys=True))
        self.assertEqual(
            normalized(aduc_core.validate_contract(left, source="same")),
            normalized(aduc_core.validate_contract(right, source="same")),
        )

    def test_cli_text_json_and_exit_codes(self) -> None:
        valid = subprocess.run([sys.executable, str(TOOL), "validate", str(COMPLETE)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        self.assertIn("VALID", valid.stdout)

        valid_json = subprocess.run([sys.executable, str(TOOL), "validate", str(COMPLETE), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(valid_json.returncode, 0, valid_json.stderr + valid_json.stdout)
        self.assertTrue(json.loads(valid_json.stdout)["valid"])

        blocked = copy.deepcopy(self.complete)
        blocked["resource"]["id"] = "not a uri"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(blocked, handle)
            blocked_path = Path(handle.name)
        blocked_run = subprocess.run([sys.executable, str(TOOL), "validate", str(blocked_path), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(blocked_run.returncode, 1, blocked_run.stderr + blocked_run.stdout)
        blocked_path.unlink(missing_ok=True)

        human_review = copy.deepcopy(self.complete)
        human_review["semantics"]["assertions"][1]["conflict"] = "contested"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(human_review, handle)
            review_path = Path(handle.name)
        review_run = subprocess.run([sys.executable, str(TOOL), "validate", str(review_path), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(review_run.returncode, 2, review_run.stderr + review_run.stdout)
        review_path.unlink(missing_ok=True)

    def test_cli_input_errors_are_usage_errors_without_traceback(self) -> None:
        missing = subprocess.run([sys.executable, str(TOOL), "validate", "does-not-exist.json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(missing.returncode, 3)
        self.assertNotIn("Traceback", missing.stderr + missing.stdout)

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            handle.write("{")
            bad_path = Path(handle.name)
        bad_json = subprocess.run([sys.executable, str(TOOL), "validate", str(bad_path)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(bad_json.returncode, 3)
        self.assertNotIn("Traceback", bad_json.stderr + bad_json.stdout)
        bad_path.unlink(missing_ok=True)

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            handle.write("[" * 140 + "0" + "]" * 140)
            deep_path = Path(handle.name)
        deep_json = subprocess.run([sys.executable, str(TOOL), "validate", str(deep_path), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(deep_json.returncode, 3, deep_json.stderr + deep_json.stdout)
        payload = json.loads(deep_json.stdout)
        self.assertEqual(payload["diagnostics"][0]["code"], "ADUC-CORE-INPUT-005")
        self.assertNotIn("Traceback", deep_json.stderr + deep_json.stdout)
        deep_path.unlink(missing_ok=True)

    def test_cli_accepts_valid_suite_and_rejects_invalid_suite(self) -> None:
        valid = subprocess.run([sys.executable, str(TOOL), "validate", str(VALID_CASES), "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        self.assertEqual(len(json.loads(valid.stdout)["results"]), 11)

        invalid = subprocess.run([sys.executable, str(TOOL), "validate", str(INVALID_CASES), "--schema-only", "--format", "json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 1, invalid.stderr + invalid.stdout)
        self.assertEqual(len(json.loads(invalid.stdout)["results"]), 15)


def codes(report: dict) -> set[str]:
    return {item["code"] for item in report["diagnostics"]}


def normalized(report: dict) -> dict:
    result = copy.deepcopy(report)
    result["source"] = "<stable>"
    return result


def walk_refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                yield child
            yield from walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_refs(child)


if __name__ == "__main__":
    unittest.main()
