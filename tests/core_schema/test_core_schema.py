from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_core_validate.py"
VALID_CASES = ROOT / "examples" / "core" / "valid" / "cases.json"
INVALID_CASES = ROOT / "examples" / "core" / "invalid" / "cases.json"
COMPLETE = ROOT / "examples" / "core" / "complete-model.example.json"
MODULE_MANIFEST = ROOT / "spec" / "core-module-manifest.json"

SPEC = importlib.util.spec_from_file_location("aduc_core_validate", TOOL)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class CoreSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_cases = json.loads(VALID_CASES.read_text(encoding="utf-8"))["cases"]
        cls.invalid_cases = json.loads(INVALID_CASES.read_text(encoding="utf-8"))["cases"]
        cls.complete = json.loads(COMPLETE.read_text(encoding="utf-8"))

    def test_schema_family_matches_frozen_manifest(self) -> None:
        manifest = json.loads(MODULE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(list(module.SCHEMA_FILES), manifest["schemaFamily"])
        for filename in module.SCHEMA_FILES:
            self.assertTrue((ROOT / "schema" / filename).is_file(), filename)

    def test_every_schema_is_draft_2020_12_valid(self) -> None:
        schemas, _registry = module.load_schema_family()
        for filename, schema in schemas.items():
            with self.subTest(filename=filename):
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertTrue(schema["$id"].startswith("https://aduc.example/schema/0.1/"))
                Draft202012Validator.check_schema(schema)

    def test_complete_model_passes_schema_and_architecture(self) -> None:
        result = module.validate_document(self.complete)
        self.assertTrue(result["schemaValid"], result["schemaErrors"])
        self.assertTrue(result["architectureValid"], result["architectureErrors"])
        self.assertTrue(result["valid"])

    def test_at_least_ten_complete_valid_fixtures_pass(self) -> None:
        self.assertGreaterEqual(len(self.valid_cases), 10)
        for case in self.valid_cases:
            with self.subTest(case=case["id"]):
                result = module.validate_document(case["document"])
                self.assertTrue(result["valid"], result)

    def test_every_invalid_fixture_fails_for_documented_schema_code(self) -> None:
        self.assertGreaterEqual(len(self.invalid_cases), 10)
        for case in self.invalid_cases:
            with self.subTest(case=case["id"]):
                result = module.validate_document(case["document"], architecture=False)
                codes = {item["code"] for item in result["schemaErrors"]}
                self.assertFalse(result["schemaValid"])
                self.assertIn(case["expectedCode"], codes, result)

    def test_schema_closes_top_level_and_module_objects(self) -> None:
        document = copy.deepcopy(self.valid_cases[2]["document"])
        document["unexpected"] = True
        result = module.validate_document(document, architecture=False)
        self.assertIn("ADUC-SCHEMA-UNKNOWN", {item["code"] for item in result["schemaErrors"]})
        document.pop("unexpected")
        document["semantics"]["assertions"][0]["legacyMeaning"] = "unsafe"
        result = module.validate_document(document, architecture=False)
        self.assertIn("ADUC-SCHEMA-UNKNOWN", {item["code"] for item in result["schemaErrors"]})

    def test_architecture_checker_remains_complementary(self) -> None:
        document = copy.deepcopy(self.valid_cases[0]["document"])
        fields = document["structure"]["records"][0]["fields"]
        fields.append(copy.deepcopy(fields[0]))
        schema_only = module.validate_document(document, architecture=False)
        combined = module.validate_document(document, architecture=True)
        self.assertTrue(schema_only["schemaValid"])
        self.assertFalse(combined["architectureValid"])
        self.assertIn("ADUC-CORE-ID-002", {item["code"] for item in combined["architectureErrors"]})

    def test_schema_family_uses_only_local_relative_refs(self) -> None:
        schemas, _registry = module.load_schema_family()
        for filename, schema in schemas.items():
            for value in _walk_refs(schema):
                with self.subTest(filename=filename, ref=value):
                    self.assertFalse(value.startswith("http://") or value.startswith("https://"), value)

    def test_cli_accepts_valid_suite_and_rejects_invalid_suite(self) -> None:
        valid = subprocess.run(
            [sys.executable, str(TOOL), str(VALID_CASES), "--format", "json"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        payload = json.loads(valid.stdout)
        self.assertGreaterEqual(payload["valid"], 10)
        invalid = subprocess.run(
            [sys.executable, str(TOOL), str(INVALID_CASES), "--schema-only", "--format", "json"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(invalid.returncode, 1, invalid.stderr + invalid.stdout)
        payload = json.loads(invalid.stdout)
        self.assertEqual(payload["invalid"], len(self.invalid_cases))

    def test_error_paths_are_stable_json_paths(self) -> None:
        case = next(item for item in self.invalid_cases if item["id"] == "09-missing-assertion-qualification")
        result = module.validate_document(case["document"], architecture=False)
        self.assertTrue(all(item["path"].startswith("$") for item in result["schemaErrors"]))
        self.assertIn("$.semantics.assertions[0]", {item["path"] for item in result["schemaErrors"]})


def _walk_refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                yield child
            yield from _walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_refs(child)


if __name__ == "__main__":
    unittest.main()
