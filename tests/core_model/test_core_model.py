from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_core_model.py"
EXAMPLE = ROOT / "examples" / "core" / "complete-model.example.json"
INVALID = ROOT / "examples" / "core" / "invalid-model-cases.json"
MANIFEST = ROOT / "spec" / "core-module-manifest.json"
MODEL = ROOT / "spec" / "ADUC_CORE_MODEL_0_1.md"
BOUNDARIES = ROOT / "docs" / "architecture" / "CORE_MODULE_BOUNDARIES_0_1.md"
ROOT_SCHEMA = ROOT / "schema" / "aduc-core.schema.json"

SPEC = importlib.util.spec_from_file_location("aduc_core_model", TOOL)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class CoreModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        cls.invalid = json.loads(INVALID.read_text(encoding="utf-8"))
        cls.invalid_by_id = {case["id"]: case for case in cls.invalid["cases"]}

    def test_exact_ten_block_order_and_minimum_envelope(self) -> None:
        self.assertEqual(
            self.manifest["topLevelOrder"],
            ["aduc", "resource", "structure", "semantics", "identity", "context", "provenance", "uncertainty", "relations", "policy"],
        )
        self.assertEqual(self.manifest["minimumEnvelope"], ["aduc", "resource", "structure"])

    def test_cardinalities_and_representations_are_frozen(self) -> None:
        modules = self.manifest["modules"]
        for name in self.manifest["topLevelOrder"]:
            self.assertIn(name, modules)
        self.assertEqual(modules["aduc"]["cardinality"], "1")
        self.assertEqual(modules["resource"]["cardinality"], "1")
        self.assertEqual(modules["structure"]["cardinality"], "1")
        self.assertEqual(modules["relations"]["cardinality"], "0..n")
        self.assertEqual(modules["relations"]["representation"], "array")
        for name in set(modules) - {"relations"}:
            self.assertEqual(modules[name]["representation"], "object")

    def test_dependency_graph_is_acyclic(self) -> None:
        self.assertEqual(module.dependency_errors(self.manifest), [])
        self.assertEqual(self.manifest["modules"]["policy"]["hardDependencies"], ["resource", "provenance"])
        self.assertEqual(self.manifest["modules"]["semantics"]["hardDependencies"], ["structure"])

    def test_complete_model_and_counterexample_suite(self) -> None:
        result = module.run(EXAMPLE, INVALID, MANIFEST)
        self.assertTrue(result["ok"], result["failures"])
        self.assertTrue(result["validExampleAccepted"])
        self.assertEqual(result["invalidRejected"], 25)
        self.assertEqual(result["invalidTotal"], 25)
        self.assertGreater(result["objectCount"], 30)

    def test_all_complete_example_references_resolve(self) -> None:
        result = module.validate_document(self.example, self.manifest)
        self.assertTrue(result["valid"], result["errors"])
        self.assertNotIn("ADUC-CORE-REF-001", {item["code"] for item in result["errors"]})

    def test_ownership_conflicts_are_rejected(self) -> None:
        for case_id in ("resource-duplicates-producer", "structure-duplicates-unit", "semantics-duplicates-measurement-uncertainty"):
            with self.subTest(case_id=case_id):
                case = self.invalid_by_id[case_id]
                result = module.validate_document(module.patch(self.example, case["patch"]), self.manifest)
                self.assertIn("ADUC-CORE-OWNER-001", {item["code"] for item in result["errors"]})

    def test_identifier_and_reference_failures_are_rejected(self) -> None:
        expected = {
            "local-object-identifier": "ADUC-CORE-ID-001",
            "duplicate-object-identifier": "ADUC-CORE-ID-002",
            "unresolved-cross-module-reference": "ADUC-CORE-REF-001",
            "structure-bound-to-wrong-resource": "ADUC-CORE-REF-002",
        }
        for case_id, code in expected.items():
            with self.subTest(case_id=case_id):
                case = self.invalid_by_id[case_id]
                result = module.validate_document(module.patch(self.example, case["patch"]), self.manifest)
                self.assertIn(code, {item["code"] for item in result["errors"]})

    def test_extensions_cannot_overwrite_or_claim_support(self) -> None:
        expected = {
            "undeclared-extension-namespace": "ADUC-CORE-EXT-001",
            "extension-overwrites-core-term": "ADUC-CORE-EXT-002",
            "unsupported-required-extension": "ADUC-CORE-EXT-003",
            "extension-uses-core-namespace": "ADUC-CORE-EXT-004",
        }
        for case_id, code in expected.items():
            with self.subTest(case_id=case_id):
                case = self.invalid_by_id[case_id]
                result = module.validate_document(module.patch(self.example, case["patch"]), self.manifest)
                self.assertIn(code, {item["code"] for item in result["errors"]})

    def test_cross_profile_safety_rules_are_preserved(self) -> None:
        expected = {
            "inferred-promoted-to-canonical": "ADUC-CORE-AUTH-001",
            "probable-identity-as-exact": "ADUC-CORE-IDENTITY-001",
            "relation-predicate-from-label": "ADUC-CORE-IRI-001",
            "classification-made-executable": "ADUC-CORE-POLICY-001",
            "hidden-provider-field": "ADUC-CORE-HIDDEN-001",
        }
        for case_id, code in expected.items():
            with self.subTest(case_id=case_id):
                case = self.invalid_by_id[case_id]
                result = module.validate_document(module.patch(self.example, case["patch"]), self.manifest)
                self.assertIn(code, {item["code"] for item in result["errors"]})

    def test_model_documents_and_official_schema_preserve_frozen_boundaries(self) -> None:
        model = MODEL.read_text(encoding="utf-8")
        boundaries = BOUNDARIES.read_text(encoding="utf-8")
        root_schema = json.loads(ROOT_SCHEMA.read_text(encoding="utf-8"))
        self.assertIn("minimum interoperable contract", model)
        self.assertIn("Published immutability", model)
        self.assertIn("Schema-family contract", model)
        self.assertIn("schema/aduc-core.schema.json", boundaries)
        self.assertIn("must not change this dependency graph without a new ADR", boundaries)
        self.assertEqual(root_schema["$id"], "https://aduc.example/schema/0.1/aduc-core.schema.json")
        self.assertEqual(root_schema["$ref"], "aduc-envelope.schema.json")
        self.assertIn("Official experimental modular", root_schema["description"])
        self.assertEqual(root_schema["$defs"]["aduc"]["properties"]["modelVersion"], {"const": "0.1.0"})

    def test_cli(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL), str(EXAMPLE), str(INVALID), "--manifest", str(MANIFEST), "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        result = json.loads(completed.stdout)
        self.assertTrue(result["ok"])
        self.assertEqual(result["invalidRejected"], 25)


if __name__ == "__main__":
    unittest.main()
